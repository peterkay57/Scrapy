from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess
import json
import os

app = FastAPI(title="Scrapy MVP API", description="Professional Web Scraper")

# ========== PROFESSIONAL HTML WEB INTERFACE (Like Crawl4AI) ==========
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartLinker Scrapy Bot | Professional Web Scraper</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Header */
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #a0a0b0;
            font-size: 1.1rem;
        }
        
        .badge {
            display: inline-block;
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-top: 15px;
        }
        
        /* Main Card */
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        /* Input Section */
        .input-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            color: #c0c0d0;
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }
        
        input {
            width: 100%;
            padding: 14px 18px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }
        
        input::placeholder {
            color: #5a5a7a;
        }
        
        /* Button */
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 14px 32px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Stats Bar */
        .stats {
            display: flex;
            gap: 20px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 12px 20px;
            flex: 1;
            text-align: center;
        }
        
        .stat-card .label {
            font-size: 0.7rem;
            color: #7a7a9a;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card .value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 10px;
        }
        
        .tab {
            padding: 8px 20px;
            background: transparent;
            border: none;
            color: #a0a0b0;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom: 2px solid #667eea;
        }
        
        /* Result Box */
        .result-box {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 16px;
            padding: 20px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .result-header h3 {
            color: #c0c0d0;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .copy-btn {
            background: rgba(102, 126, 234, 0.2);
            border: none;
            padding: 5px 12px;
            border-radius: 8px;
            color: #667eea;
            cursor: pointer;
            font-size: 0.8rem;
        }
        
        pre {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 12px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #d0d0e0;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            max-height: 400px;
            overflow-y: auto;
        }
        
        /* Loading */
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #5a5a7a;
            font-size: 0.8rem;
            margin-top: 30px;
        }
        
        /* Example Links */
        .examples {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        
        .example-link {
            background: rgba(102, 126, 234, 0.15);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #a0a0b0;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .example-link:hover {
            background: rgba(102, 126, 234, 0.3);
            color: white;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .card { padding: 20px; }
            .stats { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕷️ SmartLinker Scrapy Bot</h1>
            <p>Professional Web Scraper & Search Engine Crawler</p>
            <div class="badge">⚡ Powered by Scrapy | Fast & Scalable</div>
        </div>
        
        <div class="card">
            <div class="input-group">
                <label>🔍 Enter Search Query</label>
                <input type="text" id="query" placeholder="e.g., artificial intelligence, machine learning, python programming">
            </div>
            
            <div class="examples">
                <span class="example-link" onclick="setQuery('artificial intelligence')">🤖 AI</span>
                <span class="example-link" onclick="setQuery('machine learning')">📊 ML</span>
                <span class="example-link" onclick="setQuery('python programming')">🐍 Python</span>
                <span class="example-link" onclick="setQuery('web scraping')">🕷️ Web Scraping</span>
            </div>
            
            <button class="btn" id="scrapeBtn" onclick="scrape()">🚀 Search & Scrape</button>
        </div>
        
        <div class="card" id="statsCard" style="display: none;">
            <div class="stats">
                <div class="stat-card"><div class="label">QUERY</div><div class="value" id="statQuery">-</div></div>
                <div class="stat-card"><div class="label">RESULTS</div><div class="value" id="statCount">-</div></div>
                <div class="stat-card"><div class="label">STATUS</div><div class="value" id="statStatus">-</div></div>
            </div>
        </div>
        
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="showTab('results')">📋 Search Results</button>
                <button class="tab" onclick="showTab('json')">📄 JSON Raw</button>
            </div>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p style="color: #a0a0b0;">Scraping Google results... This may take 10-30 seconds</p>
            </div>
            
            <div id="resultsTab" class="result-box" style="display: none;">
                <div class="result-header">
                    <h3>📋 Search Results</h3>
                    <button class="copy-btn" onclick="copyToClipboard('results')">📋 Copy All</button>
                </div>
                <div id="resultsContent"></div>
            </div>
            
            <div id="jsonTab" class="result-box" style="display: none;">
                <div class="result-header">
                    <h3>📄 JSON Response</h3>
                    <button class="copy-btn" onclick="copyToClipboard('json')">📋 Copy JSON</button>
                </div>
                <pre id="jsonContent"></pre>
            </div>
        </div>
        
        <div class="footer">
            <p>SmartLinker Scrapy Bot | Searches Google and extracts titles, URLs, and descriptions</p>
            <p>⚡ API endpoint: <code style="background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;">/scrape?query=YOUR_QUERY</code></p>
        </div>
    </div>

    <script>
        let currentData = null;
        
        function setQuery(q) {
            document.getElementById('query').value = q;
        }
        
        async function scrape() {
            const query = document.getElementById('query').value;
            if (!query) {
                alert('Please enter a search query');
                return;
            }
            
            const btn = document.getElementById('scrapeBtn');
            const loading = document.getElementById('loading');
            const resultsTab = document.getElementById('resultsTab');
            const jsonTab = document.getElementById('jsonTab');
            const statsCard = document.getElementById('statsCard');
            
            btn.disabled = true;
            btn.textContent = '⏳ Scraping...';
            loading.style.display = 'block';
            resultsTab.style.display = 'none';
            jsonTab.style.display = 'none';
            statsCard.style.display = 'none';
            
            try {
                const response = await fetch(`/scrape?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                currentData = data;
                
                // Update stats
                document.getElementById('statQuery').textContent = data.query || '-';
                document.getElementById('statCount').textContent = data.count || 0;
                document.getElementById('statStatus').textContent = data.success ? '✅ Success' : '❌ Failed';
                statsCard.style.display = 'block';
                
                // Build results HTML
                let resultsHtml = '';
                if (data.results && data.results.length > 0) {
                    for (let i = 0; i < data.results.length; i++) {
                        const r = data.results[i];
                        resultsHtml += `
                            <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <div style="font-weight: bold; color: #667eea; margin-bottom: 5px;">${i+1}. ${r.title || 'No title'}</div>
                                <div style="font-size: 0.85rem; color: #4c9aff; margin-bottom: 5px;">${r.url || ''}</div>
                                <div style="font-size: 0.85rem; color: #a0a0b0;">${r.snippet || 'No description'}</div>
                            </div>
                        `;
                    }
                } else {
                    resultsHtml = '<p style="color: #a0a0b0;">No results found.</p>';
                }
                document.getElementById('resultsContent').innerHTML = resultsHtml;
                
                // JSON content
                document.getElementById('jsonContent').textContent = JSON.stringify(data, null, 2);
                
                resultsTab.style.display = 'block';
                jsonTab.style.display = 'block';
                
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                btn.disabled = false;
                btn.textContent = '🚀 Search & Scrape';
                loading.style.display = 'none';
            }
        }
        
        function showTab(tab) {
            const resultsTab = document.getElementById('resultsTab');
            const jsonTab = document.getElementById('jsonTab');
            const tabs = document.querySelectorAll('.tab');
            
            tabs.forEach(t => t.classList.remove('active'));
            
            if (tab === 'results') {
                resultsTab.style.display = 'block';
                jsonTab.style.display = 'none';
                tabs[0].classList.add('active');
            } else {
                resultsTab.style.display = 'none';
                jsonTab.style.display = 'block';
                tabs[1].classList.add('active');
            }
        }
        
        function copyToClipboard(type) {
            let content = '';
            if (type === 'results' && currentData && currentData.results) {
                content = currentData.results.map(r => `${r.title}\n${r.url}\n${r.snippet}\n---`).join('\n');
            } else if (type === 'json' && currentData) {
                content = JSON.stringify(currentData, null, 2);
            }
            navigator.clipboard.writeText(content);
            alert('Copied to clipboard!');
        }
        
        document.getElementById('query').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                scrape();
            }
        });
    </script>
</body>
</html>
"""

@app.get("/ui", response_class=HTMLResponse)
async def ui():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/scrape")
async def scrape(query: str):
    """Scrape Google search results using Scrapy"""
    try:
        result = subprocess.run(
            ['python', 'spider.py', query],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {
                "query": query,
                "success": False,
                "error": result.stderr,
                "count": 0,
                "results": []
            }
        
        results = json.loads(result.stdout)
        
        return {
            "query": query,
            "success": True,
            "count": len(results),
            "results": results[:50]
        }
        
    except subprocess.TimeoutExpired:
        return {
            "query": query,
            "success": False,
            "error": "Scraping timed out after 60 seconds",
            "count": 0,
            "results": []
        }
    except Exception as e:
        return {
            "query": query,
            "success": False,
            "error": str(e),
            "count": 0,
            "results": []
        }

@app.get("/health")
def health():
    return {"status": "ok"}            cursor: pointer;
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
