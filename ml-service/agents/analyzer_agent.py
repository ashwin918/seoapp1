"""
Analyzer Agent - SEO Analysis using Machine Learning
Uses trained ML models to analyze SEO features and provide scores
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os


class AnalyzerAgent:
    """
    Agent responsible for analyzing SEO features using ML models
    """
    
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
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
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load trained models"""
        model_file = os.path.join(self.model_dir, 'seo_models.joblib')
        
        if os.path.exists(model_file):
            try:
                saved = joblib.load(model_file)
                self.models = saved['models']
                self.scaler = saved['scaler']
                print("✅ Analyzer Agent: Loaded trained ML models")
            except:
                self._train_initial_models()
        else:
            self._train_initial_models()
    
    def _train_initial_models(self):
        """Train initial models with synthetic training data"""
        print("🧠 Analyzer Agent: Training ML models...")
        
        # Import training logic from ml_analyzer
        from ml_analyzer import SEOMLAnalyzer
        temp_analyzer = SEOMLAnalyzer()
        
        # Copy trained models
        self.models = temp_analyzer.models
        self.scaler = temp_analyzer.scaler
        
        print("✅ Analyzer Agent: ML models ready!")
    
    def analyze(self, features):
        """
        Analyze SEO features using trained ML models
        """
        print(f"🤖 Analyzer Agent: Running ML analysis")
        
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
        issues = self._identify_issues(features, predictions)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(features, predictions, issues)
        
        # Generate ML insights
        insights = self._generate_insights(features, predictions, importance)
        
        print(f"✅ Analyzer Agent: Overall Score = {predictions.get('overall', 50)}/100")
        
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
    
    def _get_feature_importance(self):
        """Get averaged feature importance from models"""
        importance = {}
        
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
    
    def _identify_issues(self, features, predictions):
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
        
        return issues
    
    def _generate_suggestions(self, features, predictions, issues):
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
        
        return suggestions
    
    def _generate_insights(self, features, predictions, importance):
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
        
        return insights
