import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scrapy.crawler import CrawlerRunner
from scrapy import Spider, Request
from twisted.internet import reactor
import threading

app = FastAPI(title="Scrapy MVP API")

# HTML Web Interface (same style as your other APIs)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Scrapy MVP - Web Scraper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        pre {
            background: white;
            padding: 10px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>🕷️ Scrapy MVP Web Scraper</h1>
    <p>Faster than Playwright for static pages. Use for: Google results, news sites, blogs.</p>
    
    <input type="text" id="url" placeholder="Enter search query (e.g., artificial intelligence)">
    <button onclick="scrape()">Scrape Google Results</button>
    
    <h3>Results:</h3>
    <pre id="result">Waiting...</pre>

    <script>
        async function scrape() {
            const query = document.getElementById('url').value;
            if (!query) {
                alert('Please enter a search query');
                return;
            }
            document.getElementById('result').innerText = 'Scraping...';
            try {
                const response = await fetch(`/scrape?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                document.getElementById('result').innerText = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').innerText = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/ui", response_class=HTMLResponse)
async def ui():
    return HTMLResponse(content=HTML_PAGE)


# ========== SCRAPY SPIDER ==========
class GoogleSpider(Spider):
    name = "google"
    
    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f'https://www.google.com/search?q={query}&num=20']

    def parse(self, response):
        for result in response.css('div.tF2Cxc'):
            yield {
                'title': result.css('h3::text').get(),
                'link': result.css('a::attr(href)').get(),
                'snippet': result.css('div.VwiC3b::text').get(),
            }


# Store results globally
scraped_results = []

def collect_results(item, response, spider):
    scraped_results.append(dict(item))


@app.get("/scrape")
async def scrape_google(query: str):
    global scraped_results
    scraped_results = []
    
    # Run Scrapy in a separate thread so it doesn't block FastAPI
    def run_spider():
        runner = CrawlerRunner()
        deferred = runner.crawl(GoogleSpider, query=query)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)
    
    thread = threading.Thread(target=run_spider)
    thread.start()
    thread.join(timeout=60)  # Wait up to 60 seconds
    
    return {
        "query": query,
        "count": len(scraped_results),
        "results": scraped_results[:50],
        "note": "Scrapy is much faster than Playwright for static pages like Google results"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Scrapy MVP API is running. Go to /ui for web interface or /scrape?query=YOUR_QUERY"}