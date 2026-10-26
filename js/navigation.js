(() => {
  const button=document.querySelector('.menu-toggle');
  const menu=document.querySelector('#site-nav');
  if (!button || !menu) return;
  function setOpen(open) {
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',window.ORA_I18N?.t(open?'关闭导航':'打开导航',open?'Close navigation':'Open navigation') || (open?'关闭导航':'打开导航'));
    menu.classList.toggle('is-open',open);
  }
  window.addEventListener('ora-language-change',()=>setOpen(button.getAttribute('aria-expanded')==='true'));
  button.addEventListener('click',()=>setOpen(button.getAttribute('aria-expanded')!=='true'));
  menu.addEventListener('click',event=>{if(event.target.closest('a')) setOpen(false)});
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape' && button.getAttribute('aria-expanded')==='true'){
      setOpen(false);button.focus();
    }
  });
  document.addEventListener('click',event=>{
    if(button.getAttribute('aria-expanded')==='true'&&!event.target.closest('.nav-shell')) setOpen(false);
  });
  window.matchMedia('(min-width: 921px)').addEventListener('change',event=>{if(event.matches)setOpen(false)});
  setOpen(false);
})();
