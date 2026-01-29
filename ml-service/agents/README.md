# SEO ML Service - Agent Architecture

This folder contains specialized agents for modular SEO analysis and content generation.

## Agent Overview

The SEO ML Service uses a **multi-agent architecture** where each agent has a specific responsibility:

```
┌─────────────────────────────────────────────────────────────┐
│                    SEO Analysis Pipeline                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │      1. Scraper Agent 🕷️             │
        │  - Fetches web content               │
        │  - Uses BeautifulSoup for parsing    │
        │  - Extracts SEO features             │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │      2. Analyzer Agent 🤖            │
        │  - ML-based SEO analysis             │
        │  - Uses trained models               │
        │  - Generates scores & insights       │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │  3. Content Suggestion Agent 💡      │
        │  - Generates SEO suggestions         │
        │  - Title & meta optimization         │
        │  - Keyword recommendations           │
        └──────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────┐
        │      4. Writer Agent ✍️              │
        │  - Formats content for platforms     │
        │  - WordPress, Shopify, GitHub        │
        │  - Optimizes existing content        │
        └──────────────────────────────────────┘
```

## Agents

### 1. **Scraper Agent** (`scraper_agent.py`)
**Responsibility**: Web scraping and feature extraction

**Key Methods**:
- `scrape_url(url)` - Fetches web content using BeautifulSoup
- `extract_features(html, url, load_time, response)` - Extracts SEO features

**Features Extracted**:
- Title, meta description, headings (H1, H2, H3)
- Images and alt text
- Internal/external links
- Content metrics (word count, vocabulary)
- Technical SEO (mobile-friendly, schema, HTTPS)
- Performance metrics (load time, page size)

---

### 2. **Analyzer Agent** (`analyzer_agent.py`)
**Responsibility**: ML-powered SEO analysis

**Key Methods**:
- `analyze(features)` - Runs ML models on extracted features
- `_identify_issues(features, predictions)` - Identifies SEO issues
- `_generate_suggestions(features, predictions, issues)` - Creates improvement suggestions

**ML Models**:
- GradientBoostingRegressor (trained on 5000+ samples)
- 33 features analyzed
- Scores: Title, Meta, Content, Technical, Performance, Social

---

### 3. **Content Suggestion Agent** (`content_suggestion_agent.py`)
**Responsibility**: SEO content recommendations

**Key Methods**:
- `generate_suggestions(features, analysis_results)` - Creates content suggestions
- `_generate_title(current_title, keyword, brand, features)` - Title optimization
- `_generate_meta_description(...)` - Meta description optimization
- `_generate_keyword_recommendations(...)` - Keyword strategy

**Suggestions Generated**:
- 3 title variations (keyword-focused, benefit-focused, action-oriented)
- 3 meta description variations
- H1 heading suggestions
- Keyword recommendations (primary, secondary, long-tail)
- Schema.org structured data

---

### 4. **Writer Agent** (`writer_agent.py`)
**Responsibility**: Content writing and platform formatting

**Key Methods**:
- `write_content(suggestions, platform)` - Formats content for platform
- `optimize_existing_content(existing_content, suggestions)` - Optimizes content

**Supported Platforms**:
- **WordPress**: Yoast SEO format
- **Shopify**: Metafields format
- **GitHub Pages**: YAML frontmatter + Markdown
- **HTML**: Complete HTML with meta tags
- **Markdown**: Pure markdown format

---

## Usage

### Using the Agent Pipeline

```python
from agents import ScraperAgent, AnalyzerAgent, ContentSuggestionAgent, WriterAgent

# Initialize agents
scraper = ScraperAgent()
analyzer = AnalyzerAgent()
content_suggester = ContentSuggestionAgent()
writer = WriterAgent()

# Step 1: Scrape
scrape_result = scraper.scrape_url('https://example.com')
features = scraper.extract_features(
    scrape_result['html'],
    scrape_result['url'],
    scrape_result['load_time'],
    scrape_result['response']
)

# Step 2: Analyze
analysis = analyzer.analyze(features)

# Step 3: Generate suggestions
suggestions = content_suggester.generate_suggestions(features, analysis)

# Step 4: Write content
formatted = writer.write_content(suggestions, platform='wordpress')
```

### Using the API Endpoint

```bash
# Agent-based analysis
curl -X POST http://localhost:5000/analyze-agents \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "platform": "wordpress"}'
```

## Benefits of Agent Architecture

1. **Modularity**: Each agent has a single responsibility
2. **Maintainability**: Easy to update individual agents
3. **Testability**: Agents can be tested independently
4. **Scalability**: Easy to add new agents or features
5. **Flexibility**: Mix and match agents as needed

## Agent Communication

Agents communicate through a **pipeline pattern**:

```
URL → Scraper → Features → Analyzer → Analysis → Content Suggester → Suggestions → Writer → Formatted Content
```

Each agent:
- Receives input from the previous agent
- Processes the data
- Outputs results for the next agent

## Future Enhancements

Potential new agents:
- **Competitor Agent**: Analyze competitor websites
- **Keyword Research Agent**: Find trending keywords
- **Link Building Agent**: Suggest backlink opportunities
- **Performance Optimizer Agent**: Optimize images and code
- **Social Media Agent**: Generate social media content

## Files

```
agents/
├── __init__.py                      # Package initialization
├── scraper_agent.py                 # Web scraping & feature extraction
├── analyzer_agent.py                # ML-based SEO analysis
├── content_suggestion_agent.py      # Content recommendations
├── writer_agent.py                  # Content writing & formatting
└── README.md                        # This file
```

## Dependencies

- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `scikit-learn` - Machine learning
- `numpy` - Numerical operations
- `lxml` - XML/HTML parser

## License

Part of the SEO ML Service project.
