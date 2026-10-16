// Clock
function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
setInterval(updateClock, 1000);
updateClock();

// Start Menu
function toggleStartMenu(e) {
    if (e) e.stopPropagation();
    document.getElementById('startMenu').classList.toggle('hidden');
}

function closeStartMenu() {
    document.getElementById('startMenu').classList.add('hidden');
}

// Window Management
function openApp(id) {
    const win = document.getElementById(id);
    if (win) {
        win.classList.remove('hidden');
        bringToFront(win);
    }
}

function closeApp(id) {
    const win = document.getElementById(id);
    if (win) win.classList.add('hidden');
}

function bringToFront(win) {
    document.querySelectorAll('.window').forEach(w => w.style.zIndex = '10');
    win.style.zIndex = '20';
}

function toggleFullscreen(id) {
    const win = document.getElementById(id);
    if (!win) return;
    if (win.dataset.fullscreen === "true") {
        win.style.width = win.dataset.prevWidth || "850px";
        win.style.height = win.dataset.prevHeight || "520px";
        win.style.top = "50px";
        win.style.left = "50px";
        win.dataset.fullscreen = "false";
    } else {
        win.dataset.prevWidth = win.style.width;
        win.dataset.prevHeight = win.style.height;
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

// Virtual File System (LocalStorage)
function getFiles() {
    const saved = localStorage.getItem('webos_files');
    return saved ? JSON.parse(saved) : [{ name: 'welcome.txt', content: 'Hello from WebOS Pro! You can create and edit notes here.' }];
}

function loadFiles() {
    const grid = document.getElementById('fileGrid');
    if (!grid) return;
    const files = getFiles();
    grid.innerHTML = '';
    files.forEach((f) => {
        grid.innerHTML += `
            <div onclick="openFile('${f.name}')" class="p-3 bg-white/5 hover:bg-white/10 rounded-xl flex flex-col items-center cursor-pointer transition">
                <i class="fa-solid fa-file-lines text-emerald-400 text-2xl mb-1"></i>
                <span class="text-xs truncate w-full text-center">${f.name}</span>
            </div>
        `;
    });
}

function createNewFilePrompt() {
    const name = prompt("Enter file name (e.g. notes.txt):");
    if (!name) return;
    const files = getFiles();
    files.push({ name, content: "" });
    localStorage.setItem('webos_files', JSON.stringify(files));
    loadFiles();
}

function openFile(name) {
    const file = getFiles().find(f => f.name === name);
    if (file) {
        openApp('notepadWindow');
        document.getElementById('notepadContent').value = file.content;
        document.getElementById('notepadContent').dataset.currentFile = name;
    }
}

function saveCurrentNote() {
    const name = document.getElementById('notepadContent').dataset.currentFile || "untitled.txt";
    const content = document.getElementById('notepadContent').value;
    const files = getFiles();
    const existing = files.find(f => f.name === name);
    if (existing) existing.content = content;
    else files.push({ name, content });
    localStorage.setItem('webos_files', JSON.stringify(files));
    alert("File saved successfully to Virtual PC!");
    loadFiles();
}

// Calculator App Logic
let calcVal = "";
function calcAppend(v) { 
    calcVal += v; 
    document.getElementById('calcDisplay').innerText = calcVal || "0"; 
}
function calcClear() { 
    calcVal = ""; 
    document.getElementById('calcDisplay').innerText = "0"; 
}
function calcCompute() { 
    try { 
        calcVal = eval(calcVal).toString(); 
        document.getElementById('calcDisplay').innerText = calcVal; 
    } catch(e) { 
        document.getElementById('calcDisplay').innerText = "Error";
        calcVal = ""; 
    } 
}

// Smart URL & Google Search Fallback Helper
function getTargetUrl(input) {
    input = input.trim();
    const isUrl = /^(https?:\/\/)?([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/.*)?$/.test(input);
    
    if (isUrl || input.startsWith('http://') || input.startsWith('https://')) {
        if (!input.startsWith('http://') && !input.startsWith('https://')) {
            return 'https://' + input;
        }
        return input;
    } else {
        // If not a valid URL format, open Google search for the typed text
        return `https://www.google.com/search?q=${encodeURIComponent(input)}`;
    }
}

// Browser Proxy Routing & Navigation
function loadUrl(e) {
    e.preventDefault();
    const rawInput = document.getElementById('urlInput').value;
    const finalUrl = getTargetUrl(rawInput);
    document.getElementById('browserFrame').src = `/api/proxy?url=${encodeURIComponent(finalUrl)}`;
}

function loadUrlBtn() {
    const rawInput = document.getElementById('urlInput').value;
    const finalUrl = getTargetUrl(rawInput);
    document.getElementById('browserFrame').src = `/api/proxy?url=${encodeURIComponent(finalUrl)}`;
}

// Window Dragging Mechanics
let activeWin = null, offX = 0, offY = 0;
function startDrag(e, id) {
    activeWin = document.getElementById(id);
    bringToFront(activeWin);
    offX = e.clientX - activeWin.offsetLeft;
    offY = e.clientY - activeWin.offsetTop;
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
}

function onDrag(e) { 
    if (activeWin) { 
        activeWin.style.left = (e.clientX - offX) + 'px'; 
        activeWin.style.top = (e.clientY - offY) + 'px'; 
    } 
}

function stopDrag() { 
    activeWin = null; 
    document.removeEventListener('mousemove', onDrag); 
    document.removeEventListener('mouseup', stopDrag); 
}
