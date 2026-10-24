(() => {
  const refs = window.ORA_REFERENCES || [];
  const grid = document.querySelector('#reference-grid');
  if (!grid) return;
  const search = document.querySelector('#reference-search');
  const buttons = [...document.querySelectorAll('.filter')];
  const status = document.querySelector('#reference-status');
  let active = 'All';
  const escapeHTML = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function render(){
    const t=window.ORA_I18N?.t||((zh)=>zh);
    const q=(search.value||'').trim().toLowerCase();
    const items=refs.filter(r=>(active==='All'||r.category===active) &&
      [r.title,r.tag,r.tagZh,r.kind,r.kindZh,r.note,r.noteZh,r.pattern,r.short,r.shortZh].join(' ').toLowerCase().includes(q));
    grid.innerHTML=items.map(r=>`<a class="reference-card theme-${escapeHTML(r.theme)}" href="${escapeHTML(r.url)}" rel="noopener noreferrer" target="_blank" aria-label="${escapeHTML(t('在新窗口打开原始来源：','Open original source: ')+r.title)}"><div class="reference-image"><div class="reference-art" aria-hidden="true"><div class="shape-a"></div><div class="shape-b"></div><div class="shape-c"></div></div><span class="reference-category">${escapeHTML(t(r.kindZh,r.kind))}</span><span class="reference-arrow" aria-hidden="true">↗</span></div><div class="reference-body"><div class="reference-meta">${escapeHTML(t(r.tagZh,r.tag))} <span>${escapeHTML(r.year==='Community'?t('社区','Community'):r.year)}</span></div><h3>${escapeHTML(r.title)}</h3><p class="reference-short">${escapeHTML(t(r.shortZh,r.short))}</p><div class="reference-insight"><span>${escapeHTML(t('设计观察','DESIGN NOTE'))}</span>${escapeHTML(t(r.noteZh,r.note))}</div></div></a>`).join('');
    if(!items.length) grid.innerHTML='<p class="empty-state">'+escapeHTML(t('没有匹配的参考，试试其他关键词或分类。','No references match. Try another category or keyword.'))+'</p>';
    status.textContent=t(`当前显示 ${items.length} / ${refs.length} 条来源明确的参考 · 卡片配图是本站的抽象示意，不是原作者的论文图片。`,`Showing ${items.length} of ${refs.length} linked references · Abstract thumbnails are ours, not reproductions of referenced work.`);
  }
  buttons.forEach(b=>b.addEventListener('click',()=>{
    active=b.dataset.filter;
    buttons.forEach(x=>{const on=x===b;x.classList.toggle('active',on);x.setAttribute('aria-pressed',String(on))});
    render();
  }));
  search.addEventListener('input',render);
  window.addEventListener('ora-language-change',render);
  render();
})();
