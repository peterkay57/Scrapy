from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess
import json

app = FastAPI(title="Scrapy MVP API")

# HTML interface (simple, clean)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Scrapy MVP</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a2e;
            color: white;
        }
        input, button {
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
        }
        input {
            width: 70%;
            background: #0f3460;
            color: white;
        }
        button {
            background: #e94560;
            color: white;
            cursor: pointer;
        }
        pre {
            background: #0f3460;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>🕷️ Scrapy MVP - Google Scraper</h1>
    <input type="text" id="query" placeholder="Enter search query">
    <button onclick="scrape()">Scrape Google</button>
    <pre id="result">Waiting...</pre>

    <script>
        async function scrape() {
            const query = document.getElementById('query').value;
            if (!query) return;
            document.getElementById('result').innerText = 'Scraping...';
            const res = await fetch(`/scrape?query=${encodeURIComponent(query)}`);
            const data = await res.json();
            document.getElementById('result').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""

@app.get("/ui", response_class=HTMLResponse)
async def ui():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/scrape")
async def scrape(query: str):
    try:
        # Run the spider in a subprocess (completely separate)
        cmd = [
            "python", "-c", f"""
import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import json

results = []

class GoogleSpider(scrapy.Spider):
    name = "google"
    start_urls = [f'https://www.google.com/search?q={query}']

    def parse(self, response):
        for r in response.css('div.tF2Cxc'):
            results.append({{
                'title': r.css('h3::text').get(),
                'url': r.css('a::attr(href)').get(),
            }})

runner = CrawlerRunner()
runner.crawl(GoogleSpider)
runner.crawl(GoogleSpider).addBoth(lambda _: reactor.stop())
reactor.run()
print(json.dumps(results[:20]))
"""
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            return {"query": query, "success": False, "error": result.stderr}
        
        import ast
        try:
            scraped_data = json.loads(result.stdout)
        except:
            scraped_data = []
        
        return {
            "query": query,
            "success": True,
            "count": len(scraped_data),
            "results": scraped_data
        }
        
    except subprocess.TimeoutExpired:
        return {"query": query, "success": False, "error": "Timeout"}
    except Exception as e:
        return {"query": query, "success": False, "error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}
