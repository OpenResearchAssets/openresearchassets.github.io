/* OpenResearchAssets browser: single source of truth is /catalog/index.json. */
(() => {
  'use strict';
  const grid = document.getElementById('reference-grid');
  const detail = document.getElementById('asset-detail');
  if (!grid && !detail) return;

  let catalog = null;
  let filtersReady = false;
  const params = new URLSearchParams(location.search);
  const tr = (zh,en) => document.documentElement.lang === 'en' ? en : zh;
  const local = value => typeof value === 'object' && !Array.isArray(value) && value !== null && 'zh' in value ? value[document.documentElement.lang === 'en' ? 'en' : 'zh'] : value;
  const safe = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeUrl = value => {
    try { const u=new URL(value,location.href); return ['https:','http:'].includes(u.protocol) ? u.href : ''; }
    catch (_) { return ''; }
  };
  const link = (url,label) => {
    const href = safeUrl(url);
    return href ? '<a href="'+safe(href)+'" target="_blank" rel="noopener noreferrer">'+safe(label)+' ↗</a>' : '';
  };
  const empty = () => tr('暂无相关结果。尝试其他关键词或筛选条件。','No matching resources. Try another query or facet.');
  const facets = () => catalog.facets || {};
  const facetText = (group,key) => local((facets()[group] || {})[key]) || key;
  const kind = entry => facetText('kinds',entry.kind);

  function media(entry) {
    const type = entry.previewStyle || 'gallery';
    const rights=entry.rights || {};
    if (rights.preview === 'original-svg' && entry.links && /^assets\/templates\/[\w-]+\.svg$/.test(entry.links.editable || '')) {
      return '<div class="ora-preview ora-template"><img loading="lazy" alt="'+safe(tr('原创可编辑图示预览','Editable original diagram preview'))+'" src="'+safe(entry.links.editable)+'"></div>';
    }
    const mark=type==='comparison' ? '<div class="ora-pair"><div><i></i><span>SIM</span></div><b>→</b><div><i></i><span>RGB</span></div></div>'
      : type==='benchmark' ? '<div class="ora-matrix"><span>SIM</span><span>REAL</span><i></i><i></i><i></i><i></i><i></i><i></i></div>'
      : type==='editorial' ? '<div class="ora-editorial"><span>RESEARCH STORY</span><strong>ONE CLEAR<br>CLAIM.</strong><i></i></div>'
      : type==='workflow' ? '<div class="ora-steps"><i></i><b>→</b><i></i><b>→</b><i></i></div>'
      : '<div class="ora-gallery-lines"><i></i><i></i><i></i></div>';
    return '<div class="ora-preview ora-'+safe(type)+'" aria-label="'+safe(tr('本站原创结构示意，非源作品截图','Authored structural illustration, not an original screenshot'))+'">'+mark+'<span class="ora-preview-caption">'+safe(tr('本站结构示意 · 非原图','Original structure sketch · not source image'))+'</span></div>';
  }

  function options(selectId,group) {
    const node=document.getElementById(selectId);
    if (!node) return;
    const original=node.value || params.get(selectId.replace('facet-','')) || '';
    node.innerHTML='<option value="">'+safe(tr(group==='stages'?'全部阶段':group==='kinds'?'全部类型':'全部领域',group==='stages'?'All stages':group==='kinds'?'All types':'All domains'))+'</option>'+
      Object.entries(facets()[group] || {}).map(([key,v])=>'<option value="'+safe(key)+'">'+safe(local(v))+'</option>').join('');
    node.value=original;
  }
  function prepareFilters() {
    ['stages','kinds','domains'].forEach((key,i)=>options(['facet-stage','facet-kind','facet-domain'][i],key));
    if (filtersReady) return;
    filtersReady=true;
    const search=document.getElementById('reference-search');
    if(search) {search.value=params.get('q') || '';search.addEventListener('input',renderGrid);}
    ['facet-stage','facet-kind','facet-domain'].forEach(id=>document.getElementById(id)?.addEventListener('change',renderGrid));
    document.querySelectorAll('[data-task-query]').forEach(b=>b.addEventListener('click',()=>{
      if(!search)return;
      search.value=b.dataset.taskQuery;renderGrid();search.focus();
    }));
    document.getElementById('facet-reset')?.addEventListener('click',()=>{
      search.value='';
      ['facet-stage','facet-kind','facet-domain'].forEach(id=>{document.getElementById(id).value='';});
      renderGrid();
    });
  }
  function allSearch(entry) {
    const a=entry.applicability || {};
    return [entry.id,entry.title,entry.kind,...entry.stages,...entry.domains,...entry.tasks,
      ...(entry.keywords?.zh || []),...(entry.keywords?.en || []),entry.description?.zh,entry.description?.en,
      ...(a.use_when?.zh || []),...(a.use_when?.en || []),
      ...(a.learn?.zh || []),...(a.learn?.en || [])].filter(Boolean).join(' ').toLowerCase();
  }
  function renderGrid() {
    if (!grid || !catalog) return;
    const q=document.getElementById('reference-search')?.value.trim().toLowerCase() || '';
    const stage=document.getElementById('facet-stage')?.value || '';
    const kindSelect=document.getElementById('facet-kind')?.value || '';
    const domain=document.getElementById('facet-domain')?.value || '';
    const words=q.split(/\s+/).filter(Boolean);
    const items=catalog.entries.filter(e=>(!stage || e.stages.includes(stage)) &&
      (!kindSelect || e.kind===kindSelect) && (!domain || e.domains.includes(domain)) &&
      words.every(w=>allSearch(e).includes(w)));
    grid.innerHTML=items.length ? items.map(e=>'<article class="ora-resource-card">'+
      '<a class="ora-resource-visual" href="asset.html?id='+encodeURIComponent(e.id)+'" aria-label="'+safe(tr('查看资产：','View asset: ')+e.title)+'">'+media(e)+'</a>'+
      '<div class="ora-resource-content"><div class="ora-resource-kicker">'+safe(kind(e))+' · '+safe(e.year || '')+'</div>'+
      '<h3><a href="asset.html?id='+encodeURIComponent(e.id)+'">'+safe(e.title)+'</a></h3>'+
      '<p>'+safe(local(e.description))+'</p>'+
      '<div class="ora-tag-row">'+e.stages.slice(0,2).map(x=>'<span>'+safe(facetText('stages',x))+'</span>').join('')+
      e.domains.slice(0,1).map(x=>'<span>'+safe(facetText('domains',x))+'</span>').join('')+'</div>'+
      '<div class="ora-resource-actions"><a href="asset.html?id='+encodeURIComponent(e.id)+'">'+safe(tr('查看复用指南','Usage guide'))+' →</a>'+
      link(e.links?.source,tr('原始来源','Original source'))+'</div></div></article>').join('') :
      '<p class="empty-state">'+safe(empty())+'</p>';
    const status=document.getElementById('reference-status');
    if(status)status.textContent=tr('已显示 ','Showing ')+items.length+' / '+catalog.entries.length+
      tr(' 项 · 第三方图像未复制入库，预览为本站原创结构示意。',' entries · Third-party images are not copied; structural previews are authored.');
    const u=new URL(location.href); q?u.searchParams.set('q',q):u.searchParams.delete('q');
    for(const [key,value] of [['stage',stage],['kind',kindSelect],['domain',domain]]) {
      value?u.searchParams.set(key,value):u.searchParams.delete(key);
    }
    history.replaceState(null,'',u.pathname+u.search+u.hash);
  }
  function points(list) {
    if(!Array.isArray(list)||!list.length)return '<p>'+safe(tr('尚未整理。','Not yet curated.'))+'</p>';
    return '<ul>'+list.map(x=>'<li>'+safe(x)+'</li>').join('')+'</ul>';
  }
  function renderDetail() {
    if(!detail || !catalog)return;
    const id=new URLSearchParams(location.search).get('id');
    const e=catalog.entries.find(x=>x.id===id);
    if(!e) {document.title=tr('未找到资产 · OpenResearchAssets','Asset not found · OpenResearchAssets');
      detail.innerHTML='<p>'+safe(tr('未找到该资产，请返回目录。','Resource not found. Return to catalog.'))+'</p><a href="index.html#references">'+safe(tr('返回目录','Return to catalog'))+'</a>';return;}
    document.title=e.title+' · OpenResearchAssets';
    const app=e.applicability || {};
    const related=catalog.entries.filter(x=>x.id===e.parent).slice(0,1);
    detail.innerHTML='<div class="ora-detail-heading"><p class="ora-eyebrow">'+safe(kind(e))+' / '+safe(e.id)+'</p>'+
      '<h1>'+safe(e.title)+'</h1><p>'+safe(local(e.description))+'</p></div>'+
      '<div class="ora-detail-grid"><section class="ora-detail-main"><div class="ora-detail-preview">'+media(e)+'</div>'+
      '<div class="ora-lesson"><h2>'+safe(tr('什么时候使用','When to use'))+'</h2>'+points(local(app.use_when))+'</div>'+
      '<div class="ora-lesson"><h2>'+safe(tr('值得学习的做法','Transferable lessons'))+'</h2>'+points(local(app.learn))+'</div>'+
      '<div class="ora-lesson"><h2>'+safe(tr('需要避免','What to avoid'))+'</h2>'+points(local(app.avoid))+'</div></section>'+
      '<aside class="ora-detail-sidebar"><h2>'+safe(tr('资产档案','Asset metadata'))+'</h2>'+
      '<dl><dt>'+safe(tr('科研阶段','Stages'))+'</dt><dd>'+e.stages.map(x=>safe(facetText('stages',x))).join(' · ')+'</dd>'+
      '<dt>'+safe(tr('领域','Domains'))+'</dt><dd>'+e.domains.map(x=>safe(facetText('domains',x))).join(' · ')+'</dd>'+
      '<dt>'+safe(tr('使用性质','Reuse'))+'</dt><dd>'+safe(e.rights?.reuse || 'unknown')+'</dd>'+
      '<dt>'+safe(tr('第三方图片','Third-party media'))+'</dt><dd>'+safe(tr('未在本站重新分发','Not redistributed by this site'))+'</dd></dl>'+
      '<div class="ora-detail-links">'+Object.entries(e.links || {}).map(([key,url])=>link(url,{source:tr('原始来源','Original source'),paper:tr('论文','Paper'),editable:tr('获取可编辑文件/说明','Editable source / instructions')}[key] || key)).join('')+'</div>'+
      '<button type="button" id="ora-copy-brief">'+safe(tr('复制给 AI 的使用说明','Copy AI usage brief'))+'</button>'+
      (related.length?'<div class="ora-related"><h3>'+safe(tr('关联资产','Related asset'))+'</h3><a href="asset.html?id='+encodeURIComponent(related[0].id)+'">'+safe(related[0].title)+' →</a></div>':'')+
      '</aside></div>';
    document.getElementById('ora-copy-brief')?.addEventListener('click',async ()=>{
      const lines=['Asset: '+e.title,'URL: '+location.href,'Tasks: '+e.tasks.join(', '),
        'Use when: '+(local(app.use_when)||[]).join('；'),'Learn: '+(local(app.learn)||[]).join('；'),
        'Avoid: '+(local(app.avoid)||[]).join('；'),
        'Source: '+(e.links?.source || ''),'Rights: '+(e.rights?.reuse || '')];
      const button=document.getElementById('ora-copy-brief');
      try {await navigator.clipboard.writeText(lines.join('\n'));button.textContent=tr('已复制','Copied');}
      catch(_) {button.textContent=tr('复制失败，请打开 AI 目录获取文本','Copy blocked: use AI catalog');}
    });
  }
  function render() {if(!catalog)return;prepareFilters();renderGrid();renderDetail();}
  const inline=document.getElementById('ora-catalog-data');
  const load=inline ? Promise.resolve(JSON.parse(inline.textContent)) :
    fetch('catalog/index.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json();});
  load.then(data=>{if(!data || !Array.isArray(data.entries))throw Error('Invalid asset catalog');
    catalog=data;render();window.addEventListener('ora-language-change',render);
  }).catch(err=>{const message=tr('资产目录加载失败。请通过 HTTP 本地服务器或在线网站访问。','Catalog unavailable. Serve this site over HTTP.');
    if(grid)grid.innerHTML='<p class="empty-state">'+safe(message)+'</p>';
    if(detail)detail.innerHTML='<p>'+safe(message)+'</p>';
    console.error('OpenResearchAssets catalog:',err);
  });
})();
