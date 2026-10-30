// Countdown Timer — service worker
// Bump CACHE_NAME on every release so clients pick up fresh assets.
var CACHE_NAME = 'countdown-v1.2.4';

// Core assets — cached atomically on install (install fails if any are missing).
var CORE_ASSETS = [
    './',
    './index.html',
    './manifest.json',
    './icons/icon.svg'
];

// Optional assets — best-effort, so a missing one can't break install/offline.
var OPTIONAL_ASSETS = [
    './icons/icon-maskable.svg',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/icon-maskable-192.png',
    './icons/icon-maskable-512.png',
    './icons/screenshot-wide.png',
    './icons/screenshot-narrow.png',
    './userguide.html'
];

// Install — cache core atomically, optional best-effort.
self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function (cache) {
            return cache.addAll(CORE_ASSETS).then(function () {
                return Promise.all(OPTIONAL_ASSETS.map(function (url) {
                    return cache.add(url).catch(function () { /* ignore missing optional asset */ });
                }));
            });
        })
    );
    self.skipWaiting();
});

// Activate — clean out old caches.
self.addEventListener('activate', function (event) {
    event.waitUntil(
        caches.keys().then(function (keys) {
            return Promise.all(
                keys.filter(function (key) { return key !== CACHE_NAME; })
                    .map(function (key) { return caches.delete(key); })
            );
        })
    );
    self.clients.claim();
});

// Fetch — cache first, network fallback, navigate falls back to index.html offline.
self.addEventListener('fetch', function (event) {
    if (event.request.method !== 'GET') return;
    event.respondWith(
        caches.match(event.request).then(function (cached) {
            if (cached) return cached;
            return fetch(event.request).then(function (response) {
                if (response && response.status === 200) {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function (cache) {
                        cache.put(event.request, clone);
                    });
                }
                return response;
            }).catch(function () {
                if (event.request.mode === 'navigate') {
                    return caches.match('./index.html');
                }
            });
        })
    );
});
