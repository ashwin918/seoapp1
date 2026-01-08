const express = require('express');
const router = express.Router();
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

router.use(isAuthenticated);

// List all websites
router.get('/', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const result = await pool.query(
            `SELECT w.*, ca.provider, ca.account_name,
                    (SELECT overall_score FROM seo_analyses WHERE website_id = w.id ORDER BY analyzed_at DESC LIMIT 1) as latest_score,
                    (SELECT analyzed_at FROM seo_analyses WHERE website_id = w.id ORDER BY analyzed_at DESC LIMIT 1) as last_analyzed
             FROM websites w 
             LEFT JOIN connected_accounts ca ON w.connected_account_id = ca.id 
             WHERE w.user_id = $1 
             ORDER BY w.created_at DESC`,
            [userId]
        );

        const connectedAccounts = await pool.query(
            'SELECT * FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        res.render('websites/index', {
            websites: result.rows,
            connectedAccounts: connectedAccounts.rows
        });

    } catch (error) {
        console.error('Websites list error:', error);
        req.flash('error', 'Error loading websites');
        res.redirect('/dashboard');
    }
});

// Add website page
router.get('/add', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const connectedAccounts = await pool.query(
            'SELECT * FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        res.render('websites/add', {
            connectedAccounts: connectedAccounts.rows
        });

    } catch (error) {
        console.error('Add website page error:', error);
        req.flash('error', 'Error loading add website page');
        res.redirect('/websites');
    }
});

// Add website POST
router.post('/add', async (req, res) => {
    try {
        const { url, name, platform, connectedAccountId } = req.body;
        const userId = req.session.user.id;

        if (!url) {
            req.flash('error', 'Please provide a website URL');
            return res.redirect('/websites/add');
        }

        // Normalize URL
        let normalizedUrl = url;
        if (!normalizedUrl.startsWith('http://') && !normalizedUrl.startsWith('https://')) {
            normalizedUrl = 'https://' + normalizedUrl;
        }

        await pool.query(
            `INSERT INTO websites (user_id, url, name, platform, connected_account_id)
             VALUES ($1, $2, $3, $4, $5)`,
            [userId, normalizedUrl, name || new URL(normalizedUrl).hostname, platform || null, connectedAccountId || null]
        );

        req.flash('success', 'Website added successfully');
        res.redirect('/websites');

    } catch (error) {
        console.error('Add website error:', error);
        req.flash('error', 'Error adding website');
        res.redirect('/websites/add');
    }
});

// View website details
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.session.user.id;

        const websiteResult = await pool.query(
            `SELECT w.*, ca.provider, ca.account_name
             FROM websites w 
             LEFT JOIN connected_accounts ca ON w.connected_account_id = ca.id 
             WHERE w.id = $1 AND w.user_id = $2`,
            [id, userId]
        );

        if (websiteResult.rows.length === 0) {
            req.flash('error', 'Website not found');
            return res.redirect('/websites');
        }

        // Get analyses for this website
        const analysesResult = await pool.query(
            'SELECT * FROM seo_analyses WHERE website_id = $1 ORDER BY analyzed_at DESC LIMIT 10',
            [id]
        );

        // Get SEO edits for this website
        const editsResult = await pool.query(
            'SELECT * FROM seo_edits WHERE website_id = $1 ORDER BY created_at DESC LIMIT 10',
            [id]
        );

        res.render('websites/detail', {
            website: websiteResult.rows[0],
            analyses: analysesResult.rows,
            edits: editsResult.rows
        });

    } catch (error) {
        console.error('Website detail error:', error);
        req.flash('error', 'Error loading website details');
        res.redirect('/websites');
    }
});

// Delete website
router.post('/:id/delete', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.session.user.id;

        await pool.query(
            'DELETE FROM websites WHERE id = $1 AND user_id = $2',
            [id, userId]
        );

        req.flash('success', 'Website deleted successfully');
        res.redirect('/websites');

    } catch (error) {
        console.error('Delete website error:', error);
        req.flash('error', 'Error deleting website');
        res.redirect('/websites');
    }
});

// Update website
router.post('/:id/update', async (req, res) => {
    try {
        const { id } = req.params;
        const { name, platform, connectedAccountId } = req.body;
        const userId = req.session.user.id;

        await pool.query(
            `UPDATE websites SET name = $1, platform = $2, connected_account_id = $3
             WHERE id = $4 AND user_id = $5`,
            [name, platform, connectedAccountId || null, id, userId]
        );

        req.flash('success', 'Website updated successfully');
        res.redirect('/websites/' + id);

    } catch (error) {
        console.error('Update website error:', error);
        req.flash('error', 'Error updating website');
        res.redirect('/websites/' + req.params.id);
    }
});

module.exports = router;
