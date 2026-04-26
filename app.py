from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import subprocess
import json

app = FastAPI(title="Scrapy API")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Scrapy MVP</title>
<style>
body{font-family:Arial;max-width:800px;margin:50px auto;padding:20px;background:#1a1a2e;color:white;}
input,button{padding:12px;font-size:16px;border-radius:8px;border:none;}
input{width:70%;background:#0f3460;color:white;}
button{background:#e94560;color:white;cursor:pointer;}
pre{background:#0f3460;padding:15px;border-radius:8px;overflow-x:auto;}
</style>
</head>
<body>
<h1>Scrapy Web Scraper</h1>
<input type="text" id="query" placeholder="Enter search query">
<button onclick="scrape()">Scrape Google</button>
<pre id="result">Waiting...</pre>
<script>
async function scrape(){
    const q=document.getElementById('query').value;
    if(!q)return;
    document.getElementById('result').innerText='Scraping...';
    const r=await fetch(`/scrape?query=${encodeURIComponent(q)}`);
    const d=await r.json();
    document.getElementById('result').innerText=JSON.stringify(d,null,2);
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
    cmd = f"""
python -c "
import scrapy, json
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

class TestSpider(scrapy.Spider):
    name='test'
    start_urls=[f'https://www.google.com/search?q={query}']

    def parse(self, response):
        for r in response.css('div.tF2Cxc'):
            yield {{'title': r.css('h3::text').get(), 'url': r.css('a::attr(href)').get()}}

results=[]
def collect(item):
    results.append(dict(item))

runner=CrawlerRunner()
runner.crawl(TestSpider).addBoth(lambda _: reactor.stop())
reactor.run()
print(json.dumps(results))
"
"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return {"query": query, "error": result.stderr}
        data = json.loads(result.stdout)
        return {"query": query, "count": len(data), "results": data}
    except Exception as e:
        return {"query": query, "error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"}
