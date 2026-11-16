(function () {
 'use strict';
 const menuBtn=document.querySelector('[data-menu]'),menu=document.getElementById('mobile-menu');
 if(menuBtn&&menu){
 const ko=document.documentElement.lang==='ko';
 const setMenu=open=>{menuBtn.setAttribute('aria-expanded',String(open));menuBtn.setAttribute('aria-label',ko?(open?'메뉴 닫기':'메뉴 열기'):(open?'Close menu':'Open menu'));menu.hidden=!open;};
 menuBtn.addEventListener('click',()=>setMenu(menuBtn.getAttribute('aria-expanded')!=='true'));
 document.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&!menu.hidden){setMenu(false);menuBtn.focus();}});
 document.addEventListener('click',ev=>{if(!ev.target.closest('.site-header'))setMenu(false);});
 window.matchMedia('(min-width:1101px)').addEventListener('change',ev=>{if(ev.matches)setMenu(false);});
 }
 const shop=window.SCROLLREALM_SHOP_URLS||{};
 const isKorean = document.documentElement.lang === 'ko';
 document.querySelectorAll('[data-shop]').forEach(button => {
   const url = shop[button.dataset.shop];
   const available = typeof url === 'string' && /^https:\/\/(?:[a-z0-9-]+\.)*(?:naver\.com|naver\.me)(?:\/|$)/i.test(url);
   button.disabled = !available;
   if (!available) {
     button.setAttribute('aria-disabled', 'true');
     return;
   }
   button.removeAttribute('aria-disabled');
   button.textContent = isKorean ? '구매하기' : 'Buy now';
   const note = button.parentElement.querySelector('[data-shop-notice]');
   if (note) note.textContent = isKorean ? '네이버스토어에서 구매하실 수 있습니다.' : 'Purchase through our Naver Store.';
   button.addEventListener('click', () => window.open(url, '_blank', 'noopener,noreferrer'));
 });
 const form=document.getElementById('contact-form');if(form){form.addEventListener('submit',ev=>{ev.preventDefault();const note=document.getElementById('contact-notice');if(note)note.textContent=document.documentElement.lang==='ko'?'전송 서비스가 연결되지 않았습니다. 문의가 접수되지 않았습니다.':'Submission is not configured. Your inquiry was not sent.';});}
 document.querySelectorAll('.gallery-thumbs button').forEach(b=>b.addEventListener('click',()=>{const stage=b.closest('.detail-media')?.querySelector('.gallery-stage img');if(stage){stage.src=b.dataset.gallerySrc;stage.alt=b.querySelector('img')?.alt||stage.alt;document.querySelectorAll('.gallery-thumbs button').forEach(x=>x.classList.remove('is-active'));b.classList.add('is-active');}}));
 document.querySelectorAll('[data-zoom]').forEach(b=>b.addEventListener('click',()=>{const src=b.closest('.gallery-stage')?.querySelector('img')?.src;if(!src)return;let d=document.querySelector('.lightbox');if(!d){d=document.createElement('dialog');d.className='lightbox';d.innerHTML='<button class="lightbox-close" type="button" aria-label="Close">×</button><img alt="Expanded image">';document.body.append(d);d.querySelector('button').addEventListener('click',()=>d.close());}d.querySelector('img').src=src;d.querySelector('img').alt=b.closest('.gallery-stage')?.querySelector('img')?.alt||'Expanded image';d.showModal();}));
 const data=window.SCROLLREALM_CONTENT||{};
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 document.querySelectorAll('[data-milestones]').forEach(root=>{const lang=root.dataset.lang;const v=data.milestones;if(!Array.isArray(v))return;root.innerHTML=v.map((r,i)=>`<article class="milestone"><span class="step">${String(i+1).padStart(2,'0')}</span><div><div class="small-meta">${esc(lang==='ko'?r.status_ko:r.status_en)}</div><h3>${esc(lang==='ko'?r.ko:r.en)}</h3><p>${esc(lang==='ko'?r.description_ko:r.description_en)}</p></div></article>`).join('');});
 if (!Array.isArray(data.news)) return;
 document.querySelectorAll('[data-news-grid]').forEach(root => {
   const prefix = root.dataset.linkPrefix || '';
   const assets = root.dataset.assetPrefix || '';
   root.innerHTML = data.news.map(story => {
     const title = isKorean ? story.title_ko : story.title;
     const intro = isKorean ? story.intro_ko : story.intro;
     const category = isKorean ? story.category_ko : story.category;
     const date = story.date ? ` · <time datetime="${esc(story.date)}">${esc(story.date)}</time>` : '';
     return `<a class="news-tile" href="${esc(prefix + 'news/' + story.id + '/index.html')}">
       <figure class="dynamic-news-photo"><img alt="" src="${esc(assets + story.img)}" loading="lazy"></figure>
       <div class="small-meta">${esc(category)}${date}</div><h3>${esc(title)}</h3><p>${esc(intro)}</p>
     </a>`;
   }).join('');
 });

 document.querySelectorAll('[data-article-id]').forEach(article => {
   const story = data.news.find(entry => entry.id === article.dataset.articleId);
   if (!story) return;
   const category = isKorean ? story.category_ko : story.category;
   const fields = {
     '.article-header h1': isKorean ? story.title_ko : story.title,
     '.article-header p': isKorean ? story.intro_ko : story.intro,
     '.article-header .small-meta': story.date ? `${category} · ${story.date}` : category,
     '.article-text > p': isKorean ? story.body_ko : story.body_en,
   };
   for (const [selector, value] of Object.entries(fields)) {
     const element = article.querySelector(selector);
     if (element && typeof value === 'string' && value.trim()) element.textContent = value;
   }
 });
})();
