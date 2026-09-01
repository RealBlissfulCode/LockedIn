# -*- coding: utf-8 -*-
"""The unlock screen.

Nothing personal is in the page in readable form. Everything that would identify
us, our money or our calendar is encrypted into window._SEALED at build time, and
so is the application code itself, because the editors and defaults carry our
names and our employers. Until the right code is entered the page holds a lock
screen, a recipe database and a block of base64.

Be honest about what this is: the passcode is four digits, so it stops anyone who
finds the URL, not someone determined who has the file. The 200k PBKDF2 rounds
make each guess cost about a quarter of a second, which is the most a four digit
code can buy you.
"""

GATE_HTML = (
    '<div id="gate">'
    '<div class="gatebox">'
    '<div class="gatemark"></div>'
    '<h1>The Handbook</h1>'
    '<p class="gsub">Private. Enter the code.</p>'
    '<div class="gdots" id="gdots">'
    '<i></i><i></i><i></i><i></i>'
    '</div>'
    '<input id="gin" type="password" inputmode="numeric" autocomplete="off" '
    'aria-label="Passcode" maxlength="12">'
    '<div class="gpad" id="gpad">'
    '<button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button>'
    '<button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button>'
    '<button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button>'
    '<button class="gghost" data-k="clear">clear</button>'
    '<button data-k="0">0</button>'
    '<button class="gghost" data-k="back">&#9003;</button>'
    '</div>'
    '<p class="gerr" id="gerr" hidden>That is not it.</p>'
    '<p class="gnote">Everything you enter stays on this device. '
    'Nothing is uploaded and there is no account.</p>'
    '</div></div>'
)


