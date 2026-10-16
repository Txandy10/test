from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters (e.g., /api/proxy?url=https://api.example.com/data)
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        target_url = query_params.get('url', [None])[0]
        
        if not target_url:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'url' query parameter"}).encode())
            return

        try:
            # Fetch data from the target API
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": "Vercel-Proxy-Bot"}
            )
            with urllib.request.urlopen(req) as response:
                data = response.read()
                
                # Send back the response with CORS headers enabled
                self.send_response(200)
                self.send_header('Content-type', response.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*') # Allows any frontend to call your proxy
                self.end_headers()
                self.wfile.write(data)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
