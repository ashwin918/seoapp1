# SEO Bot 🤖 bert tech

A powerful SEO analysis and management web application built with Node.js, Express, PostgreSQL, and session authentication.

## Features.................................................................................................................

- **🔍 SEO Analysis**: Analyze any URL and get comprehensive SEO scores and recommendationsll
- **📊 Score Tracking**: Track your website's SEO performance over time
- **🔗 Platform Connections**: Connect GitHub, WordPress, and Shopify (demo OAuth)
- **✏️ SEO Editing**: Make and manage SEO changes directly from the dashboard
- **📈 Dashboard**: Beautiful analytics dashboard with stats and insights
- **🔐 Session Auth**: Secure session-based authentication with PostgreSQL storage

## Tech Stack

- **Backend**: Node.js, Express.js
- **Database**: PostgreSQL
- **Template Engine**: EJS
- **Session**: express-session with connect-pg-simple
- **Styling**: Custom CSS with modern design system

## Prerequisites

- Node.js v16 or higher
- PostgreSQL 12 or higher
- npm or yarn

## Installation

1. **Clone the repository**
   ```bash
   cd d:\finalyearproject\seo
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Update the database credentials in `.env`:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=seobot
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

4. **Create the database**
   ```sql
   CREATE DATABASE seobot;
   ```

5. **Initialize the database tables**
   ```bash
   npm run db:init
   ```

6. **Start the application**
   ```bash
   # Development mode (with auto-reload)
   npm run dev
   
   # Production mode
   npm start
   ```

7. **Open in browser**
   ```
   http://localhost:3000
   ```

## Project Structure

```
seo/
├── config/
│   └── database.js         # PostgreSQL connection pool
├── middleware/
│   └── auth.js             # Authentication middleware
├── public/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── app.js          # Frontend JavaScript
├── routes/
│   ├── auth.js             # Login/Register routes
│   ├── dashboard.js        # Dashboard routes
│   ├── analyze.js          # SEO analysis routes
│   ├── websites.js         # Website management routes
│   ├── oauth.js            # OAuth connection routes
│   ├── seo.js              # SEO editing routes
│   └── api.js              # REST API routes
├── scripts/
│   └── init-db.js          # Database initialization
├── views/
│   ├── partials/           # Reusable EJS partials
│   ├── auth/               # Login/Register pages
│   ├── dashboard/          # Dashboard pages
│   ├── analyze/            # Analysis pages
│   ├── websites/           # Website management pages
│   ├── oauth/              # OAuth pages
│   ├── seo/                # SEO editing pages
│   └── ...                 # Other views
├── .env                    # Environment variables
├── .env.example            # Environment template
├── package.json            # Dependencies
├── server.js               # Main application entry
└── README.md               # This file
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Login action
- `GET /register` - Registration page
- `POST /register` - Registration action
- `GET /logout` - Logout

### Dashboard
- `GET /dashboard` - Main dashboard
- `GET /dashboard/settings` - User settings
- `POST /dashboard/settings/profile` - Update profile

### Analysis
- `GET /analyze` - Analysis form
- `POST /analyze` - Perform analysis
- `GET /analyze/:id` - View analysis result
- `GET /analyze/history/all` - Analysis history

### Websites
- `GET /websites` - List websites
- `GET /websites/add` - Add website form
- `POST /websites/add` - Add website
- `GET /websites/:id` - Website details
- `POST /websites/:id/delete` - Delete website

### OAuth (Demo)
- `GET /oauth` - Connections page
- `GET /oauth/github` - Connect GitHub
- `GET /oauth/wordpress` - Connect WordPress
- `GET /oauth/shopify` - Connect Shopify
- `POST /oauth/:provider/disconnect` - Disconnect provider

### SEO Editing
- `GET /seo/edit/:websiteId` - SEO editor
- `POST /seo/edit/:websiteId` - Save SEO change
- `POST /seo/apply/:editId` - Apply change
- `POST /seo/cancel/:editId` - Cancel change

### API
- `POST /api/analyze` - Quick analysis (JSON)
- `GET /api/stats` - User statistics
- `GET /api/analyses/recent` - Recent analyses
- `GET /api/accounts` - Connected accounts

## OAuth Integration (Demo)

This application includes a **demo OAuth flow** for:
- **GitHub**: Connect GitHub accounts and repositories
- **WordPress**: Connect WordPress sites
- **Shopify**: Connect Shopify stores

Note: This is a simulated OAuth flow for demonstration purposes. In a production environment, you would implement real OAuth 2.0 with actual provider credentials.

## SEO Analysis Features

The analyzer checks for:
- ✅ Page title (length and presence)
- ✅ Meta description (length and presence)
- ✅ H1 tags (count and content)
- ✅ H2 tags
- ✅ Image alt attributes
- ✅ Internal and external links
- ✅ Word count
- ✅ robots.txt presence
- ✅ sitemap.xml presence
- ✅ Mobile-friendliness (viewport meta)
- ✅ Page load time

## License

ISC

## Author

Created with ❤️ for better SEO
