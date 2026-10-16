from flask import Flask, request, Response
import requests

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
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_to_send = [
            (name, value) for name, value in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(resp.content, resp.status_code, headers_to_send)

    except Exception as e:
        return f"Failed to proxy request: {e}", 500
