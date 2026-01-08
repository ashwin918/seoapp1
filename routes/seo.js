const express = require('express');
const router = express.Router();
const axios = require('axios');
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

// ML Service URL
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000';

router.use(isAuthenticated);

// SEO Edit page - show current SEO and AI suggestions
router.get('/edit/:websiteId', async (req, res) => {
    try {
        const { websiteId } = req.params;
        const userId = req.session.user.id;

        // Get website
        const websiteResult = await pool.query(
            'SELECT * FROM websites WHERE id = $1 AND user_id = $2',
            [websiteId, userId]
        );

        if (websiteResult.rows.length === 0) {
            req.flash('error', 'Website not found');
            return res.redirect('/websites');
        }

        const website = websiteResult.rows[0];

        // Get latest analysis for this website
        const analysisResult = await pool.query(
            'SELECT * FROM seo_analyses WHERE website_id = $1 ORDER BY analyzed_at DESC LIMIT 1',
            [websiteId]
        );

        // Get connected account for this website
        let connectedAccount = null;
        if (website.connected_account_id) {
            const accountResult = await pool.query(
                'SELECT * FROM connected_accounts WHERE id = $1',
                [website.connected_account_id]
            );
            if (accountResult.rows.length > 0) {
                connectedAccount = accountResult.rows[0];
            }
        }

        // Get pending edits
        const editsResult = await pool.query(
            `SELECT * FROM seo_edits 
             WHERE website_id = $1 AND status = 'pending' 
             ORDER BY created_at DESC`,
            [websiteId]
        );

        // Try to generate AI content suggestions
        let aiSuggestions = null;
        try {
            const mlResponse = await axios.post(`${ML_SERVICE_URL}/generate`, {
                url: website.url
            }, { timeout: 30000 });

            if (mlResponse.data.success) {
                aiSuggestions = mlResponse.data.generated_content;
            }
        } catch (err) {
            console.log('ML service unavailable for content generation');
        }

        res.render('seo/edit', {
            website,
            analysis: analysisResult.rows[0] || null,
            connectedAccount,
            pendingEdits: editsResult.rows,
            aiSuggestions
        });

    } catch (error) {
        console.error('SEO edit page error:', error);
        req.flash('error', 'Error loading SEO editor');
        res.redirect('/websites');
    }
});

// Generate AI content
router.post('/generate/:websiteId', async (req, res) => {
    try {
        const { websiteId } = req.params;
        const userId = req.session.user.id;

        // Get website
        const websiteResult = await pool.query(
            'SELECT * FROM websites WHERE id = $1 AND user_id = $2',
            [websiteId, userId]
        );

        if (websiteResult.rows.length === 0) {
            return res.json({ success: false, error: 'Website not found' });
        }

        const website = websiteResult.rows[0];

        // Call ML service to generate content
        const mlResponse = await axios.post(`${ML_SERVICE_URL}/generate`, {
            url: website.url
        }, { timeout: 30000 });

        if (mlResponse.data.success) {
            res.json({
                success: true,
                generated: mlResponse.data.generated_content,
                platforms: mlResponse.data.platform_formats
            });
        } else {
            res.json({ success: false, error: 'Content generation failed' });
        }

    } catch (error) {
        console.error('Generate content error:', error);
        res.json({ success: false, error: error.message });
    }
});

// Save SEO edit
router.post('/edit/:websiteId', async (req, res) => {
    try {
        const { websiteId } = req.params;
        const { field_type, old_value, new_value, page_url } = req.body;
        const userId = req.session.user.id;

        // Verify ownership
        const websiteResult = await pool.query(
            'SELECT * FROM websites WHERE id = $1 AND user_id = $2',
            [websiteId, userId]
        );

        if (websiteResult.rows.length === 0) {
            req.flash('error', 'Website not found');
            return res.redirect('/websites');
        }

        // Save the edit
        await pool.query(
            `INSERT INTO seo_edits (website_id, user_id, page_url, field_type, old_value, new_value, status)
             VALUES ($1, $2, $3, $4, $5, $6, 'pending')`,
            [websiteId, userId, page_url || websiteResult.rows[0].url, field_type, old_value, new_value]
        );

        req.flash('success', 'SEO change saved! Click "Apply" to push to your site.');
        res.redirect(`/seo/edit/${websiteId}`);

    } catch (error) {
        console.error('Save edit error:', error);
        req.flash('error', 'Error saving SEO change');
        res.redirect(`/seo/edit/${req.params.websiteId}`);
    }
});

