// Register the Service Worker on startup
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js', {
                scope: '/'
            });
            await navigator.serviceWorker.ready;
            console.log('Service Worker is active and ready:', registration.scope);
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    });
}

// Clock updates
function updateClock() {
    const clockEl = document.getElementById('clock');
    if (clockEl) {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}
setInterval(updateClock, 1000);
updateClock();

// App Window Management Functions
function openApp(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.remove('hidden');
        win.style.zIndex = String(Date.now());
    }
}

function closeApp(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.add('hidden');
    }
}

function toggleFullscreen(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        if (!win.dataset.maximized) {
            win.dataset.prevStyle = win.style.cssText;
            win.style.top = '0px';
            win.style.left = '0px';
            win.style.width = '100vw';
            win.style.height = 'calc(100vh - 3.5rem)';
            win.dataset.maximized = 'true';
        } else {
            win.style.cssText = win.dataset.prevStyle;
            delete win.dataset.maximized;
        }
    }
}

// Start Menu Controls
function toggleStartMenu(event) {
    if (event) event.stopPropagation();
    const menu = document.getElementById('startMenu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

function closeStartMenu() {
    const menu = document.getElementById('startMenu');
    if (menu && !menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
    }
}

// Browser Proxy Loading Function using Vercel Rewrites
function loadUrl(event) {
    event.preventDefault();
    loadUrlBtn();
}

function loadUrlBtn() {
    const input = document.getElementById('urlInput');
    const frame = document.getElementById('browserFrame');
    if (!input || !frame) return;

    let targetUrl = input.value.trim();
    if (!targetUrl) return;

    // Handle search queries vs direct URLs
    if (!targetUrl.includes('.') && !targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = 'https://www.google.com/search?q=' + encodeURIComponent(targetUrl);
    } else if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = 'https://' + targetUrl;
    }

    // Route through the Vercel rewrite proxy path
    const proxyUrl = `/proxy/?url=${encodeURIComponent(targetUrl)}`;
    frame.src = proxyUrl;
}

// Calculator Logic
let calcExpression = "0";

function calcAppend(val) {
    if (calcExpression === "0" && val !== '.') {
        calcExpression = val;
    } else {
        calcExpression += val;
    }
    updateCalcDisplay();
}

function calcClear() {
    calcExpression = "0";
    updateCalcDisplay();
}

function calcCompute() {
    try {
        calcExpression = String(eval(calcExpression));
    } catch (e) {
        calcExpression = "Error";
    }
    updateCalcDisplay();
}

function updateCalcDisplay() {
    const display = document.getElementById('calcDisplay');
    if (display) {
        display.textContent = calcExpression;
    }
}

// Settings / Wallpaper Logic
function setWallpaper(imageUrl) {
    const desktop = document.getElementById('desktop');
    if (desktop) {
        desktop.style.backgroundImage = `url('${imageUrl}')`;
        desktop.style.backgroundSize = 'cover';
        desktop.style.backgroundPosition = 'center';
    }
}

// Files & Notepad Placeholders
function loadFiles() {
    const grid = document.getElementById('fileGrid');
    if (grid && grid.children.length === 0) {
        grid.innerHTML = '<div class="text-xs text-slate-400">No files saved yet. Click New File to create one!</div>';
    }
}

function createNewFilePrompt() {
    alert('File creation feature active.');
}

function saveCurrentNote() {
    alert('Note saved successfully!');
}

// Window Dragging Logic
let activeWindow = null;
let startX = 0, startY = 0, initialX = 0, initialY = 0;

function startDrag(event, windowId) {
    activeWindow = document.getElementById(windowId);
    if (!activeWindow) return;

    activeWindow.style.zIndex = String(Date.now());
    startX = event.clientX;
    startY = event.clientY;
    initialX = activeWindow.offsetLeft;
    initialY = activeWindow.offsetTop;

    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
}

function onDrag(event) {
    if (!activeWindow) return;
    const dx = event.clientX - startX;
    const dy = event.clientY - startY;
    activeWindow.style.left = `${initialX + dx}px`;
    activeWindow.style.top = `${initialY + dy}px`;
}

function stopDrag() {
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);
    activeWindow = null;
}
