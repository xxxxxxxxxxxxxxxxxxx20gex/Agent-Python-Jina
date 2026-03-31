#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Scraper - Advanced web scraping with compliance
"""

import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import time
import json
import os
from typing import Dict, List, Optional, Any

class WebScraper:
    """Advanced web scraper with robots.txt compliance"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize scraper with configuration"""
        self.config = config or {
            'delay': 2,
            'timeout': 15,
            'max_retries': 3,
            'user_agent': 'Research Bot (respectful crawler)',
            'respect_robots_txt': True
        }
        
        self.headers = {
            'User-Agent': self.config['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        self.robot_parsers = {}
        self.last_request_time = {}
    
    def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt"""
        if not self.config['respect_robots_txt']:
            return True
        
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.robot_parsers:
            rp = RobotFileParser()
            rp.set_url(f"{base_url}/robots.txt")
            try:
                rp.read()
                self.robot_parsers[base_url] = rp
            except:
                return True
        
        return self.robot_parsers[base_url].can_fetch("*", url)
    
    def _wait_if_needed(self, domain: str):
        """Implement rate limiting"""
        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < self.config['delay']:
                time.sleep(self.config['delay'] - elapsed)
        
        self.last_request_time[domain] = time.time()
    
    def scrape_page(self, url: str) -> Dict[str, Any]:
        """Scrape a single page"""
        if not self.can_fetch(url):
            raise PermissionError(f"robots.txt disallows fetching: {url}")
        
        parsed = urlparse(url)
        domain = parsed.netloc
        self._wait_if_needed(domain)
        
        for attempt in range(self.config['max_retries']):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    timeout=self.config['timeout']
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                return {
                    'url': url,
                    'status_code': response.status_code,
                    'title': soup.find('title').text.strip() if soup.find('title') else '',
                    'html': str(soup),
                    'text': soup.get_text(strip=True),
                    'links': [a.get('href') for a in soup.find_all('a', href=True)],
                    'images': [img.get('src') for img in soup.find_all('img', src=True)],
                    'meta': self._extract_meta(soup),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
            except requests.exceptions.RequestException as e:
                if attempt == self.config['max_retries'] - 1:
                    raise
                time.sleep(2 ** attempt)
    
    def _extract_meta(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta tags"""
        meta = {}
        for tag in soup.find_all('meta'):
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                meta[name] = content
        return meta
    
    def extract_structured_data(
        self, 
        url: str, 
        selectors: Dict[str, str]
    ) -> Dict[str, Any]:
        """Extract specific data using CSS selectors"""
        data = self.scrape_page(url)
        soup = BeautifulSoup(data['html'], 'html.parser')
        
        result = {'url': url}
        for key, selector in selectors.items():
            elements = soup.select(selector)
            if len(elements) == 1:
                result[key] = elements[0].get_text(strip=True)
            else:
                result[key] = [el.get_text(strip=True) for el in elements]
        
        return result
    
    def scrape_batch(
        self, 
        urls: List[str], 
        delay: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Scrape multiple URLs"""
        if delay:
            self.config['delay'] = delay
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"Scraping {i}/{len(urls)}: {url}")
            try:
                data = self.scrape_page(url)
                results.append(data)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                results.append({'url': url, 'error': str(e)})
        
        return results
    
    def save(self, data: Any, filepath: str, format: str = 'json'):
        """Save scraped data"""
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    f.write(data.get('text', str(data)))
                else:
                    f.write(str(data))
    
    def set_delay(self, delay: float):
        """Set request delay"""
        self.config['delay'] = delay


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <url> [output_file]")
        sys.exit(1)
    
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'output.json'
    
    scraper = WebScraper()
    
    print(f"Scraping: {url}")
    data = scraper.scrape_page(url)
    
    scraper.save(data, output)
    print(f"Saved to: {output}")


if __name__ == "__main__":
    main()