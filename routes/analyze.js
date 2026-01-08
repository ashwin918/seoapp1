const express = require('express');
const router = express.Router();
const axios = require('axios');
const cheerio = require('cheerio');
const pool = require('../config/database');
const { isAuthenticated } = require('../middleware/auth');

// ML Service URL
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000';

router.use(isAuthenticated);

// Analyze page
router.get('/', (req, res) => {
    res.render('analyze/index');
});

// Perform analysis
router.post('/', async (req, res) => {
    try {
        const { url, websiteId } = req.body;
        const userId = req.session.user.id;

        if (!url) {
            req.flash('error', 'Please provide a URL to analyze');
            return res.redirect('/analyze');
        }

        // Normalize URL
        let normalizedUrl = url;
        if (!normalizedUrl.startsWith('http://') && !normalizedUrl.startsWith('https://')) {
            normalizedUrl = 'https://' + normalizedUrl;
        }

        let analysisData;
        let useMLService = true;

        // Try ML service first
        try {
            const mlResponse = await axios.post(`${ML_SERVICE_URL}/analyze`, {
                url: normalizedUrl
            }, {
                timeout: 30000
            });
            analysisData = mlResponse.data;
        } catch (mlError) {
            console.log('ML service unavailable, falling back to basic analysis');
            useMLService = false;
        }

        // Fallback to basic analysis if ML service is down
        if (!useMLService) {
            analysisData = await performBasicAnalysis(normalizedUrl);
        }

        // Save analysis to database
        const analysisResult = await pool.query(
            `INSERT INTO seo_analyses 
             (website_id, user_id, url, overall_score, title_score, meta_score, content_score, 
              technical_score, performance_score, title, meta_description, h1_tags, h2_tags,
              images_without_alt, total_images, word_count, internal_links, external_links,
              has_sitemap, has_robots, is_mobile_friendly, page_load_time, issues, suggestions)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24)
             RETURNING *`,
            [
                websiteId || null,
                userId,
                normalizedUrl,
                analysisData.overall_score || analysisData.scores?.overall || 0,
                analysisData.scores?.title || 0,
                analysisData.scores?.meta || 0,
                analysisData.scores?.content || 0,
                analysisData.scores?.technical || 0,
                analysisData.scores?.performance || 0,
                analysisData.features?.title || '',
                analysisData.features?.meta_description || '',
                JSON.stringify(analysisData.features?.h1_tags || []),
                JSON.stringify(analysisData.features?.h2_tags || []),
                analysisData.features?.images_without_alt || 0,
                analysisData.features?.total_images || 0,
                analysisData.features?.word_count || 0,
                analysisData.features?.internal_links || 0,
                analysisData.features?.external_links || 0,
                false, // has_sitemap - would need separate check
                false, // has_robots
                analysisData.features?.is_mobile_friendly || false,
                analysisData.load_time || analysisData.features?.load_time || 0,
                JSON.stringify(analysisData.issues || []),
                JSON.stringify(analysisData.suggestions || [])
            ]
        );

        // Update website last_analyzed if websiteId provided
        if (websiteId) {
            await pool.query(
                'UPDATE websites SET last_analyzed = CURRENT_TIMESTAMP WHERE id = $1',
                [websiteId]
            );
        }

        res.render('analyze/result', {
            analysis: analysisResult.rows[0],
            mlAnalysis: analysisData.ml_analysis || null,
            seoData: {
                title: analysisData.features?.title || '',
                metaDescription: analysisData.features?.meta_description || '',
                h1Tags: analysisData.features?.h1_tags || [],
                h2Tags: analysisData.features?.h2_tags || [],
                wordCount: analysisData.features?.word_count || 0,
                imagesWithoutAlt: analysisData.features?.images_without_alt || 0,
                totalImages: analysisData.features?.total_images || 0,
                internalLinks: analysisData.features?.internal_links || 0,
                externalLinks: analysisData.features?.external_links || 0,
                hasRobots: false,
                hasSitemap: false,
                isMobileFriendly: analysisData.features?.is_mobile_friendly || false,
                loadTime: analysisData.load_time || 0,
                vocabularyRichness: analysisData.features?.vocabulary_richness || 0,
                topKeywords: analysisData.features?.top_keywords || [],
                hasSchema: analysisData.features?.has_schema || false,
                hasHttps: analysisData.features?.url_has_https || false,
                ogScore: analysisData.features?.og_score || 0
            },
            scores: {
                overall: analysisData.overall_score || 0,
                title: analysisData.scores?.title || 0,
                meta: analysisData.scores?.meta || 0,
                content: analysisData.scores?.content || 0,
                technical: analysisData.scores?.technical || 0,
                performance: analysisData.scores?.performance || 0,
                social: analysisData.scores?.social || 0
            },
            grade: analysisData.grade || 'N/A',
            issues: analysisData.issues || [],
            suggestions: analysisData.suggestions || [],
            insights: analysisData.insights || [],
            useML: useMLService
        });

    } catch (error) {
        console.error('Analysis error:', error);
        req.flash('error', 'An error occurred during analysis: ' + error.message);
        res.redirect('/analyze');
    }
});

