// desktop.js - WebOS Frontend and Proxy Window Manager

// Register the Service Worker on startup
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('WebOS Proxy Service Worker active:', registration.scope);
      })
      .catch((error) => {
        console.error('Service Worker registration failed:', error);
      });
  });
}

/**
 * Opens a new window on the WebOS desktop containing a proxied iframe.
 * @param {string} targetUrl - The external URL or game link to load.
 */
function openWebOSBrowser(targetUrl) {
  // Prevent empty inputs
  if (!targetUrl) return;

  // Format URL if user forgot https://
  if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
    targetUrl = 'https://' + targetUrl;
  }

  // Create the desktop window container
  const windowEl = document.createElement('div');
  windowEl.className = 'os-window';
  windowEl.style.cssText = `
    position: absolute;
    top: 50px;
    left: 50px;
    width: 800px;
    height: 500px;
    background: #1e1e1e;
    border: 1px solid #444;
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    z-index: 1000;
  `;

  // Construct window header with controls
  const headerEl = document.createElement('div');
  headerEl.className = 'window-header';
  headerEl.style.cssText = `
    background: #2d2d2d;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #fff;
    font-family: sans-serif;
    font-size: 14px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    cursor: move;
  `;
  headerEl.innerHTML = `
    <span class="window-title">Browser: ${targetUrl}</span>
    <div class="window-controls">
      <button class="close-btn" style="background: #ff5f56; border: none; width: 12px; height: 12px; border-radius: 50%; cursor: pointer;"></button>
    </div>
  `;

  // Construct window body containing the iframe pointing to our proxy route
  const bodyEl = document.createElement('div');
  bodyEl.className = 'window-body';
  bodyEl.style.cssText = `
    flex: 1;
    background: #fff;
    overflow: hidden;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
  `;

  // Route through the client-side proxy path handled by sw.js
  const proxiedSrc = `/proxy/?url=${encodeURIComponent(targetUrl)}`;
  bodyEl.innerHTML = `<iframe src="${proxiedSrc}" style="width: 100%; height: 100%; border: none;"></iframe>`;

  // Assemble window
  windowEl.appendChild(headerEl);
  windowEl.appendChild(bodyEl);
  document.body.appendChild(windowEl);

  // Close button functionality
  headerEl.querySelector('.close-btn').addEventListener('click', () => {
    windowEl.remove();
  });

  // Basic drag-and-drop window movement logic
  let isDragging = false;
  let offsetX, offsetY;

  headerEl.addEventListener('mousedown', (e) => {
    isDragging = true;
    offsetX = e.clientX - windowEl.offsetLeft;
    offsetY = e.clientY - windowEl.offsetTop;
    windowEl.style.zIndex = String(Date.now()); // Bring to front
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    windowEl.style.left = `${e.clientX - offsetX}px`;
    windowEl.style.top = `${e.clientY - offsetY}px`;
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
  });
}

// Hook up event listeners when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const launchButton = document.getElementById('launch-url-btn');
  const urlInput = document.getElementById('desktop-url-input');

  if (launchButton && urlInput) {
    launchButton.addEventListener('click', () => {
      openWebOSBrowser(urlInput.value);
    });

    urlInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        openWebOSBrowser(urlInput.value);
      }
    });
  }
});
