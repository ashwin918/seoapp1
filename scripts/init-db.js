const pool = require('../config/database');

const initDatabase = async () => {
    const client = await pool.connect();

    try {
        console.log('🚀 Initializing database...');

        // Create users table
        await client.query(`
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                avatar_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        console.log('✅ Users table created');

        // Create connected accounts table (for OAuth)
        await client.query(`
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
        `);
        console.log('✅ Connected accounts table created');

        // Create websites table
        await client.query(`
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
        `);
        console.log('✅ Websites table created');

        // Create SEO analyses table
        await client.query(`
            CREATE TABLE IF NOT EXISTS seo_analyses (
                id SERIAL PRIMARY KEY,
                website_id INTEGER REFERENCES websites(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                url VARCHAR(500) NOT NULL,
                overall_score INTEGER,
                title_score INTEGER,
                meta_score INTEGER,
                content_score INTEGER,
                technical_score INTEGER,
                performance_score INTEGER,
                title TEXT,
                meta_description TEXT,
                h1_tags JSONB,
                h2_tags JSONB,
                images_without_alt INTEGER,
                total_images INTEGER,
                word_count INTEGER,
                internal_links INTEGER,
                external_links INTEGER,
                has_sitemap BOOLEAN,
                has_robots BOOLEAN,
                is_mobile_friendly BOOLEAN,
                page_load_time FLOAT,
                issues JSONB,
                suggestions JSONB,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        `);
        console.log('✅ SEO analyses table created');

        // Create SEO changes/edits table
        await client.query(`
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
        `);
        console.log('✅ SEO edits table created');

        // Create session table for connect-pg-simple
        await client.query(`
            CREATE TABLE IF NOT EXISTS "session" (
                "sid" VARCHAR NOT NULL COLLATE "default",
                "sess" JSON NOT NULL,
                "expire" TIMESTAMP(6) NOT NULL,
                PRIMARY KEY ("sid")
            );
            CREATE INDEX IF NOT EXISTS "IDX_session_expire" ON "session" ("expire");
        `);
        console.log('✅ Session table created');

        console.log('🎉 Database initialization complete!');

    } catch (error) {
        console.error('❌ Error initializing database:', error);
        throw error;
    } finally {
        client.release();
        await pool.end();
    }
};

initDatabase();
