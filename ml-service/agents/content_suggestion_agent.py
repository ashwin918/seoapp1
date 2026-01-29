"""
Content Suggestion Agent - AI-Powered SEO Content Suggestions
Generates optimized content suggestions based on analysis
"""

import re
import random


class ContentSuggestionAgent:
    """
    Agent responsible for generating SEO content suggestions
    """
    
    def __init__(self):
        # Title templates by industry/type
        self.title_templates = [
            "{keyword} - {benefit} | {brand}",
            "{benefit} with {keyword} | {brand}",
            "{keyword}: {action} for {benefit}",
            "Best {keyword} - {benefit} in {year}",
            "{keyword} Guide: {benefit} Made Easy",
            "{action} {keyword} - {benefit} | {brand}",
            "Top {keyword} for {benefit} [{year}]",
            "{number} {keyword} Tips for {benefit}",
        ]
        
        # Meta description templates
        self.meta_templates = [
            "Discover {keyword} that delivers {benefit}. {action} today and {result}. {cta}",
            "Looking for {keyword}? Get {benefit} with our {solution}. {cta}",
            "{action} {keyword} for {benefit}. Trusted by {social_proof}. {cta}",
            "The ultimate guide to {keyword}. Learn how to {benefit} with {solution}. {cta}",
            "{brand} offers the best {keyword} for {benefit}. {action} now and {result}.",
            "Get {benefit} with our {keyword}. {number}+ satisfied customers. {cta}",
        ]
        
        self.ctas = [
            "Get started free →",
            "Learn more today!",
            "Try it now →",
            "Start your journey!",
            "See how it works →",
            "Get your free quote!",
            "Join thousands of users!",
            "Schedule a demo →",
        ]
        
        self.benefits = [
            "better results", "improved performance", "higher rankings",
            "increased traffic", "more conversions", "saved time",
            "reduced costs", "expert solutions", "proven results",
        ]
    
    def generate_suggestions(self, features, analysis_results):
        """
        Generate optimized SEO content suggestions based on analysis
        """
        print(f"💡 Content Suggestion Agent: Generating suggestions")
        
        # Extract current content
        current_title = features.get('title', '')
        current_meta = features.get('meta_description', '')
        top_keywords = features.get('top_keywords', [])
        domain = features.get('domain', '')
        
        # Get primary keyword
        primary_keyword = self._extract_primary_keyword(top_keywords, current_title)
        
        # Extract brand from domain
        brand = self._extract_brand(domain)
        
        # Generate content
        generated = {
            'title': self._generate_title(current_title, primary_keyword, brand, features),
            'meta_description': self._generate_meta_description(current_meta, primary_keyword, brand, features),
            'h1_suggestion': self._generate_h1(features, primary_keyword),
            'content_suggestions': self._generate_content_suggestions(features, analysis_results),
            'keyword_recommendations': self._generate_keyword_recommendations(top_keywords),
            'schema_suggestion': self._generate_schema_suggestion(features, brand),
        }
        
        print(f"✅ Content Suggestion Agent: Generated {len(generated)} suggestion types")
        
        return generated
    
    def _extract_primary_keyword(self, top_keywords, title):
        """Extract the primary keyword from analysis"""
        if top_keywords:
            return top_keywords[0][0]
        
        # Fall back to extracting from title
        words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
        stop_words = {'with', 'your', 'this', 'that', 'from', 'have', 'been', 'were', 'will', 'would'}
        words = [w for w in words if w not in stop_words]
        
        if words:
            return words[0]
        return "your product"
    
    def _extract_brand(self, domain):
        """Extract brand name from domain"""
        # Remove common TLDs and www
        brand = domain.replace('www.', '')
        brand = re.sub(r'\.(com|org|net|io|co|app|dev|ai).*', '', brand)
        brand = brand.replace('-', ' ').replace('_', ' ')
        return brand.title()
    
    def _generate_title(self, current_title, keyword, brand, features):
        """Generate optimized title suggestions"""
        current_length = len(current_title)
        
        # Analyze current title issues
        issues = []
        if current_length < 30:
            issues.append('too_short')
        elif current_length > 60:
            issues.append('too_long')
        
        if keyword.lower() not in current_title.lower():
            issues.append('missing_keyword')
        
        # Generate suggestions
        suggestions = []
        
        # Variation 1: Keyword-focused
        title1 = f"{keyword.title()} - Expert Solutions & Results | {brand}"
        if len(title1) > 60:
            title1 = f"{keyword.title()} - Best Solutions | {brand}"
        suggestions.append({
            'content': title1[:60],
            'length': len(title1[:60]),
            'reason': 'Keyword-first approach for better SEO visibility',
            'improvement': '+15-20% click potential'
        })
        
        # Variation 2: Benefit-focused
        benefit = random.choice(self.benefits)
        title2 = f"{benefit.title()} with {keyword.title()} | {brand}"
        suggestions.append({
            'content': title2[:60],
            'length': len(title2[:60]),
            'reason': 'Benefit-first approach appeals to user intent',
            'improvement': '+10-15% engagement'
        })
        
        # Variation 3: Action-oriented
        title3 = f"Get {keyword.title()} That Works - {brand}"
        suggestions.append({
            'content': title3[:60],
            'length': len(title3[:60]),
            'reason': 'Action-oriented title drives clicks',
            'improvement': '+12% CTR potential'
        })
        
        return {
            'current': current_title,
            'current_length': current_length,
            'optimal_length': '50-60 characters',
            'issues': issues,
            'suggestions': suggestions
        }
    
    def _generate_meta_description(self, current_meta, keyword, brand, features):
        """Generate optimized meta description suggestions"""
        current_length = len(current_meta)
        
        suggestions = []
        
        # Generate compelling meta descriptions
        cta = random.choice(self.ctas)
        
        # Variation 1: Benefit + CTA
        meta1 = f"Discover the best {keyword} solutions that deliver real results. Trusted by thousands of customers. {cta}"
        suggestions.append({
            'content': meta1[:160],
            'length': len(meta1[:160]),
            'reason': 'Combines social proof with clear call-to-action',
            'improvement': '+20% CTR'
        })
        
        # Variation 2: Problem-solution
        meta2 = f"Looking for {keyword}? {brand} offers proven solutions for better results. Get started today and see the difference. {cta}"
        suggestions.append({
            'content': meta2[:160],
            'length': len(meta2[:160]),
            'reason': 'Addresses user intent directly',
            'improvement': '+18% engagement'
        })
        
        # Variation 3: Feature-focused
        meta3 = f"{brand}'s {keyword} helps you achieve your goals faster. Easy to use, powerful results. Join thousands of happy users. {cta}"
        suggestions.append({
            'content': meta3[:160],
            'length': len(meta3[:160]),
            'reason': 'Highlights benefits and social proof',
            'improvement': '+15% CTR'
        })
        
        return {
            'current': current_meta,
            'current_length': current_length,
            'optimal_length': '150-160 characters',
            'suggestions': suggestions
        }
    
    def _generate_h1(self, features, keyword):
        """Generate H1 suggestions"""
        current_h1s = features.get('h1_tags', [])
        
        suggestions = [
            f"The Complete Guide to {keyword.title()}",
            f"Discover {keyword.title()} That Delivers Results",
            f"{keyword.title()}: Everything You Need to Know",
            f"Best {keyword.title()} Solutions for Your Needs",
        ]
        
        return {
            'current': current_h1s[0] if current_h1s else None,
            'count': len(current_h1s),
            'issue': 'missing' if len(current_h1s) == 0 else 'multiple' if len(current_h1s) > 1 else None,
            'suggestions': suggestions[:3]
        }
    
    def _generate_content_suggestions(self, features, analysis):
        """Generate content improvement suggestions"""
        suggestions = []
        word_count = features.get('word_count', 0)
        
        if word_count < 500:
            suggestions.append({
                'type': 'content_length',
                'priority': 'high',
                'suggestion': 'Add more content to reach at least 500-1000 words',
                'sections_to_add': [
                    'Introduction with keyword context',
                    'Benefits and features section',
                    'How it works / Step-by-step guide',
                    'FAQ section with common questions',
                    'Conclusion with clear CTA'
                ]
            })
        
        if features.get('images_without_alt', 0) > 0:
            suggestions.append({
                'type': 'image_optimization',
                'priority': 'medium',
                'suggestion': f"Add alt text to {features.get('images_without_alt')} images",
                'example': f"alt=\"{features.get('top_keywords', [['product']])[0][0]} - descriptive image caption\""
            })
        
        return suggestions
    
    def _generate_keyword_recommendations(self, top_keywords):
        """Generate keyword optimization recommendations"""
        if not top_keywords:
            return {
                'primary': None,
                'secondary': [],
                'recommendation': 'Add more keyword-rich content'
            }
        
        # Get primary keyword
        primary = top_keywords[0][0] if top_keywords else None
        
        # Get secondary keywords
        secondary = [kw[0] for kw in top_keywords[1:5]] if len(top_keywords) > 1 else []
        
        # Long-tail suggestions
        long_tail = []
        if primary:
            long_tail = [
                f"best {primary}",
                f"how to {primary}",
                f"{primary} guide",
                f"{primary} tips",
                f"{primary} for beginners"
            ]
        
        return {
            'primary': primary,
            'primary_count': top_keywords[0][1] if top_keywords else 0,
            'secondary': secondary,
            'long_tail_suggestions': long_tail,
            'recommendation': f"Primary keyword '{primary}' appears {top_keywords[0][1] if top_keywords else 0} times. Consider natural distribution."
        }
    
    def _generate_schema_suggestion(self, features, brand):
        """Generate Schema.org structured data suggestion"""
        
        # Detect page type
        if features.get('form_count', 0) > 0:
            page_type = 'WebPage'
        elif features.get('video_count', 0) > 0:
            page_type = 'VideoObject'
        else:
            page_type = 'WebPage'
        
        schema = {
            "@context": "https://schema.org",
            "@type": page_type,
            "name": features.get('title', brand),
            "description": features.get('meta_description', ''),
            "url": features.get('url', ''),
            "publisher": {
                "@type": "Organization",
                "name": brand
            }
        }
        
        return {
            'type': page_type,
            'schema': schema,
            'implementation': f'<script type="application/ld+json">{{\\n  // Add this to your <head> section\\n  {schema}\\n}}</script>'
        }
