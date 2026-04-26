#!/usr/bin/env python
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
import json
import sys

class GoogleSpider(scrapy.Spider):
    name = "google"
    
    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f'https://www.google.com/search?q={query}&num=20']
        self.results = []
    
    def parse(self, response):
        for result in response.css('div.tF2Cxc'):
            title = result.css('h3::text').get()
            link = result.css('a::attr(href)').get()
            snippet = result.css('div.VwiC3b::text').get()
            
            if title and link:
                self.results.append({
                    'title': title,
                    'url': link,
                    'snippet': snippet or ''
                })
        
        # Follow next page (optional)
        next_page = response.css('a#pnnext::attr(href)').get()
        if next_page and len(self.results) < 50:
            yield response.follow(next_page, self.parse)

def run_spider(query):
    configure_logging({'LOG_LEVEL': 'ERROR'})
    runner = CrawlerRunner()
    
    deferred = runner.crawl(GoogleSpider, query=query)
    deferred.addBoth(lambda _: reactor.stop())
    
    reactor.run()
    
    # Get results from the spider instance
    spider = runner.spiders[0] if runner.spiders else None
    if spider and hasattr(spider, 'results'):
        return spider.results
    return []

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "python"
    results = run_spider(query)
    print(json.dumps(results))    runner = CrawlerRunner()
    
    deferred = runner.crawl(GoogleSpider, query=query)
    deferred.addBoth(lambda _: reactor.stop())
    
    reactor.run()
    
    # Get results from the spider instance
    spider = runner.spiders[0] if runner.spiders else None
    if spider and hasattr(spider, 'results'):
        return spider.results
    return []

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "python"
    results = run_spider(query)
    print(json.dumps(results))
