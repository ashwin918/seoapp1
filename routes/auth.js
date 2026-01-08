const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const pool = require('../config/database');
const { isGuest, isAuthenticated } = require('../middleware/auth');

// Login page
router.get('/login', isGuest, (req, res) => {
    res.render('auth/login');
});

// Register page
router.get('/register', isGuest, (req, res) => {
    res.render('auth/register');
});

// Login POST
router.post('/login', isGuest, async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            req.flash('error', 'Please provide email and password');
            return res.redirect('/login');
        }

        const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);

        if (result.rows.length === 0) {
            req.flash('error', 'Invalid email or password');
            return res.redirect('/login');
        }

        const user = result.rows[0];
        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            req.flash('error', 'Invalid email or password');
            return res.redirect('/login');
        }

        // Set session
        req.session.user = {
            id: user.id,
            email: user.email,
            name: user.name,
            avatar_url: user.avatar_url
        };

        req.flash('success', 'Welcome back, ' + user.name + '!');
        res.redirect('/dashboard');

    } catch (error) {
        console.error('Login error:', error);
        req.flash('error', 'An error occurred during login');
        res.redirect('/login');
    }
});

// Register POST
router.post('/register', isGuest, async (req, res) => {
    try {
        const { name, email, password, confirmPassword } = req.body;

        // Validation
        if (!name || !email || !password) {
            req.flash('error', 'Please fill in all fields');
            return res.redirect('/register');
        }

        if (password !== confirmPassword) {
            req.flash('error', 'Passwords do not match');
            return res.redirect('/register');
        }

        if (password.length < 6) {
            req.flash('error', 'Password must be at least 6 characters');
            return res.redirect('/register');
        }

        // Check if user exists
        const existingUser = await pool.query('SELECT id FROM users WHERE email = $1', [email]);
        if (existingUser.rows.length > 0) {
            req.flash('error', 'Email already registered');
            return res.redirect('/register');
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 12);

        // Create user
        const result = await pool.query(
            'INSERT INTO users (name, email, password) VALUES ($1, $2, $3) RETURNING id, name, email',
            [name, email, hashedPassword]
        );

        const user = result.rows[0];

        // Set session
        req.session.user = {
            id: user.id,
            email: user.email,
            name: user.name,
            avatar_url: null
        };

        req.flash('success', 'Account created successfully! Welcome to SEO Bot.');
        res.redirect('/dashboard');

    } catch (error) {
        console.error('Registration error:', error);
        req.flash('error', 'An error occurred during registration');
        res.redirect('/register');
    }
});

// Logout
router.get('/logout', isAuthenticated, (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('Logout error:', err);
        }
        res.redirect('/');
    });
});

module.exports = router;
