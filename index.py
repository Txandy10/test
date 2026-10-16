from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

@app.route("/")
def index():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vercel Web Proxy</title>
            <style>
                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                    color: #f8fafc;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .card {
                    background: rgba(30, 41, 59, 0.7);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
                    text-align: center;
                    width: 100%;
                    max-width: 500px;
                }
                h2 {
                    margin-bottom: 8px;
                    font-size: 24px;
                    font-weight: 700;
                    letter-spacing: -0.025em;
                }
                p {
                    color: #94a3b8;
                    font-size: 14px;
                    margin-bottom: 24px;
                }
                .form-group {
                    display: flex;
                    gap: 8px;
                }
                input[type="text"] {
                    flex: 1;
                    padding: 12px 16px;
                    background: #0f172a;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    color: #fff;
                    font-size: 15px;
                    outline: none;
                    transition: border-color 0.2s;
                }
                input[type="text"]:focus {
                    border-color: #6366f1;
                }
                button {
                    background: #6366f1;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 8px;
                    font-size: 15px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                button:hover {
                    background: #4f46e5;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Web Proxy</h2>
                <p>Enter any URL below to browse securely through Vercel.</p>
                <form action="/proxy" method="get">
                    <div class="form-group">
                        <input type="text" name="url" placeholder="https://example.com" required autocomplete="off">
                        <button type="submit">Go</button>
                    </div>
                </form>
            </div>
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
