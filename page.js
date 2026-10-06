(()=>{
 const root=document.getElementById('megacrew-reforma');if(!root)return;
 root.querySelectorAll('a[href]').forEach(a=>a.addEventListener('click',e=>{
  const u=new URL(a.href,location.href);if(u.origin!==location.origin||!u.hash)return;
  const target=root.querySelector('#mc-'+u.hash.slice(1));if(!target)return;
  e.preventDefault();const admin=document.getElementById('wpadminbar');const offset=admin?admin.getBoundingClientRect().height:0;
  window.scrollTo({top:Math.max(0,window.scrollY+target.getBoundingClientRect().top-offset-18),behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
 }));
})();
