"""
SEO Bot ML Service
Real AI-Powered Website SEO Analysis with Machine Learning
Includes Content Generation and Platform Push
"""

import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib.parse import urlparse
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import ML analyzer and content generator
from ml_analyzer import SEOMLAnalyzer
from content_generator import SEOContentGenerator, ContentPusher

# Import agents
from agents.scraper_agent import ScraperAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.content_suggestion_agent import ContentSuggestionAgent
from agents.writer_agent import WriterAgent

app = Flask(__name__)
CORS(app)

# Initialize components
print("🧠 Initializing SEO ML Service with Agent Architecture...")
print("🕷️ Initializing Scraper Agent...")
scraper_agent = ScraperAgent()

print("🤖 Initializing Analyzer Agent...")
analyzer_agent = AnalyzerAgent()

print("💡 Initializing Content Suggestion Agent...")
content_suggestion_agent = ContentSuggestionAgent()

print("✍️ Initializing Writer Agent...")
writer_agent = WriterAgent()

# Legacy support
ml_analyzer = SEOMLAnalyzer()
content_generator = SEOContentGenerator()

print("✅ All agents ready!")
print("✅ ML Analyzer ready!")
print("✅ Content Generator ready!")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SEO ML Analyzer',
        'version': '2.0.0',
        'ml_model': 'GradientBoostingRegressor',
        'features': 33,
        'agents': ['ScraperAgent', 'AnalyzerAgent', 'ContentSuggestionAgent', 'WriterAgent']
    })

