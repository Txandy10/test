from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the incoming request URL
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Check if a target URL was passed (e.g. /api/proxy?url=https://example.com)
        target_url = query_params.get('url', [None])[0]
        
        if not target_url:
            # If no URL is provided, show a simple HTML form pointing to /api/proxy
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
                <!DOCTYPE html>
                <html>
                <head><title>Vercel API Proxy</title></head>
                <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                    <h2>Vercel API & Data Proxy</h2>
                    <form action="/api/proxy" method="get">
                        <input type="text" name="url" placeholder="https://api.ipify.org?format=json" style="width: 400px; padding: 8px;" required>
                        <button type="submit" style="padding: 8px 15px;">Fetch Data</button>
                    </form>
                </body>
                </html>
            """
            self.wfile.write(html.encode('utf-8'))
            return

        # Ensure URL has a scheme
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url

        try:
            # Fetch data from the target site/API
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                content_type = response.headers.get('Content-Type', 'application/json')
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
