var CACHE_NAME='python-platform-v1';
var urlsToCache=['/','/static/css/main.min.css','/static/js/main.min.js'];

self.addEventListener('install',function(e){e.waitUntil(caches.open(CACHE_NAME).then(function(cache){return cache.addAll(urlsToCache)}));self.skipWaiting()});

self.addEventListener('fetch',function(e){e.respondWith(caches.match(e.request).then(function(response){if(response){return response}var fetchRequest=e.request.clone();return fetch(fetchRequest).then(function(response){if(!response||response.status!==200||response.type!=='basic'){return response}var responseToCache=response.clone();caches.open(CACHE_NAME).then(function(cache){cache.put(e.request,responseToCache)});return response})}).catch(function(){if(e.request.headers.get('Accept').indexOf('text/html')!==-1){return caches.match('/')}return null}))});

self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(cacheNames){return Promise.all(cacheNames.filter(function(cacheName){return cacheName!==CACHE_NAME}).map(function(cacheName){return caches.delete(cacheName)}))}));self.claim()});
