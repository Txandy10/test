// sw.js - Client-side Proxy Service Worker

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Check if the request is targeting our client-side proxy path
  if (url.pathname.startsWith('/proxy/')) {
    // Extract the target URL from query parameters
    const targetUrl = url.searchParams.get('url');

    if (targetUrl) {
      event.respondWith(
        fetch(targetUrl, {
          method: event.request.method,
          headers: event.request.headers,
          body: ['GET', 'HEAD'].includes(event.request.method) ? undefined : event.request.body,
          redirect: 'follow'
        }).catch((error) => {
          console.error('Proxy fetch failed:', error);
          return new Response('Proxy Error: Unable to load target site due to network restrictions or CORS.', {
            status: 500,
            headers: { 'Content-Type': 'text/plain' }
          });
        })
      );
    }
  }
});
