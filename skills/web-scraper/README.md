# Web Scraper Skill

A professional-grade web scraping skill with robots.txt compliance, rate limiting, and structured data extraction.

## Features

✅ **Compliant & Respectful**
- Automatic robots.txt checking
- Configurable rate limiting
- Proper User-Agent identification

✅ **Powerful Extraction**
- CSS selector support
- Batch processing
- Structured data extraction
- Multiple output formats

✅ **Robust & Reliable**
- Automatic retry with exponential backoff
- Error handling
- Timeout management

## Quick Start

### Installation

```bash
pip install requests beautifulsoup4 lxml
```

### Basic Usage

```python
from skills.web_scraper.scripts.scraper import WebScraper

# Initialize
scraper = WebScraper()

# Scrape a page
data = scraper.scrape_page("https://example.com")

# Save results
scraper.save(data, "output.json")
```

### Command Line

```bash
python skills/web-scraper/scripts/scraper.py https://example.com output.json
```

## Documentation

- **SKILL.md** - Skill overview and usage guidelines
- **references/examples.md** - 10+ practical examples
- **references/api-reference.md** - Complete API documentation
- **config.json** - Configuration options

## Examples

### Extract Structured Data

```python
data = scraper.extract_structured_data(
    url="https://example.com/product",
    selectors={
        'title': 'h1.product-name',
        'price': 'span.price',
        'description': 'div.description'
    }
)
```

### Batch Scraping

```python
urls = ["url1", "url2", "url3"]
results = scraper.scrape_batch(urls, delay=2)
```

## Configuration

Edit `config.json` or pass config dict:

```python
config = {
    'delay': 3,              # 3 seconds between requests
    'timeout': 20,           # 20 second timeout
    'max_retries': 5,        # Retry up to 5 times
    'respect_robots_txt': True
}

scraper = WebScraper(config)
```

## Best Practices

1. ✅ Always check robots.txt
2. ✅ Use reasonable delays (≥2 seconds)
3. ✅ Handle errors gracefully
4. ✅ Save data incrementally
5. ✅ Respect Terms of Service

## Legal & Ethical

⚠️ **Important:**
- Check website's Terms of Service
- Only for personal/research use
- Respect robots.txt directives
- Use appropriate rate limits
- Not for commercial scraping

## Support

See documentation in `references/` folder:
- `examples.md` - Practical examples
- `api-reference.md` - API documentation

## License

For educational and research purposes only.