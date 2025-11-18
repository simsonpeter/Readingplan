// Service Worker for Offline Support with Auto-Update
const CACHE_NAME = 'njc-bible-v2';
const RUNTIME_CACHE = 'njc-bible-runtime-v2';
const VERSION_MANIFEST = './app-version.json';

// Content files that should use Network-First strategy (auto-update when online)
const CONTENT_FILES = [
  './plan/njcplan.json',
  './bibles/tamilbible.json',
  './bibles/tamilromanizedbible.json',
  './bibles/englishbible.json',
  './bibles/dutchbible.json',
  './dictionary/TSVPA1975.dictionary.SQLite3',
  './dictionary/easton_dictionary.SQLite3',
  './dictionary/robinson_morphological.SQLite3',
  './app-version.json'
];

// Static files to cache immediately on install (Cache-First strategy)
const STATIC_CACHE_FILES = [
  './',
  './index.html',
  './manifest.json',
  'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js',
  'https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.wasm'
];

// Also cache content files initially for offline support
const INITIAL_CONTENT_CACHE = [
  ...CONTENT_FILES
];

// Install event - cache static files and initial content
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    Promise.all([
      // Cache static files
      caches.open(CACHE_NAME).then((cache) => {
        console.log('[Service Worker] Caching static files');
        return cache.addAll(STATIC_CACHE_FILES.map(url => new Request(url, { credentials: 'same-origin' })));
      }),
      // Cache content files for offline support
      caches.open(RUNTIME_CACHE).then((cache) => {
        console.log('[Service Worker] Caching initial content files');
        return cache.addAll(INITIAL_CONTENT_CACHE.map(url => new Request(url, { credentials: 'same-origin' })));
      })
    ]).catch((err) => {
      console.error('[Service Worker] Cache install failed:', err);
    })
  );
  self.skipWaiting(); // Activate immediately
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim(); // Take control of all pages immediately
});

// Check if URL is a content file
function isContentFile(url) {
  try {
    const urlObj = new URL(url);
    const pathname = urlObj.pathname;
    
    // Check if it's a devotion file (Network-First strategy)
    if (pathname.includes('/devotions/') && pathname.endsWith('.txt')) {
      return true;
    }
    
    return CONTENT_FILES.some(contentFile => {
      // Remove leading './' from content file path
      const cleanPath = contentFile.replace(/^\.\//, '');
      // Check if URL pathname ends with or contains the content file path
      return pathname.includes(cleanPath) || pathname.endsWith(cleanPath);
    });
  } catch (e) {
    // Fallback: simple string matching
    if (url.includes('/devotions/') && url.endsWith('.txt')) {
      return true;
    }
    return CONTENT_FILES.some(contentFile => {
      const cleanPath = contentFile.replace(/^\.\//, '');
      return url.includes(cleanPath);
    });
  }
}

// Fetch event - Network-First for content, Cache-First for static
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension and other non-http(s) requests
  if (!event.request.url.startsWith('http')) {
    return;
  }

  const requestUrl = event.request.url;
  const isContent = isContentFile(requestUrl);

  if (isContent) {
    // NETWORK-FIRST strategy for content files (auto-updates when online)
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          // If network request succeeds, update cache and return response
          if (networkResponse && networkResponse.status === 200) {
            const responseToCache = networkResponse.clone();
            caches.open(RUNTIME_CACHE).then((cache) => {
              console.log('[Service Worker] Updating cache from network:', requestUrl);
              cache.put(event.request, responseToCache);
            });
            return networkResponse;
          }
          // If network fails, try cache
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
              console.log('[Service Worker] Network failed, serving from cache:', requestUrl);
              return cachedResponse;
            }
            return networkResponse;
          });
        })
        .catch((error) => {
          // Network failed, try cache
          console.log('[Service Worker] Network error, trying cache:', requestUrl);
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
              console.log('[Service Worker] Serving from cache (offline):', requestUrl);
              return cachedResponse;
            }
            // No cache available, return error
            console.error('[Service Worker] No cache available for:', requestUrl);
            throw error;
          });
        })
    );
  } else {
    // CACHE-FIRST strategy for static files (HTML, CSS, JS, etc.)
    event.respondWith(
      caches.match(event.request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            console.log('[Service Worker] Serving from cache:', requestUrl);
            // Also try to update cache in background
            fetch(event.request)
              .then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                  const responseToCache = networkResponse.clone();
                  caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                  });
                }
              })
              .catch(() => {
                // Ignore network errors for background updates
              });
            return cachedResponse;
          }

          // Not in cache, fetch from network
          console.log('[Service Worker] Fetching from network:', requestUrl);
          return fetch(event.request)
            .then((response) => {
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }

              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(event.request, responseToCache);
                });

              return response;
            })
            .catch((error) => {
              console.error('[Service Worker] Fetch failed:', error);
              if (event.request.destination === 'document') {
                return caches.match('./index.html');
              }
              throw error;
            });
        })
    );
  }
});

// Handle messages from the main app
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  if (event.data && event.data.type === 'CHECK_UPDATE') {
    // Check for content updates
    checkForContentUpdates().then((hasUpdate) => {
      event.ports[0].postMessage({ hasUpdate });
    });
  }
});

// Check for content updates by comparing version manifest
async function checkForContentUpdates() {
  try {
    const networkResponse = await fetch(VERSION_MANIFEST + '?t=' + Date.now());
    if (networkResponse.ok) {
      const networkVersion = await networkResponse.json();
      const cachedResponse = await caches.match(VERSION_MANIFEST);
      if (cachedResponse) {
        const cachedVersion = await cachedResponse.json();
        if (networkVersion.version !== cachedVersion.version) {
          console.log('[Service Worker] New version detected:', networkVersion.version);
          return true;
        }
      } else {
        // No cached version, consider it an update
        return true;
      }
    }
  } catch (error) {
    console.log('[Service Worker] Could not check for updates (offline):', error);
  }
  return false;
}

