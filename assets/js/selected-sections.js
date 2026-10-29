(() => {
 const en=document.documentElement.lang==='en';
 document.querySelectorAll('.imported-layout [data-message]').forEach(button=>button.addEventListener('click',()=>{
  let note=document.getElementById('selected-toast');
  if(!note){const wrap=document.createElement('div');wrap.className='imported-layout';note=document.createElement('div');note.id='selected-toast';note.setAttribute('role','status');note.setAttribute('aria-live','polite');wrap.append(note);document.body.append(wrap);}
  note.textContent=button.dataset.message;note.classList.add('sr-visible');clearTimeout(note.hideTimer);note.hideTimer=setTimeout(()=>note.classList.remove('sr-visible'),4200);
 }));
 document.querySelectorAll('.imported-layout form[data-unconfigured]').forEach(form=>form.addEventListener('submit',event=>{
  event.preventDefault();form.querySelector('.sr-form-status').textContent=en?'This service is being prepared. Nothing has been sent or saved.':'현재 서비스를 준비하고 있습니다. 입력한 내용은 전송·저장되지 않았습니다.';
 }));
})();
