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
        
        # If no URL is provided, serve the full WebOS Desktop Environment
        if not target_url:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>WebOS Proxy Desktop</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    body {
                        background: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000&auto=format&fit=crop') no-repeat center center fixed;
                        background-size: cover;
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                        overflow: hidden;
                        user-select: none;
                    }
                    .glass {
                        background: rgba(15, 23, 42, 0.75);
                        backdrop-filter: blur(16px);
                        -webkit-backdrop-filter: blur(16px);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                    .glass-window {
                        background: rgba(15, 23, 42, 0.85);
                        backdrop-filter: blur(20px);
                        -webkit-backdrop-filter: blur(20px);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
                    }
                    .app-icon:hover {
                        background: rgba(255, 255, 255, 0.15);
                        transform: translateY(-3px);
                    }
                    .window-anim {
                        animation: windowOpen 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                    }
                    @keyframes windowOpen {
                        0% { opacity: 0; transform: scale(0.92) translateY(10px); }
                        100% { opacity: 1; transform: scale(1) translateY(0); }
                    }
                    /* Custom Scrollbar */
                    ::-webkit-scrollbar { width: 6px; height: 6px; }
                    ::-webkit-scrollbar-track { background: transparent; }
                    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 3px; }
                    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.4); }
                </style>
            </head>
            <body class="h-screen w-screen flex flex-col justify-between text-slate-100">

                <!-- Desktop Grid Area -->
                <div id="desktop" class="flex-1 p-6 grid grid-cols-1 sm:grid-cols-6 gap-6 content-start z-0">
                    <!-- Browser App Icon -->
                    <div onclick="openApp('browserWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-indigo-500">
                            <i class="fa-solid fa-globe"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Web Browser</span>
                    </div>

                    <!-- Files App Icon -->
                    <div onclick="openApp('filesWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-amber-400">
                            <i class="fa-solid fa-folder-open"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Files</span>
                    </div>

                    <!-- Notepad App Icon -->
                    <div onclick="openApp('notepadWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-emerald-500">
                            <i class="fa-solid fa-note-sticky"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Notepad</span>
                    </div>

                    <!-- Settings App Icon -->
                    <div onclick="openApp('settingsWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-slate-700 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-slate-600">
                            <i class="fa-solid fa-gear"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Settings</span>
                    </div>
                </div>

                <!-- WINDOWS CONTAINER -->

                <!-- 1. BROWSER WINDOW -->
                <div id="browserWindow" class="window window-anim hidden absolute top-12 left-16 w-[850px] h-[540px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <!-- Window Titlebar -->
                    <div class="h-11 bg-slate-900/60 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'browserWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('browserWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('browserWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('browserWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-globe mr-1.5 text-indigo-400"></i> WebOS Browser</span>
                        </div>
                    </div>
                    <!-- Browser Navbar / Address Bar -->
                    <div class="bg-slate-900/40 p-2.5 border-b border-white/10 flex items-center space-x-2">
                        <button onclick="navigateBrowser(-1)" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10"><i class="fa-solid fa-arrow-left"></i></button>
                        <button onclick="navigateBrowser(1)" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10"><i class="fa-solid fa-arrow-right"></i></button>
                        <button onclick="refreshBrowser()" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10"><i class="fa-solid fa-rotate-right"></i></button>
                        <form onsubmit="loadUrl(event)" class="flex-1 flex">
                            <input id="urlInput" type="text" placeholder="Search or enter URL (e.g. https://example.com)" class="w-full bg-slate-950/60 border border-white/10 rounded-lg px-4 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500">
                        </form>
                        <button onclick="loadUrlBtn()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition">Go</button>
                    </div>
                    <!-- Browser Iframe / Viewport -->
                    <div class="flex-1 bg-white relative">
                        <iframe id="browserFrame" src="about:blank" class="w-full h-full border-none"></iframe>
                    </div>
                </div>

                <!-- 2. FILES APP WINDOW -->
                <div id="filesWindow" class="window window-anim hidden absolute top-20 left-32 w-[650px] h-[420px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/60 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'filesWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('filesWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('filesWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('filesWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-folder-open mr-1.5 text-amber-400"></i> File Manager</span>
                        </div>
                    </div>
                    <div class="flex-1 p-6 grid grid-cols-4 gap-4 overflow-y-auto">
                        <div class="p-4 bg-white/5 hover:bg-white/10 rounded-xl flex flex-col items-center justify-center cursor-pointer border border-white/5">
                            <i class="fa-solid fa-folder text-amber-400 text-3xl mb-2"></i>
                            <span class="text-xs font-medium">Documents</span>
                        </div>
                        <div class="p-4 bg-white/5 hover:bg-white/10 rounded-xl flex flex-col items-center justify-center cursor-pointer border border-white/5">
                            <i class="fa-solid fa-image text-indigo-400 text-3xl mb-2"></i>
                            <span class="text-xs font-medium">Wallpapers</span>
                        </div>
                        <div class="p-4 bg-white/5 hover:bg-white/10 rounded-xl flex flex-col items-center justify-center cursor-pointer border border-white/5">
                            <i class="fa-solid fa-file-lines text-emerald-400 text-3xl mb-2"></i>
                            <span class="text-xs font-medium">notes.txt</span>
                        </div>
                    </div>
                </div>

                <!-- 3. NOTEPAD WINDOW -->
                <div id="notepadWindow" class="window window-anim hidden absolute top-28 left-48 w-[550px] h-[380px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/60 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'notepadWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('notepadWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('notepadWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('notepadWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-note-sticky mr-1.5 text-emerald-400"></i> Notepad</span>
                        </div>
                    </div>
                    <textarea class="flex-1 bg-slate-950/40 p-4 text-sm text-slate-200 resize-none border-none focus:outline-none" placeholder="Type your notes here..."></textarea>
                </div>

                <!-- 4. SETTINGS WINDOW -->
                <div id="settingsWindow" class="window window-anim hidden absolute top-16 left-64 w-[550px] h-[400px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/60 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'settingsWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('settingsWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('settingsWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('settingsWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-gear mr-1.5 text-slate-300"></i> Settings</span>
                        </div>
                    </div>
                    <div class="flex-1 p-6 space-y-6 overflow-y-auto">
                        <div>
                            <h3 class="text-sm font-semibold text-slate-300 mb-3">Change Wallpaper</h3>
                            <div class="grid grid-cols-3 gap-3">
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000&auto=format&fit=crop')" class="h-20 rounded-lg bg-cover bg-center cursor-pointer border-2 border-indigo-500" style="background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2000&auto=format&fit=crop')" class="h-20 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50" style="background-image: url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2000&auto=format&fit=crop')" class="h-20 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50" style="background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop')"></div>
                            </div>
                        </div>
                        <div class="border-t border-white/10 pt-4">
                            <h3 class="text-sm font-semibold text-slate-300 mb-2">System Information</h3>
                            <p class="text-xs text-slate-400">WebOS v2.0 • Powered by Vercel Serverless & Python Flask</p>
                        </div>
                    </div>
                </div>

                <!-- TASKBAR -->
                <div class="h-14 glass border-t border-white/10 flex items-center justify-between px-4 z-50">
                    <div class="flex items-center space-x-3">
                        <button class="w-10 h-10 bg-indigo-600 hover:bg-indigo-500 rounded-xl flex items-center justify-center text-white shadow-lg transition">
                            <i class="fa-solid fa-cubes"></i>
                        </button>
                        <div class="h-6 w-[1px] bg-white/10"></div>
                        <button onclick="openApp('browserWindow')" class="px-3 py-2 hover:bg-white/10 rounded-lg text-xs font-medium flex items-center space-x-2 transition">
                            <i class="fa-solid fa-globe text-indigo-400"></i>
                            <span class="hidden sm:inline">Browser</span>
                        </button>
                        <button onclick="openApp('filesWindow')" class="px-3 py-2 hover:bg-white/10 rounded-lg text-xs font-medium flex items-center space-x-2 transition">
                            <i class="fa-solid fa-folder-open text-amber-400"></i>
                            <span class="hidden sm:inline">Files</span>
                        </button>
                    </div>
                    <!-- System Tray / Clock -->
                    <div class="flex items-center space-x-4 text-xs text-slate-300">
                        <div class="flex items-center space-x-2"><i class="fa-solid fa-wifi text-emerald-400"></i></div>
                        <div class="flex items-center space-x-2"><i class="fa-solid fa-volume-high"></i></div>
                        <div id="clock" class="font-medium bg-white/5 px-3 py-1.5 rounded-lg border border-white/5"></div>
                    </div>
                </div>

                <!-- OS JavaScript Engine -->
                <script>
                    // Clock
                    function updateClock() {
                        const now = new Date();
                        document.getElementById('clock').innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                    }
                    setInterval(updateClock, 1000);
                    updateClock();

                    // Window Manager State
                    function openApp(id) {
                        const win = document.getElementById(id);
                        win.classList.remove('hidden');
                        bringToFront(win);
                    }

                    function closeApp(id) {
                        document.getElementById(id).classList.add('hidden');
                    }

                    function bringToFront(win) {
                        const windows = document.querySelectorAll('.window');
                        windows.forEach(w => w.style.zIndex = '10');
                        win.style.zIndex = '20';
                    }

                    // Fullscreen / Windowed Toggle
                    function toggleFullscreen(id) {
                        const win = document.getElementById(id);
                        if (win.dataset.fullscreen === "true") {
                            win.style.width = win.dataset.prevWidth || "850px";
                            win.style.height = win.dataset.prevHeight || "540px";
                            win.style.top = win.dataset.prevTop || "50px";
                            win.style.left = win.dataset.prevLeft || "50px";
                            win.dataset.fullscreen = "false";
                        } else {
                            win.dataset.prevWidth = win.style.width;
                            win.dataset.prevHeight = win.style.height;
                            win.dataset.prevTop = win.style.top;
                            win.dataset.prevLeft = win.style.left;
                            win.style.width = "100vw";
                            win.style.height = "calc(100vh - 56px)";
                            win.style.top = "0px";
                            win.style.left = "0px";
                            win.dataset.fullscreen = "true";
                        }
                    }

                    // Wallpaper Switcher
                    function setWallpaper(url) {
                        document.body.style.backgroundImage = `url('${url}')`;
                    }

                    // Browser Navigation Logic
                    function loadUrl(event) {
                        event.preventDefault();
                        const url = document.getElementById('urlInput').value;
                        const frame = document.getElementById('browserFrame');
                        frame.src = `/proxy?url=${encodeURIComponent(url)}`;
                    }

                    function loadUrlBtn() {
                        const url = document.getElementById('urlInput').value;
                        const frame = document.getElementById('browserFrame');
                        frame.src = `/proxy?url=${encodeURIComponent(url)}`;
                    }

                    function refreshBrowser() {
                        const frame = document.getElementById('browserFrame');
                        frame.contentWindow.location.reload();
                    }

                    // Draggable Windows
                    let activeWindow = null;
                    let offsetX = 0, offsetY = 0;

                    function startDrag(e, id) {
                        activeWindow = document.getElementById(id);
                        bringToFront(activeWindow);
                        offsetX = e.clientX - activeWindow.offsetLeft;
                        offsetY = e.clientY - activeWindow.offsetTop;
                        
                        document.addEventListener('mousemove', onDrag);
                        document.addEventListener('mouseup', stopDrag);
                    }

                    function onDrag(e) {
                        if (!activeWindow) return;
                        activeWindow.style.left = (e.clientX - offsetX) + 'px';
                        activeWindow.style.top = (e.clientY - offsetY) + 'px';
                    }

                    function stopDrag() {
                        activeWindow = null;
                        document.removeEventListener('mousemove', onDrag);
                        document.removeEventListener('mouseup', stopDrag);
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            return

        # Backend Proxy Handler (for fetching & rewriting target websites)
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
                    
                    for tag in soup.find_all(['a', 'img', 'link', 'script'], href=True):
                        attr = 'href' if tag.has_attr('href') else 'src'
                        if tag.has_attr(attr):
                            abs_url = urljoin(target_url, tag[attr])
                            tag[attr] = f"/?url={abs_url}"

                    for tag in soup.find_all('img', src=True):
                        abs_url = urljoin(target_url, tag['src'])
                        tag['src'] = f"/?url={abs_url}"

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
