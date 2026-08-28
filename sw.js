/* Offline shell. Bump CACHE when assets change; the version query does the rest. */
var CACHE='meal-handbook-027be106';
var CORE=['/','/index.html','/assets/app.css?v=027be106','/assets/app.js?v=027be106',
          '/assets/data.js?v=027be106','/manifest.webmanifest',
          '/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];

self.addEventListener('install',function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(CORE).catch(function(){});}));
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){ if(k!==CACHE) return caches.delete(k); }));
  }).then(function(){return self.clients.claim();}));
});

self.addEventListener('fetch',function(e){
  var req=e.request;
  if(req.method!=='GET') return;
  var url=new URL(req.url);
  if(url.origin!==location.origin) return;

  // Shell: network first so a redeploy shows up, cache as the fallback.
  if(req.mode==='navigate'){
    e.respondWith(fetch(req).then(function(res){
      var copy=res.clone(); caches.open(CACHE).then(function(c){c.put('/index.html',copy);});
      return res;
    }).catch(function(){return caches.match('/index.html');}));
    return;
  }
  // Everything else: cache first, it is all immutable and versioned.
  e.respondWith(caches.match(req).then(function(hit){
    return hit || fetch(req).then(function(res){
      if(res && res.status===200){
        var copy=res.clone(); caches.open(CACHE).then(function(c){c.put(req,copy);});
      }
      return res;
    });
  }));
});
