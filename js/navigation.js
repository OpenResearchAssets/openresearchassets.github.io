/* Single source for primary navigation, secondary site links and responsive menus.
 * Page HTML supplies only an empty #site-nav and its data-page / data-root.
 * Language state lives in ORA_I18N; route state never depends on query strings.
 */
(() => {
  'use strict';
  const menu=document.getElementById('site-nav');
  const button=document.querySelector('.menu-toggle');
  if(!menu || !button)return;
  const root=menu.dataset.root||'';
  const current=menu.dataset.page||'curated';
  const path=name=>root+name;
  const links=[
    {key:'curated',href:path('index.html'),zh:'精选',en:'Curated'},
    {key:'community',href:path('community.html'),zh:'社区',en:'Community'},
    {key:'findings',href:path('findings.html'),zh:'发现',en:'Findings'},
    {key:'contribute',href:path('contribute.html'),zh:'投稿',en:'Contribute'}
  ];
  const translate=(zh,en)=>window.ORA_I18N?.t(zh,en)||
    (document.documentElement.lang==='en'?en:zh);
  const escapeHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const main=menu.closest('.nav-shell');
  let headerCTA=main?.querySelector('.nav-cta');
  if(!headerCTA&&main){
    headerCTA=document.createElement('a');
    headerCTA.className='nav-cta';
    main.insertBefore(headerCTA,main.querySelector('.lang-toggle')||button);
  }
  // Desktop: Curated / Community / Findings plus one Contribute action. Mobile includes all.
  if(headerCTA){headerCTA.href=links[3].href;if(current==='contribute')headerCTA.setAttribute('aria-current','page');else headerCTA.removeAttribute('aria-current');}
  function renderNavigation(){
    menu.innerHTML=links.map((item,i)=>{
      const active=current===item.key?' aria-current="page"':'';
      return '<a href="'+escapeHtml(item.href)+'"'+active+
        (i===3?' class="mobile-only"':'')+'>'+escapeHtml(translate(item.zh,item.en))+'</a>';
    }).join('');
    if(headerCTA)headerCTA.textContent=translate('投稿 ↗','Contribute ↗');
    button.setAttribute('aria-label',translate('打开导航','Open navigation'));
  }
  const footer=document.querySelector('.footer-inner');
  function renderFooter(){
    if(!footer)return;
    const secondary=[
      [path('quality.html'),'质量自查','Quality check'],
      [path('principles.html'),'设计原则','Principles'],
      [path('for-agents/'),'给 AI 使用','For AI'],
      ['https://github.com/OpenResearchAssets/openresearchassets.github.io','GitHub 仓库','GitHub repository'],
      [path('docs/ASSET_POLICY.md'),'版权与来源','Licensing'],
      ['https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=asset-removal.yml','撤除与纠错','Removal & corrections']
    ];
    footer.innerHTML='<a class="brand" href="'+path('index.html')+'"><img src="'+path('assets/mark.svg')+
      '" alt="" width="24" height="24"><span>OpenResearchAssets</span></a>'+
      '<span class="ora-footer-motto">'+escapeHtml(translate('精选好图与实用研究资产','Research visuals & useful workflows'))+'</span>'+
      '<nav class="ora-footer-links" aria-label="'+escapeHtml(translate('更多信息','More information'))+'">'+
      secondary.map(([href,zh,en])=>'<a href="'+escapeHtml(href)+'"'+(href.startsWith('https://')?' target="_blank" rel="noopener noreferrer"':'')+'>'+escapeHtml(translate(zh,en))+'</a>').join('')+'</nav>';
  }
  function setOpen(open){
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',translate(open?'关闭导航':'打开导航',open?'Close navigation':'Open navigation'));
    menu.classList.toggle('is-open',open);
  }
  renderNavigation();
  renderFooter();
  button.addEventListener('click',()=>setOpen(button.getAttribute('aria-expanded')!=='true'));
  menu.addEventListener('click',event=>{if(event.target.closest('a'))setOpen(false);});
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&button.getAttribute('aria-expanded')==='true'){setOpen(false);button.focus();}
  });
  document.addEventListener('click',event=>{
    if(button.getAttribute('aria-expanded')==='true'&&!event.target.closest('.nav-shell'))setOpen(false);
  });
  window.matchMedia('(min-width: 921px)').addEventListener('change',event=>{if(event.matches)setOpen(false);});
  window.addEventListener('ora-language-change',()=>{
    const wasOpen=button.getAttribute('aria-expanded')==='true';
    renderNavigation();renderFooter();setOpen(wasOpen);
  });
  setOpen(false);
})();
