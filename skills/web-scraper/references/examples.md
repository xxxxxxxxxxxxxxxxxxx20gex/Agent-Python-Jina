# Web Scraper Examples

## Example 1: Basic Page Scraping

```python
from skills.web_scraper.scripts.scraper import WebScraper

# Initialize scraper
scraper = WebScraper()

# Scrape a page
data = scraper.scrape_page("https://example.com")

# Access extracted data
print(f"Title: {data['title']}")
print(f"Links found: {len(data['links'])}")
print(f"Images found: {len(data['images'])}")

# Save to file
scraper.save(data, "output/example.json")
```

## Example 2: E-commerce Product Scraping

```python
# Define selectors for product data
selectors = {
    'name': 'h1.product-title',
    'price': 'span.price',
    'description': 'div.product-description',
    'rating': 'span.rating',
    'reviews': 'div.review'
}

# Extract structured data
product = scraper.extract_structured_data(
    url="https://shop.example.com/product/123",
    selectors=selectors
)

print(f"Product: {product['name']}")
print(f"Price: {product['price']}")
```

## Example 3: News Article Extraction

```python
# Scrape multiple news articles
news_urls = [
    "https://news.example.com/article1",
    "https://news.example.com/article2",
    "https://news.example.com/article3"
]

# Batch scraping with 3-second delay
articles = scraper.scrape_batch(news_urls, delay=3)

# Save each article
for i, article in enumerate(articles, 1):
    scraper.save(article, f"news/article_{i}.json")
```

## Example 4: Academic Paper Metadata

```python
# Extract paper information
paper_selectors = {
    'title': 'h1.paper-title',
    'authors': 'span.author',
    'abstract': 'div.abstract',
    'keywords': 'span.keyword',
    'publication_date': 'time.published'
}

paper = scraper.extract_structured_data(
    url="https://papers.example.com/paper/456",
    selectors=paper_selectors
)

# Authors will be a list
print(f"Authors: {', '.join(paper['authors'])}")
```

## Example 5: Respecting robots.txt

```python
# Check before scraping
url = "https://example.com/data"

if scraper.can_fetch(url):
    data = scraper.scrape_page(url)
    print("✓ Scraping allowed")
else:
    print("✗ Scraping disallowed by robots.txt")
```

## Example 6: Custom Configuration

```python
# Create scraper with custom settings
config = {
    'delay': 5,              # 5 seconds between requests
    'timeout': 30,           # 30 second timeout
    'max_retries': 5,        # Retry up to 5 times
    'user_agent': 'MyBot/1.0',
    'respect_robots_txt': True
}

scraper = WebScraper(config)
```

## Example 7: Error Handling

```python
urls = ["url1", "url2", "url3"]
results = []

for url in urls:
    try:
        data = scraper.scrape_page(url)
        results.append(data)
        print(f"✓ Success: {url}")
    except PermissionError:
        print(f"✗ Blocked by robots.txt: {url}")
    except requests.exceptions.Timeout:
        print(f"✗ Timeout: {url}")
    except Exception as e:
        print(f"✗ Error: {url} - {e}")
```

## Example 8: Building a Knowledge Base

```python
import os

# Scrape a collection of pages
base_url = "https://docs.example.com"
pages = [
    "/intro",
    "/getting-started",
    "/advanced",
    "/api-reference"
]

# Create knowledge base structure
kb_dir = "knowledge_base"
os.makedirs(kb_dir, exist_ok=True)

for page in pages:
    url = base_url + page
    print(f"Scraping: {url}")
    
    data = scraper.scrape_page(url)
    
    # Save as markdown
    filename = page.strip('/').replace('/', '_') + '.md'
    filepath = os.path.join(kb_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {data['title']}\n\n")
        f.write(f"Source: {url}\n\n")
        f.write(data['text'])
    
    print(f"✓ Saved: {filepath}")
```

## Example 9: Extracting Links for Crawling

```python
# Get all links from a page
data = scraper.scrape_page("https://example.com")

# Filter internal links
from urllib.parse import urljoin, urlparse

base_domain = urlparse("https://example.com").netloc
internal_links = []

for link in data['links']:
    full_url = urljoin("https://example.com", link)
    if urlparse(full_url).netloc == base_domain:
        internal_links.append(full_url)

print(f"Found {len(internal_links)} internal links")

# Scrape them all (with rate limiting)
for link in internal_links[:10]:  # Limit to first 10
    try:
        page_data = scraper.scrape_page(link)
        print(f"✓ {link}")
    except Exception as e:
        print(f"✗ {link}: {e}")
```

## Example 10: Saving in Different Formats

```python
data = scraper.scrape_page("https://example.com")

# Save as JSON
scraper.save(data, "output/page.json", format='json')

# Save as text
scraper.save(data, "output/page.txt", format='txt')

# Custom CSV export
import csv

with open('output/links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'Text'])
    
    soup = BeautifulSoup(data['html'], 'html.parser')
    for link in soup.find_all('a', href=True):
        writer.writerow([link['href'], link.get_text(strip=True)])
```

## Tips & Best Practices

### 1. Start Small
Test with a few URLs before scaling up.

### 2. Monitor Rate Limits
```python
scraper.set_delay(3)  # Increase delay if needed
```

### 3. Save Incrementally
Don't wait until all scraping is done to save data.

### 4. Log Everything
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Scraping: {url}")
```

### 5. Handle Failures Gracefully
Always use try-except blocks and continue on errors.

### 6. Respect the Website
- Check Terms of Service
- Use reasonable delays
- Don't overload servers
- Identify your bot clearly

## Common Patterns

### Pattern 1: Pagination
```python
page = 1
while True:
    url = f"https://example.com/items?page={page}"
    data = scraper.scrape_page(url)
    
    # Check if there are more pages
    soup = BeautifulSoup(data['html'], 'html.parser')
    if not soup.find('a', class_='next-page'):
        break
    
    page += 1
```

### Pattern 2: Authentication
```python
session = requests.Session()
session.post('https://example.com/login', data={
    'username': 'user',
    'password': 'pass'
})

# Use session for authenticated requests
response = session.get('https://example.com/protected')
```

### Pattern 3: Dynamic Content
For JavaScript-rendered content, consider using Selenium:
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
# Then parse with BeautifulSoup
```