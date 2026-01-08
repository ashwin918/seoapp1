const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

router.use(isAuthenticated);

// OAuth connections page
router.get('/', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const result = await pool.query(
            'SELECT * FROM connected_accounts WHERE user_id = $1',
            [userId]
        );

        res.render('oauth/index', {
            connectedAccounts: result.rows
        });

    } catch (error) {
        console.error('OAuth page error:', error);
        req.flash('error', 'Error loading connections');
        res.redirect('/dashboard');
    }
});

// ==================== GITHUB OAuth (Dummy) ====================

// Initiate GitHub OAuth
router.get('/github', (req, res) => {
    // Store state in session for verification
    const state = crypto.randomBytes(16).toString('hex');
    req.session.oauthState = state;
    req.session.oauthProvider = 'github';

    // Render the dummy OAuth page (simulates GitHub login)
    res.render('oauth/connect', {
        provider: 'GitHub',
        providerSlug: 'github',
        state: state,
        icon: 'fa-github',
        color: '#333'
    });
});

// GitHub callback (dummy)
router.post('/github/callback', async (req, res) => {
    try {
        const { username, accountName, state } = req.body;
        const userId = req.session.user.id;

        if (state !== req.session.oauthState) {
            req.flash('error', 'Invalid OAuth state');
            return res.redirect('/oauth');
        }

        // Generate dummy tokens
        const accessToken = 'gh_' + crypto.randomBytes(20).toString('hex');
        const providerId = 'gh_user_' + crypto.randomBytes(8).toString('hex');

        // Check if already connected
        const existing = await pool.query(
            'SELECT id FROM connected_accounts WHERE user_id = $1 AND provider = $2',
            [userId, 'github']
        );

        if (existing.rows.length > 0) {
            // Update existing
            await pool.query(
                `UPDATE connected_accounts 
                 SET provider_user_id = $1, access_token = $2, account_name = $3, account_url = $4, connected_at = CURRENT_TIMESTAMP
                 WHERE user_id = $5 AND provider = $6`,
                [providerId, accessToken, accountName || username, `https://github.com/${username}`, userId, 'github']
            );
        } else {
            // Insert new
            await pool.query(
                `INSERT INTO connected_accounts (user_id, provider, provider_user_id, access_token, account_name, account_url)
                 VALUES ($1, $2, $3, $4, $5, $6)`,
                [userId, 'github', providerId, accessToken, accountName || username, `https://github.com/${username}`]
            );
        }

        delete req.session.oauthState;
        delete req.session.oauthProvider;

        req.flash('success', 'GitHub account connected successfully!');
        res.redirect('/oauth');

    } catch (error) {
        console.error('GitHub callback error:', error);
        req.flash('error', 'Error connecting GitHub account');
        res.redirect('/oauth');
    }
});

// ==================== WORDPRESS OAuth (Dummy) ====================

router.get('/wordpress', (req, res) => {
    const state = crypto.randomBytes(16).toString('hex');
    req.session.oauthState = state;
    req.session.oauthProvider = 'wordpress';

    res.render('oauth/connect', {
        provider: 'WordPress',
        providerSlug: 'wordpress',
        state: state,
        icon: 'fa-wordpress',
        color: '#21759B'
    });
});

