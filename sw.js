/* Offline cache. The version string is stamped by src/build_data.py, so a rebuild
   always produces a new cache name and the old one is dropped on activate. */
var CACHE='handbook-270ee651';
var CORE=['/','/index.html',
          '/assets/app.css?v=270ee651',
          '/assets/core.js?v=270ee651',
          '/assets/ui.js?v=270ee651',
          '/assets/views.js?v=270ee651',
          '/assets/app.js?v=270ee651',
          '/assets/data.js?v=270ee651',
          '/manifest.webmanifest',
          '/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];

self.addEventListener('install',function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){
    return c.addAll(CORE).catch(function(){});
  }));
});

/* The page asks for this once the user accepts the update prompt. Without it a
   new build waits until every tab is closed. */
self.addEventListener('message',function(e){
  if(e.data&&e.data.type==='SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.map(function(k){ if(k!==CACHE) return caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});

self.addEventListener('fetch',function(e){
  var req=e.request;
  if(req.method!=='GET') return;
  var url=new URL(req.url);
  if(url.origin!==location.origin) return;

  /* Navigations: network first, so a deploy is picked up as soon as there is a
     connection, with the cached shell as the offline fallback. */
  if(req.mode==='navigate'){
    e.respondWith(fetch(req).then(function(res){
      var copy=res.clone();
      caches.open(CACHE).then(function(c){c.put('/index.html',copy);});
      return res;
    }).catch(function(){
      return caches.match('/index.html');
    }));
    return;
  }

  /* Everything else is content-hashed, so cache first is safe and instant. */
  e.respondWith(caches.match(req).then(function(hit){
    if(hit) return hit;
    return fetch(req).then(function(res){
      if(res&&res.status===200&&res.type==='basic'){
        var copy=res.clone();
        caches.open(CACHE).then(function(c){c.put(req,copy);});
      }
      return res;
    });
  }));
});
