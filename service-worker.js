const CACHE_NAME = 'mdj-cache-v1';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/about.html',
  '/activities.html',
  '/news.html',
  '/contact.html',
  '/login.html',
  '/profile.html',
  '/media.html',
  '/img/logo.png',
  '/sitemap.xml',
  '/robots.txt'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((key) => {
        if (key !== CACHE_NAME) return caches.delete(key);
      }))
    )
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        const respClone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(request, respClone)).catch(() => {});
        return response;
      }).catch(() => cached);
    })
  );
});