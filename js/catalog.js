/* OpenResearchAssets browser: single source of truth is /catalog/index.json. */
(() => {
  'use strict';
  const grid = document.getElementById('reference-grid');
  const detail = document.getElementById('asset-detail');
  if (!grid && !detail) return;

  let catalog = null;
  let filtersReady = false;
  let showAll = false;
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
    const rights=entry.rights || {};
    const visual=entry.visual || {};
    if (visual.kind==='licensed-paper-figure' &&
        /^assets\/third-party\/[a-z0-9-]+\/[a-z0-9-]+\.png$/.test(visual.src || '')) {
      return '<div class="ora-preview ora-official"><img loading="eager" decoding="async" src="'+safe(visual.src)+'" alt="'+safe(local(visual.alt))+'">'+
        '<span class="ora-curated-mark">'+safe(tr('官方原图 · CC BY 4.0','OFFICIAL FIGURE · CC BY 4.0'))+'</span></div>';
    }
    if (visual.kind==='authored-analysis' &&
      /^assets\/editorials\/[a-z0-9-]+\.svg$/.test(visual.src || '')) {
      return '<div class="ora-preview ora-curated"><img loading="eager" decoding="async" src="'+safe(visual.src)+'" alt="'+safe(local(visual.alt))+'">'+
        '<span class="ora-curated-mark">'+safe(tr('原创分析图','ORIGINAL ANALYSIS'))+'</span></div>';
    }
    if (rights.preview==='original-svg' && /^assets\/templates\/[\w-]+\.svg$/.test(entry.links?.editable || '')) {
      return '<div class="ora-preview ora-template"><img loading="lazy" decoding="async" alt="'+safe(tr('原创可编辑 SVG','Editable original SVG'))+'" src="'+safe(entry.links.editable)+'"><span class="ora-curated-mark">'+safe(tr('原创可编辑 · SVG','EDITABLE ORIGINAL · SVG'))+'</span></div>';
    }
    if(entry.kind==='resource-index') {
      const terms=(local(entry.keywords)||[]).slice(0,3);
      return '<div class="ora-preview ora-directory"><div class="ora-cover-panel"><div class="ora-cover-eyebrow">'+
        safe(tr('RESOURCE DIRECTORY  /  EXPLORE','RESOURCE DIRECTORY  /  EXPLORE'))+'</div>'+
        '<strong class="ora-cover-heading">'+safe(entry.title)+'</strong>'+
        '<div class="ora-directory-hits">'+terms.map((w,i)=>'<div class="ora-hit"><b>'+String(i+1).padStart(2,'0')+'</b><span>'+safe(w)+'</span><i></i></div>').join('')+'</div></div>'+
        '<span class="ora-curated-mark">'+safe(tr('外部资源 · 参考','EXTERNAL REFERENCE'))+'</span></div>';
    }
    if(entry.kind==='workflow') {
      const skill=entry.id==='quality-critic-skill';
      const lessons=(local(entry.applicability?.learn)||[]).slice(0,3);
      return '<div class="ora-preview '+(skill?'ora-skill-preview':'ora-workflow-preview')+'"><div class="ora-cover-panel">'+
        '<div class="ora-cover-eyebrow">'+safe(skill?tr('REVIEW PROTOCOL / SKILL','REVIEW PROTOCOL / SKILL'):tr('RESEARCH WORKFLOW','RESEARCH WORKFLOW'))+'</div>'+
        '<strong class="ora-cover-heading">'+safe(entry.title.split('/')[0].trim())+'</strong>'+
        '<div class="ora-cover-steps">'+lessons.map((w,i)=>'<div class="ora-cover-step" title="'+safe(w)+'"><b>'+String(i+1).padStart(2,'0')+'</b><span>'+safe(w)+'</span></div>').join('')+'</div></div>'+
        '<span class="ora-curated-mark">'+safe(skill?tr('审核规范 · 非自动审图','REVIEW PROTOCOL · MANUAL'):tr('工作流程 · 可阅读','READABLE WORKFLOW'))+'</span></div>';
    }
    return '<div class="ora-preview ora-empty"><span>'+safe(tr('暂无经审查的预览 · 请阅读资产详情','No reviewed preview · Read asset details'))+'</span></div>';
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
    if(search) {search.value=params.get('q') || '';search.addEventListener('input',()=>{showAll=false;renderGrid();});}
    ['facet-stage','facet-kind','facet-domain'].forEach(id=>document.getElementById(id)?.addEventListener('change',()=>{showAll=false;renderGrid();}));
    document.querySelectorAll('[data-task-query]').forEach(b=>b.addEventListener('click',()=>{
      if(!search)return;
      search.value=b.dataset.taskQuery;showAll=false;renderGrid();search.focus();
    }));
    document.getElementById('facet-reset')?.addEventListener('click',()=>{
      search.value='';
      ['facet-stage','facet-kind','facet-domain'].forEach(id=>{document.getElementById(id).value='';});
      showAll=false;renderGrid();
    });
    document.getElementById('catalog-more')?.addEventListener('click',()=>{showAll=true;renderGrid();});
  }
  function allSearch(entry) {
    const a=entry.applicability || {};
    return [entry.id,entry.title,entry.kind,...entry.stages,...entry.domains,...entry.tasks,
      ...(entry.keywords?.zh || []),...(entry.keywords?.en || []),entry.description?.zh,entry.description?.en,
      ...(a.use_when?.zh || []),...(a.use_when?.en || []),
      ...(a.learn?.zh || []),...(a.learn?.en || []),
      ...(entry.caseStudy?.composition?.zh || []),...(entry.caseStudy?.composition?.en || []),
      ...(entry.caseStudy?.reuseSteps?.zh || []),...(entry.caseStudy?.reuseSteps?.en || [])].filter(Boolean).join(' ').toLowerCase();
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
    const shown = (!q && !stage && !kindSelect && !domain && !showAll) ? items.slice(0,9) : items;
    grid.innerHTML=shown.length ? shown.map(e=>'<article class="ora-resource-card">'+
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
    if(status)status.textContent=tr('已显示 ','Showing ')+shown.length+' / '+catalog.entries.length+
      tr(' 项 · 第三方图像未复制入库，预览为本站原创结构示意。',' entries · Third-party images are not copied; structural previews are authored.');
    const more=document.getElementById('catalog-more');
    if(more) more.hidden = (shown.length === items.length);
    const count=document.getElementById('catalog-count');
    if(count) count.textContent=String(catalog.entries.length);
    const u=new URL(location.href); q?u.searchParams.set('q',q):u.searchParams.delete('q');
    for(const [key,value] of [['stage',stage],['kind',kindSelect],['domain',domain]]) {
      value?u.searchParams.set(key,value):u.searchParams.delete(key);
    }
    // file:// and inline-browser-test documents may not permit history updates.
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      try { history.replaceState(null,'',u.pathname+u.search+u.hash); }
      catch (err) { console.warn('Catalog URL state unavailable:',err); }
    }
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
    const study=e.caseStudy;
    const editorial=study ? '<section class="ora-case-study"><div class="ora-case-intro"><span>'+safe(tr('CASE STUDY / DESIGN EVIDENCE','CASE STUDY / DESIGN EVIDENCE'))+'</span><h2>'+safe(tr('为什么这个案例值得研究？','What makes this case worth studying?'))+'</h2><p>'+safe(local(study.insight))+'</p></div>'+
      '<div class="ora-study-grid"><section><h3>'+safe(tr('视觉与信息结构','Visual / information structure'))+'</h3>'+points(local(study.composition))+'</section>'+
      '<section><h3>'+safe(tr('迁移到自己论文的步骤','How to transfer the design'))+'</h3>'+points(local(study.reuseSteps))+'</section></div>'+
      '<div class="ora-case-check"><h3>'+safe(tr('事实、风险与授权检查','Scientific and rights checks'))+'</h3>'+points(local(study.verification))+'</div></section>' : '';
    const baseLessons='<div class="ora-lesson"><h2>'+safe(tr('什么时候使用','When to use'))+'</h2>'+points(local(app.use_when))+'</div>'+
      (study ? '' : '<div class="ora-lesson"><h2>'+safe(tr('值得学习的做法','Transferable lessons'))+'</h2>'+points(local(app.learn))+'</div>'+
        '<div class="ora-lesson"><h2>'+safe(tr('需要避免','What to avoid'))+'</h2>'+points(local(app.avoid))+'</div>');
    const rightsNote=e.visual?.kind==='licensed-paper-figure'
      ? tr('原作者图像 · 依据论文 CC BY 4.0 收录 · 保留署名','Third-party figure · copied under paper CC BY 4.0 with attribution')
      : e.kind==='editable-template' || (e.kind==='workflow' && e.rights?.third_party_media==='none')
      ? tr('本站原创资产，不含第三方图像','Original site asset, no third-party image')
      : tr('仅供学习参考，第三方原图未在本站再分发','Reference only; external artwork not republished');
    detail.innerHTML='<div class="ora-detail-heading"><p class="ora-eyebrow">'+safe(kind(e))+' / '+safe(e.id)+'</p>'+
      '<h1>'+safe(e.title)+'</h1><p>'+safe(local(e.description))+'</p></div>'+
      '<div class="ora-detail-grid"><section class="ora-detail-main"><div class="ora-detail-preview">'+media(e)+'</div>'+(e.visual ? '<p class="ora-disclosure">'+safe(local(e.visual.label))+' · '+
        (e.visual.kind==='licensed-paper-figure'
          ? safe(tr('原始论文许可 CC BY 4.0；作者与来源见右侧档案。','Paper license CC BY 4.0; attribution and source appear in the metadata.'))
          : safe(tr('请打开官方来源查看原始视觉内容','Open the official source to inspect the original artwork')))+
        ' · <a href="'+safe(e.visual.src)+'" target="_blank" rel="noopener noreferrer">'+
        safe(e.visual.kind==='licensed-paper-figure'?tr('查看真实原图','View the authentic figure'):tr('放大查看本站分析 SVG','Open full-size analysis SVG'))+' ↗</a></p>' : '')+baseLessons+editorial+'</section>'+
      '<aside class="ora-detail-sidebar"><h2>'+safe(tr('资产档案','Asset metadata'))+'</h2>'+
      '<dl><dt>'+safe(tr('科研阶段','Stages'))+'</dt><dd>'+e.stages.map(x=>safe(facetText('stages',x))).join(' · ')+'</dd>'+
      '<dt>'+safe(tr('领域','Domains'))+'</dt><dd>'+e.domains.map(x=>safe(facetText('domains',x))).join(' · ')+'</dd>'+
      '<dt>'+safe(tr('使用性质','Reuse'))+'</dt><dd>'+safe(e.rights?.reuse || 'unknown')+'</dd>'+
      '<dt>'+safe(tr('素材来源与边界','Asset media status'))+'</dt><dd>'+safe(rightsNote)+'</dd>'+
      (e.visual?.kind==='licensed-paper-figure'?'<dt>'+safe(tr('图片署名','Figure credit'))+'</dt><dd>'+safe(e.rights?.attribution||'')+'</dd>'+
        '<dt>'+safe(tr('图片修改','Image modifications'))+'</dt><dd>'+safe(tr('未修改','Unmodified'))+'</dd>':'')+'</dl>'+
      '<div class="ora-detail-links">'+Object.entries(e.links || {}).map(([key,url])=>link(url,{source:tr('原始来源','Original source'),paper:tr('论文','Paper'),officialFigure:tr('官方媒体原图','Original upstream figure'),license:tr('授权条款 CC BY 4.0','License CC BY 4.0'),editable:tr('获取可编辑文件/说明','Editable source / instructions')}[key] || key)).join('')+
      '<a href="catalog/entries/'+encodeURIComponent(e.id)+'.json" target="_blank" rel="noopener noreferrer">'+safe(tr('供 AI 使用的单项 JSON','Single-entry JSON for AI'))+' ↗</a></div>'+
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
