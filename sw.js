/* Network first, cache as fallback. A redeploy always wins; the cache only
   exists so the app still opens with no signal. */
var CACHE='handbook-a83c43e3';
var CORE=['/','/index.html','/assets/app.css','/assets/app.js','/assets/data.js',
          '/manifest.webmanifest','/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];
self.addEventListener('install',function(e){self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(CORE).catch(function(){});}));});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(k){
    return Promise.all(k.map(function(x){if(x!==CACHE)return caches.delete(x);}));
  }).then(function(){return self.clients.claim();}));});
self.addEventListener('message',function(e){ if(e.data==='skipWaiting') self.skipWaiting(); });
self.addEventListener('fetch',function(e){
  var req=e.request; if(req.method!=='GET')return;
  var u; try{u=new URL(req.url);}catch(err){return;}
  if(u.origin!==location.origin)return;
  e.respondWith(
    fetch(req).then(function(res){
      if(res&&res.status===200){
        var copy=res.clone();
        caches.open(CACHE).then(function(c){c.put(req,copy);});
      }
      return res;
    }).catch(function(){
      return caches.match(req).then(function(hit){
        return hit || caches.match('/index.html');
      });
    })
  );
});
