"""
Writer Agent - SEO Content Writing and Optimization
Writes and optimizes SEO content for different platforms
"""

import json


class WriterAgent:
    """
    Agent responsible for writing and formatting SEO content for various platforms
    """
    
    def __init__(self):
        self.platform_formatters = {
            'wordpress': self._format_wordpress,
            'shopify': self._format_shopify,
            'github': self._format_github,
            'html': self._format_html,
            'markdown': self._format_markdown
        }
    
    def write_content(self, suggestions, platform='wordpress'):
        """
        Write and format content based on suggestions for a specific platform
        """
        print(f"✍️ Writer Agent: Writing content for {platform}")
        
        if platform not in self.platform_formatters:
            print(f"⚠️ Writer Agent: Unknown platform {platform}, using default")
            platform = 'wordpress'
        
        formatter = self.platform_formatters[platform]
        formatted_content = formatter(suggestions)
        
        print(f"✅ Writer Agent: Content formatted for {platform}")
        
        return formatted_content
    
    def _format_wordpress(self, suggestions):
        """Format content for WordPress API"""
        title_suggestion = suggestions.get('title', {}).get('suggestions', [{}])[0].get('content', '')
        meta_suggestion = suggestions.get('meta_description', {}).get('suggestions', [{}])[0].get('content', '')
        
        return {
            'title': title_suggestion,
            'excerpt': meta_suggestion,
            'meta': {
                'yoast_wpseo_title': title_suggestion,
                'yoast_wpseo_metadesc': meta_suggestion,
            },
            'content': self._generate_blog_content(suggestions)
        }
    
    def _format_shopify(self, suggestions):
        """Format content for Shopify API"""
        title_suggestion = suggestions.get('title', {}).get('suggestions', [{}])[0].get('content', '')
        meta_suggestion = suggestions.get('meta_description', {}).get('suggestions', [{}])[0].get('content', '')
        
        return {
            'metafields': [
                {
                    'namespace': 'seo',
                    'key': 'title',
                    'value': title_suggestion,
                    'type': 'single_line_text_field'
                },
                {
                    'namespace': 'seo',
                    'key': 'description',
                    'value': meta_suggestion,
                    'type': 'multi_line_text_field'
                }
            ]
        }
    
    def _format_github(self, suggestions):
        """Format content for GitHub Pages"""
        title_suggestion = suggestions.get('title', {}).get('suggestions', [{}])[0].get('content', '')
        meta_suggestion = suggestions.get('meta_description', {}).get('suggestions', [{}])[0].get('content', '')
        
        yaml_front_matter = f"""---
title: "{title_suggestion}"
description: "{meta_suggestion}"
---
"""
        return {
            'front_matter': yaml_front_matter,
            'content': self._generate_markdown_content(suggestions)
        }
    
    def _format_html(self, suggestions):
        """Format content as HTML"""
        title_suggestion = suggestions.get('title', {}).get('suggestions', [{}])[0].get('content', '')
        meta_suggestion = suggestions.get('meta_description', {}).get('suggestions', [{}])[0].get('content', '')
        h1_suggestion = suggestions.get('h1_suggestion', {}).get('suggestions', [None])[0]
        
        schema = suggestions.get('schema_suggestion', {}).get('schema', {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_suggestion}</title>
    <meta name="description" content="{meta_suggestion}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title_suggestion}">
    <meta property="og:description" content="{meta_suggestion}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title_suggestion}">
    <meta name="twitter:description" content="{meta_suggestion}">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {json.dumps(schema, indent=2)}
    </script>
</head>
<body>
    <h1>{h1_suggestion or title_suggestion}</h1>
    {self._generate_blog_content(suggestions)}
</body>
</html>"""
        
        return {
            'html': html,
            'title': title_suggestion,
            'meta_description': meta_suggestion
        }
    
    def _format_markdown(self, suggestions):
        """Format content as Markdown"""
        title_suggestion = suggestions.get('title', {}).get('suggestions', [{}])[0].get('content', '')
        meta_suggestion = suggestions.get('meta_description', {}).get('suggestions', [{}])[0].get('content', '')
        h1_suggestion = suggestions.get('h1_suggestion', {}).get('suggestions', [None])[0]
        
        markdown = f"""# {h1_suggestion or title_suggestion}

{meta_suggestion}

{self._generate_markdown_content(suggestions)}
"""
        
        return {
            'markdown': markdown,
            'title': title_suggestion,
            'meta_description': meta_suggestion
        }
    
    def _generate_blog_content(self, suggestions):
        """Generate HTML blog content from suggestions"""
        keyword_recs = suggestions.get('keyword_recommendations', {})
        primary_keyword = keyword_recs.get('primary', 'your topic')
        
        content = f"""
<div class="seo-optimized-content">
    <p>Welcome to our comprehensive guide on {primary_keyword}. This article will help you understand everything you need to know.</p>
    
    <h2>What is {primary_keyword.title()}?</h2>
    <p>Learn the fundamentals and key concepts that make {primary_keyword} essential for your success.</p>
    
    <h2>Benefits of {primary_keyword.title()}</h2>
    <ul>
        <li>Improved performance and results</li>
        <li>Better user experience</li>
        <li>Increased efficiency</li>
        <li>Cost-effective solutions</li>
    </ul>
    
    <h2>How to Get Started</h2>
    <p>Follow these simple steps to begin your journey with {primary_keyword}:</p>
    <ol>
        <li>Understand your goals and requirements</li>
        <li>Research and plan your approach</li>
        <li>Implement best practices</li>
        <li>Monitor and optimize continuously</li>
    </ol>
    
    <h2>Frequently Asked Questions</h2>
    <h3>Why is {primary_keyword} important?</h3>
    <p>{primary_keyword.title()} is crucial for achieving better results and staying competitive in today's market.</p>
    
    <h3>How long does it take to see results?</h3>
    <p>Results can vary, but most users see improvements within the first few weeks of implementation.</p>
    
    <h2>Conclusion</h2>
    <p>Start your {primary_keyword} journey today and experience the benefits firsthand. Get in touch with us to learn more!</p>
</div>
"""
        return content
    
    def _generate_markdown_content(self, suggestions):
        """Generate Markdown content from suggestions"""
        keyword_recs = suggestions.get('keyword_recommendations', {})
        primary_keyword = keyword_recs.get('primary', 'your topic')
        
        content = f"""
Welcome to our comprehensive guide on {primary_keyword}. This article will help you understand everything you need to know.

## What is {primary_keyword.title()}?

Learn the fundamentals and key concepts that make {primary_keyword} essential for your success.

## Benefits of {primary_keyword.title()}

- Improved performance and results
- Better user experience
- Increased efficiency
- Cost-effective solutions

## How to Get Started

Follow these simple steps to begin your journey with {primary_keyword}:

1. Understand your goals and requirements
2. Research and plan your approach
3. Implement best practices
4. Monitor and optimize continuously

## Frequently Asked Questions

### Why is {primary_keyword} important?

{primary_keyword.title()} is crucial for achieving better results and staying competitive in today's market.

### How long does it take to see results?

Results can vary, but most users see improvements within the first few weeks of implementation.

## Conclusion

Start your {primary_keyword} journey today and experience the benefits firsthand. Get in touch with us to learn more!
"""
        return content
    
    def optimize_existing_content(self, existing_content, suggestions):
        """
        Optimize existing content based on suggestions
        """
        print(f"✍️ Writer Agent: Optimizing existing content")
        
        optimizations = []
        
        # Title optimization
        if suggestions.get('title'):
            title_issues = suggestions['title'].get('issues', [])
            if title_issues:
                optimizations.append({
                    'type': 'title',
                    'current': suggestions['title'].get('current'),
                    'suggested': suggestions['title']['suggestions'][0]['content'],
                    'reason': suggestions['title']['suggestions'][0]['reason']
                })
        
        # Meta description optimization
        if suggestions.get('meta_description'):
            meta_current = suggestions['meta_description'].get('current', '')
            if len(meta_current) < 120 or len(meta_current) > 160:
                optimizations.append({
                    'type': 'meta_description',
                    'current': meta_current,
                    'suggested': suggestions['meta_description']['suggestions'][0]['content'],
                    'reason': suggestions['meta_description']['suggestions'][0]['reason']
                })
        
        # Content suggestions
        content_suggestions = suggestions.get('content_suggestions', [])
        for suggestion in content_suggestions:
            optimizations.append({
                'type': suggestion['type'],
                'priority': suggestion['priority'],
                'suggestion': suggestion['suggestion']
            })
        
        print(f"✅ Writer Agent: Generated {len(optimizations)} optimizations")
        
        return {
            'optimizations': optimizations,
            'total_improvements': len(optimizations)
        }
