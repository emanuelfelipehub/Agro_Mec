document.addEventListener('DOMContentLoaded',()=>{
 const btn=document.querySelector('.menu-btn'),nav=document.querySelector('.nav');
 if(btn&&nav) btn.addEventListener('click',()=>nav.classList.toggle('open'));
 document.querySelectorAll('.flash').forEach((el,i)=>setTimeout(()=>{el.style.opacity='0';el.style.transform='translateX(30px)';setTimeout(()=>el.remove(),250)},3600+i*250));
 document.querySelectorAll('[data-count]').forEach(el=>{const target=parseFloat(el.dataset.count)||0;const duration=700;const start=performance.now();const tick=now=>{const p=Math.min((now-start)/duration,1);el.textContent=Number.isInteger(target)?Math.round(target*p): (target*p).toFixed(1);if(p<1)requestAnimationFrame(tick)};requestAnimationFrame(tick)});
 document.querySelectorAll('form[data-confirm]').forEach(form=>form.addEventListener('submit',e=>{if(!confirm(form.dataset.confirm))e.preventDefault()}));
 const path=location.pathname;document.querySelectorAll('.nav a').forEach(a=>{if(a.getAttribute('href')!== '/' && path.startsWith(a.getAttribute('href')))a.classList.add('active');else if(path==='/'&&a.getAttribute('href')==='/')a.classList.add('active')});
});
