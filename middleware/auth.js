// Authentication middleware
const isAuthenticated = (req, res, next) => {
    if (req.session.user) {
        return next();
    }
    req.flash('error', 'Please login to access this page');
    res.redirect('/login');
};

// Guest only middleware (for login/register pages)
const isGuest = (req, res, next) => {
    if (!req.session.user) {
        return next();
    }
    res.redirect('/dashboard');
};

module.exports = { isAuthenticated, isGuest };
