"""
Scraper Agent - Web Content Scraping and Extraction
Uses BeautifulSoup to scrape and parse web content
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import time
import copy


class ScraperAgent:
    """
    Agent responsible for scraping web content and extracting SEO features
    """
    
    def __init__(self):
        self.user_agent = 'SEOBot-ML/2.0 (AI SEO Analyzer; Machine Learning)'
        self.timeout = 15
        
    def scrape_url(self, url):
        """
        Scrape a URL and return HTML content with metadata
        """
        print(f"🕷️ Scraper Agent: Fetching {url}")
        
        # Normalize URL
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
        start_time = time.time()
        
        try:
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            load_time = time.time() - start_time
            
            print(f"✅ Scraper Agent: Fetched {len(response.content)/1024:.1f} KB in {load_time:.2f}s")
            
            return {
                'success': True,
                'url': url,
                'html': response.text,
                'response': response,
                'load_time': load_time,
                'status_code': response.status_code
            }
            
        except requests.RequestException as e:
            print(f"❌ Scraper Agent: Failed to fetch {url} - {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def extract_features(self, html, url, load_time, response):
        """
        Extract SEO features from HTML using BeautifulSoup
        """
        print(f"🔬 Scraper Agent: Extracting features from HTML")
        
        soup = BeautifulSoup(html, 'lxml')
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
        
        # Content extraction
        content_soup = copy.copy(soup)
        body = content_soup.find('body')
        if body:
            # Remove script and style elements
            for script in body.find_all(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            text = body.get_text(separator=' ', strip=True)
        else:
            text = content_soup.get_text(separator=' ', strip=True)
        
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
        
        print(f"✅ Scraper Agent: Extracted {len(features)} features")
        
        return features
