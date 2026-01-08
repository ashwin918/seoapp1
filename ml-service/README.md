# SEO Bot ML Service

AI-powered SEO analysis using Python and Machine Learning.

## Features

- **Deep HTML Analysis**: Extracts 50+ SEO features from web pages
- **ML-Based Scoring**: Uses weighted algorithms for accurate scoring
- **Issue Detection**: Identifies critical, warning, and informational issues
- **Smart Suggestions**: Provides actionable improvement recommendations
- **AI Insights**: Generates intelligent insights about content quality

## Setup

1. **Create virtual environment**:
   ```bash
   cd ml-service
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (optional)**:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Run the service**:
   ```bash
   python app.py
   ```

   The service will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns service status.

### Analyze URL
```
POST /analyze
Content-Type: application/json

{
    "url": "https://example.com"
}
```

**Response**:
```json
{
    "url": "https://example.com",
    "overall_score": 75,
    "grade": "B",
    "scores": {
        "title": 85,
        "meta": 70,
        "content": 80,
        "technical": 75,
        "performance": 90,
        "social": 50
    },
    "issues": [...],
    "suggestions": [...],
    "insights": [...],
    "features": {...}
}
```

## Scoring Algorithm

The ML analyzer calculates scores based on:

| Category | Weight | Factors |
|----------|--------|---------|
| Title | 15% | Length, keyword presence |
| Meta | 15% | Description length, canonical |
| Content | 25% | Word count, headings, images |
| Technical | 20% | HTTPS, mobile, schema |
| Performance | 15% | Load time, page size |
| Social | 10% | OG tags, Twitter card |

## Integration

The Node.js app automatically calls this service when analyzing URLs.
If the ML service is unavailable, it falls back to basic analysis.

Add to your `.env`:
```
ML_SERVICE_URL=http://localhost:5000
```

## Running in Production

Use Gunicorn for production:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Project Structure

```
ml-service/
├── app.py              # Flask application
├── ml_analyzer.py      # ML analysis logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
