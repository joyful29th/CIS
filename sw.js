// 勤務表アプリ: オフラインで動かすための仕組み。アプリ本体を端末に保存し、ネットがあるときだけ新しい版を取りに行く。
const CACHE="roster-a1e34a59";
const APP=["./","./index.html","./manifest.webmanifest","./icon-180.png","./icon-192.png","./icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(APP)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k.startsWith("roster-")).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{
  const u=new URL(e.request.url);if(e.request.method!=="GET")return;
  const font=u.host==="fonts.googleapis.com"||u.host==="fonts.gstatic.com";
  if(u.origin!==location.origin&&!font)return;
  e.respondWith(caches.open(CACHE).then(async c=>{
    const hit=await c.match(e.request,{ignoreSearch:e.request.mode==="navigate"})||(e.request.mode==="navigate"?await c.match("./index.html"):null);
    const net=fetch(e.request).then(r=>{if(r&&(r.ok||r.type==="opaque"))c.put(e.request,r.clone());return r}).catch(()=>null);
    return hit||await net||new Response("オフラインです",{status:503,headers:{"Content-Type":"text/plain; charset=utf-8"}});
  }));
});
