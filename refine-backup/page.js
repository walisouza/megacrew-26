(()=>{
const root=document.getElementById('megacrew-reforma');if(!root)return;
const wrapper=root.querySelector('.mc-desktop');
const resize=()=>wrapper.style.setProperty('--mc-scale',String(wrapper.clientWidth/1440));
new ResizeObserver(resize).observe(wrapper);resize();
root.querySelectorAll('a[href]').forEach(a=>a.addEventListener('click',e=>{
 const slug=new URL(a.href,location.href).hash.slice(1);const mode=matchMedia('(max-width:900px)').matches?'m':'d';
 const target=document.getElementById('mc-'+mode+'-'+slug);if(target){e.preventDefault();window.scrollTo({top:window.scrollY+target.getBoundingClientRect().top-40,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});}
}));
const answers=/*ANSWERS*/,questions=/*QUESTIONS*/;
const panel=root.querySelector('#mc-answer-panel');
root.querySelectorAll('.mc-faq-trigger').forEach(b=>b.addEventListener('click',()=>{
 const i=Number(b.dataset.answer);const same=b.getAttribute('aria-expanded')==='true';
 root.querySelectorAll('.mc-faq-trigger').forEach(x=>x.setAttribute('aria-expanded','false'));
 if(same){panel.hidden=true;return;}
 b.setAttribute('aria-expanded','true');panel.hidden=false;panel.querySelector('h3').textContent=questions[i];panel.querySelector('p').textContent=answers[i];

}));
root.querySelector('.mc-answer-close').addEventListener('click',()=>{panel.hidden=true;root.querySelectorAll('.mc-faq-trigger').forEach(x=>x.setAttribute('aria-expanded','false'));});
})();
