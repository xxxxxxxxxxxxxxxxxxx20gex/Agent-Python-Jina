---
name: web-scraper
description: Advanced web scraping with robots.txt compliance, rate limiting, and structured data extraction
---

# Web Scraper Skill

## When to Use This Skill

Use this skill when you need to:
- Extract data from websites
- Crawl multiple pages systematically
- Respect robots.txt and rate limits
- Parse HTML and extract structured data
- Download and organize web content
- Build knowledge bases from online sources

## How to Apply

### 1. Single Page Scraping

```python
from skills.web_scraper.scripts.scraper import WebScraper

scraper = WebScraper()
data = scraper.scrape_page("https://example.com")
```

### 2. Batch Scraping

```python
urls = ["url1", "url2", "url3"]
results = scraper.scrape_batch(urls, delay=2)
```

### 3. Structured Data Extraction

```python
# Extract specific elements
data = scraper.extract_structured_data(
    url="https://example.com",
    selectors={
        'title': 'h1.title',
        'content': 'div.content',
        'links': 'a.link'
    }
)
```

## Key Features

### ✅ Compliance
- Automatic robots.txt checking
- Configurable rate limiting
- Respectful User-Agent headers

### 🔍 Data Extraction
- CSS selector support
- XPath queries
- Regular expression matching
- JSON-LD parsing

### 💾 Storage
- Multiple output formats (JSON, CSV, Markdown)
- Organized file structure
- Metadata preservation

### 🛡️ Error Handling
- Retry logic with exponential backoff
- Timeout management
- Connection error recovery

## Constraints & Trade-offs

### Legal & Ethical
- ⚠️ Always check website's Terms of Service
- ⚠️ Respect robots.txt directives
- ⚠️ Use reasonable rate limits (default: 2 seconds)
- ⚠️ Only for personal/research use, not commercial

### Technical
- Dynamic content (JavaScript) requires additional tools
- Some sites may block automated access
- Large-scale scraping may be slow due to rate limits

### Performance
- Trade-off between speed and politeness
- Memory usage increases with batch size
- Network latency affects overall speed

## Best Practices

1. **Check robots.txt first**
   ```python
   if scraper.can_fetch(url):
       data = scraper.scrape_page(url)
   ```

2. **Use appropriate delays**
   ```python
   scraper.set_delay(2)  # 2 seconds between requests
   ```

3. **Handle errors gracefully**
   ```python
   try:
       data = scraper.scrape_page(url)
   except ScraperError as e:
       logger.error(f"Failed to scrape: {e}")
   ```

4. **Save incrementally**
   ```python
   for url in urls:
       data = scraper.scrape_page(url)
       scraper.save(data, f"output/{url_to_filename(url)}.json")
   ```

## Examples

See `references/examples.md` for detailed examples including:
- E-commerce product scraping
- News article extraction
- Social media data collection
- Academic paper metadata

## Configuration

Default settings in `config.json`:
```json
{
  "delay": 2,
  "timeout": 15,
  "max_retries": 3,
  "user_agent": "Research Bot (respectful crawler)",
  "respect_robots_txt": true
}
```

## Dependencies

- requests
- beautifulsoup4
- lxml (optional, for faster parsing)

Install with:
```bash
pip install requests beautifulsoup4 lxml
```