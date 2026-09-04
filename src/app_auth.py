# -*- coding: utf-8 -*-
"""Sign in, and everything that has to be true before the app can draw.

The passcode gate is gone. It protected one household by encrypting the whole
page behind four digits, which was right when there was one household and no
server. A product cannot work that way: there is nothing to bake in at build
time because the data belongs to whoever signed in.

So the page now boots to a sign in screen, gets a token from Google, and hands
it to api/auth.php. The server checks the signature and sets a session cookie.
After that the app pulls its state from api/doc.php.
"""

APP_AUTH = r"""
/* ============================ session ============================ */
var ACCOUNT=null, HOUSE=null, CLIENT_ID='';

function api(path,opts){
  opts=opts||{};
  var o={credentials:'same-origin',headers:{'X-LockedIn':'1'}};
  if(opts.body!==undefined){
    o.method='POST';
    o.headers['Content-Type']='application/json';
    o.body=JSON.stringify(opts.body);
  }
  return fetch('api/'+path,o).then(function(r){
    return r.json().catch(function(){return {ok:false,error:'bad_response'};})
      .then(function(j){ j.__status=r.status; return j; });
  });
}

/* Everything the app needs to know about who is looking at it. Called on boot
   and again after anything that could change the household. */
function loadSession(){
  return api('auth.php?do=me').then(function(r){
    CLIENT_ID=r.clientId||CLIENT_ID;
    ACCOUNT=r.signedIn?r.account:null;
    HOUSE=r.signedIn?r.household:null;
    return r;
  });
}

/* ============================ the sign in screen ============================ */
function signInScreen(msg){
  var g=document.getElementById('gate');
  if(!g) return;
  g.innerHTML=
    '<div class="gatebox">'+
    '<div class="gatemark"></div>'+
    '<h1>LockedIn</h1>'+
    '<p class="gsub">Meals, training, money and plans. For one person or a whole house.</p>'+
    '<div id="gbtn" class="gbtn"></div>'+
    '<p class="gerr" id="gerr"'+(msg?'':' hidden')+'>'+E(msg||'')+'</p>'+
    (msg?'<p class="gnote"><a class="glink" href="api/check.php">Run the setup check</a></p>':'')+
    '<p class="gnote">Sign in with Google. We only ever ask for your name, your email '+
    'and your picture, and there is no password for anyone to lose.</p>'+
    '<button class="glink" id="gjoin">I have an invite code</button>'+
    '</div>';
  document.getElementById('gjoin').onclick=joinScreen;
  mountGoogle();
}

/* Google's script is loaded on demand rather than in the page head, so a
   signed in visitor never pays for it. */
function withGoogle(cb){
  if(window.google&&google.accounts&&google.accounts.id) return cb();
  var s=document.createElement('script');
  s.src='https://accounts.google.com/gsi/client';
  s.async=true; s.defer=true;
  s.onload=cb;
  s.onerror=function(){
    var e=document.getElementById('gerr');
    if(e){e.textContent='Could not reach Google. Check the connection and reload.';e.hidden=false;}
  };
  document.head.appendChild(s);
}

function mountGoogle(){
  var slot=document.getElementById('gbtn');
  if(!slot) return;
  if(!CLIENT_ID){
    slot.innerHTML='<p class="gerr">This copy has no Google client id set. '+
      'Fill in google_client_id in api/config.php.</p>';
    return;
  }
  withGoogle(function(){
    google.accounts.id.initialize({
      client_id:CLIENT_ID,
      callback:onGoogleCredential,
      auto_select:false,
      cancel_on_tap_outside:true
    });
    google.accounts.id.renderButton(slot,{
      theme:(S.theme==='light'?'outline':'filled_black'),
      size:'large', shape:'pill', text:'continue_with', width:280
    });
    google.accounts.id.prompt();
  });
}

function onGoogleCredential(res){
  var slot=document.getElementById('gbtn');
  if(slot) slot.innerHTML='<div class="gwait">Signing in</div>';
  api('auth.php?do=google',{body:{credential:res.credential}}).then(function(r){
    if(!r.ok){
      /* Say which of the two it is. Google refusing the token and the server
         not being able to store the result need completely different fixes,
         and "try again" is the wrong advice for both. */
      var why={
        bad_token:'Google would not confirm that sign in. If this keeps happening, this '+
          'site is probably not listed under Authorized JavaScript origins on the OAuth client.',
        email_in_use:'That email address is already on another account.',
        not_configured:'This server has no api/config.php yet.',
        db_not_ready:'Signed in with Google, but the database is not ready. Open '+
          '/api/check.php and it will say which part.',
        db_unavailable:'Signed in with Google, but the server cannot reach its database. '+
          'Open /api/check.php and it will say which part.',
        server_error:'Something broke on the server. Open /api/check.php and it will say what.',
        bad_response:'The server replied with something that was not an answer. Open '+
          '/api/check.php and it will say what.',
        bad_origin:'The browser blocked that request. Reload the page and try again.'
      }[r.error]||('Sign in failed ('+(r.error||('HTTP '+r.__status))+'). Open /api/check.php.');
      signInScreen(why);
      return;
    }
    /* A code typed on the join screen before signing in is applied now. */
    var pending=sessionStorage.getItem('li_invite')||'';
    var next=pending
      ? api('household.php?do=join',{body:{code:pending}}).then(function(){
          sessionStorage.removeItem('li_invite');})
      : Promise.resolve();
    next.then(boot);
  });
}

/* ============================ joining with a code ============================ */
function joinScreen(){
  var g=document.getElementById('gate');
  g.innerHTML=
    '<div class="gatebox">'+
    '<div class="gatemark"></div>'+
    '<h1>Join a household</h1>'+
    '<p class="gsub">Type the code you were sent. We will show you whose it is '+
    'before anything happens.</p>'+
    '<input id="gcode" class="gcode" maxlength="8" autocomplete="off" '+
      'autocapitalize="characters" spellcheck="false" placeholder="ABCD1234">'+
    '<p class="gerr" id="gerr" hidden></p>'+
    '<div id="gpeek"></div>'+
    '<button class="glink" id="gback">Back to sign in</button>'+
    '</div>';
  document.getElementById('gback').onclick=function(){signInScreen();};
  var box=document.getElementById('gcode');
  box.focus();
  box.oninput=function(){
    this.value=this.value.toUpperCase().replace(/[^A-Z0-9]/g,'');
    var code=this.value;
    var out=document.getElementById('gpeek');
    if(code.length<8){ out.innerHTML=''; return; }
    api('household.php?do=peek&code='+encodeURIComponent(code)).then(function(r){
      if(!r.valid){
        out.innerHTML='<p class="gerr">That code is not valid, or it has already been used.</p>';
        return;
      }
      sessionStorage.setItem('li_invite',code);
      out.innerHTML='<div class="gfound"><b>'+E(r.household)+'</b>'+
        (r.forName?'<span>Saved as '+E(r.forName)+'</span>':'')+'</div>'+
        '<div id="gbtn" class="gbtn"></div>'+
        '<p class="gnote">Sign in and you will land straight in there.</p>';
      mountGoogle();
    });
  };
}

/* ============================ boot ============================ */
/* Order matters. Find out who is signed in, pull their state down, then draw.
   Drawing first and filling in later means the first paint is somebody else's
   data, or nobody's. */
function boot(){
  return loadSession().then(function(r){
    if(!r.signedIn){ signInScreen(); return; }
    return pullState().then(function(){
      var g=document.getElementById('gate');
      if(g&&g.parentNode) g.parentNode.removeChild(g);
      var app=document.getElementById('app');
      app.hidden=false;
      document.body.classList.add('unlocked');
      applyTheme();
      chrome();
      if(!ACCOUNT.onboarded||!MEMS().length){ startOnboarding(); return; }
      route();
      syncStart();
    });
  });
}

function signOut(){
  api('auth.php?do=out',{body:{}}).then(function(){
    try{localStorage.removeItem(KEY);}catch(e){}
    location.reload();
  });
}
"""
