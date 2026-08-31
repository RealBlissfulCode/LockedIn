var CACHE='handbook-2c377e0a';
var CORE=['/','/index.html','/assets/app.css?v=2c377e0a','/assets/app.js?v=2c377e0a',
          '/assets/data.js?v=2c377e0a','/manifest.webmanifest',
          '/icons/icon.svg','/icons/icon-192.png','/icons/icon-512.png'];
self.addEventListener('install',function(e){self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(CORE).catch(function(){});}));});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(k){
    return Promise.all(k.map(function(x){if(x!==CACHE)return caches.delete(x);}));
  }).then(function(){return self.clients.claim();}));});
self.addEventListener('fetch',function(e){
  var req=e.request; if(req.method!=='GET')return;
  var u=new URL(req.url); if(u.origin!==location.origin)return;
  if(req.mode==='navigate'){
    e.respondWith(fetch(req).then(function(res){
      var c=res.clone(); caches.open(CACHE).then(function(x){x.put('/index.html',c);});
      return res;}).catch(function(){return caches.match('/index.html');}));
    return;}
  e.respondWith(caches.match(req).then(function(hit){
    return hit||fetch(req).then(function(res){
      if(res&&res.status===200){var c=res.clone();caches.open(CACHE).then(function(x){x.put(req,c);});}
      return res;});}));});