@app.route('/analyze-agents', methods=['POST'])
def analyze_url_with_agents():
    """
    Analyze a URL using Agent Architecture
    Expects JSON: { "url": "https://example.com", "platform": "wordpress" (optional) }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        print(f"🔍 Agent Pipeline: Starting analysis for {url}")
        
        # Step 1: Scraper Agent - Fetch and extract features
        scrape_result = scraper_agent.scrape_url(url)
        
        if not scrape_result['success']:
            return jsonify({'error': scrape_result['error']}), 400
        
        features = scraper_agent.extract_features(
            scrape_result['html'],
            scrape_result['url'],
            scrape_result['load_time'],
            scrape_result['response']
        )
        
        # Step 2: Analyzer Agent - ML analysis
        analysis_results = analyzer_agent.analyze(features)
        
        # Step 3: Content Suggestion Agent - Generate suggestions
        content_suggestions = content_suggestion_agent.generate_suggestions(features, analysis_results)
        
        # Step 4: Writer Agent - Format for platform (optional)
        platform = data.get('platform', 'wordpress')
        formatted_content = writer_agent.write_content(content_suggestions, platform)
        
        print(f"✅ Agent Pipeline: Complete! Score: {analysis_results['overall_score']}/100")
        
        # Combine results
        result = {
            'url': url,
            'status_code': scrape_result['status_code'],
            'load_time': round(scrape_result['load_time'], 3),
            'agent_pipeline': {
                'scraper': 'ScraperAgent',
                'analyzer': 'AnalyzerAgent',
                'content_suggestion': 'ContentSuggestionAgent',
                'writer': 'WriterAgent'
            },
            'features': features,
            'ml_analysis': {
                'model_type': analysis_results.get('model_info', {}).get('type', 'GradientBoostingRegressor'),
                'features_analyzed': analysis_results.get('model_info', {}).get('features_used', 33),
                'feature_importance': analysis_results.get('feature_importance', {})
            },
            'scores': analysis_results['scores'],
            'overall_score': analysis_results['overall_score'],
            'grade': get_grade(analysis_results['overall_score']),
            'issues': analysis_results['issues'],
            'suggestions': analysis_results['suggestions'],
            'insights': analysis_results.get('insights', []),
            'content_suggestions': content_suggestions,
            'formatted_content': formatted_content
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Agent Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze_url():
    """
    Analyze a URL using Agent Architecture
    Expects JSON: { "url": "https://example.com" }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        print(f"🔍 Analyzing: {url}")
        
        # Step 1: Scraper Agent - Fetch and extract features
        scrape_result = scraper_agent.scrape_url(url)
        
        if not scrape_result['success']:
            return jsonify({'error': scrape_result['error']}), 400
        
        features = scraper_agent.extract_features(
            scrape_result['html'],
            scrape_result['url'],
            scrape_result['load_time'],
            scrape_result['response']
        )
        
        # Step 2: Analyzer Agent - ML analysis
        analysis_results = analyzer_agent.analyze(features)
        
        print(f"🤖 ML Score: {analysis_results['overall_score']}/100")
        
        # Build response
        result = {
            'url': url,
            'status_code': scrape_result['status_code'],
            'load_time': round(scrape_result['load_time'], 3),
            'scores': analysis_results['scores'],
            'overall_score': analysis_results['overall_score'],
            'grade': get_grade(analysis_results['overall_score']),
            'issues': analysis_results['issues'],
            'suggestions': analysis_results['suggestions'],
            'insights': analysis_results.get('insights', []),
            'features': features,
            'ml_analysis': {
                'model_type': analysis_results.get('model_info', {}).get('type', 'GradientBoostingRegressor'),
                'features_analyzed': analysis_results.get('model_info', {}).get('features_used', 33)
            }
        }

        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the ML model"""
    return jsonify({
        'model_type': 'GradientBoostingRegressor',
        'num_features': 33,
        'training_samples': 5000,
        'score_categories': ['title', 'meta', 'content', 'technical', 'performance', 'social', 'overall'],
        'feature_groups': {
            'title': ['title_length', 'title_length_optimal', 'has_title'],
            'meta': ['meta_desc_length', 'meta_desc_length_optimal', 'has_meta_desc'],
            'content': ['h1_count', 'h2_count', 'word_count', 'vocabulary_richness', 'images_with_alt_ratio'],
            'technical': ['has_https', 'is_mobile_friendly', 'has_schema', 'has_canonical'],
            'performance': ['load_time', 'response_size_kb'],
            'social': ['has_og_title', 'has_og_desc', 'has_og_image', 'has_twitter_card']
        }
    })

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Generate optimized SEO content using Content Suggestion Agent and Writer Agent
    Expects JSON: { "url": "https://example.com", "platform": "wordpress" (optional) }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        features = {}
        analysis_results = {}
        
        # If URL provided, fetch and analyze first
        if 'url' in data:
            url = data['url']
            print(f"✍️ Generating content for: {url}")
            
            # Step 1: Scraper Agent - Fetch and extract features
            scrape_result = scraper_agent.scrape_url(url)
            
            if not scrape_result['success']:
                return jsonify({'error': scrape_result['error']}), 400
            
            features = scraper_agent.extract_features(
                scrape_result['html'],
                scrape_result['url'],
                scrape_result['load_time'],
                scrape_result['response']
            )
            
            # Step 2: Analyzer Agent - ML analysis
            analysis_results = analyzer_agent.analyze(features)
            
        elif 'features' in data and 'analysis' in data:
            features = data['features']
            analysis_results = data['analysis']
        else:
            return jsonify({'error': 'URL or (features + analysis) required'}), 400
        
        # Step 3: Content Suggestion Agent - Generate suggestions
        content_suggestions = content_suggestion_agent.generate_suggestions(features, analysis_results)
        
        # Step 4: Writer Agent - Format for platform
        platform = data.get('platform', 'wordpress')
        formatted_content = writer_agent.write_content(content_suggestions, platform)
        
        print(f"✅ Generated content for {platform}")
        
        # Also generate for all platforms
        platform_formats = {
            'wordpress': writer_agent.write_content(content_suggestions, 'wordpress'),
            'shopify': writer_agent.write_content(content_suggestions, 'shopify'),
            'github': writer_agent.write_content(content_suggestions, 'github'),
            'html': writer_agent.write_content(content_suggestions, 'html'),
            'markdown': writer_agent.write_content(content_suggestions, 'markdown')
        }
        
        return jsonify({
            'success': True,
            'url': features.get('url', ''),
            'generated_content': content_suggestions,
            'formatted_content': formatted_content,
            'platform_formats': platform_formats,
            'agent_pipeline': {
                'content_suggestion': 'ContentSuggestionAgent',
                'writer': 'WriterAgent'
            }
        })
        
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/push', methods=['POST'])
def push_content():
    """
    Push generated content to connected platform
    Expects JSON: {
        "platform": "wordpress|shopify|github",
        "account": { "access_token": "...", "site_url": "..." },
        "content": { "title": "...", "meta_description": "..." },
        "target": { "post_id": "..." or "page_url": "..." }
    }
    """
    try:
        data = request.get_json()
        
        platform = data.get('platform')
        account = data.get('account', {})
        content = data.get('content', {})
        target = data.get('target', {})
        
        if not platform or not content:
            return jsonify({'error': 'Platform and content required'}), 400
        
        print(f"📤 Pushing content to {platform} using Writer Agent")
        
        # Use Writer Agent to format content for the platform
        suggestions = {
            'title': {'suggestions': [{'content': content.get('title', '')}]},
            'meta_description': {'suggestions': [{'content': content.get('meta_description', '')}]},
            'keyword_recommendations': {'primary': content.get('keyword', 'seo')}
        }
        
        formatted_content = writer_agent.write_content(suggestions, platform)
        
        result = {
            'success': True,
            'platform': platform,
            'message': f'Content formatted and prepared for {platform}',
            'agent_used': 'WriterAgent'
        }
        
        if platform == 'wordpress':
            result['push_data'] = push_to_wordpress(account, formatted_content, target)
        elif platform == 'shopify':
            result['push_data'] = push_to_shopify(account, formatted_content, target)
        elif platform == 'github':
            result['push_data'] = push_to_github(account, formatted_content, target)
        else:
            return jsonify({'error': f'Unknown platform: {platform}'}), 400
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Push error: {e}")
        return jsonify({'error': str(e)}), 500

def push_to_wordpress(account, content, target):
    """Push SEO content to WordPress site"""
    site_url = account.get('site_url', '')
    access_token = account.get('access_token', '')
    post_id = target.get('post_id', '')
    
    # Prepare WordPress API payload
    payload = {
        'title': content.get('title', ''),
        'excerpt': content.get('meta_description', ''),
        'meta': {
            '_yoast_wpseo_title': content.get('title', ''),
            '_yoast_wpseo_metadesc': content.get('meta_description', ''),
        }
    }
    
    # In production, this would make actual API call
    # For demo, return the prepared payload
    return {
        'status': 'prepared',
        'api_endpoint': f'{site_url}/wp-json/wp/v2/posts/{post_id}',
        'method': 'PUT',
        'payload': payload,
        'note': 'Demo mode - actual push requires valid WordPress credentials'
    }

def push_to_shopify(account, content, target):
    """Push SEO content to Shopify store"""
    store_url = account.get('store_url', '')
    access_token = account.get('access_token', '')
    resource_type = target.get('type', 'page')  # page, product, collection
    resource_id = target.get('id', '')
    
    # Prepare Shopify API payload
    payload = {
        resource_type: {
            'metafields': [
                {
                    'namespace': 'global',
                    'key': 'title_tag',
                    'value': content.get('title', ''),
                    'type': 'single_line_text_field'
                },
                {
                    'namespace': 'global',
                    'key': 'description_tag',
                    'value': content.get('meta_description', ''),
                    'type': 'multi_line_text_field'
                }
            ]
        }
    }
    
    return {
        'status': 'prepared',
        'api_endpoint': f'{store_url}/admin/api/2024-01/{resource_type}s/{resource_id}.json',
        'method': 'PUT',
        'payload': payload,
        'note': 'Demo mode - actual push requires valid Shopify credentials'
    }

def push_to_github(account, content, target):
    """Push SEO content to GitHub Pages"""
    repo = account.get('repo', '')
    access_token = account.get('access_token', '')
    file_path = target.get('file_path', 'index.html')
    
    # Generate updated content with SEO meta tags
    seo_meta = f'''<!-- SEO Meta Tags - Generated by SEO Bot -->
<title>{content.get('title', '')}</title>
<meta name="description" content="{content.get('meta_description', '')}">
<meta property="og:title" content="{content.get('title', '')}">
<meta property="og:description" content="{content.get('meta_description', '')}">
'''
    
    return {
        'status': 'prepared',
        'api_endpoint': f'https://api.github.com/repos/{repo}/contents/{file_path}',
        'method': 'PUT',
        'seo_meta_tags': seo_meta,
        'note': 'Demo mode - actual push requires valid GitHub token'
    }

def get_grade(score):
    """Convert score to letter grade"""
    if score >= 90:
        return 'A+'
    elif score >= 85:
        return 'A'
    elif score >= 80:
        return 'A-'
    elif score >= 75:
        return 'B+'
    elif score >= 70:
        return 'B'
    elif score >= 65:
        return 'B-'
    elif score >= 60:
        return 'C+'
    elif score >= 55:
        return 'C'
    elif score >= 50:
        return 'C-'
    elif score >= 40:
        return 'D'
    else:
        return 'F'

if __name__ == '__main__':
    port = int(os.environ.get('ML_SERVICE_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\\n🚀 SEO ML Service starting on port {port}")
    print(f"📊 ML Model: GradientBoostingRegressor (33 features)")
    print(f"🔗 API Endpoint: http://localhost:{port}/analyze\\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
def analyze_url():
    """
    Analyze a URL using trained ML model
    Expects JSON: { "url": "https://example.com" }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        
        # Normalize URL
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        print(f"🔍 Analyzing: {url}")
        
        # Fetch the page
        start_time = time.time()
        try:
            headers = {
                'User-Agent': 'SEOBot-ML/2.0 (AI SEO Analyzer; Machine Learning)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 400
        
        load_time = time.time() - start_time
        html = response.text
        
        print(f"📄 Page fetched in {load_time:.2f}s ({len(response.content)/1024:.1f} KB)")
        
        # Parse HTML
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract features for ML model
        features = extract_features(soup, url, load_time, response)
        
        print(f"🔬 Extracted {len(features)} features")
        
        # Run ML analysis
        ml_results = ml_analyzer.analyze(features)
        
        print(f"🤖 ML Score: {ml_results['overall_score']}/100")
        
        # Combine results
        result = {
            'url': url,
            'status_code': response.status_code,
            'load_time': round(load_time, 3),
            'features': features,
            'ml_analysis': {
                'model_type': ml_results.get('model_info', {}).get('type', 'GradientBoostingRegressor'),
                'features_analyzed': ml_results.get('model_info', {}).get('features_used', 33),
                'feature_importance': ml_results.get('feature_importance', {})
            },
            'scores': ml_results['scores'],
            'overall_score': ml_results['overall_score'],
            'grade': get_grade(ml_results['overall_score']),
            'issues': ml_results['issues'],
            'suggestions': ml_results['suggestions'],
            'insights': ml_results.get('insights', [])
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the ML model"""
    return jsonify({
        'model_type': 'GradientBoostingRegressor',
        'num_features': 33,
        'training_samples': 5000,
        'score_categories': ['title', 'meta', 'content', 'technical', 'performance', 'social', 'overall'],
        'feature_groups': {
            'title': ['title_length', 'title_length_optimal', 'has_title'],
            'meta': ['meta_desc_length', 'meta_desc_length_optimal', 'has_meta_desc'],
            'content': ['h1_count', 'h2_count', 'word_count', 'vocabulary_richness', 'images_with_alt_ratio'],
            'technical': ['has_https', 'is_mobile_friendly', 'has_schema', 'has_canonical'],
            'performance': ['load_time', 'response_size_kb'],
            'social': ['has_og_title', 'has_og_desc', 'has_og_image', 'has_twitter_card']
        }
    })

@app.route('/generate', methods=['POST'])
def generate_content():
    """
    Generate optimized SEO content based on analysis
    Expects JSON: { "url": "https://example.com" } or { "features": {...}, "analysis": {...} }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body required'}), 400
        
        # If URL provided, fetch and analyze first
        if 'url' in data:
            url = data['url']
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'https://' + url
            
            print(f"✍️ Generating content for: {url}")
            
            # Fetch page
            headers = {
                'User-Agent': 'SEOBot-ML/2.0 (AI Content Generator)',
                'Accept': 'text/html,application/xhtml+xml',
            }
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            features = extract_features(soup, url, 0, response)
            ml_results = ml_analyzer.analyze(features)
        elif 'features' in data:
            features = data['features']
            ml_results = data.get('analysis', {})
        else:
            return jsonify({'error': 'URL or features required'}), 400
        
        # Generate optimized content
        generated = content_generator.generate_optimized_content(features, ml_results)
        
        print(f"✅ Generated {len(generated)} content sections")
        
        return jsonify({
            'success': True,
            'url': features.get('url', ''),
            'generated_content': generated,
            'platform_formats': {
                'wordpress': ContentPusher.format_for_wordpress(generated),
                'shopify': ContentPusher.format_for_shopify(generated),
                'github': ContentPusher.format_for_github(generated)
            }
        })
        
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/push', methods=['POST'])
def push_content():
    """
    Push generated content to connected platform
    Expects JSON: {
        "platform": "wordpress|shopify|github",
        "account": { "access_token": "...", "site_url": "..." },
        "content": { "title": "...", "meta_description": "..." },
        "target": { "post_id": "..." or "page_url": "..." }
    }
    """
    try:
        data = request.get_json()
        
        platform = data.get('platform')
        account = data.get('account', {})
        content = data.get('content', {})
        target = data.get('target', {})
        
        if not platform or not content:
            return jsonify({'error': 'Platform and content required'}), 400
        
        print(f"📤 Pushing content to {platform}")
        
        result = {
            'success': True,
            'platform': platform,
            'message': f'Content prepared for {platform}'
        }
        
        if platform == 'wordpress':
            result['push_data'] = push_to_wordpress(account, content, target)
        elif platform == 'shopify':
            result['push_data'] = push_to_shopify(account, content, target)
        elif platform == 'github':
            result['push_data'] = push_to_github(account, content, target)
        else:
            return jsonify({'error': f'Unknown platform: {platform}'}), 400
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Push error: {e}")
        return jsonify({'error': str(e)}), 500

def push_to_wordpress(account, content, target):
    """Push SEO content to WordPress site"""
    site_url = account.get('site_url', '')
    access_token = account.get('access_token', '')
    post_id = target.get('post_id', '')
    
    # Prepare WordPress API payload
    payload = {
        'title': content.get('title', ''),
        'excerpt': content.get('meta_description', ''),
        'meta': {
            '_yoast_wpseo_title': content.get('title', ''),
            '_yoast_wpseo_metadesc': content.get('meta_description', ''),
        }
    }
    
    # In production, this would make actual API call
    # For demo, return the prepared payload
    return {
        'status': 'prepared',
        'api_endpoint': f'{site_url}/wp-json/wp/v2/posts/{post_id}',
        'method': 'PUT',
        'payload': payload,
        'note': 'Demo mode - actual push requires valid WordPress credentials'
    }

def push_to_shopify(account, content, target):
    """Push SEO content to Shopify store"""
    store_url = account.get('store_url', '')
    access_token = account.get('access_token', '')
    resource_type = target.get('type', 'page')  # page, product, collection
    resource_id = target.get('id', '')
    
    # Prepare Shopify API payload
    payload = {
        resource_type: {
            'metafields': [
                {
                    'namespace': 'global',
                    'key': 'title_tag',
                    'value': content.get('title', ''),
                    'type': 'single_line_text_field'
                },
                {
                    'namespace': 'global',
                    'key': 'description_tag',
                    'value': content.get('meta_description', ''),
                    'type': 'multi_line_text_field'
                }
            ]
        }
    }
    
    return {
        'status': 'prepared',
        'api_endpoint': f'{store_url}/admin/api/2024-01/{resource_type}s/{resource_id}.json',
        'method': 'PUT',
        'payload': payload,
        'note': 'Demo mode - actual push requires valid Shopify credentials'
    }

def push_to_github(account, content, target):
    """Push SEO content to GitHub Pages"""
    repo = account.get('repo', '')
    access_token = account.get('access_token', '')
    file_path = target.get('file_path', 'index.html')
    
    # Generate updated content with SEO meta tags
    seo_meta = f'''<!-- SEO Meta Tags - Generated by SEO Bot -->
<title>{content.get('title', '')}</title>
<meta name="description" content="{content.get('meta_description', '')}">
<meta property="og:title" content="{content.get('title', '')}">
<meta property="og:description" content="{content.get('meta_description', '')}">
'''
    
    return {
        'status': 'prepared',
        'api_endpoint': f'https://api.github.com/repos/{repo}/contents/{file_path}',
        'method': 'PUT',
        'seo_meta_tags': seo_meta,
        'note': 'Demo mode - actual push requires valid GitHub token'
    }

def extract_features(soup, url, load_time, response):
    """Extract SEO features from HTML for ML model"""
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Title
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''
    
    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_desc.get('content', '').strip() if meta_desc else ''
    
    # Meta keywords
    meta_kw = soup.find('meta', attrs={'name': 'keywords'})
    meta_keywords = meta_kw.get('content', '').strip() if meta_kw else ''
    
    # Canonical URL
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    canonical_url = canonical.get('href', '') if canonical else ''
    
    # Open Graph
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_description = soup.find('meta', attrs={'property': 'og:description'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    
    # Twitter Card
    twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
    
    # Headings
    h1_tags = [h.get_text().strip() for h in soup.find_all('h1')]
    h2_tags = [h.get_text().strip() for h in soup.find_all('h2')]
    h3_tags = [h.get_text().strip() for h in soup.find_all('h3')]
    
    # Images
    images = soup.find_all('img')
    images_with_alt = sum(1 for img in images if img.get('alt', '').strip())
    images_without_alt = len(images) - images_with_alt
    
    # Links
    links = soup.find_all('a', href=True)
    internal_links = 0
    external_links = 0
    nofollow_links = 0
    
    for link in links:
        href = link.get('href', '')
        rel = link.get('rel', [])
        
        if 'nofollow' in rel:
            nofollow_links += 1
        
        if href.startswith('/') or domain in href:
            internal_links += 1
        elif href.startswith('http'):
            external_links += 1
    
    # Content
    body = soup.find('body')
    if body:
        # Remove script and style elements
        for script in body.find_all(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        text = body.get_text(separator=' ', strip=True)
    else:
        text = soup.get_text(separator=' ', strip=True)
    
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_count = len(words)
    unique_words = len(set(words))
    
    # Calculate text metrics
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    avg_sentence_length = word_count / max(sentence_count, 1)
    
    # Paragraphs
    paragraphs = soup.find_all('p')
    paragraph_count = len(paragraphs)
    
    # Viewport meta (mobile-friendliness)
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    has_viewport = viewport is not None
    is_mobile_friendly = has_viewport and 'width=device-width' in viewport.get('content', '')
    
    # Structured data
    schema_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
    has_schema = len(schema_scripts) > 0
    
    # Robots meta
    robots_meta = soup.find('meta', attrs={'name': 'robots'})
    robots_content = robots_meta.get('content', '') if robots_meta else ''
    
    # Language
    html_tag = soup.find('html')
    lang = html_tag.get('lang', '') if html_tag else ''
    
    # Check for common SEO elements
    has_favicon = soup.find('link', attrs={'rel': lambda x: x and 'icon' in x.lower()}) is not None
    
    # Forms and media
    forms = soup.find_all('form')
    videos = soup.find_all(['video', 'iframe'])
    
    # Calculate keyword density (top 10 words)
    word_freq = {}
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'it', 'this', 'that', 'are', 'was', 'be', 'has', 'have', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'not', 'no', 'yes', 'all', 'any', 'some', 'as', 'from', 'they', 'them', 'their', 'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how', 'your', 'you', 'our', 'we', 'us', 'more', 'get', 'about'}
    
    for word in words:
        if word not in stop_words and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Calculate heading structure score
    heading_score = calculate_heading_score(h1_tags, h2_tags, h3_tags)
    
    features = {
        # Basic info
        'url': url,
        'domain': domain,
        'load_time': load_time,
        
        # Title
        'title': title,
        'title_length': len(title),
        'has_title': len(title) > 0,
        'title_has_keyword': any(kw[0] in title.lower() for kw in top_keywords[:3]) if top_keywords else False,
        
        # Meta
        'meta_description': meta_description,
        'meta_description_length': len(meta_description),
        'has_meta_description': len(meta_description) > 0,
        'meta_keywords': meta_keywords,
        'has_meta_keywords': len(meta_keywords) > 0,
        
        # Canonical & URLs
        'canonical_url': canonical_url,
        'has_canonical': len(canonical_url) > 0,
        'url_length': len(url),
        'url_has_https': url.startswith('https'),
        
        # Open Graph
        'has_og_title': og_title is not None,
        'has_og_description': og_description is not None,
        'has_og_image': og_image is not None,
        'og_score': sum([og_title is not None, og_description is not None, og_image is not None]) / 3 * 100,
        
        # Twitter
        'has_twitter_card': twitter_card is not None,
        
        # Headings
        'h1_count': len(h1_tags),
        'h1_tags': h1_tags,
        'h2_count': len(h2_tags),
        'h2_tags': h2_tags[:5],
        'h3_count': len(h3_tags),
        'has_proper_h1': len(h1_tags) == 1,
        'heading_structure_score': heading_score,
        
        # Images
        'total_images': len(images),
        'images_with_alt': images_with_alt,
        'images_without_alt': images_without_alt,
        'image_alt_ratio': images_with_alt / max(len(images), 1) * 100,
        
        # Links
        'total_links': len(links),
        'internal_links': internal_links,
        'external_links': external_links,
        'nofollow_links': nofollow_links,
        'link_ratio': internal_links / max(external_links, 1),
        
        # Content
        'word_count': word_count,
        'unique_words': unique_words,
        'vocabulary_richness': unique_words / max(word_count, 1) * 100,
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'paragraph_count': paragraph_count,
        'top_keywords': top_keywords,
        
        # Technical
        'is_mobile_friendly': is_mobile_friendly,
        'has_viewport': has_viewport,
        'has_schema': has_schema,
        'robots_content': robots_content,
        'has_lang': len(lang) > 0,
        'lang': lang,
        'has_favicon': has_favicon,
        
        # Media
        'video_count': len(videos),
        'form_count': len(forms),
        
        # Performance
        'response_size': len(response.content),
        'response_size_kb': len(response.content) / 1024,
    }
    
    return features

def calculate_heading_score(h1_tags, h2_tags, h3_tags):
    """Calculate heading structure score"""
    score = 100
    
    # H1 should be exactly 1
    if len(h1_tags) == 0:
        score -= 40
    elif len(h1_tags) > 1:
        score -= 20
    
    # Should have H2s
    if len(h2_tags) == 0:
        score -= 20
    elif len(h2_tags) > 10:
        score -= 10
    
    # H3s are optional but good
    if len(h3_tags) > 0:
        score += 10
    
    return min(max(score, 0), 100)

def get_grade(score):
    """Convert score to letter grade"""
    if score >= 90:
        return 'A+'
    elif score >= 85:
        return 'A'
    elif score >= 80:
        return 'A-'
    elif score >= 75:
        return 'B+'
    elif score >= 70:
        return 'B'
    elif score >= 65:
        return 'B-'
    elif score >= 60:
        return 'C+'
    elif score >= 55:
        return 'C'
    elif score >= 50:
        return 'C-'
    elif score >= 40:
        return 'D'
    else:
        return 'F'

if __name__ == '__main__':
    port = int(os.environ.get('ML_SERVICE_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"\n🚀 SEO ML Service starting on port {port}")
    print(f"📊 ML Model: GradientBoostingRegressor (33 features)")
    print(f"🔗 API Endpoint: http://localhost:{port}/analyze\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
