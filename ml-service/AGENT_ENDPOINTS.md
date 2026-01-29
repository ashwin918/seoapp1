# Agent Architecture - Endpoint Mapping

This document shows how each API endpoint uses the agent architecture.

## 🔄 Agent Flow by Endpoint

### 1. **POST /analyze** - SEO Analysis
**Purpose**: Analyze a website's SEO using ML models

**Agent Pipeline**:
```
Request → Scraper Agent → Analyzer Agent → Response
```

**Agents Used**:
- 🕷️ **Scraper Agent**: Fetches and extracts SEO features from URL
- 🤖 **Analyzer Agent**: Runs ML analysis on extracted features

**Example Request**:
```json
POST /analyze
{
  "url": "https://example.com"
}
```

**Response Includes**:
- SEO scores (title, meta, content, technical, performance, social)
- Overall score and grade
- Issues and suggestions
- ML insights
- Extracted features

---

### 2. **POST /generate** - Content Generation
**Purpose**: Generate SEO-optimized content suggestions

**Agent Pipeline**:
```
Request → Scraper Agent → Analyzer Agent → Content Suggestion Agent → Writer Agent → Response
```

**Agents Used**:
- 🕷️ **Scraper Agent**: Fetches website content (if URL provided)
- 🤖 **Analyzer Agent**: Analyzes SEO quality
- 💡 **Content Suggestion Agent**: Generates title/meta/keyword suggestions
- ✍️ **Writer Agent**: Formats content for all platforms

**Example Request**:
```json
POST /generate
{
  "url": "https://example.com",
  "platform": "wordpress"
}
```

**Response Includes**:
- Content suggestions (title variations, meta descriptions, keywords)
- Formatted content for specified platform
- Platform formats for all platforms (WordPress, Shopify, GitHub, HTML, Markdown)

---

### 3. **POST /push** - Push Content to Platform
**Purpose**: Push SEO content to connected platform

**Agent Pipeline**:
```
Request → Writer Agent → Platform API → Response
```

**Agents Used**:
- ✍️ **Writer Agent**: Formats content for target platform

**Example Request**:
```json
POST /push
{
  "platform": "wordpress",
  "account": {
    "access_token": "xxx",
    "site_url": "https://mysite.com"
  },
  "content": {
    "title": "New SEO Title",
    "meta_description": "Optimized description"
  },
  "target": {
    "post_id": "123"
  }
}
```

**Response Includes**:
- Success status
- Platform-specific push data
- Agent used confirmation

---

### 4. **POST /analyze-agents** - Full Agent Pipeline
**Purpose**: Complete SEO analysis with all agents (advanced endpoint)

**Agent Pipeline**:
```
Request → Scraper Agent → Analyzer Agent → Content Suggestion Agent → Writer Agent → Response
```

**Agents Used**: ALL 4 agents

**Example Request**:
```json
POST /analyze-agents
{
  "url": "https://example.com",
  "platform": "wordpress"
}
```

**Response Includes**:
- Everything from /analyze
- Everything from /generate
- Agent pipeline information
- Feature importance from ML model

---

## 📊 Agent Responsibility Matrix

| Endpoint | Scraper 🕷️ | Analyzer 🤖 | Content Suggestion 💡 | Writer ✍️ |
|----------|------------|-------------|---------------------|-----------|
| `/analyze` | ✅ | ✅ | ❌ | ❌ |
| `/generate` | ✅ | ✅ | ✅ | ✅ |
| `/push` | ❌ | ❌ | ❌ | ✅ |
| `/analyze-agents` | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 Use Cases

### Use Case 1: Quick SEO Analysis
**Endpoint**: `POST /analyze`
**When**: You just want to check SEO scores and issues
**Agents**: Scraper + Analyzer

### Use Case 2: Content Editing/Suggestions
**Endpoint**: `POST /generate`
**When**: You want AI-generated content suggestions for your site
**Agents**: Scraper + Analyzer + Content Suggestion + Writer

### Use Case 3: Direct Publishing
**Endpoint**: `POST /push`
**When**: You want to push content directly to WordPress/Shopify/GitHub
**Agents**: Writer

### Use Case 4: Complete Analysis + Content
**Endpoint**: `POST /analyze-agents`
**When**: You want everything (analysis + suggestions + formatted content)
**Agents**: All 4 agents

---

## 🔧 Integration with Node.js Backend

### From `routes/analyze.js`:
```javascript
// Calls /analyze endpoint
const mlResponse = await axios.post(`${ML_SERVICE_URL}/analyze`, {
    url: normalizedUrl
});
// Uses: Scraper Agent + Analyzer Agent
```

### From `routes/seo.js`:
```javascript
// Calls /generate endpoint for content suggestions
const mlResponse = await axios.post(`${ML_SERVICE_URL}/generate`, {
    url: website.url
});
// Uses: All 4 agents

// Calls /push endpoint when user clicks "Use" button
await axios.post(`${ML_SERVICE_URL}/push`, {
    platform: platform,
    account: accountData,
    content: content,
    target: { page_url: website.url }
});
// Uses: Writer Agent
```

---

## 🚀 Agent Benefits

1. **Modularity**: Each agent has a single, clear responsibility
2. **Reusability**: Agents can be used in different combinations
3. **Testability**: Each agent can be tested independently
4. **Maintainability**: Easy to update or replace individual agents
5. **Scalability**: Easy to add new agents (e.g., Competitor Agent, SEO Audit Agent)

---

## 📝 Summary

The agent architecture provides a clean, modular approach to SEO analysis:

- **Scraper Agent** handles all web scraping using BeautifulSoup
- **Analyzer Agent** runs ML models for SEO scoring
- **Content Suggestion Agent** generates SEO content recommendations
- **Writer Agent** formats content for different platforms

Each endpoint uses the appropriate combination of agents to fulfill its purpose, making the system flexible and maintainable.