// Basic analysis fallback
async function performBasicAnalysis(url) {
    const startTime = Date.now();
    const response = await axios.get(url, {
        timeout: 15000,
        headers: { 'User-Agent': 'SEOBot/1.0' }
    });
    const loadTime = (Date.now() - startTime) / 1000;

    const $ = cheerio.load(response.data);

    const title = $('title').text().trim() || '';
    const metaDescription = $('meta[name="description"]').attr('content') || '';

    const h1Tags = [];
    $('h1').each((i, el) => h1Tags.push($(el).text().trim()));

    const h2Tags = [];
    $('h2').each((i, el) => h2Tags.push($(el).text().trim()));

    const images = $('img');
    let imagesWithoutAlt = 0;
    images.each((i, el) => {
        if (!$(el).attr('alt') || $(el).attr('alt').trim() === '') {
            imagesWithoutAlt++;
        }
    });

    const links = $('a[href]');
    let internalLinks = 0;
    let externalLinks = 0;

    links.each((i, el) => {
        const href = $(el).attr('href');
        if (href && href.startsWith('http')) {
            externalLinks++;
        } else {
            internalLinks++;
        }
    });

    const bodyText = $('body').text().replace(/\s+/g, ' ').trim();
    const wordCount = bodyText.split(' ').filter(w => w.length > 0).length;

    const viewportMeta = $('meta[name="viewport"]').attr('content') || '';
    const isMobileFriendly = viewportMeta.includes('width=device-width');

    // Calculate scores
    let titleScore = title ? (title.length >= 30 && title.length <= 60 ? 100 : 60) : 0;
    let metaScore = metaDescription ? (metaDescription.length >= 120 && metaDescription.length <= 160 ? 100 : 60) : 0;
    let contentScore = h1Tags.length === 1 ? 70 : (h1Tags.length > 0 ? 50 : 20);
    contentScore += wordCount >= 300 ? 30 : 10;
    let technicalScore = isMobileFriendly ? 80 : 40;
    let performanceScore = loadTime < 2 ? 100 : (loadTime < 4 ? 70 : 40);

    const overallScore = Math.round(
        (titleScore * 0.15) +
        (metaScore * 0.15) +
        (contentScore * 0.25) +
        (technicalScore * 0.25) +
        (performanceScore * 0.20)
    );

    return {
        url,
        load_time: loadTime,
        overall_score: overallScore,
        scores: {
            title: titleScore,
            meta: metaScore,
            content: contentScore,
            technical: technicalScore,
            performance: performanceScore,
            social: 0
        },
        features: {
            title,
            title_length: title.length,
            meta_description: metaDescription,
            meta_description_length: metaDescription.length,
            h1_tags: h1Tags,
            h2_tags: h2Tags.slice(0, 5),
            h1_count: h1Tags.length,
            word_count: wordCount,
            total_images: images.length,
            images_without_alt: imagesWithoutAlt,
            internal_links: internalLinks,
            external_links: externalLinks,
            is_mobile_friendly: isMobileFriendly,
            load_time: loadTime
        },
        issues: generateBasicIssues(title, metaDescription, h1Tags, wordCount, isMobileFriendly, loadTime),
        suggestions: [],
        grade: overallScore >= 80 ? 'A' : overallScore >= 60 ? 'B' : overallScore >= 40 ? 'C' : 'D'
    };
}

