(() => {
  const refs=window.ORA_REFERENCES || [];
  const grid=document.querySelector('#reference-grid');
  if (!grid) return;
  const search=document.querySelector('#reference-search');
  const buttons=[...document.querySelectorAll('.filter')];
  const status=document.querySelector('#reference-status');
  let active='All';
  const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function render(){
    const q=(search.value||'').trim().toLowerCase();
    const items=refs.filter(x=>(active==='All'||x.category===active)&&[x.title,x.tag,x.note,x.pattern].join(' ').toLowerCase().includes(q));
    grid.innerHTML=items.map((r,i)=>`<a class="reference-card theme-${escapeHTML(r.theme)}" href="${escapeHTML(r.url)}" rel="noopener noreferrer" target="_blank" aria-label="Open ${escapeHTML(r.title)} source in a new tab"><div class="reference-image"><div class="reference-art" aria-hidden="true"><div class="shape-a"></div><div class="shape-b"></div><div class="shape-c"></div></div><span class="reference-category">${escapeHTML(r.kind)}</span><span class="reference-arrow" aria-hidden="true">↗</span></div><div class="reference-body"><div class="reference-meta">${escapeHTML(r.tag)} <span>${escapeHTML(r.year)}</span></div><h3>${escapeHTML(r.title)}</h3><p class="reference-short">${escapeHTML(r.short)}</p><div class="reference-insight"><span>DESIGN NOTE</span>${escapeHTML(r.note)}</div></div></a>`).join('');
    if(!items.length) grid.innerHTML='<p class="empty-state">No references match. Try another category or keyword.</p>';
    status.textContent=`Showing ${items.length} of ${refs.length} carefully linked references · Abstract thumbnails are our own, not reproductions of referenced work.`;
  }
  buttons.forEach(b=>b.addEventListener('click',()=>{active=b.dataset.filter;buttons.forEach(x=>{const on=x===b;x.classList.toggle('active',on);x.setAttribute('aria-pressed',String(on))});render()}));
  search.addEventListener('input',render);
  render();
})();
