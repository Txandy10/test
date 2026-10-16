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
        
        # Serve the WebOS Desktop Environment if no URL is requested
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
                <title>WebOS Pro Desktop</title>
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
                        background: rgba(15, 23, 42, 0.8);
                        backdrop-filter: blur(20px);
                        -webkit-backdrop-filter: blur(20px);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }
                    .glass-window {
                        background: rgba(15, 23, 42, 0.9);
                        backdrop-filter: blur(24px);
                        -webkit-backdrop-filter: blur(24px);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
                    }
                    .app-icon:hover {
                        background: rgba(255, 255, 255, 0.15);
                        transform: translateY(-3px);
                    }
                    .window-anim {
                        animation: windowOpen 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                    }
                    @keyframes windowOpen {
                        0% { opacity: 0; transform: scale(0.92) translateY(10px); }
                        100% { opacity: 1; transform: scale(1) translateY(0); }
                    }
                    ::-webkit-scrollbar { width: 6px; height: 6px; }
                    ::-webkit-scrollbar-track { background: transparent; }
                    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 3px; }
                    ::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.4); }
                </style>
            </head>
            <body class="h-screen w-screen flex flex-col justify-between text-slate-100">

                <!-- Desktop Workspace -->
                <div id="desktop" class="flex-1 p-6 grid grid-cols-2 sm:grid-cols-6 gap-6 content-start z-0" onclick="closeAllMenus()">
                    <!-- Browser -->
                    <div onclick="openApp('browserWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-indigo-500">
                            <i class="fa-solid fa-globe"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Browser</span>
                    </div>

                    <!-- Files -->
                    <div onclick="openApp('filesWindow'); loadFiles();" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-amber-400">
                            <i class="fa-solid fa-folder-open"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Files</span>
                    </div>

                    <!-- Notepad -->
                    <div onclick="openApp('notepadWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-emerald-500">
                            <i class="fa-solid fa-note-sticky"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Notepad</span>
                    </div>

                    <!-- Calculator -->
                    <div onclick="openApp('calcWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-blue-500">
                            <i class="fa-solid fa-calculator"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Calculator</span>
                    </div>

                    <!-- Terminal -->
                    <div onclick="openApp('terminalWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-slate-900 rounded-xl flex items-center justify-center text-emerald-400 text-2xl shadow-lg border border-slate-700">
                            <i class="fa-solid fa-terminal"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Terminal</span>
                    </div>

                    <!-- Settings -->
                    <div onclick="openApp('settingsWindow')" class="app-icon flex flex-col items-center justify-center w-20 h-20 rounded-2xl cursor-pointer transition-all duration-200 group">
                        <div class="w-12 h-12 bg-slate-700 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg group-hover:bg-slate-600">
                            <i class="fa-solid fa-gear"></i>
                        </div>
                        <span class="text-xs mt-2 font-medium drop-shadow-md">Settings</span>
                    </div>
                </div>

                <!-- START MENU POPUP -->
                <div id="startMenu" class="hidden absolute bottom-16 left-3 w-80 h-96 glass-window rounded-2xl shadow-2xl z-50 flex flex-col p-4 border border-white/10 animate-in fade-in zoom-in-95 duration-150">
                    <div class="flex items-center space-x-3 pb-4 border-b border-white/10">
                        <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-bold"><i class="fa-solid fa-cubes"></i></div>
                        <div>
                            <h4 class="text-sm font-semibold text-white">WebOS Pro</h4>
                            <p class="text-[10px] text-slate-400">Virtual Cloud Workstation</p>
                        </div>
                    </div>
                    <div class="flex-1 py-3 grid grid-cols-3 gap-3 overflow-y-auto">
                        <div onclick="openApp('browserWindow'); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-globe text-indigo-400 text-xl mb-1"></i>
                            <span class="text-[11px]">Browser</span>
                        </div>
                        <div onclick="openApp('filesWindow'); loadFiles(); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-folder-open text-amber-400 text-xl mb-1"></i>
                            <span class="text-[11px]">Files</span>
                        </div>
                        <div onclick="openApp('notepadWindow'); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-note-sticky text-emerald-400 text-xl mb-1"></i>
                            <span class="text-[11px]">Notepad</span>
                        </div>
                        <div onclick="openApp('calcWindow'); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-calculator text-blue-400 text-xl mb-1"></i>
                            <span class="text-[11px]">Calc</span>
                        </div>
                        <div onclick="openApp('terminalWindow'); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-terminal text-emerald-400 text-xl mb-1"></i>
                            <span class="text-[11px]">Terminal</span>
                        </div>
                        <div onclick="openApp('settingsWindow'); toggleStartMenu();" class="flex flex-col items-center justify-center p-2 rounded-xl hover:bg-white/10 cursor-pointer">
                            <i class="fa-solid fa-gear text-slate-300 text-xl mb-1"></i>
                            <span class="text-[11px]">Settings</span>
                        </div>
                    </div>
                    <div class="pt-3 border-t border-white/10 flex justify-between items-center text-xs text-slate-400">
                        <span>User Session #1</span>
                        <button onclick="location.reload()" class="hover:text-rose-400 flex items-center space-x-1"><i class="fa-solid fa-power-off"></i><span>Restart</span></button>
                    </div>
                </div>

                <!-- WINDOWS -->

                <!-- 1. BROWSER WINDOW -->
                <div id="browserWindow" class="window window-anim hidden absolute top-10 left-12 w-[900px] h-[560px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/70 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'browserWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('browserWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('browserWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('browserWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-globe mr-1.5 text-indigo-400"></i> Google / Web Proxy</span>
                        </div>
                    </div>
                    <div class="bg-slate-900/50 p-2.5 border-b border-white/10 flex items-center space-x-2">
                        <button onclick="navigateBrowser(-1)" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/15"><i class="fa-solid fa-arrow-left"></i></button>
                        <button onclick="navigateBrowser(1)" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/15"><i class="fa-solid fa-arrow-right"></i></button>
                        <button onclick="refreshBrowser()" class="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/15"><i class="fa-solid fa-rotate-right"></i></button>
                        <form onsubmit="loadUrl(event)" class="flex-1 flex">
                            <input id="urlInput" type="text" placeholder="Search Google or type URL (e.g. https://example.com)" class="w-full bg-slate-950/70 border border-white/10 rounded-lg px-4 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500">
                        </form>
                        <button onclick="loadUrlBtn()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition">Go</button>
                    </div>
                    <div class="flex-1 bg-white relative flex flex-col">
                        <iframe id="browserFrame" src="about:blank" class="w-full flex-1 border-none"></iframe>
                        <!-- Download bar simulation -->
                        <div id="downloadBar" class="hidden bg-slate-900 text-white px-4 py-2 border-t border-slate-700 flex justify-between items-center text-xs">
                            <div class="flex items-center space-x-2">
                                <i class="fa-solid fa-file-arrow-down text-indigo-400"></i>
                                <span id="downloadFileName">file.txt</span>
                            </div>
                            <div class="space-x-2">
                                <button onclick="saveToVirtualPC()" class="bg-amber-600 hover:bg-amber-500 px-3 py-1 rounded text-white font-medium">Save to Fake PC</button>
                                <button onclick="saveToRealDevice()" class="bg-indigo-600 hover:bg-indigo-500 px-3 py-1 rounded text-white font-medium">Download to Real Device</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. FILES APP WINDOW -->
                <div id="filesWindow" class="window window-anim hidden absolute top-16 left-24 w-[700px] h-[450px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/70 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'filesWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('filesWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('filesWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('filesWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-folder-open mr-1.5 text-amber-400"></i> Virtual File Manager</span>
                        </div>
                        <button onclick="createNewFilePrompt()" class="bg-amber-600 hover:bg-amber-500 text-white px-3 py-1 rounded text-xs font-medium"><i class="fa-solid fa-plus mr-1"></i> New File</button>
                    </div>
                    <div class="flex-1 p-6 grid grid-cols-4 gap-4 overflow-y-auto content-start" id="fileGrid">
                        <!-- Populated by JS -->
                    </div>
                </div>

                <!-- 3. NOTEPAD WINDOW -->
                <div id="notepadWindow" class="window window-anim hidden absolute top-20 left-36 w-[600px] h-[400px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/70 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'notepadWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('notepadWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('notepadWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('notepadWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-note-sticky mr-1.5 text-emerald-400"></i> Notepad</span>
                        </div>
                        <button onclick="saveCurrentNote()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1 rounded text-xs font-medium"><i class="fa-solid fa-save mr-1"></i> Save to PC</button>
                    </div>
                    <textarea id="notepadContent" class="flex-1 bg-slate-950/60 p-4 text-sm text-slate-200 resize-none border-none focus:outline-none font-mono" placeholder="Type your notes here..."></textarea>
                </div>

                <!-- 4. CALCULATOR WINDOW -->
                <div id="calcWindow" class="window window-anim hidden absolute top-24 left-44 w-[320px] h-[420px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/70 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'calcWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('calcWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-calculator mr-1.5 text-blue-400"></i> Calculator</span>
                        </div>
                    </div>
                    <div class="p-4 flex flex-col flex-1 bg-slate-950/40">
                        <div id="calcDisplay" class="bg-slate-900 text-right text-3xl font-bold p-4 rounded-xl mb-4 text-white tracking-wider border border-white/5">0</div>
                        <div class="grid grid-cols-4 gap-2 flex-1">
                            <button onclick="calcClear()" class="bg-rose-600/80 hover:bg-rose-600 rounded-lg text-white font-bold">C</button>
                            <button onclick="calcAppend('/')" class="bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold">/</button>
                            <button onclick="calcAppend('*')" class="bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold">×</button>
                            <button onclick="calcAppend('-')" class="bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold">-</button>
                            <button onclick="calcAppend('7')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">7</button>
                            <button onclick="calcAppend('8')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">8</button>
                            <button onclick="calcAppend('9')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">9</button>
                            <button onclick="calcAppend('+')" class="bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold row-span-2">+</button>
                            <button onclick="calcAppend('4')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">4</button>
                            <button onclick="calcAppend('5')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">5</button>
                            <button onclick="calcAppend('6')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">6</button>
                            <button onclick="calcAppend('1')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">1</button>
                            <button onclick="calcAppend('2')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">2</button>
                            <button onclick="calcAppend('3')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">3</button>
                            <button onclick="calcCompute()" class="bg-blue-600 hover:bg-blue-500 rounded-lg text-white font-bold row-span-2">=</button>
                            <button onclick="calcAppend('0')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold col-span-2">0</button>
                            <button onclick="calcAppend('.')" class="bg-slate-700/60 hover:bg-slate-700 rounded-lg text-white font-bold">.</button>
                        </div>
                    </div>
                </div>

                <!-- 5. TERMINAL WINDOW -->
                <div id="terminalWindow" class="window window-anim hidden absolute top-28 left-52 w-[650px] h-[380px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10 bg-slate-950">
                    <div class="h-11 bg-slate-900 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'terminalWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('terminalWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('terminalWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('terminalWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-terminal mr-1.5 text-emerald-400"></i> bash - webos@cloud</span>
                        </div>
                    </div>
                    <div id="terminalBody" class="flex-1 p-4 font-mono text-xs text-emerald-400 overflow-y-auto space-y-1">
                        <div>WebOS Cloud Terminal v3.0 [Linux Kernel 6.2.0-proxy]</div>
                        <div>Type 'help' for available commands.</div>
                        <br>
                    </div>
                    <div class="p-2 bg-slate-900 border-t border-white/10 flex items-center">
                        <span class="text-emerald-400 font-mono text-xs mr-2">webos@cloud:~$</span>
                        <input id="termInput" type="text" onkeydown="handleTerminal(event)" class="flex-1 bg-transparent border-none text-xs text-white font-mono focus:outline-none">
                    </div>
                </div>

                <!-- 6. SETTINGS WINDOW -->
                <div id="settingsWindow" class="window window-anim hidden absolute top-12 left-60 w-[600px] h-[440px] glass-window rounded-xl flex flex-col overflow-hidden shadow-2xl z-10">
                    <div class="h-11 bg-slate-900/70 border-b border-white/10 flex items-center justify-between px-4 select-none cursor-move" onmousedown="startDrag(event, 'settingsWindow')">
                        <div class="flex items-center space-x-2">
                            <div onclick="closeApp('settingsWindow')" class="w-3 h-3 rounded-full bg-rose-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleMinimize('settingsWindow')" class="w-3 h-3 rounded-full bg-amber-500 hover:opacity-80 cursor-pointer"></div>
                            <div onclick="toggleFullscreen('settingsWindow')" class="w-3 h-3 rounded-full bg-emerald-500 hover:opacity-80 cursor-pointer"></div>
                            <span class="text-xs font-semibold text-slate-300 ml-2"><i class="fa-solid fa-gear mr-1.5 text-slate-300"></i> Control Panel & Settings</span>
                        </div>
                    </div>
                    <div class="flex-1 p-6 space-y-6 overflow-y-auto">
                        <div>
                            <h3 class="text-sm font-semibold text-slate-200 mb-3"><i class="fa-solid fa-image mr-2 text-indigo-400"></i>Select Base Wallpaper</h3>
                            <div class="grid grid-cols-3 gap-3">
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-indigo-500 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=600&auto=format&fit=crop')"></div>
                                <div onclick="setWallpaper('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2000&auto=format&fit=crop')" class="h-24 rounded-lg bg-cover bg-center cursor-pointer border-2 border-transparent hover:border-white/50 shadow-md hover:scale-105 transition" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop')"></div>
                            </div>
                        </div>
                        <div class="border-t border-white/10 pt-4 flex justify-between items-center">
                            <div>
                                <h3 class="text-sm font-semibold text-slate-200">System Storage</h3>
                                <p class="text-xs text-slate-400">Virtual NVMe Drive (LocalStorage)</p>
                            </div>
                            <button onclick="clearVirtualStorage()" class="bg-rose-600/80 hover:bg-rose-600 text-white px-3 py-1.5 rounded-lg text-xs font-medium">Reset Virtual PC</button>
                        </div>
                    </div>
                </div>

                <!-- TASKBAR -->
                <div class="h-14 glass border-t border-white/10 flex items-center justify-between px-4 z-50">
                    <div class="flex items-center space-x-3">
                        <button onclick="toggleStartMenu(event)" class="w-10 h-10 bg-indigo-600 hover:bg-indigo-500 rounded-xl flex items-center justify-center text-white shadow-lg transition active:scale-95">
                            <i class="fa-solid fa-cubes text-lg"></i>
                        </button>
                        <div class="h-6 w-[1px] bg-white/10"></div>
                        <button onclick="openApp('browserWindow')" class="px-3 py-2 hover:bg-white/10 rounded-lg text-xs font-medium flex items-center space-x-2 transition">
                            <i class="fa-solid fa-globe text-indigo-400 text-sm"></i>
                            <span class="hidden sm:inline">Browser</span>
                        </button>
                        <button onclick="openApp('filesWindow'); loadFiles();" class="px-3 py-2 hover:bg-white/10 rounded-lg text-xs font-medium flex items-center space-x-2 transition">
                            <i class="fa-solid fa-folder-open text-amber-400 text-sm"></i>
                            <span class="hidden sm:inline">Files</span>
                        </button>
                        <button onclick="openApp('notepadWindow')" class="px-3 py-2 hover:bg-white/10 rounded-lg text-xs font-medium flex items-center space-x-2 transition">
                            <i class="fa-solid fa-note-sticky text-emerald-400 text-sm"></i>
                            <span class="hidden sm:inline">Notepad</span>
                        </button>
                    </div>
                    <!-- System Tray / Clock -->
                    <div class="flex items-center space-x-4 text-xs text-slate-300">
                        <div class="flex items-center space-x-2"><i class="fa-solid fa-wifi text-emerald-400"></i></div>
                        <div class="flex items-center space-x-2"><i class="fa-solid fa-shield-halved text-indigo-400"></i></div>
                        <div id="clock" class="font-medium bg-white/5 px-3 py-1.5 rounded-lg border border-white/5"></div>
                    </div>
                </div>

                <!-- JAVASCRIPT OS ENGINE -->
                <script>
                    // Clock
                    function updateClock() {
                        const now = new Date();
                        document.getElementById('clock').innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                    }
                    setInterval(updateClock, 1000);
                    updateClock();

                    // Start Menu
                    function toggleStartMenu(e) {
                        if(e) e.stopPropagation();
                        const menu = document.getElementById('startMenu');
                        menu.classList.toggle('hidden');
                    }

                    function closeAllMenus() {
                        document.getElementById('startMenu').classList.add('hidden');
                    }

                    // Window Management
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
                        localStorage.setItem('webos_wallpaper', url);
                    }
                    const savedWp = localStorage.getItem('webos_wallpaper');
                    if(savedWp) setWallpaper(savedWp);

                    // Virtual File System (VFS)
                    function getFiles() {
                        const defaultFiles = [
                            { name: "welcome.txt", content: "Welcome to WebOS Pro! You can create, edit, and save files directly to your virtual PC." },
                            { name: "todo.list", content: "- Build proxy\n- Test web apps\n- Deploy to Vercel" }
                        ];
                        const stored = localStorage.getItem('webos_vfs');
                        return stored ? JSON.parse(stored) : defaultFiles;
                    }

                    function saveFiles(files) {
                        localStorage.setItem('webos_vfs', JSON.stringify(files));
                    }

                    function loadFiles() {
                        const grid = document.getElementById('fileGrid');
                        const files = getFiles();
                        grid.innerHTML = '';
                        files.forEach((f, idx) => {
                            grid.innerHTML += `
                                <div onclick="openFile('${f.name}')" class="p-4 bg-white/5 hover:bg-white/10 rounded-xl flex flex-col items-center justify-center cursor-pointer border border-white/5 group relative">
                                    <i class="fa-solid fa-file-lines text-emerald-400 text-3xl mb-2 group-hover:scale-110 transition"></i>
                                    <span class="text-xs font-medium text-center truncate w-full">${f.name}</span>
                                    <button onclick="event.stopPropagation(); deleteFile(${idx})" class="absolute top-2 right-2 text-rose-400 hover:text-rose-300 opacity-0 group-hover:opacity-100 transition"><i class="fa-solid fa-trash text-xs"></i></button>
                                </div>
                            `;
                        });
                    }

                    function createNewFilePrompt() {
                        const name = prompt("Enter file name (e.g. notes.txt):");
                        if(!name) return;
                        const files = getFiles();
                        files.push({ name: name, content: "" });
                        saveFiles(files);
                        loadFiles();
                    }

                    function openFile(name) {
                        const files = getFiles();
                        const file = files.find(f => f.name === name);
                        if(file) {
                            openApp('notepadWindow');
                            document.getElementById('notepadContent').value = file.content;
                            document.getElementById('notepadContent').dataset.currentFile = name;
                        }
                    }

                    function deleteFile(idx) {
                        const files = getFiles();
                        files.splice(idx, 1);
                        saveFiles(files);
                        loadFiles();
                    }

                    function saveCurrentNote() {
                        const content = document.getElementById('notepadContent').value;
                        const filename = document.getElementById('notepadContent').dataset.currentFile || "untitled.txt";
                        const files = getFiles();
                        const existing = files.find(f => f.name === filename);
                        if(existing) {
                            existing.content = content;
                        } else {
                            files.push({ name: filename, content: content });
                        }
                        saveFiles(files);
                        alert("File saved successfully to Virtual PC!");
                        loadFiles();
                    }

                    function clearVirtualStorage() {
                        if(confirm("Are you sure you want to reset your Virtual PC storage?")) {
                            localStorage.removeItem('webos_vfs');
                            loadFiles();
                            alert("Virtual PC reset.");
                        }
                    }

                    // Calculator Logic
                    let calcValue = "";
                    function calcAppend(val) {
                        calcValue += val;
                        document.getElementById('calcDisplay').innerText = calcValue || "0";
                    }
                    function calcClear() {
                        calcValue = "";
                        document.getElementById('calcDisplay').innerText = "0";
                    }
                    function calcCompute() {
                        try {
                            calcValue = eval(calcValue).toString();
                            document.getElementById('calcDisplay').innerText = calcValue;
                        } catch(e) {
                            document.getElementById('calcDisplay').innerText = "Error";
                            calcValue = "";
                        }
                    }

                    // Terminal Logic
                    function handleTerminal(e) {
                        if(e.key === 'Enter') {
                            const input = document.getElementById('termInput');
                            const val = input.value.trim();
                            const body = document.getElementById('terminalBody');
                            body.innerHTML += `<div>webos@cloud:~$ ${val}</div>`;
                            
                            if(val === 'help') {
                                body.innerHTML += `<div>Available commands: clear, date, ls, whoami, echo [text], reboot</div>`;
                            } else if(val === 'clear') {
                                body.innerHTML = '';
                            } else if(val === 'date') {
                                body.innerHTML += `<div>${new Date()}</div>`;
                            } else if(val === 'ls') {
                                const files = getFiles();
                                body.innerHTML += `<div>${files.map(f => f.name).join('   ')}</div>`;
                            } else if(val === 'whoami') {
                                body.innerHTML += `<div>webos-user-admin</div>`;
                            } else if(val.startsWith('echo ')) {
                                body.innerHTML += `<div>${val.substring(5)}</div>`;
                            } else if(val === 'reboot') {
                                location.reload();
                            } else if(val !== '') {
                                body.innerHTML += `<div>bash: ${val}: command not found</div>`;
                            }
                            
                            input.value = '';
                            body.scrollTop = body.scrollHeight;
                        }
                    }

                    // Browser Navigation & Download simulation
                    let currentTargetUrl = "";
                    function loadUrl(event) {
                        event.preventDefault();
                        const url = document.getElementById('urlInput').value;
                        currentTargetUrl = url;
                        const frame = document.getElementById('browserFrame');
                        frame.src = `/proxy?url=${encodeURIComponent(url)}`;
                    }

                    function loadUrlBtn() {
                        const url = document.getElementById('urlInput').value;
                        currentTargetUrl = url;
                        const frame = document.getElementById('browserFrame');
                        frame.src = `/proxy?url=${encodeURIComponent(url)}`;
                    }

                    function refreshBrowser() {
                        const frame = document.getElementById('browserFrame');
                        frame.contentWindow.location.reload();
                    }

                    function saveToVirtualPC() {
                        const files = getFiles();
                        const fileName = currentTargetUrl.split('/').pop() || "downloaded_page.html";
                        files.push({ name: fileName, content: "Proxied URL: " + currentTargetUrl });
                        saveFiles(files);
                        alert("Saved '" + fileName + "' to Virtual PC files!");
                        document.getElementById('downloadBar').classList.add('hidden');
                        loadFiles();
                    }

                    function saveToRealDevice() {
                        const blob = new Blob(["Proxied content from: " + currentTargetUrl], { type: "text/plain" });
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = currentTargetUrl.split('/').pop() || "download.txt";
                        link.click();
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

        # Proxy Backend Handler
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