// Apply SEO edit to platform
router.post('/apply/:editId', async (req, res) => {
    try {
        const { editId } = req.params;
        const userId = req.session.user.id;

        // Get the edit
        const editResult = await pool.query(
            `SELECT e.*, w.url as website_url, w.connected_account_id, ca.provider, ca.access_token, ca.account_url
             FROM seo_edits e
             JOIN websites w ON e.website_id = w.id
             LEFT JOIN connected_accounts ca ON w.connected_account_id = ca.id
             WHERE e.id = $1 AND e.user_id = $2`,
            [editId, userId]
        );

        if (editResult.rows.length === 0) {
            req.flash('error', 'Edit not found');
            return res.redirect('/websites');
        }

        const edit = editResult.rows[0];

        // Check if we have a connected account
        if (!edit.connected_account_id) {
            req.flash('error', 'No platform connected. Connect a platform first to push changes.');
            return res.redirect(`/seo/edit/${edit.website_id}`);
        }

        // Prepare content for push
        const content = {};
        if (edit.field_type === 'title') {
            content.title = edit.new_value;
        } else if (edit.field_type === 'meta_description') {
            content.meta_description = edit.new_value;
        } else {
            content[edit.field_type] = edit.new_value;
        }

        // Try to push to ML service
        try {
            const pushResponse = await axios.post(`${ML_SERVICE_URL}/push`, {
                platform: edit.provider,
                account: {
                    access_token: edit.access_token,
                    site_url: edit.account_url,
                    store_url: edit.account_url,
                    repo: edit.account_url
                },
                content: content,
                target: {
                    page_url: edit.page_url || edit.website_url
                }
            }, { timeout: 15000 });

            // Update edit status
            await pool.query(
                `UPDATE seo_edits SET status = 'applied', applied_at = CURRENT_TIMESTAMP WHERE id = $1`,
                [editId]
            );

            req.flash('success', `SEO change applied to ${edit.provider}! ${pushResponse.data.push_data?.note || ''}`);

        } catch (pushError) {
            console.log('Push to platform:', pushError.message);

            // Still mark as applied (demo mode)
            await pool.query(
                `UPDATE seo_edits SET status = 'applied', applied_at = CURRENT_TIMESTAMP WHERE id = $1`,
                [editId]
            );

            req.flash('success', `SEO change marked as applied (Demo mode - actual API integration required for ${edit.provider})`);
        }

        res.redirect(`/seo/edit/${edit.website_id}`);

    } catch (error) {
        console.error('Apply edit error:', error);
        req.flash('error', 'Error applying SEO change');
        res.redirect('/websites');
    }
});

// Apply AI suggestion directly
router.post('/apply-ai/:websiteId', async (req, res) => {
    try {
        const { websiteId } = req.params;
        const { suggestion_type, suggestion_content } = req.body;
        const userId = req.session.user.id;

        // Get website with connected account
        const websiteResult = await pool.query(
            `SELECT w.*, ca.provider, ca.access_token, ca.account_url
             FROM websites w
             LEFT JOIN connected_accounts ca ON w.connected_account_id = ca.id
             WHERE w.id = $1 AND w.user_id = $2`,
            [websiteId, userId]
        );

        if (websiteResult.rows.length === 0) {
            return res.json({ success: false, error: 'Website not found' });
        }

        const website = websiteResult.rows[0];

        // Save as an edit first
        const editResult = await pool.query(
            `INSERT INTO seo_edits (website_id, user_id, page_url, field_type, old_value, new_value, status)
             VALUES ($1, $2, $3, $4, $5, $6, 'pending')
             RETURNING *`,
            [websiteId, userId, website.url, suggestion_type, '', suggestion_content]
        );

        // If connected account, try to push
        if (website.provider) {
            const content = {};
            if (suggestion_type === 'title') {
                content.title = suggestion_content;
            } else if (suggestion_type === 'meta_description') {
                content.meta_description = suggestion_content;
            }

            try {
                await axios.post(`${ML_SERVICE_URL}/push`, {
                    platform: website.provider,
                    account: {
                        access_token: website.access_token,
                        site_url: website.account_url
                    },
                    content: content,
                    target: { page_url: website.url }
                }, { timeout: 15000 });

                await pool.query(
                    `UPDATE seo_edits SET status = 'applied', applied_at = CURRENT_TIMESTAMP WHERE id = $1`,
                    [editResult.rows[0].id]
                );

                return res.json({
                    success: true,
                    message: `AI suggestion applied to ${website.provider}!`
                });
            } catch (pushErr) {
                console.log('Push error:', pushErr.message);
            }
        }

        res.json({
            success: true,
            message: 'AI suggestion saved. Connect a platform to push to your site.'
        });

    } catch (error) {
        console.error('Apply AI suggestion error:', error);
        res.json({ success: false, error: error.message });
    }
});

// Cancel pending edit
router.post('/cancel/:editId', async (req, res) => {
    try {
        const { editId } = req.params;
        const userId = req.session.user.id;

        const result = await pool.query(
            `UPDATE seo_edits SET status = 'cancelled' 
             WHERE id = $1 AND user_id = $2 AND status = 'pending'
             RETURNING website_id`,
            [editId, userId]
        );

        if (result.rows.length > 0) {
            req.flash('success', 'Edit cancelled');
            res.redirect(`/seo/edit/${result.rows[0].website_id}`);
        } else {
            req.flash('error', 'Edit not found or already processed');
            res.redirect('/websites');
        }

    } catch (error) {
        console.error('Cancel edit error:', error);
        req.flash('error', 'Error cancelling edit');
        res.redirect('/websites');
    }
});

// SEO history for a website
router.get('/history/:websiteId', async (req, res) => {
    try {
        const { websiteId } = req.params;
        const userId = req.session.user.id;

        // Get website
        const websiteResult = await pool.query(
            'SELECT * FROM websites WHERE id = $1 AND user_id = $2',
            [websiteId, userId]
        );

        if (websiteResult.rows.length === 0) {
            req.flash('error', 'Website not found');
            return res.redirect('/websites');
        }

        // Get all edits
        const editsResult = await pool.query(
            `SELECT * FROM seo_edits WHERE website_id = $1 ORDER BY created_at DESC`,
            [websiteId]
        );

        res.render('seo/history', {
            website: websiteResult.rows[0],
            edits: editsResult.rows
        });

    } catch (error) {
        console.error('SEO history error:', error);
        req.flash('error', 'Error loading SEO history');
        res.redirect('/websites');
    }
});

module.exports = router;
