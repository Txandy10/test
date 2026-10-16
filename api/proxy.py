from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urljoin
import urllib.request
import json
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        target_url = query_params.get('url', [None])[0]

        if not target_url:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No URL provided"}).encode())
            return

        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url

        try:
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content_type = response.headers.get('Content-Type', '')
                raw_content = response.read()

                if 'text/html' in content_type:
                    soup = BeautifulSoup(raw_content, 'html.parser')
                    
                    # 1. Rewrite standard tags (a, img, link, script)
                    for tag in soup.find_all(['a', 'img', 'link', 'script']):
                        attr = 'href' if tag.has_attr('href') else ('src' if tag.has_attr('src') else None)
                        if attr:
                            original_url = tag[attr]
                            if original_url and not original_url.startswith('data:'):
                                abs_url = urljoin(target_url, original_url)
                                tag[attr] = f"/api/proxy?url={abs_url}"

                    # 2. Rewrite responsive images (srcset)
                    for tag in soup.find_all(attrs={'srcset': True}):
                        srcset = tag['srcset']
                        new_srcset_parts = []
                        for part in srcset.split(','):
                            part = part.strip()
                            if not part:
                                continue
                            bits = part.split(' ')
                            img_url = bits[0]
                            descriptor = bits[1] if len(bits) > 1 else ''
                            
                            if not img_url.startswith('data:'):
                                abs_url = urljoin(target_url, img_url)
                                proxy_url = f"/api/proxy?url={abs_url}"
                                new_srcset_parts.append(f"{proxy_url} {descriptor}".strip())
                            else:
                                new_srcset_parts.append(part)
                        
                        tag['srcset'] = ', '.join(new_srcset_parts)

                    content = str(soup).encode('utf-8')
                else:
                    content = raw_content
                
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
