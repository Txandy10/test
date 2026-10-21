// Register Ultraviolet Service Worker on startup
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            await navigator.serviceWorker.register('/sw.js', { scope: '/' });
            await navigator.serviceWorker.ready;
            console.log('UV Service Worker active & ready.');
        } catch (error) {
            console.error('Service Worker registration failed:', error);
        }
    });
}

// Clock & Date updates
function updateClock() {
    const now = new Date();
    const timeEl = document.getElementById('taskbarTime');
    const dateEl = document.getElementById('taskbarDate');
    if (timeEl) timeEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    if (dateEl) dateEl.textContent = now.toLocaleDateString();
}
setInterval(updateClock, 1000);
updateClock();

// Window & Taskbar Management
let activeZIndex = 10;

function openApp(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.remove('hidden');
        activeZIndex++;
        win.style.zIndex = String(activeZIndex);
        updateTaskbarIndicator(windowId, true);
    }
}

function closeApp(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.add('hidden');
        updateTaskbarIndicator(windowId, false);
    }
}

function minimizeApp(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.add('hidden');
    }
}

function toggleAppWindow(windowId) {
    const win = document.getElementById(windowId);
    if (!win) return;
    if (win.classList.contains('hidden')) {
        openApp(windowId);
    } else {
        minimizeApp(windowId);
    }
}

function toggleMaximize(windowId) {
    const win = document.getElementById(windowId);
    if (!win) return;
    if (!win.dataset.maximized) {
        win.dataset.prevStyle = win.style.cssText;
        win.style.top = '0px';
        win.style.left = '0px';
        win.style.width = '100vw';
        win.style.height = 'calc(100vh - 48px)';
        win.style.borderRadius = '0px';
        win.dataset.maximized = 'true';
    } else {
        win.style.cssText = win.dataset.prevStyle;
        delete win.dataset.maximized;
    }
}

function updateTaskbarIndicator(windowId, isActive) {
    const icon = document.getElementById(`tb-${windowId}`);
    if (icon) {
        if (isActive) icon.classList.add('active');
        else icon.classList.remove('active');
    }
}

// Start Menu Controls
function toggleStartMenu(event) {
    if (event) event.stopPropagation();
    const menu = document.getElementById('startMenu');
    if (menu) {
        menu.classList.toggle('show');
    }
}

function closeStartMenu() {
    const menu = document.getElementById('startMenu');
    if (menu && menu.classList.contains('show')) {
        menu.classList.remove('show');
    }
}

// Browser URL Loader (Using Vercel Rewrite Proxy)
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

    if (!targetUrl.includes('.') && !targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = 'https://www.google.com/search?q=' + encodeURIComponent(targetUrl);
    } else if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
        targetUrl = 'https://' + targetUrl;
    }

    const proxyUrl = `/proxy/?url=${encodeURIComponent(targetUrl)}`;
    frame.src = proxyUrl;
}

// File Explorer & Storage
function loadFiles() {
    const grid = document.getElementById('fileGrid');
    if (!grid) return;
    
    let files = JSON.parse(localStorage.getItem('webos_files') || 'null');
    if (!files) {
        files = [
            { name: 'Welcome.txt', content: 'Welcome to WebOS Pro Windows 11 Edition!\n\nAll apps are fully operational.' },
            { name: 'Notes.txt', content: 'Tip: Use the Terminal app to run commands like matrix, help, and calc.' }
        ];
        localStorage.setItem('webos_files', JSON.stringify(files));
    }

    grid.innerHTML = '';
    files.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'flex flex-col items-center p-3 hover:bg-white/10 rounded-xl cursor-pointer group';
        item.innerHTML = `
            <i class="fa-solid fa-file-lines text-amber-400 text-3xl mb-2"></i>
            <span class="text-xs text-white text-center truncate w-full">${file.name}</span>
        `;
        item.onclick = () => {
            openApp('notepadWindow');
            document.getElementById('notepadContent').value = file.content;
        };
        grid.appendChild(item);
    });
}

function createNewFilePrompt() {
    const name = prompt('Enter file name (e.g. myfile.txt):');
    if (!name) return;
    let files = JSON.parse(localStorage.getItem('webos_files') || '[]');
    files.push({ name: name, content: '' });
    localStorage.setItem('webos_files', JSON.stringify(files));
    loadFiles();
}

function saveCurrentNote() {
    const content = document.getElementById('notepadContent').value;
    let files = JSON.parse(localStorage.getItem('webos_files') || '[]');
    if (files.length > 0) {
        files[0].content = content;
        localStorage.setItem('webos_files', JSON.stringify(files));
    }
    const status = document.getElementById('noteStatus');
    if (status) {
        status.textContent = 'Saved successfully!';
        setTimeout(() => status.textContent = 'Saved', 2000);
    }
}

function downloadNote() {
    const content = document.getElementById('notepadContent').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'document.txt';
    a.click();
}

// Calculator Logic
let calcExpression = "0";

function calcAppend(val) {
    if (calcExpression === "0" && val !== '.') calcExpression = val;
    else calcExpression += val;
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
    if (display) display.textContent = calcExpression;
}