function generateBasicIssues(title, metaDesc, h1Tags, wordCount, mobileFriendly, loadTime) {
    const issues = [];

    if (!title) issues.push({ type: 'critical', category: 'title', message: 'Missing page title' });
    else if (title.length < 30) issues.push({ type: 'warning', category: 'title', message: 'Title too short' });
    else if (title.length > 60) issues.push({ type: 'warning', category: 'title', message: 'Title too long' });

    if (!metaDesc) issues.push({ type: 'critical', category: 'meta', message: 'Missing meta description' });

    if (h1Tags.length === 0) issues.push({ type: 'critical', category: 'content', message: 'Missing H1 heading' });
    else if (h1Tags.length > 1) issues.push({ type: 'warning', category: 'content', message: 'Multiple H1 tags' });

    if (wordCount < 300) issues.push({ type: 'warning', category: 'content', message: 'Thin content' });
    if (!mobileFriendly) issues.push({ type: 'critical', category: 'technical', message: 'Not mobile-friendly' });
    if (loadTime > 3) issues.push({ type: 'warning', category: 'performance', message: 'Slow load time' });

    return issues;
}

// View specific analysis
router.get('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const userId = req.session.user.id;

        const result = await pool.query(
            'SELECT * FROM seo_analyses WHERE id = $1 AND user_id = $2',
            [id, userId]
        );

        if (result.rows.length === 0) {
            req.flash('error', 'Analysis not found');
            return res.redirect('/dashboard');
        }

        const analysis = result.rows[0];

        res.render('analyze/result', {
            analysis,
            mlAnalysis: null,
            seoData: {
                title: analysis.title,
                metaDescription: analysis.meta_description,
                h1Tags: analysis.h1_tags || [],
                h2Tags: analysis.h2_tags || [],
                wordCount: analysis.word_count,
                imagesWithoutAlt: analysis.images_without_alt,
                totalImages: analysis.total_images,
                internalLinks: analysis.internal_links,
                externalLinks: analysis.external_links,
                hasRobots: analysis.has_robots,
                hasSitemap: analysis.has_sitemap,
                isMobileFriendly: analysis.is_mobile_friendly,
                loadTime: analysis.page_load_time
            },
            scores: {
                overall: analysis.overall_score,
                title: analysis.title_score,
                meta: analysis.meta_score,
                content: analysis.content_score,
                technical: analysis.technical_score,
                performance: analysis.performance_score,
                social: 0
            },
            grade: analysis.overall_score >= 80 ? 'A' : analysis.overall_score >= 60 ? 'B' : 'C',
            issues: analysis.issues || [],
            suggestions: analysis.suggestions || [],
            insights: [],
            useML: false
        });

    } catch (error) {
        console.error('View analysis error:', error);
        req.flash('error', 'Error loading analysis');
        res.redirect('/dashboard');
    }
});

// Analysis history
router.get('/history/all', async (req, res) => {
    try {
        const userId = req.session.user.id;

        const result = await pool.query(
            `SELECT sa.*, w.name as website_name 
             FROM seo_analyses sa 
             LEFT JOIN websites w ON sa.website_id = w.id 
             WHERE sa.user_id = $1 
             ORDER BY sa.analyzed_at DESC`,
            [userId]
        );

        res.render('analyze/history', {
            analyses: result.rows
        });

    } catch (error) {
        console.error('History error:', error);
        req.flash('error', 'Error loading analysis history');
        res.redirect('/dashboard');
    }
});

module.exports = router;
