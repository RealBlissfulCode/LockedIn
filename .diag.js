const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const ROOT=__dirname;
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.webmanifest':'application/manifest+json'};
const server=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p==='/')p='/index.html';const f=path.join(ROOT,p);
 if(!fs.existsSync(f)||fs.statSync(f).isDirectory()){r.writeHead(404);r.end();return;}
 r.writeHead(200,{'Content-Type':types[path.extname(f)]||'text/plain'});fs.createReadStream(f).pipe(r);});
(async()=>{await new Promise(r=>server.listen(8399,r));
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(let i=0;i<8;i++){
 const p=await b.newPage();
 await p.route('**://fonts.googleapis.com/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));
 await p.goto('http://127.0.0.1:8399/',{waitUntil:'domcontentloaded'});
 await p.evaluate(()=>{location.hash='#/meals'});await p.waitForTimeout(350);
 await p.click('#addOwn'); await p.waitForSelector('.mask');
 await p.fill('#on','Test recipe'); await p.fill('#ok','400'); await p.fill('#op','30');
 const beforeVal = await p.inputValue('#on');
 await p.click('#oSave'); await p.waitForTimeout(250);
 const res = await p.evaluate(()=>({
   mine: window.Handbook.state().mine.length,
   inAll: window.Handbook.all().some(r=>r.n==='Test recipe'),
   maskOpen: document.querySelectorAll('.mask').length,
   nameField: document.querySelector('#on') ? document.querySelector('#on').value : '(gone)'
 }));
 console.log(i, 'filled='+JSON.stringify(beforeVal), JSON.stringify(res));
 await p.close();
}
await b.close();server.close();})();
