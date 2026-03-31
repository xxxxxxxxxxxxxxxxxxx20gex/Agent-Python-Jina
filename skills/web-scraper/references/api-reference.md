# Web Scraper API Reference

## WebScraper Class

### Constructor

```python
WebScraper(config: Optional[Dict] = None)
```

**Parameters:**
- `config` (dict, optional): Configuration dictionary

**Default Configuration:**
```python
{
    'delay': 2,                    # Seconds between requests
    'timeout': 15,                 # Request timeout in seconds
    'max_retries': 3,              # Maximum retry attempts
    'user_agent': 'Research Bot',  # User-Agent header
    'respect_robots_txt': True     # Check robots.txt
}
```

### Methods

#### can_fetch()

```python
can_fetch(url: str) -> bool
```

Check if URL can be fetched according to robots.txt.

**Parameters:**
- `url` (str): URL to check

**Returns:**
- `bool`: True if allowed, False otherwise

**Example:**
```python
if scraper.can_fetch("https://example.com"):
    data = scraper.scrape_page("https://example.com")
```

---

#### scrape_page()

```python
scrape_page(url: str) -> Dict[str, Any]
```

Scrape a single web page.

**Parameters:**
- `url` (str): URL to scrape

**Returns:**
- `dict`: Scraped data containing:
  - `url` (str): The scraped URL
  - `status_code` (int): HTTP status code
  - `title` (str): Page title
  - `html` (str): Full HTML content
  - `text` (str): Extracted text
  - `links` (list): All links found
  - `images` (list): All image URLs
  - `meta` (dict): Meta tags
  - `timestamp` (str): Scrape timestamp

**Raises:**
- `PermissionError`: If robots.txt disallows
- `requests.exceptions.RequestException`: On network errors

**Example:**
```python
data = scraper.scrape_page("https://example.com")
print(data['title'])
```

---

#### extract_structured_data()

```python
extract_structured_data(
    url: str, 
    selectors: Dict[str, str]
) -> Dict[str, Any]
```

Extract specific data using CSS selectors.

**Parameters:**
- `url` (str): URL to scrape
- `selectors` (dict): CSS selectors for data extraction
  - Key: field name
  - Value: CSS selector

**Returns:**
- `dict`: Extracted data with field names as keys

**Example:**
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

---

#### scrape_batch()

```python
scrape_batch(
    urls: List[str], 
    delay: Optional[float] = None
) -> List[Dict[str, Any]]
```

Scrape multiple URLs.

**Parameters:**
- `urls` (list): List of URLs to scrape
- `delay` (float, optional): Override default delay

**Returns:**
- `list`: List of scraped data dictionaries

**Example:**
```python
urls = ["url1", "url2", "url3"]
results = scraper.scrape_batch(urls, delay=3)
```

---

#### save()

```python
save(data: Any, filepath: str, format: str = 'json')
```

Save scraped data to file.

**Parameters:**
- `data` (any): Data to save
- `filepath` (str): Output file path
- `format` (str): Output format ('json' or 'txt')

**Example:**
```python
scraper.save(data, "output/page.json")
scraper.save(data, "output/page.txt", format='txt')
```

---

#### set_delay()

```python
set_delay(delay: float)
```

Set request delay.

**Parameters:**
- `delay` (float): Delay in seconds

**Example:**
```python
scraper.set_delay(5)  # 5 seconds between requests
```

---

## Data Structures

### Scraped Page Data

```python
{
    'url': str,              # Source URL
    'status_code': int,      # HTTP status (200, 404, etc.)
    'title': str,            # Page title
    'html': str,             # Full HTML
    'text': str,             # Extracted text
    'links': List[str],      # All links
    'images': List[str],     # All image URLs
    'meta': Dict[str, str],  # Meta tags
    'timestamp': str         # ISO format timestamp
}
```

### Meta Tags

```python
{
    'description': str,      # Meta description
    'keywords': str,         # Meta keywords
    'author': str,           # Author
    'og:title': str,         # Open Graph title
    'og:description': str,   # Open Graph description
    # ... other meta tags
}
```

---

## Error Handling

### Exceptions

- `PermissionError`: robots.txt disallows access
- `requests.exceptions.Timeout`: Request timeout
- `requests.exceptions.HTTPError`: HTTP error (4xx, 5xx)
- `requests.exceptions.ConnectionError`: Connection failed
- `requests.exceptions.RequestException`: General request error

### Example Error Handling

```python
try:
    data = scraper.scrape_page(url)
except PermissionError:
    print("Blocked by robots.txt")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Configuration Options

### delay

**Type:** `float`  
**Default:** `2`  
**Description:** Seconds to wait between requests to the same domain

```python
config = {'delay': 5}  # 5 seconds
```

### timeout

**Type:** `int`  
**Default:** `15`  
**Description:** Request timeout in seconds

```python
config = {'timeout': 30}  # 30 seconds
```

### max_retries

**Type:** `int`  
**Default:** `3`  
**Description:** Maximum number of retry attempts on failure

```python
config = {'max_retries': 5}
```

### user_agent

**Type:** `str`  
**Default:** `'Research Bot (respectful crawler)'`  
**Description:** User-Agent header for requests

```python
config = {'user_agent': 'MyBot/1.0 (+http://mysite.com/bot)'}
```

### respect_robots_txt

**Type:** `bool`  
**Default:** `True`  
**Description:** Whether to check and respect robots.txt

```python
config = {'respect_robots_txt': False}  # Not recommended
```

---

## Command Line Usage

```bash
# Basic usage
python scraper.py <url> [output_file]

# Examples
python scraper.py https://example.com
python scraper.py https://example.com output.json
```

---

## Advanced Usage

### Custom Headers

```python
scraper.headers['Authorization'] = 'Bearer token123'
scraper.headers['Accept-Language'] = 'en-US'
```

### Session Management

```python
import requests

session = requests.Session()
session.post('https://example.com/login', data={'user': 'me'})

# Use session in scraper
scraper.session = session
```

### Proxy Support

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

# Add to requests
response = requests.get(url, proxies=proxies)
```

---

## Performance Tips

1. **Batch Processing**: Use `scrape_batch()` for multiple URLs
2. **Appropriate Delays**: Balance speed and politeness
3. **Retry Logic**: Built-in exponential backoff
4. **Timeout Settings**: Adjust based on target sites
5. **Incremental Saving**: Save data as you go

---

## Limitations

- **JavaScript Content**: Requires additional tools (Selenium, Playwright)
- **Rate Limiting**: Intentionally slow to be respectful
- **Authentication**: Basic support, may need customization
- **CAPTCHAs**: Cannot bypass (by design)
- **Dynamic Sites**: Limited to static HTML parsing

---

## Dependencies

```bash
pip install requests beautifulsoup4 lxml
```

**Required:**
- `requests` >= 2.28.0
- `beautifulsoup4` >= 4.11.0

**Optional:**
- `lxml` >= 4.9.0 (faster parsing)

---

## Version History

**1.0.0** (2026-03-31)
- Initial release
- Basic scraping functionality
- robots.txt compliance
- Rate limiting
- Structured data extraction