const express = require('express');
const router = express.Router();
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

router.use(isAuthenticated);

// Dashboard home
router.get('/', async (req, res) => {
    try {
        const userId = req.session.user.id;

        // Get connected accounts count
        const accountsResult = await pool.query(
            'SELECT COUNT(*) as count FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        // Get websites count
        const websitesResult = await pool.query(
            'SELECT COUNT(*) as count FROM websites WHERE user_id = $1',
            [userId]
        );

        // Get recent analyses
        const analysesResult = await pool.query(
            `SELECT sa.*, w.name as website_name 
             FROM seo_analyses sa 
             LEFT JOIN websites w ON sa.website_id = w.id 
             WHERE sa.user_id = $1 
             ORDER BY sa.analyzed_at DESC 
             LIMIT 5`,
            [userId]
        );

        // Get recent websites
        const recentWebsites = await pool.query(
            `SELECT w.*, ca.provider, 
                    (SELECT overall_score FROM seo_analyses WHERE website_id = w.id ORDER BY analyzed_at DESC LIMIT 1) as latest_score
             FROM websites w 
             LEFT JOIN connected_accounts ca ON w.connected_account_id = ca.id 
             WHERE w.user_id = $1 
             ORDER BY w.created_at DESC 
             LIMIT 5`,
            [userId]
        );

        // Get connected accounts
        const connectedAccounts = await pool.query(
            'SELECT * FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        // Calculate stats
        const totalAnalyses = await pool.query(
            'SELECT COUNT(*) as count FROM seo_analyses WHERE user_id = $1',
            [userId]
        );

        const avgScore = await pool.query(
            'SELECT AVG(overall_score) as avg FROM seo_analyses WHERE user_id = $1',
            [userId]
        );

        res.render('dashboard/index', {
            stats: {
                connectedAccounts: parseInt(accountsResult.rows[0].count),
                websites: parseInt(websitesResult.rows[0].count),
                totalAnalyses: parseInt(totalAnalyses.rows[0].count),
                avgScore: Math.round(avgScore.rows[0].avg || 0)
            },
            recentAnalyses: analysesResult.rows,
            recentWebsites: recentWebsites.rows,
            connectedAccounts: connectedAccounts.rows
        });

    } catch (error) {
        console.error('Dashboard error:', error);
        req.flash('error', 'Error loading dashboard');
        res.render('dashboard/index', {
            stats: { connectedAccounts: 0, websites: 0, totalAnalyses: 0, avgScore: 0 },
            recentAnalyses: [],
            recentWebsites: [],
            connectedAccounts: []
        });
    }
});

// Settings page
router.get('/settings', async (req, res) => {
    try {
        const userId = req.session.user.id;
        const user = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);

        res.render('dashboard/settings', {
            userDetails: user.rows[0]
        });
    } catch (error) {
        console.error('Settings error:', error);
        req.flash('error', 'Error loading settings');
        res.redirect('/dashboard');
    }
});

// Update profile
router.post('/settings/profile', async (req, res) => {
    try {
        const { name, email } = req.body;
        const userId = req.session.user.id;

        await pool.query(
            'UPDATE users SET name = $1, email = $2, updated_at = CURRENT_TIMESTAMP WHERE id = $3',
            [name, email, userId]
        );

        req.session.user.name = name;
        req.session.user.email = email;

        req.flash('success', 'Profile updated successfully');
        res.redirect('/dashboard/settings');
    } catch (error) {
        console.error('Update profile error:', error);
        req.flash('error', 'Error updating profile');
        res.redirect('/dashboard/settings');
    }
});

module.exports = router;
