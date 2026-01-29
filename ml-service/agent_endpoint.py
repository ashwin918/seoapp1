"""
Agent Pipeline Endpoint for SEO Analysis
Uses the agent architecture for modular SEO analysis
"""

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
