scrapy
fastapi
uvicorn
twisted           
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