GATE_JS = r"""
(function(){
'use strict';
var SEALED=window._SEALED, REMEMBER='handbook.unlocked';
var gate=document.getElementById('gate'), app=document.getElementById('app');
var input=document.getElementById('gin'), dots=document.getElementById('gdots');
var err=document.getElementById('gerr'), busy=false;

function bytes(s){return new TextEncoder().encode(s);}
function unhex(h){var a=new Uint8Array(h.length/2);
  for(var i=0;i<a.length;i++)a[i]=parseInt(h.substr(i*2,2),16);return a;}
function hex(buf){var a=new Uint8Array(buf),s='';
  for(var i=0;i<a.length;i++)s+=('0'+a[i].toString(16)).slice(-2);return s;}
function unb64(b){var s=atob(b),a=new Uint8Array(s.length);
  for(var i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a;}

/* passcode -> 64 bytes -> encryption key + mac key. Mirrors _derive() in build.py. */
function derive(code){
  var C=window.crypto&&window.crypto.subtle;
  if(!C) return Promise.reject(new Error('nocrypto'));
  return C.importKey('raw',bytes(code),'PBKDF2',false,['deriveBits']).then(function(k){
    return C.deriveBits({name:'PBKDF2',salt:bytes(SEALED.s),
      iterations:SEALED.r,hash:'SHA-256'},k,512);
  }).then(function(bits){
    var b=new Uint8Array(bits);
    return {enc:b.slice(0,32), mac:b.slice(32,64)};
  });
}

function hmacKey(raw){
  return window.crypto.subtle.importKey('raw',raw,{name:'HMAC',hash:'SHA-256'},false,['sign']);
}

/* HMAC-SHA256 in counter mode. Same construction as _keystream() in build.py. */
function keystream(key,nonce,n){
  var blocks=Math.ceil(n/32), jobs=[];
  for(var i=0;i<blocks;i++){
    var msg=new Uint8Array(nonce.length+4);
    msg.set(nonce,0);
    msg[nonce.length]=(i>>>24)&255; msg[nonce.length+1]=(i>>>16)&255;
    msg[nonce.length+2]=(i>>>8)&255; msg[nonce.length+3]=i&255;
    jobs.push(window.crypto.subtle.sign('HMAC',key,msg));
  }
  return Promise.all(jobs).then(function(parts){
    var out=new Uint8Array(blocks*32);
    for(var j=0;j<parts.length;j++) out.set(new Uint8Array(parts[j]),j*32);
    return out.slice(0,n);
  });
}

function open_(code){
  var nonce=unhex(SEALED.n), cipher=unb64(SEALED.d), keys;
  return derive(code).then(function(k){ keys=k; return hmacKey(k.mac); })
  .then(function(mk){
    var msg=new Uint8Array(nonce.length+cipher.length);
    msg.set(nonce,0); msg.set(cipher,nonce.length);
    return window.crypto.subtle.sign('HMAC',mk,msg);
  }).then(function(sig){
    /* Wrong code fails here, before anything is decrypted or run. */
    if(hex(sig).slice(0,32)!==SEALED.t) throw new Error('bad code');
    return hmacKey(keys.enc);
  }).then(function(ek){
    return keystream(ek,nonce,cipher.length);
  }).then(function(ks){
    var plain=new Uint8Array(cipher.length);
    for(var i=0;i<cipher.length;i++) plain[i]=cipher[i]^ks[i];
    var obj=JSON.parse(new TextDecoder().decode(plain));
    /* The sync token is a hash of the mac key, so the server is exactly as
       private as the passcode and nothing extra has to be remembered. */
    return window.crypto.subtle.digest('SHA-256',keys.mac).then(function(h){
      obj.__token=hex(h);
      return obj;
    });
  });
}

/* The app itself comes out of the sealed blob, so until the code is right there
   is no application on the page at all, only the gate. */
function boot(seed){
  window._SEED=seed;
  gate.parentNode.removeChild(gate);
  app.hidden=false;
  document.body.classList.add('unlocked');
  var s=document.createElement('script');
  s.textContent=seed.app;
  document.body.appendChild(s);
}

function fail(msg){
  busy=false;
  err.textContent=msg||'That is not it.';
  err.hidden=false;
  input.value=''; paint();
  gate.querySelector('.gatebox').classList.remove('shake');
  void gate.offsetWidth;
  gate.querySelector('.gatebox').classList.add('shake');
}

function paint(){
  var n=input.value.length;
  [].forEach.call(dots.children,function(d,i){d.className=i<n?'on':'';});
}

function attempt(){
  if(busy) return;
  var code=input.value;
  if(code.length<4) return;
  busy=true; err.hidden=true;
  gate.classList.add('working');
  open_(code).then(function(seed){
    try{localStorage.setItem(REMEMBER,code);}catch(e){}
    gate.classList.remove('working');
    boot(seed);
  }).catch(function(e){
    gate.classList.remove('working');
    if(e&&e.message==='nocrypto'){
      fail('This browser cannot decrypt the page. Open it over https.');
      return;
    }
    fail();
  });
}

document.getElementById('gpad').addEventListener('click',function(e){
  var b=e.target.closest('button'); if(!b) return;
  var k=b.dataset.k;
  if(k==='clear') input.value='';
  else if(k==='back') input.value=input.value.slice(0,-1);
  else if(input.value.length<12) input.value+=k;
  paint(); err.hidden=true;
  if(input.value.length>=4) attempt();
});
input.addEventListener('input',function(){
  paint(); err.hidden=true;
  if(input.value.length>=4) attempt();
});
input.addEventListener('keydown',function(e){ if(e.key==='Enter') attempt(); });

/* Already unlocked on this device. Settings has a Lock button that clears it. */
var saved=null;
try{saved=localStorage.getItem(REMEMBER);}catch(e){}
if(saved){
  gate.classList.add('working');
  open_(saved).then(function(seed){ boot(seed); })
  .catch(function(){ try{localStorage.removeItem(REMEMBER);}catch(e){}
    gate.classList.remove('working'); input.focus(); });
}else{
  setTimeout(function(){ try{input.focus();}catch(e){} },80);
}
})();
"""
