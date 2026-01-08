-- SEO Bot Database Schema
-- PostgreSQL Database

-- Create the database (run this separately if needed)
-- CREATE DATABASE seobot;

-- Connect to the database
-- \c seobot;

-- =============================================
-- Users Table
-- =============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster email lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- =============================================
-- Connected Accounts Table (OAuth)
-- =============================================
CREATE TABLE IF NOT EXISTS connected_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    account_name VARCHAR(255),
    account_url VARCHAR(500),
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, provider)
);

-- Index for faster user lookups
CREATE INDEX IF NOT EXISTS idx_connected_accounts_user_id ON connected_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_connected_accounts_provider ON connected_accounts(provider);

-- =============================================
-- Websites Table
-- =============================================
CREATE TABLE IF NOT EXISTS websites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    name VARCHAR(255),
    platform VARCHAR(50),
    connected_account_id INTEGER REFERENCES connected_accounts(id) ON DELETE SET NULL,
    last_analyzed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster user lookups
CREATE INDEX IF NOT EXISTS idx_websites_user_id ON websites(user_id);

-- =============================================
-- SEO Analyses Table
-- =============================================
CREATE TABLE IF NOT EXISTS seo_analyses (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    
    -- Scores
    overall_score INTEGER,
    title_score INTEGER,
    meta_score INTEGER,
    content_score INTEGER,
    technical_score INTEGER,
    performance_score INTEGER,
    
    -- SEO Data
    title TEXT,
    meta_description TEXT,
    h1_tags JSONB,
    h2_tags JSONB,
    
    -- Image Analysis
    images_without_alt INTEGER,
    total_images INTEGER,
    
    -- Content Analysis
    word_count INTEGER,
    internal_links INTEGER,
    external_links INTEGER,
    
    -- Technical Analysis
    has_sitemap BOOLEAN,
    has_robots BOOLEAN,
    is_mobile_friendly BOOLEAN,
    page_load_time FLOAT,
    
    -- Issues and Suggestions
    issues JSONB,
    suggestions JSONB,
    
    -- Timestamp
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_seo_analyses_user_id ON seo_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_seo_analyses_website_id ON seo_analyses(website_id);
CREATE INDEX IF NOT EXISTS idx_seo_analyses_analyzed_at ON seo_analyses(analyzed_at DESC);

-- =============================================
-- SEO Edits Table
-- =============================================
CREATE TABLE IF NOT EXISTS seo_edits (
    id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    page_url VARCHAR(500),
    field_type VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    applied_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_seo_edits_website_id ON seo_edits(website_id);
CREATE INDEX IF NOT EXISTS idx_seo_edits_user_id ON seo_edits(user_id);
CREATE INDEX IF NOT EXISTS idx_seo_edits_status ON seo_edits(status);

-- =============================================
-- Session Table (for connect-pg-simple)
-- =============================================
CREATE TABLE IF NOT EXISTS "session" (
    "sid" VARCHAR NOT NULL COLLATE "default",
    "sess" JSON NOT NULL,
    "expire" TIMESTAMP(6) NOT NULL,
    PRIMARY KEY ("sid")
);

CREATE INDEX IF NOT EXISTS "IDX_session_expire" ON "session" ("expire");

-- =============================================
-- Sample Data (Optional - for testing)
-- =============================================

-- Uncomment below to insert a test user (password: password123)
-- INSERT INTO users (email, password, name) VALUES 
-- ('test@example.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4bQfqT7p4QHR4B3e', 'Test User');

-- =============================================
-- Useful Queries
-- =============================================

-- Get user with their connected accounts
-- SELECT u.*, ca.provider, ca.account_name 
-- FROM users u 
-- LEFT JOIN connected_accounts ca ON u.id = ca.user_id 
-- WHERE u.id = 1;

-- Get website with latest analysis score
-- SELECT w.*, 
--        (SELECT overall_score FROM seo_analyses WHERE website_id = w.id ORDER BY analyzed_at DESC LIMIT 1) as latest_score
-- FROM websites w 
-- WHERE w.user_id = 1;

-- Get analysis history for a user
-- SELECT * FROM seo_analyses WHERE user_id = 1 ORDER BY analyzed_at DESC;

-- Get pending SEO edits
-- SELECT * FROM seo_edits WHERE status = 'pending' ORDER BY created_at DESC;
