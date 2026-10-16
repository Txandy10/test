from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

@app.route("/")
def index():
    return """
        <!DOCTYPE html>
        <html>
        <head><title>Vercel Python Web Proxy</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>Vercel Web Proxy</h2>
            <form action="/proxy" method="get">
                <input type="text" name="url" placeholder="https://example.com" style="width: 400px; padding: 8px;" required>
                <button type="submit" style="padding: 8px 15px;">Go</button>
            </form>
        </body>
        </html>
    """

@app.route("/proxy")
def proxy():
    target_url = request.args.get("url")
    
    if not target_url:
        return "Error: No URL provided.", 400
    
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        resp = requests.get(target_url, headers=headers, allow_redirects=True, timeout=10)
        
        content_type = resp.headers.get('Content-Type', '')

        # If the response is HTML, rewrite links and asset paths so they stay inside the proxy
        if 'text/html' in content_type:
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Rewrite <a> tags (links)
            for tag in soup.find_all('a', href=True):
                absolute_url = urljoin(target_url, tag['href'])
                tag['href'] = f"/proxy?url={absolute_url}"
                
            # Rewrite <img> tags (images)
            for tag in soup.find_all('img', src=True):
                absolute_url = urljoin(target_url, tag['src'])
                tag['src'] = f"/proxy?url={absolute_url}"
                
            # Rewrite <link> tags (stylesheets, etc.)
            for tag in soup.find_all('link', href=True):
                absolute_url = urljoin(target_url, tag['href'])
                tag['href'] = f"/proxy?url={absolute_url}"

            # Rewrite <script> tags
            for tag in soup.find_all('script', src=True):
                absolute_url = urljoin(target_url, tag['src'])
                tag['src'] = f"/proxy?url={absolute_url}"

            content = str(soup).encode('utf-8')
        else:
            content = resp.content

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_to_send = [
            (name, value) for name, value in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(content, resp.status_code, headers_to_send)

    except Exception as e:
        return f"Failed to proxy request: {e}", 500