// Terminal / CMD Simulation
function handleTerminal(event) {
    if (event.key === 'Enter') {
        const input = document.getElementById('termInput');
        const output = document.getElementById('termOutput');
        const cmd = input.value.trim();
        if (!cmd) return;

        const line = document.createElement('div');
        line.innerHTML = `<span class="text-green-500">C:\\WebOS></span> ${escapeHtml(cmd)}`;
        output.appendChild(line);

        const response = document.createElement('div');
        response.className = 'text-slate-300 mb-1';

        const lower = cmd.toLowerCase();
        if (lower === 'help') {
            response.innerHTML = 'Available commands: <br>- <b>dir</b>: List virtual files<br>- <b>cls</b>: Clear screen<br>- <b>date</b>: Show current date<br>- <b>time</b>: Show current time<br>- <b>matrix</b>: Hacker animation<br>- <b>calc</b>: Open calculator<br>- <b>ver</b>: Windows version';
        } else if (lower === 'dir') {
            response.innerHTML = 'Directory of C:\\WebOS\\Documents<br><br>Welcome.txt<br>Notes.txt';
        } else if (lower === 'cls') {
            output.innerHTML = '';
            input.value = '';
            return;
        } else if (lower === 'date') {
            response.textContent = new Date().toDateString();
        } else if (lower === 'time') {
            response.textContent = new Date().toLocaleTimeString();
        } else if (lower === 'ver') {
            response.textContent = 'Microsoft Windows [Version 11.2600.888]';
        } else if (lower === 'calc') {
            openApp('calcWindow');
            response.textContent = 'Opening Calculator...';
        } else if (lower === 'matrix') {
            response.innerHTML = '<span class="text-green-400 font-mono">01010100 01110010 01100001 01101110 01110011 01101101 01101001 01110011 01110011 01101001 01101111 01101110 00100000 01010011 01110101 01100011 01100011 01100101 01110011 01110011</span>';
        } else {
            response.textContent = `'${cmd}' is not recognized as an internal or external command. Type 'help'.`;
        }

        output.appendChild(response);
        input.value = '';
        const body = document.getElementById('termBody');
        body.scrollTop = body.scrollHeight;
    }
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Retro Snake Game
let snakeInterval = null;
function initSnake() {
    const canvas = document.getElementById('snakeCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    let snake = [{x: 160, y: 160}, {x: 140, y: 160}, {x: 120, y: 160}];
    let food = {x: 200, y: 200};
    let dx = 20, dy = 0;
    let score = 0;
    let changingDirection = false;

    if (snakeInterval) clearInterval(snakeInterval);

    function main() {
        if (hasGameEnded()) {
            clearInterval(snakeInterval);
            alert('Game Over! Score: ' + score);
            return;
        }
        changingDirection = false;
        clearCanvas();
        drawFood();
        moveSnake();
        drawSnake();
    }

    function clearCanvas() {
        ctx.fillStyle = "#121212";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function drawSnake() {
        snake.forEach(part => {
            ctx.fillStyle = "#60cdff";
            ctx.strokeStyle = "#000";
            ctx.fillRect(part.x, part.y, 20, 20);
            ctx.strokeRect(part.x, part.y, 20, 20);
        });
    }

    function moveSnake() {
        const head = {x: snake[0].x + dx, y: snake[0].y + dy};
        snake.unshift(head);
        const hasEatenFood = snake[0].x === food.x && snake[0].y === food.y;
        if (hasEatenFood) {
            score += 10;
            document.getElementById('snakeScore').textContent = score;
            generateFood();
        } else {
            snake.pop();
        }
    }

    function randomGrid(min, max) {
        return Math.round((Math.random() * (max - min) + min) / 20) * 20;
    }

    function generateFood() {
        food.x = randomGrid(0, canvas.width - 20);
        food.y = randomGrid(0, canvas.height - 20);
        snake.forEach(part => {
            if (part.x === food.x && part.y === food.y) generateFood();
        });
    }

    function drawFood() {
        ctx.fillStyle = "#e81123";
        ctx.fillRect(food.x, food.y, 20, 20);
    }

    function hasGameEnded() {
        for (let i = 4; i < snake.length; i++) {
            if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) return true;
        }
        return snake[0].x < 0 || snake[0].x >= canvas.width || snake[0].y < 0 || snake[0].y >= canvas.height;
    }

    document.addEventListener('keydown', changeDirection);
    function changeDirection(event) {
        const keyPressed = event.keyCode;
        const LEFT = 37, UP = 38, RIGHT = 39, DOWN = 40;
        if (changingDirection) return;
        if (keyPressed === LEFT && dx === 0) { dx = -20; dy = 0; changingDirection = true; }
        if (keyPressed === UP && dy === 0) { dx = 0; dy = -20; changingDirection = true; }
        if (keyPressed === RIGHT && dx === 0) { dx = 20; dy = 0; changingDirection = true; }
        if (keyPressed === DOWN && dy === 0) { dx = 0; dy = 20; changingDirection = true; }
    }

    generateFood();
    snakeInterval = setInterval(main, 100);
}

// Wallpaper Settings
function setWallpaper(imageUrl) {
    document.body.style.backgroundImage = `url('${imageUrl}')`;
}

// Window Dragging Engine
let activeWindow = null;
let startX = 0, startY = 0, initialX = 0, initialY = 0;

function startDrag(event, windowId) {
    activeWindow = document.getElementById(windowId);
    if (!activeWindow) return;

    activeZIndex++;
    activeWindow.style.zIndex = String(activeZIndex);
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