router.post('/wordpress/callback', async (req, res) => {
    try {
        const { siteUrl, username, state } = req.body;
        const userId = req.session.user.id;

        if (state !== req.session.oauthState) {
            req.flash('error', 'Invalid OAuth state');
            return res.redirect('/oauth');
        }

        const accessToken = 'wp_' + crypto.randomBytes(20).toString('hex');
        const refreshToken = 'wpr_' + crypto.randomBytes(20).toString('hex');
        const providerId = 'wp_user_' + crypto.randomBytes(8).toString('hex');

        const existing = await pool.query(
            'SELECT id FROM connected_accounts WHERE user_id = $1 AND provider = $2',
            [userId, 'wordpress']
        );

        const normalizedUrl = siteUrl.startsWith('http') ? siteUrl : 'https://' + siteUrl;

        if (existing.rows.length > 0) {
            await pool.query(
                `UPDATE connected_accounts 
                 SET provider_user_id = $1, access_token = $2, refresh_token = $3, account_name = $4, account_url = $5, connected_at = CURRENT_TIMESTAMP
                 WHERE user_id = $6 AND provider = $7`,
                [providerId, accessToken, refreshToken, username, normalizedUrl, userId, 'wordpress']
            );
        } else {
            await pool.query(
                `INSERT INTO connected_accounts (user_id, provider, provider_user_id, access_token, refresh_token, account_name, account_url)
                 VALUES ($1, $2, $3, $4, $5, $6, $7)`,
                [userId, 'wordpress', providerId, accessToken, refreshToken, username, normalizedUrl]
            );
        }

        delete req.session.oauthState;
        delete req.session.oauthProvider;

        req.flash('success', 'WordPress site connected successfully!');
        res.redirect('/oauth');

    } catch (error) {
        console.error('WordPress callback error:', error);
        req.flash('error', 'Error connecting WordPress site');
        res.redirect('/oauth');
    }
});

// ==================== SHOPIFY OAuth (Dummy) ====================

router.get('/shopify', (req, res) => {
    const state = crypto.randomBytes(16).toString('hex');
    req.session.oauthState = state;
    req.session.oauthProvider = 'shopify';

    res.render('oauth/connect', {
        provider: 'Shopify',
        providerSlug: 'shopify',
        state: state,
        icon: 'fa-shopify',
        color: '#96BF48'
    });
});

router.post('/shopify/callback', async (req, res) => {
    try {
        const { storeName, storeUrl, state } = req.body;
        const userId = req.session.user.id;

        if (state !== req.session.oauthState) {
            req.flash('error', 'Invalid OAuth state');
            return res.redirect('/oauth');
        }

        const accessToken = 'shpat_' + crypto.randomBytes(20).toString('hex');
        const providerId = 'shop_' + crypto.randomBytes(8).toString('hex');

        const existing = await pool.query(
            'SELECT id FROM connected_accounts WHERE user_id = $1 AND provider = $2',
            [userId, 'shopify']
        );

        const normalizedUrl = storeUrl ? (storeUrl.startsWith('http') ? storeUrl : 'https://' + storeUrl) : `https://${storeName}.myshopify.com`;

        if (existing.rows.length > 0) {
            await pool.query(
                `UPDATE connected_accounts 
                 SET provider_user_id = $1, access_token = $2, account_name = $3, account_url = $4, connected_at = CURRENT_TIMESTAMP
                 WHERE user_id = $5 AND provider = $6`,
                [providerId, accessToken, storeName, normalizedUrl, userId, 'shopify']
            );
        } else {
            await pool.query(
                `INSERT INTO connected_accounts (user_id, provider, provider_user_id, access_token, account_name, account_url)
                 VALUES ($1, $2, $3, $4, $5, $6)`,
                [userId, 'shopify', providerId, accessToken, storeName, normalizedUrl]
            );
        }

        delete req.session.oauthState;
        delete req.session.oauthProvider;

        req.flash('success', 'Shopify store connected successfully!');
        res.redirect('/oauth');

    } catch (error) {
        console.error('Shopify callback error:', error);
        req.flash('error', 'Error connecting Shopify store');
        res.redirect('/oauth');
    }
});

// ==================== Disconnect Account ====================

router.post('/:provider/disconnect', async (req, res) => {
    try {
        const { provider } = req.params;
        const userId = req.session.user.id;

        await pool.query(
            'DELETE FROM connected_accounts WHERE user_id = $1 AND provider = $2',
            [userId, provider]
        );

        req.flash('success', `${provider.charAt(0).toUpperCase() + provider.slice(1)} disconnected successfully`);
        res.redirect('/oauth');

    } catch (error) {
        console.error('Disconnect error:', error);
        req.flash('error', 'Error disconnecting account');
        res.redirect('/oauth');
    }
});

module.exports = router;
