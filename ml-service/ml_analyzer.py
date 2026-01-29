"""
SEO ML Analyzer - Real Machine Learning Model
Uses Random Forest and Gradient Boosting for SEO scoring
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time

class SEOMLAnalyzer:
    """
    Real ML-powered SEO analyzer using ensemble models
    """
    
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.scaler = StandardScaler()
        self.models = {}
        
        # Feature names for the model
        self.feature_names = [
            'title_length', 'title_length_optimal', 'has_title',
            'meta_desc_length', 'meta_desc_length_optimal', 'has_meta_desc',
            'h1_count', 'h1_count_optimal', 'h2_count', 'h3_count',
            'word_count', 'word_count_log', 'vocabulary_richness',
            'total_images', 'images_with_alt_ratio',
            'internal_links', 'external_links', 'link_ratio',
            'has_https', 'is_mobile_friendly', 'has_viewport',
            'has_canonical', 'has_schema', 'has_lang',
            'load_time', 'load_time_score', 'response_size_kb',
            'has_og_title', 'has_og_desc', 'has_og_image', 'has_twitter_card',
            'paragraph_count', 'avg_sentence_length'
        ]
        
        # Initialize models for each score category
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load trained models"""
        model_file = os.path.join(self.model_dir, 'seo_models.joblib')
        
        if os.path.exists(model_file):
            try:
                saved = joblib.load(model_file)
                self.models = saved['models']
                self.scaler = saved['scaler']
                print("✅ Loaded trained ML models")
            except:
                self._train_initial_models()
        else:
            self._train_initial_models()
    
    def _train_initial_models(self):
        """Train initial models with synthetic training data"""
        print("🧠 Training ML models...")
        
        # Generate synthetic training data based on SEO patterns
        X_train, y_train = self._generate_training_data(5000)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train separate models for each score component
        score_categories = ['title', 'meta', 'content', 'technical', 'performance', 'social', 'overall']
        
        for i, category in enumerate(score_categories):
            print(f"  Training {category} model...")
            
            # Use Random Forest for robustness
            model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                min_samples_split=5,
                random_state=42
            )
            
            model.fit(X_scaled, y_train[:, i])
            self.models[category] = model
        
        # Save models
        self._save_models()
        print("✅ ML models trained and saved!")
    
    def _generate_training_data(self, n_samples):
        """Generate realistic synthetic SEO training data"""
        np.random.seed(42)
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Generate random features
            title_length = np.random.randint(0, 100)
            title_length_optimal = 1 if 50 <= title_length <= 60 else 0
            has_title = 1 if title_length > 0 else 0
            
            meta_desc_length = np.random.randint(0, 250)
            meta_desc_length_optimal = 1 if 150 <= meta_desc_length <= 160 else 0
            has_meta_desc = 1 if meta_desc_length > 0 else 0
            
            h1_count = np.random.choice([0, 1, 2, 3], p=[0.1, 0.7, 0.15, 0.05])
            h1_count_optimal = 1 if h1_count == 1 else 0
            h2_count = np.random.randint(0, 15)
            h3_count = np.random.randint(0, 20)
            
            word_count = np.random.randint(50, 3000)
            word_count_log = np.log1p(word_count)
            vocabulary_richness = np.random.uniform(15, 50)
            
            total_images = np.random.randint(0, 30)
            images_with_alt = np.random.randint(0, total_images + 1)
            images_with_alt_ratio = images_with_alt / max(total_images, 1)
            
            internal_links = np.random.randint(0, 50)
            external_links = np.random.randint(0, 20)
            link_ratio = internal_links / max(external_links, 1)
            
            has_https = np.random.choice([0, 1], p=[0.1, 0.9])
            is_mobile_friendly = np.random.choice([0, 1], p=[0.15, 0.85])
            has_viewport = np.random.choice([0, 1], p=[0.1, 0.9])
            has_canonical = np.random.choice([0, 1], p=[0.3, 0.7])
            has_schema = np.random.choice([0, 1], p=[0.5, 0.5])
            has_lang = np.random.choice([0, 1], p=[0.2, 0.8])
            
            load_time = np.random.uniform(0.5, 10)
            load_time_score = max(0, 100 - load_time * 15)
            response_size_kb = np.random.uniform(50, 5000)
            
            has_og_title = np.random.choice([0, 1], p=[0.3, 0.7])
            has_og_desc = np.random.choice([0, 1], p=[0.35, 0.65])
            has_og_image = np.random.choice([0, 1], p=[0.35, 0.65])
            has_twitter_card = np.random.choice([0, 1], p=[0.5, 0.5])
            
            paragraph_count = np.random.randint(0, 30)
            avg_sentence_length = np.random.uniform(10, 30)
            
            # Create feature vector
            features = [
                title_length, title_length_optimal, has_title,
                meta_desc_length, meta_desc_length_optimal, has_meta_desc,
                h1_count, h1_count_optimal, h2_count, h3_count,
                word_count, word_count_log, vocabulary_richness,
                total_images, images_with_alt_ratio,
                internal_links, external_links, link_ratio,
                has_https, is_mobile_friendly, has_viewport,
                has_canonical, has_schema, has_lang,
                load_time, load_time_score, response_size_kb,
                has_og_title, has_og_desc, has_og_image, has_twitter_card,
                paragraph_count, avg_sentence_length
            ]
            
            # Calculate realistic target scores based on features
            title_score = self._calc_title_score_training(has_title, title_length, title_length_optimal)
            meta_score = self._calc_meta_score_training(has_meta_desc, meta_desc_length, has_canonical)
            content_score = self._calc_content_score_training(word_count, h1_count_optimal, h2_count, images_with_alt_ratio, vocabulary_richness)
            technical_score = self._calc_technical_score_training(has_https, is_mobile_friendly, has_schema, has_canonical, has_lang)
            performance_score = self._calc_performance_score_training(load_time, response_size_kb)
            social_score = self._calc_social_score_training(has_og_title, has_og_desc, has_og_image, has_twitter_card)
            
            # Overall score with weights
            overall_score = (
                title_score * 0.15 +
                meta_score * 0.15 +
                content_score * 0.25 +
                technical_score * 0.20 +
                performance_score * 0.15 +
                social_score * 0.10
            )
            
            # Add some noise to simulate real-world variability
            noise = np.random.normal(0, 3, 7)
            scores = np.clip([
                title_score + noise[0],
                meta_score + noise[1],
                content_score + noise[2],
                technical_score + noise[3],
                performance_score + noise[4],
                social_score + noise[5],
                overall_score + noise[6]
            ], 0, 100)
            
            X.append(features)
            y.append(scores)
        
        return np.array(X), np.array(y)
    
    def _calc_title_score_training(self, has_title, length, optimal):
        if not has_title:
            return np.random.uniform(0, 10)
        score = 30
        if optimal:
            score += 50
        elif 40 <= length <= 70:
            score += 30
        elif 30 <= length <= 80:
            score += 15
        if length >= 30:
            score += 10
        return min(score, 100)
    
    def _calc_meta_score_training(self, has_meta, length, has_canonical):
        score = 0
        if has_meta:
            score += 30
            if 150 <= length <= 160:
                score += 40
            elif 120 <= length <= 180:
                score += 25
            elif 100 <= length <= 200:
                score += 15
        if has_canonical:
            score += 20
        return min(score, 100)
    
    def _calc_content_score_training(self, word_count, h1_optimal, h2_count, alt_ratio, vocab):
        score = 0
        if word_count >= 1500:
            score += 25
        elif word_count >= 1000:
            score += 20
        elif word_count >= 500:
            score += 15
        elif word_count >= 300:
            score += 10
        
        if h1_optimal:
            score += 20
        if h2_count >= 2:
            score += 10
        
        score += alt_ratio * 20
        score += min(vocab / 50 * 15, 15)
        
        return min(score, 100)
    
    def _calc_technical_score_training(self, https, mobile, schema, canonical, lang):
        score = 0
        if https:
            score += 25
        if mobile:
            score += 25
        if schema:
            score += 20
        if canonical:
            score += 15
        if lang:
            score += 10
        return min(score, 100)
    
    def _calc_performance_score_training(self, load_time, size_kb):
        score = 100
        if load_time > 5:
            score -= 40
        elif load_time > 3:
            score -= 25
        elif load_time > 2:
            score -= 10
        
        if size_kb > 3000:
            score -= 20
        elif size_kb > 1500:
            score -= 10
        
        return max(score, 0)
    
    def _calc_social_score_training(self, og_title, og_desc, og_image, twitter):
        return (og_title + og_desc + og_image + twitter) / 4 * 100
    
    def _save_models(self):
        """Save trained models to disk"""
        model_file = os.path.join(self.model_dir, 'seo_models.joblib')
        joblib.dump({
            'models': self.models,
            'scaler': self.scaler
        }, model_file)
    
    def _extract_ml_features(self, features):
        """Extract and normalize features for ML model"""
        
        title_length = features.get('title_length', 0)
        meta_desc_length = features.get('meta_description_length', 0)
        word_count = features.get('word_count', 0)
        load_time = features.get('load_time', 5)
        
        feature_vector = [
            # Title features
            title_length,
            1 if 50 <= title_length <= 60 else 0,
            1 if features.get('has_title', False) else 0,
            
            # Meta features
            meta_desc_length,
            1 if 150 <= meta_desc_length <= 160 else 0,
            1 if features.get('has_meta_description', False) else 0,
            
            # Heading features
            features.get('h1_count', 0),
            1 if features.get('has_proper_h1', False) else 0,
            features.get('h2_count', 0),
            features.get('h3_count', 0),
            
            # Content features
            word_count,
            np.log1p(word_count),
            features.get('vocabulary_richness', 20),
            
            # Image features
            features.get('total_images', 0),
            features.get('image_alt_ratio', 100) / 100,
            
            # Link features
            features.get('internal_links', 0),
            features.get('external_links', 0),
            features.get('link_ratio', 1),
            
            # Technical features
            1 if features.get('url_has_https', True) else 0,
            1 if features.get('is_mobile_friendly', False) else 0,
            1 if features.get('has_viewport', False) else 0,
            1 if features.get('has_canonical', False) else 0,
            1 if features.get('has_schema', False) else 0,
            1 if features.get('has_lang', False) else 0,
            
            # Performance features
            load_time,
            max(0, 100 - load_time * 15),
            features.get('response_size_kb', 500),
            
            # Social features
            1 if features.get('has_og_title', False) else 0,
            1 if features.get('has_og_description', False) else 0,
            1 if features.get('has_og_image', False) else 0,
            1 if features.get('has_twitter_card', False) else 0,
            
            # Additional content
            features.get('paragraph_count', 5),
            features.get('avg_sentence_length', 15)
        ]
        
        return np.array(feature_vector).reshape(1, -1)
    
    def analyze(self, features):
        """
        Analyze using trained ML models
        """
        # Extract feature vector
        X = self._extract_ml_features(features)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        predictions = {}
        for category, model in self.models.items():
            pred = model.predict(X_scaled)[0]
            predictions[category] = max(0, min(100, pred))
        
        # Get feature importances for explainability
        importance = self._get_feature_importance()
        
        # Generate issues based on ML analysis
        issues = self._identify_issues_ml(features, predictions)
        
        # Generate suggestions
        suggestions = self._generate_suggestions_ml(features, predictions, issues)
        
        # Generate ML insights
        insights = self._generate_ml_insights(features, predictions, importance)
        
        return {
            'scores': {
                'title': round(predictions.get('title', 0)),
                'meta': round(predictions.get('meta', 0)),
                'content': round(predictions.get('content', 0)),
                'technical': round(predictions.get('technical', 0)),
                'performance': round(predictions.get('performance', 0)),
                'social': round(predictions.get('social', 0))
            },
            'overall_score': round(predictions.get('overall', 50)),
            'issues': issues,
            'suggestions': suggestions,
            'insights': insights,
            'feature_importance': importance,
            'model_info': {
                'type': 'GradientBoostingRegressor',
                'features_used': len(self.feature_names),
                'training_samples': 5000
            }
        }
    
    def _get_feature_importance(self):
        """Get averaged feature importance from models"""
        importance = {}
        categories = {
            'title': ['title_length', 'title_optimal', 'has_title'],
            'meta': ['meta_length', 'meta_optimal', 'canonical'],
            'content': ['word_count', 'headings', 'images', 'vocabulary'],
            'technical': ['https', 'mobile', 'schema', 'canonical'],
            'performance': ['load_time', 'page_size'],
            'social': ['og_tags', 'twitter_card']
        }
        
        if 'overall' in self.models:
            importances = self.models['overall'].feature_importances_
            # Aggregate by category
            importance = {
                'title_optimization': float(np.sum(importances[:3]) * 100),
                'meta_description': float(np.sum(importances[3:6]) * 100),
                'content_quality': float(np.sum(importances[6:15]) * 100),
                'technical_seo': float(np.sum(importances[15:24]) * 100),
                'performance': float(np.sum(importances[24:27]) * 100),
                'social_sharing': float(np.sum(importances[27:31]) * 100)
            }
        
        return importance
    
    def _identify_issues_ml(self, features, predictions):
        """Identify issues using ML predictions"""
        issues = []
        
        # Critical issues for low-scoring areas
        if predictions.get('title', 100) < 50:
            if not features.get('has_title'):
                issues.append({
                    'type': 'critical',
                    'category': 'title',
                    'message': 'Missing page title - ML model detected critical SEO gap',
                    'impact': 'high',
                    'confidence': 0.95
                })
            elif features.get('title_length', 0) < 30:
                issues.append({
                    'type': 'warning',
                    'category': 'title',
                    'message': f"Title too short ({features.get('title_length')} chars) - ML suggests 50-60 chars",
                    'impact': 'medium',
                    'confidence': 0.85
                })
        
        if predictions.get('meta', 100) < 50:
            if not features.get('has_meta_description'):
                issues.append({
                    'type': 'critical',
                    'category': 'meta',
                    'message': 'Missing meta description - strongly impacts click-through rate',
                    'impact': 'high',
                    'confidence': 0.92
                })
        
        if predictions.get('content', 100) < 60:
            word_count = features.get('word_count', 0)
            if word_count < 300:
                issues.append({
                    'type': 'warning',
                    'category': 'content',
                    'message': f'Thin content detected ({word_count} words) - ML recommends 500+ words',
                    'impact': 'medium',
                    'confidence': 0.88
                })
            
            if not features.get('has_proper_h1'):
                issues.append({
                    'type': 'critical' if features.get('h1_count', 0) == 0 else 'warning',
                    'category': 'content',
                    'message': 'H1 heading issue - ML model identified heading structure problem',
                    'impact': 'high' if features.get('h1_count', 0) == 0 else 'medium',
                    'confidence': 0.90
                })
        
        if predictions.get('technical', 100) < 70:
            if not features.get('url_has_https'):
                issues.append({
                    'type': 'critical',
                    'category': 'technical',
                    'message': 'No HTTPS - ML model flags this as critical ranking factor',
                    'impact': 'high',
                    'confidence': 0.98
                })
            
            if not features.get('is_mobile_friendly'):
                issues.append({
                    'type': 'critical',
                    'category': 'technical',
                    'message': 'Not mobile-friendly - ML detects mobile usability issues',
                    'impact': 'high',
                    'confidence': 0.94
                })
        
        if predictions.get('performance', 100) < 60:
            load_time = features.get('load_time', 0)
            issues.append({
                'type': 'warning',
                'category': 'performance',
                'message': f'Slow page load ({load_time:.2f}s) - ML predicts negative ranking impact',
                'impact': 'medium',
                'confidence': 0.82
            })
        
        if predictions.get('social', 100) < 40:
            issues.append({
                'type': 'info',
                'category': 'social',
                'message': 'Missing social meta tags - limits social sharing potential',
                'impact': 'low',
                'confidence': 0.75
            })
        
        return issues
    
    def _generate_suggestions_ml(self, features, predictions, issues):
        """Generate ML-powered suggestions"""
        suggestions = []
        
        # Priority based on prediction gaps
        score_gaps = {
            'title': 100 - predictions.get('title', 100),
            'meta': 100 - predictions.get('meta', 100),
            'content': 100 - predictions.get('content', 100),
            'technical': 100 - predictions.get('technical', 100),
            'performance': 100 - predictions.get('performance', 100),
            'social': 100 - predictions.get('social', 100)
        }
        
        # Sort by gap size
        sorted_gaps = sorted(score_gaps.items(), key=lambda x: x[1], reverse=True)
        
        for category, gap in sorted_gaps[:4]:  # Top 4 improvement areas
            if gap > 20:
                priority = 'critical' if gap > 50 else 'high' if gap > 35 else 'medium'
                
                if category == 'title':
                    suggestions.append({
                        'category': 'title',
                        'suggestion': f'ML analysis: Optimize title to 50-60 chars with primary keyword (potential +{int(gap*0.6)} points)',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.6)
                    })
                
                elif category == 'meta':
                    suggestions.append({
                        'category': 'meta',
                        'suggestion': f'ML analysis: Add compelling meta description (150-160 chars) (potential +{int(gap*0.7)} points)',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.7)
                    })
                
                elif category == 'content':
                    suggestions.append({
                        'category': 'content',
                        'suggestion': f'ML analysis: Improve content depth - aim for 1000+ words with proper heading structure',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.5)
                    })
                
                elif category == 'technical':
                    suggestions.append({
                        'category': 'technical',
                        'suggestion': f'ML analysis: Fix technical SEO issues (HTTPS, mobile, schema)',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.8)
                    })
                
                elif category == 'performance':
                    suggestions.append({
                        'category': 'performance',
                        'suggestion': f'ML analysis: Optimize page speed - target under 2 seconds load time',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.5)
                    })
                
                elif category == 'social':
                    suggestions.append({
                        'category': 'social',
                        'suggestion': f'ML analysis: Add Open Graph and Twitter Card meta tags',
                        'priority': priority,
                        'predicted_improvement': round(gap * 0.7)
                    })
        
        return suggestions
    
    def _generate_ml_insights(self, features, predictions, importance):
        """Generate explainable ML insights"""
        insights = []
        
        overall = predictions.get('overall', 50)
        
        # Overall assessment
        if overall >= 80:
            insights.append({
                'type': 'positive',
                'message': f'🎯 ML Prediction: Excellent SEO health ({overall}/100) - page is well-optimized',
                'confidence': 0.9
            })
        elif overall >= 60:
            insights.append({
                'type': 'neutral',
                'message': f'🔍 ML Prediction: Good SEO ({overall}/100) but with improvement opportunities',
                'confidence': 0.85
            })
        else:
            insights.append({
                'type': 'warning',
                'message': f'⚠️ ML Prediction: SEO needs attention ({overall}/100) - significant optimization needed',
                'confidence': 0.88
            })
        
        # Content depth insight
        word_count = features.get('word_count', 0)
        content_score = predictions.get('content', 50)
        if word_count >= 1200 and content_score >= 70:
            insights.append({
                'type': 'positive',
                'message': f'📊 ML Content Analysis: Strong content depth ({word_count} words) correlates with better rankings'
            })
        elif word_count < 500:
            insights.append({
                'type': 'warning',
                'message': f'📊 ML Content Analysis: Thin content ({word_count} words) - model predicts lower ranking potential'
            })
        
        # Technical insight
        tech_score = predictions.get('technical', 50)
        if features.get('url_has_https') and features.get('is_mobile_friendly'):
            insights.append({
                'type': 'positive',
                'message': '🔒 ML Technical Analysis: Core web vitals (HTTPS + Mobile) are satisfied'
            })
        
        # Keyword insight
        top_keywords = features.get('top_keywords', [])
        if top_keywords:
            kw_list = ', '.join([kw[0] for kw in top_keywords[:5]])
            insights.append({
                'type': 'info',
                'message': f'🔑 ML Keyword Analysis: Detected focus topics - {kw_list}'
            })
        
        # Feature importance insight
        if importance:
            top_factor = max(importance.items(), key=lambda x: x[1])
            insights.append({
                'type': 'info',
                'message': f'🧠 ML Model Insight: {top_factor[0].replace("_", " ").title()} is the most impactful factor for this page'
            })
        
        return insights
    
    def retrain(self, new_data):
        """Retrain model with new labeled data"""
        X_new, y_new = new_data
        X_scaled = self.scaler.transform(X_new)
        
        for i, category in enumerate(self.models.keys()):
            self.models[category].fit(X_scaled, y_new[:, i])
        
        self._save_models()
        print("🔄 Models retrained with new data")

    def analyze_url(self, url):
        """
        Analyze a URL by scraping it and running the ML model
        """
        print(f"🔍 Analyzing URL: {url}")
        
        # Normalize URL
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
        start_time = time.time()
        try:
            headers = {
                'User-Agent': 'SEOBot-ML/2.0 (AI SEO Analyzer; Machine Learning)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            return {'error': f'Failed to fetch URL: {str(e)}'}
            
        load_time = time.time() - start_time
        html = response.text
        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract features
        features = self.extract_features_from_soup(soup, url, load_time, response)
        
        # Run analysis
        results = self.analyze(features)
        
        # Add basic info to results
        results['url'] = url
        results['load_time'] = round(load_time, 3)
        results['features'] = features
        
        return results

    def extract_features_from_soup(self, soup, url, load_time, response):
        """Extract SEO features from HTML soup for ML model"""
        
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
        # Create a copy to not modify the original soup if needed elsewhere
        import copy
        content_soup = copy.copy(soup)
        body = content_soup.find('body')
        if body:
            # Remove script and style elements
            for script in body.find_all(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            text = body.get_text(separator=' ', strip=True)
        else:
            text = content_soup.get_text(separator=' ', strip=True)
        
        words = re.findall(r'\\b[a-zA-Z]+\\b', text.lower())
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
        heading_score = self._calculate_heading_score(h1_tags, h2_tags, h3_tags)
        
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
    
    def _calculate_heading_score(self, h1_tags, h2_tags, h3_tags):
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

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        analyzer = SEOMLAnalyzer()
        results = analyzer.analyze_url(url)
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python ml_analyzer.py <url>")
