const express = require('express');
const router = express.Router();
const axios = require('axios');
const cheerio = require('cheerio');
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

router.use(isAuthenticated);

// Quick analyze API
router.post('/analyze', async (req, res) => {
    try {
        const { url } = req.body;

        if (!url) {
            return res.status(400).json({ error: 'URL is required' });
        }

        let normalizedUrl = url;
        if (!normalizedUrl.startsWith('http://') && !normalizedUrl.startsWith('https://')) {
            normalizedUrl = 'https://' + normalizedUrl;
        }

        const startTime = Date.now();
        let response;
        try {
            response = await axios.get(normalizedUrl, {
                timeout: 15000,
                headers: { 'User-Agent': 'SEOBot/1.0' }
            });
        } catch (fetchError) {
            return res.status(400).json({ error: 'Could not fetch URL' });
        }
        const loadTime = (Date.now() - startTime) / 1000;

        const $ = cheerio.load(response.data);

        const title = $('title').text().trim();
        const metaDescription = $('meta[name="description"]').attr('content') || '';
        const h1Count = $('h1').length;

        // Quick score calculation
        let score = 50;
        if (title && title.length >= 30 && title.length <= 60) score += 15;
        if (metaDescription && metaDescription.length >= 120 && metaDescription.length <= 160) score += 15;
        if (h1Count === 1) score += 10;
        if (loadTime < 2) score += 10;

        res.json({
            url: normalizedUrl,
            score: Math.min(score, 100),
            title,
            metaDescription,
            h1Count,
            loadTime
        });

    } catch (error) {
        console.error('API analyze error:', error);
        res.status(500).json({ error: 'Analysis failed' });
    }
});

// Get user stats
router.get('/stats', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const [websites, analyses, accounts, avgScore] = await Promise.all([
            pool.query('SELECT COUNT(*) as count FROM websites WHERE user_id = $1', [userId]),
            pool.query('SELECT COUNT(*) as count FROM seo_analyses WHERE user_id = $1', [userId]),
            pool.query('SELECT COUNT(*) as count FROM connected_accounts WHERE user_id = $1', [userId]),
            pool.query('SELECT AVG(overall_score) as avg FROM seo_analyses WHERE user_id = $1', [userId])
        ]);

        res.json({
            websites: parseInt(websites.rows[0].count),
            analyses: parseInt(analyses.rows[0].count),
            connectedAccounts: parseInt(accounts.rows[0].count),
            avgScore: Math.round(avgScore.rows[0].avg || 0)
        });

    } catch (error) {
        console.error('API stats error:', error);
        res.status(500).json({ error: 'Failed to get stats' });
    }
});

// Get recent analyses
router.get('/analyses/recent', async (req, res) => {
    try {
        const userId = req.session.user.id;
        const limit = parseInt(req.query.limit) || 10;

        const result = await pool.query(
            `SELECT id, url, overall_score, analyzed_at 
             FROM seo_analyses WHERE user_id = $1 
             ORDER BY analyzed_at DESC LIMIT $2`,
            [userId, limit]
        );

        res.json(result.rows);

    } catch (error) {
        console.error('API recent analyses error:', error);
        res.status(500).json({ error: 'Failed to get analyses' });
    }
});

// Get connected accounts
router.get('/accounts', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const result = await pool.query(
            'SELECT id, provider, account_name, account_url, connected_at FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        res.json(result.rows);

    } catch (error) {
        console.error('API accounts error:', error);
        res.status(500).json({ error: 'Failed to get accounts' });
    }
});

module.exports = router;
