/* OpenResearchAssets browser: single source of truth is /catalog/index.json. */
(() => {
  'use strict';
  const grid = document.getElementById('reference-grid');
  const detail = document.getElementById('asset-detail');
  if (!grid && !detail) return;

  let catalog = null;
  let filtersReady = false;
  let showAll = false;
  let skillsExpanded = false;
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
  // 投稿身份与收录时间分离；历史不可核实的信息不推测。
  const contributorName = entry => {
    const name=entry.submission?.github;
    return typeof name==='string' && /^[a-z\d](?:[a-z\d-]{0,38})$/i.test(name) ? name : '';
  };
  const evidenceUrl = value => {
    const u=safeUrl(value);
    return /^https:\/\/github\.com\/OpenResearchAssets\/openresearchassets\.github\.io\/(?:issues|pull)\/\d+$/.test(u) ? u : '';
  };
  function provenance(entry, detailed=false) {
    const user=contributorName(entry);
    const date=entry.submission?.added_on;
    const verifiedDate=typeof date==='string' && /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : '';
    if(!user && !verifiedDate && !detailed) return '';
    const userPart=user
      ? '<a class="ora-contributor" href="https://github.com/'+safe(user)+'" target="_blank" rel="noopener noreferrer"><img src="https://github.com/'+safe(user)+'.png?size=40" alt="" width="20" height="20" loading="lazy">@'+safe(user)+'</a>'
      : safe(tr('历史档案 · 投稿者未记录','Legacy record · contributor not recorded'));
    const datePart=verifiedDate
      ? '<time datetime="'+safe(verifiedDate)+'">'+safe(verifiedDate)+'</time>'
      : safe(tr('历史收录日期待追溯','Historical publication date not verified'));
    const review=evidenceUrl(entry.submission?.issue_url);
    return '<div class="ora-provenance"><span>'+safe(tr('投稿','Submitted by'))+' '+userPart+'</span><span>'+safe(tr('收录','Added on'))+' '+datePart+'</span>'+
      (review?'<a href="'+safe(review)+'" target="_blank" rel="noopener noreferrer">'+safe(tr('审核记录','Review history'))+' ↗</a>':'')+'</div>';
  }

  function media(entry) {
    const rights=entry.rights || {};
    const visual=entry.visual || {};
    const verified=(visual.kind==='verified-paper-figure'||visual.kind==='verified-site-screenshot') &&
      /^assets\/third-party\/[a-z0-9-]+\/[a-z0-9-]+\.jpg$/.test(visual.src || '');
    if(verified) {
      return '<div class="ora-preview ora-verified '+(visual.kind==='verified-paper-figure'?'ora-paper-fig':'ora-site-capture')+'">'+
        '<img loading="eager" decoding="async" src="'+safe(visual.src)+'" alt="'+safe(local(visual.alt))+'">'+
        '<span class="ora-curated-mark">'+safe(local(visual.label))+'</span></div>';
    }
    const localLicensed=(visual.kind==='licensed-source-image'||visual.kind==='licensed-paper-figure') &&
      /^assets\/third-party\/[a-z0-9-]+\/[a-z0-9-]+\.png$/.test(visual.src || '');
    const remote=visual.kind==='external-reference-image' &&
      /^https:\/\/(?:depth-anything-3\.github\.io|media\.luminis-sim\.com|tianxingchen\.github\.io|supermimic\.github\.io|raw\.githubusercontent\.com|instruct-pix2pix\.timothybrooks\.com|opengraph\.githubassets\.com|figures\.semanticscholar\.org|moveit\.ai)\//.test(visual.src || '');
    if(localLicensed||remote){
      const caption=local(localLicensed ? visual.label : visual.alt);
      const mark=local(visual.label);
      return '<div class="ora-preview '+(remote?'ora-external':'ora-official')+'"><img '+(remote?'loading="lazy" ':'loading="eager" ')+'decoding="async" '+(remote?'referrerpolicy="no-referrer" ':'')+'src="'+safe(visual.src)+'" alt="'+safe(caption)+'" onerror="this.closest(\'.ora-preview\').classList.add(\'ora-image-error\')">'+
        '<span class="ora-curated-mark">'+safe(mark)+'</span><span class="ora-image-fallback">'+safe(tr('来源图片暂不可加载，请打开原始网站查看','Source image unavailable; open the original website'))+'</span></div>';
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
    const original=node.value || (selectId.startsWith('facet-') ? params.get(selectId.replace('facet-','')) : '') || '';
    node.innerHTML='<option value="">'+safe(tr(group==='stages'?'全部阶段':group==='kinds'?'全部类型':group==='topics'?'全部主题':'全部领域',group==='stages'?'All stages':group==='kinds'?'All types':group==='topics'?'All topics':'All domains'))+'</option>'+
      Object.entries(facets()[group] || {}).filter(([key])=>group!=='kinds'||key!=='workflow').map(([key,v])=>'<option value="'+safe(key)+'">'+safe(local(v))+'</option>').join('');
    node.value=original;
  }
  function prepareFilters() {
    ['stages','kinds','domains','topics'].forEach((key,i)=>options(['facet-stage','facet-kind','facet-domain','facet-topic'][i],key));
    options('skill-domain','domains');options('skill-topic','topics');
    const kindSelect=document.getElementById('skill-type');
    if(kindSelect){const active=kindSelect.value;kindSelect.innerHTML='<option value="">'+safe(tr('全部类型','All types'))+'</option>'+
      [['skill','Skill'],['tool',tr('工具 / 框架','Tool / framework')],['workflow','Workflow']].map(([v,label])=>'<option value="'+v+'">'+safe(label)+'</option>').join('');kindSelect.value=active;}
    renderSkillChips();
    if (filtersReady) return;
    filtersReady=true;
    const search=document.getElementById('reference-search');
    if(search) {search.value=params.get('q') || '';search.addEventListener('input',()=>{showAll=false;renderGrid();});}
    ['facet-stage','facet-kind','facet-domain','facet-topic'].forEach(id=>document.getElementById(id)?.addEventListener('change',()=>{showAll=false;renderGrid();}));
    document.getElementById('skill-search')?.addEventListener('input',()=>{skillsExpanded=false;renderSkills();});
    ['skill-domain','skill-topic','skill-type'].forEach(id=>document.getElementById(id)?.addEventListener('change',()=>{skillsExpanded=false;renderSkills();}));
    document.getElementById('skill-topic-chips')?.addEventListener('click',event=>{
      const btn=event.target.closest('button[data-topic]');
      if(!btn)return;
      const select=document.getElementById('skill-topic');if(select)select.value=btn.dataset.topic;
      skillsExpanded=false;renderSkillChips();renderSkills();
    });
    document.getElementById('skill-reset')?.addEventListener('click',()=>{
      document.getElementById('skill-search').value='';
      ['skill-domain','skill-topic','skill-type'].forEach(id=>{document.getElementById(id).value='';});
      skillsExpanded=false;renderSkillChips();renderSkills();
    });
    document.getElementById('skill-more')?.addEventListener('click',()=>{skillsExpanded=true;renderSkills();});
    document.querySelectorAll('[data-task-query]').forEach(b=>b.addEventListener('click',()=>{
      if(!search)return;
      search.value=b.dataset.taskQuery;showAll=false;renderGrid();search.focus();
    }));
    document.getElementById('facet-reset')?.addEventListener('click',()=>{
      search.value='';
      ['facet-stage','facet-kind','facet-domain','facet-topic'].forEach(id=>{document.getElementById(id).value='';});
      showAll=false;renderGrid();
    });
    document.getElementById('catalog-more')?.addEventListener('click',()=>{showAll=true;renderGrid();});
  }
  function allSearch(entry) {
    const a=entry.applicability || {};
    return [entry.id,entry.title,entry.kind,...entry.stages,...entry.domains,...(entry.topics||[]),...entry.tasks,
      ...(entry.keywords?.zh || []),...(entry.keywords?.en || []),entry.description?.zh,entry.description?.en,
      ...(a.use_when?.zh || []),...(a.use_when?.en || []),
      ...(a.learn?.zh || []),...(a.learn?.en || []),
      ...(entry.caseStudy?.composition?.zh || []),...(entry.caseStudy?.composition?.en || []),
      ...(entry.caseStudy?.reuseSteps?.zh || []),...(entry.caseStudy?.reuseSteps?.en || [])].filter(Boolean).join(' ').toLowerCase();
  }

  const isGallery=e=>e.kind==='visual-reference'||e.kind==='website-reference'||
    e.kind==='editable-template'||(e.kind==='resource-index'&&e.id!=='research-skills-directory');
  const galleryList=()=>catalog.entries.filter(isGallery);
  function renderSkillChips() {
    const mount=document.getElementById('skill-topic-chips');
    if(!mount||!catalog)return;
    const list=catalog.entries.filter(e=>e.kind==='workflow'&&['popular','practice'].includes(e.curation?.track));
    const counts=new Map();
    list.forEach(e=>(e.topics||[]).forEach(k=>counts.set(k,(counts.get(k)||0)+1)));
    const top=[...counts].sort((a,b)=>b[1]-a[1]).slice(0,8);
    const active=document.getElementById('skill-topic')?.value||'';
    mount.innerHTML='<button type="button" data-topic="" class="'+(active?'':'is-active')+'" aria-pressed="'+(!active)+'">'+safe(tr('全部主题','All topics'))+'</button>'+
      top.map(([topic,n])=>'<button type="button" data-topic="'+safe(topic)+'" class="'+(active===topic?'is-active':'')+'" aria-pressed="'+(active===topic)+'">'+safe(facetText('topics',topic))+' <span>'+n+'</span></button>').join('');
  }
  function getSkillFilters() {
    return {q:document.getElementById('skill-search')?.value.trim().toLowerCase()||'',
      domain:document.getElementById('skill-domain')?.value||'',
      topic:document.getElementById('skill-topic')?.value||'',
      type:document.getElementById('skill-type')?.value||''};
  }
  const starCounts=new Map();
  let refreshingStars=false;
  const starText=n=>Number(n).toLocaleString('en-US');
  function renderSkills() {
    if (!catalog) return;
    const popular=document.getElementById('popular-skills');
    const practice=document.getElementById('practice-skills');
    if (!popular && !practice) return;
    const card=e=>{
      const c=e.curation||{};
      const repo=c.github_repo||'';
      const star=Number.isInteger(c.stars_snapshot)
        ? '<span class="ora-skill-stars" data-star-repo="'+safe(repo)+'" data-star-scope="'+safe(c.star_scope||'repository')+'" aria-label="'+safe(tr('GitHub 仓库 Stars','GitHub repository stars'))+'"><b>★ '+safe(starText(starCounts.get(repo)??c.stars_snapshot))+'</b><small>'+safe(c.star_scope==='parent-repository'?tr('母仓库 Star','Parent repo stars'):tr('仓库 Star','Repo stars'))+' · '+safe(starCounts.has(repo)?tr('实时','live'):c.stars_checked_on)+'</small></span>'
        : '';
      const proof=c.track==='practice' ? '<div class="ora-skill-evidence"><span>'+safe(tr('公开实践证据','Public usage evidence'))+'</span>'+
        (c.evidence||[]).slice(0,2).map(p=>'<a href="'+safe(p)+'" target="_blank" rel="noopener noreferrer">'+safe(p.split('/').pop())+' ↗</a>').join('')+'</div>' : '';
      const state=c.track==='popular'?(e.trial?tr('已有任务试运行 · 非自动调用 Skill','Source-guided trial · no native Skill invocation'):tr('外部高热度 · 未经本站亲测','Popular external · not tested here')):tr('已有公开项目产物 · 未做独立效益评测','Public project artifacts · no independent evaluation');
      const typeLabel=c.type==='skill'?(c.star_scope==='parent-repository'?tr('独立 Skill','Individual Skill'):tr('Skill 集合','Skill collection')):({tool:tr('工具 / 框架','Tool / framework'),workflow:'Workflow'}[c.type]||tr('待分类','Unclassified'));
      const topical=(e.topics||[]).slice(0,2).map(k=>'<span>'+safe(facetText('topics',k))+'</span>').join('');
      const context=e.domains.slice(0,2).map(k=>'<span>'+safe(facetText('domains',k))+'</span>').join('');
      return '<article class="ora-skill-card"><div class="ora-skill-meta"><span>'+safe(typeLabel)+'</span>'+star+'</div>'+
       '<h4><a href="asset.html?id='+encodeURIComponent(e.id)+'">'+safe(e.title)+'</a></h4>'+
       '<p>'+safe(local(e.description))+'</p>'+(e.execution?.outputs?'<p class="ora-skill-output"><strong>'+safe(tr('产出','Output'))+'</strong>'+safe((local(e.execution.outputs)||[])[0]||'')+'</p>':'')+
       '<div class="ora-skill-tags">'+context+topical+'</div>'+provenance(e)+'<p class="ora-skill-status">'+safe(state)+'</p>'+
       (e.trial?.run_url?'<p class="ora-skill-trial"><a target="_blank" rel="noopener noreferrer" href="'+safe(e.trial.run_url)+'">'+safe(tr('查看真实任务试运行证据','View task-run evidence'))+' ↗</a></p>':'')+proof+
       '<div class="ora-skill-actions"><a href="asset.html?id='+encodeURIComponent(e.id)+'">'+safe(tr('详情与讨论','Details & discussion'))+' ↗</a>'+
       link(e.links?.source,e.execution?.source_file_sha?tr('打开原始 SKILL.md','Open original SKILL.md'):tr('查看源项目','Source'))+'</div></article>';
    };
    const filters=getSkillFilters();
    const active=Boolean(filters.q||filters.domain||filters.topic||filters.type);
    const match=e=>(!filters.domain||e.domains.includes(filters.domain))&&
      (!filters.topic||(e.topics||[]).includes(filters.topic))&&
      (!filters.type||e.curation?.type===filters.type)&&
      filters.q.split(/\s+/).filter(Boolean).every(w=>allSearch(e).includes(w));
    const allPopular=catalog.entries.filter(e=>e.curation?.track==='popular'&&match(e))
      .sort((a,b)=>b.curation.stars_snapshot-a.curation.stars_snapshot);
    const allPractice=catalog.entries.filter(e=>e.curation?.track==='practice'&&match(e));
    // Homepage preview is intentionally representative of distinct research tasks,
    // not just repeated parent-repository star counts. Filtering and Show all remain complete.
    const featured=allPopular.filter(e=>Number.isInteger(e.curation?.homepage_order))
      .sort((a,b)=>a.curation.homepage_order-b.curation.homepage_order);
    const visiblePopular=(active||skillsExpanded)?allPopular:(featured.length===8?featured:allPopular.slice(0,8));
    if(popular)popular.innerHTML=visiblePopular.map(card).join('')||'<p class="empty-state">'+safe(empty())+'</p>';
    if(practice)practice.innerHTML=allPractice.map(card).join('')||'<p class="empty-state">'+safe(empty())+'</p>';
    const more=document.getElementById('skill-more');
    if(more){more.hidden=active||skillsExpanded||allPopular.length<=8;
      more.textContent=tr('查看全部 ','See all ')+allPopular.length+tr(' 项高热度资源',' popular resources');}
    const status=document.getElementById('skill-status');
    if(status)status.textContent=tr('匹配 ','Matching ')+(allPopular.length+allPractice.length)+' / '+
      catalog.entries.filter(e=>['popular','practice'].includes(e.curation?.track)).length+tr(' 项正式精选',' curated selections');
    renderSkillChips();
    if(!popular||refreshingStars||location.protocol==='file:')return;
    const repos=[...new Set(catalog.entries.filter(e=>e.curation?.track==='popular')
      .map(e=>e.curation.github_repo).filter(x=>typeof x==='string'&&x.includes('/')))];
    if(repos.every(x=>starCounts.has(x)))return;
    refreshingStars=true;
    Promise.all(repos.filter(x=>!starCounts.has(x)).map(async repo=>{
      try{
        const response=await fetch('https://api.github.com/repos/'+repo,{headers:{Accept:'application/vnd.github+json'}});
        if(!response.ok)return;
        const data=await response.json();
        if(Number.isInteger(data.stargazers_count)&&data.stargazers_count>=0)starCounts.set(repo,data.stargazers_count);
      }catch(_){}
    })).finally(()=>{
      refreshingStars=false;
      popular.querySelectorAll('[data-star-repo]').forEach(node=>{
        const repo=node.dataset.starRepo;
        if(starCounts.has(repo))node.innerHTML='<b>★ '+safe(starText(starCounts.get(repo)))+'</b><small>'+safe(node.dataset.starScope==='parent-repository'?tr('母仓库 Star','Parent repo stars'):tr('仓库 Star','Repo stars'))+' · '+safe(tr('实时','live'))+'</small>';
      });
    });
  }
  const visualCategory = e => {
    const labels={
      'teaser':[ 'Teaser','Teaser'],
      'results':['结果展示','Results'],
      'ablation':['消融实验','Ablation'],
      'project-site':['交互主页','Project site'],
      'experimental-setup':['实验设置','Experimental setup'],
      'spatial-visualization':['空间可视化','Spatial visualization']
    };
    const name=e.curation?.visual_category;
    const label=labels[name];
    return label ? tr(label[0],label[1]) : '';
  };
  function renderFeaturedSites() {
    const mount=document.getElementById('featured-project-sites');
    if(!mount || !catalog)return;
    const sites=catalog.entries.filter(e=>e.kind==='website-reference' && e.curation?.visual_category==='project-site');
    mount.innerHTML=sites.map(e=>{
      const source=safeUrl(e.links?.source);
      if(!source)return '';
      return '<article class="ora-featured-site">'+
        '<a class="ora-featured-preview" href="'+safe(source)+'" target="_blank" rel="noopener noreferrer" aria-label="'+safe(tr('打开官方研究主页：','Visit original research site: ')+e.title)+'">'+media(e)+'</a>'+
        '<div class="ora-featured-info"><p class="ora-featured-eyebrow">'+safe(tr('可交互研究主页','Interactive research site'))+'</p>'+
        '<h4><a href="'+safe(source)+'" target="_blank" rel="noopener noreferrer">'+safe(e.title.split(' · ')[0])+' ↗</a></h4>'+
        '<p>'+safe(local(e.description))+'</p>'+provenance(e)+
        '<div class="ora-featured-actions"><a class="ora-open-source" href="'+safe(source)+'" target="_blank" rel="noopener noreferrer">'+safe(tr('立即打开原作者网站','Visit official site'))+' ↗</a>'+
        '<a href="asset.html?id='+encodeURIComponent(e.id)+'">'+safe(tr('详情与讨论','Details & discussion'))+' →</a></div></div></article>';
    }).join('') || '<p class="empty-state">'+safe(empty())+'</p>';
  }

  function renderGrid() {
    if (!grid || !catalog) return;
    const q=document.getElementById('reference-search')?.value.trim().toLowerCase() || '';
    const stage=document.getElementById('facet-stage')?.value || '';
    const kindSelect=document.getElementById('facet-kind')?.value || '';
    const domain=document.getElementById('facet-domain')?.value || '';
    const topic=document.getElementById('facet-topic')?.value || '';
    const words=q.split(/\s+/).filter(Boolean);
    const weight={ 'visual-reference':0,'website-reference':0,'editable-template':1,'resource-index':2 };
    const items=galleryList().sort((a,b)=>weight[a.kind]-weight[b.kind]).filter(e=>(!stage || e.stages.includes(stage)) &&
      (!kindSelect || e.kind===kindSelect) && (!domain || e.domains.includes(domain)) && (!topic || (e.topics||[]).includes(topic)) &&
      words.every(w=>allSearch(e).includes(w)));
    const shown = (!q && !stage && !kindSelect && !domain && !topic && !showAll) ? items.slice(0,9) : items;
    grid.innerHTML=shown.length ? shown.map(e=>{
      const source=safeUrl(e.links?.source);
      const details='asset.html?id='+encodeURIComponent(e.id);
      const href=source || details;
      const ext=source ? ' target="_blank" rel="noopener noreferrer"' : '';
      const figure=safeUrl(e.links?.officialFigure);
      return '<article class="ora-resource-card">'+
        '<a class="ora-resource-visual" href="'+safe(href)+'"'+ext+' aria-label="'+safe(tr('直接打开原作者：','Open original project: ')+e.title)+'">'+media(e)+'</a>'+
        '<div class="ora-resource-content"><div class="ora-resource-kicker">'+safe(visualCategory(e)||kind(e))+' · '+safe(e.year || '')+'</div>'+
        '<h3><a href="'+safe(href)+'"'+ext+'>'+safe(e.title)+'</a></h3>'+
        '<p>'+safe(local(e.description))+'</p>'+provenance(e)+
        '<div class="ora-tag-row">'+e.stages.slice(0,2).map(x=>'<span>'+safe(facetText('stages',x))+'</span>').join('')+
        e.domains.slice(0,1).map(x=>'<span>'+safe(facetText('domains',x))+'</span>').join('')+(e.topics||[]).slice(0,1).map(x=>'<span>'+safe(facetText('topics',x))+'</span>').join('')+'</div>'+
        '<div class="ora-resource-actions">'+
        (source ? '<a class="ora-open-source" href="'+safe(source)+'" target="_blank" rel="noopener noreferrer">'+safe(tr('直达原作者主页','Open original site'))+' ↗</a>' : '')+
        (figure && figure!==source ? '<a href="'+safe(figure)+'" target="_blank" rel="noopener noreferrer">'+safe(tr('查看原图','View original figure'))+' ↗</a>' : '')+
        '<a class="ora-open-details" href="'+safe(details)+'">'+safe(tr('详情与讨论','Details & discussion'))+' →</a>'+
        '</div></div></article>';
    }).join('') :
      '<p class="empty-state">'+safe(empty())+'</p>';
    const status=document.getElementById('reference-status');
    if(status)status.textContent=tr('已显示 ','Showing ')+shown.length+' / '+galleryList().length+
      tr(' 项 · ',' entries · ')+catalog.entries.filter(e=>['licensed-source-image','external-reference-image','verified-paper-figure','verified-site-screenshot'].includes(e.visual?.kind)).length+tr(' 项真实来源视觉参考；外部媒体版权仍属原权利人。',' authentic source-media previews; linked media rights remain with original owners.');
    const more=document.getElementById('catalog-more');
    if(more) more.hidden = (shown.length === items.length);
    const count=document.getElementById('catalog-count');
    if(count) count.textContent=String(galleryList().length);
    const u=new URL(location.href); q?u.searchParams.set('q',q):u.searchParams.delete('q');
    for(const [key,value] of [['stage',stage],['kind',kindSelect],['domain',domain],['topic',topic]]) {
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
    const exec=e.execution;
    const executionGuide=exec ? '<section class="ora-execution"><div class="ora-execution-head"><span>'+safe(e.trial?tr('有公开试运行 · 未自动调用 Skill','SOURCE-GUIDED TRIAL · NO NATIVE SKILL INVOCATION'):tr('来源已核实 · 未实际运行','SOURCE REVIEWED · NOT EXECUTED'))+'</span>'+
      '<h2>'+safe(tr('如何使用这项能力','How to use this capability'))+'</h2>'+
      '<p>'+safe(tr('这是一份根据上游 SKILL.md 整理的用法提要，不是已安装的 Skill；请在执行前复核原文、当前依赖、权限与许可。','This is a curated note from the original SKILL.md, not an installed skill. Recheck current dependencies, permissions and license.'))+'</p></div>'+
      '<div class="ora-execution-grid"><div><h3>'+safe(tr('需要准备','Inputs'))+'</h3>'+points(local(exec.inputs))+'</div>'+
      '<div><h3>'+safe(tr('预期产出','Outputs'))+'</h3>'+points(local(exec.outputs))+'</div>'+
      '<div><h3>'+safe(tr('运行条件','Requirements'))+'</h3>'+points(local(exec.requirements))+'</div>'+
      '<div><h3>'+safe(tr('如何验收','Checks'))+'</h3>'+points(local(exec.checks))+'</div></div>'+
      '<h3>'+safe(tr('操作步骤','Steps'))+'</h3><ol class="ora-execution-steps">'+(local(exec.steps)||[]).map(v=>'<li>'+safe(v)+'</li>').join('')+'</ol>'+
      '<div class="ora-execution-actions">'+link(e.links?.source,tr('打开完整 SKILL.md','Read full SKILL.md'))+
      '<button type="button" id="ora-copy-execution">'+safe(tr('复制使用说明','Copy usage brief'))+'</button></div>'+
      '<p class="ora-execution-provenance">'+safe(tr('上游文件 Blob SHA','Upstream file blob SHA'))+': <code>'+safe(exec.source_file_sha||'')+'</code> · '+safe(exec.source_checked_on||'')+'</p></section>' : '';
    const trialEvidence=e.trial?.run_url ? '<aside class="ora-trial-evidence"><h3>'+safe(tr('公开试运行证据','Public trial evidence'))+'</h3>'+
      '<p>'+safe(local(e.trial.summary))+'</p><p>'+safe(tr('这不是 Skill 安装证据，也不是和无 Skill 基线的受控比较。','Not proof of installing a Skill, nor a controlled comparison with a no-Skill baseline.'))+'</p>'+
      '<a href="'+safe(e.trial.run_url)+'" target="_blank" rel="noopener noreferrer">'+safe(tr('查看实际 CI 记录与下载产物','View real CI run and outputs'))+' ↗</a></aside>' : '';
    const baseLessons='<div class="ora-lesson"><h2>'+safe(tr('什么时候使用','When to use'))+'</h2>'+points(local(app.use_when))+'</div>'+
      (study ? '' : '<div class="ora-lesson"><h2>'+safe(tr('值得学习的做法','Transferable lessons'))+'</h2>'+points(local(app.learn))+'</div>'+
        '<div class="ora-lesson"><h2>'+safe(tr('需要避免','What to avoid'))+'</h2>'+points(local(app.avoid))+'</div>');
    const isFigure=e.visual?.kind==='verified-paper-figure';
    const isSite=e.visual?.kind==='verified-site-screenshot';
    const rightsNote=isFigure
      ? (e.rights?.license_url ? tr('论文 Figure 1 · CC BY 4.0 · 已标注截取修改','Paper Figure 1 · CC BY 4.0 · excerpt modifications disclosed') :
          tr('论文 Figure 1 评论性低清预览，原权利归作者，可申请撤除','Paper Figure 1 · contextual low-resolution review, authors retain rights'))
      : isSite ? tr('真实官方主页首屏截图；原网站权利归其作者','Real official project-site first viewport; website rights remain with creators')
      : e.visual?.kind==='external-reference-image'?tr('来自原站的外部真实图片链接，未在本站重新授权','External source image link; not relicensed by this site')
      : e.kind==='editable-template'||(e.kind==='workflow'&&e.rights?.third_party_media==='none')
      ? tr('本站原创资产，不含第三方图像','Original site asset, no third-party image')
      : tr('外部参考或原创分析，按单项版权元数据核对','External reference or authored analysis; review item-specific rights');
    detail.innerHTML='<div class="ora-detail-heading"><p class="ora-eyebrow">'+safe(kind(e))+' / '+safe(e.id)+'</p>'+
      '<h1>'+safe(e.title)+'</h1><p>'+safe(local(e.description))+'</p>'+provenance(e,true)+'</div>'+
      '<div class="ora-detail-grid"><section class="ora-detail-main"><div class="ora-detail-preview">'+media(e)+'</div>'+trialEvidence+executionGuide+(e.analysisVisual ? '<p class="ora-analysis-link"><a target="_blank" rel="noopener noreferrer" href="'+safe(e.analysisVisual.src)+'">'+safe(tr('查看本站原创结构分析 SVG','View authored structure-analysis SVG'))+' ↗</a></p>' : '')+(e.visual ? '<p class="ora-disclosure">'+safe(local(e.visual.label))+' · '+
        (e.figureIdentity ? '<strong>'+safe(e.figureIdentity.original_name)+'</strong> · '+
          safe(tr('原始作者与来源见资产档案；图片是带出处的缩略预览，不是自制科研结果。','See author/source details; this is an attributed preview, not our experiment.')) :
          safe(tr('请打开官方来源核对原始内容','Open the official source to verify original media')))+
        ' · <a href="'+safe(e.figureIdentity?.original_source||e.visual.src)+'" target="_blank" rel="noopener noreferrer">'+
        safe(tr('打开官方原始来源','Open verified original source'))+' ↗</a></p>' : '')+baseLessons+editorial+'</section>'+
      '<aside class="ora-detail-sidebar"><h2>'+safe(tr('资产档案','Asset metadata'))+'</h2>'+
      '<dl>'+(e.submission?.original_author ? '<dt>'+safe(tr('原作者','Original creator'))+'</dt><dd>'+safe(e.submission.original_author)+'</dd>':'')+'<dt>'+safe(tr('科研阶段','Stages'))+'</dt><dd>'+e.stages.map(x=>safe(facetText('stages',x))).join(' · ')+'</dd>'+
      '<dt>'+safe(tr('领域','Domains'))+'</dt><dd>'+e.domains.map(x=>safe(facetText('domains',x))).join(' · ')+'</dd>'+      '<dt>'+safe(tr('主题','Topics'))+'</dt><dd>'+(e.topics||[]).map(x=>safe(facetText('topics',x))).join(' · ')+'</dd>'+      (e.curation?.type?'<dt>'+safe(tr('能力类型','Capability type'))+'</dt><dd>'+safe(e.curation.type)+'</dd>':'')+
      '<dt>'+safe(tr('使用性质','Reuse'))+'</dt><dd>'+safe(e.rights?.reuse || 'unknown')+'</dd>'+
      '<dt>'+safe(tr('素材来源与边界','Asset media status'))+'</dt><dd>'+safe(rightsNote)+'</dd>'+
      (e.figureIdentity?'<dt>'+safe(tr('图像准确身份','Exact image identity'))+'</dt><dd>'+safe(e.figureIdentity.original_name)+'</dd>'+
        '<dt>'+safe(tr('原作者 / 来源','Author / source'))+'</dt><dd>'+safe(e.figureIdentity.credit)+'</dd>'+
        '<dt>'+safe(tr('截图或裁切处理','Preview transformations'))+'</dt><dd>'+safe(e.figureIdentity.modifications)+'</dd>'+
        '<dt>'+safe(tr('获取时间','Reference date'))+'</dt><dd>'+safe(e.figureIdentity.capture_date)+'</dd>':'')+'</dl>'+
      '<div class="ora-detail-links">'+Object.entries(e.links || {}).map(([key,url])=>link(url,{source:tr('原始来源','Original source'),paper:tr('论文','Paper'),officialFigure:tr('原始 Figure / 网页','Original figure / webpage'),license:tr('授权条款 CC BY 4.0','License CC BY 4.0'),editable:tr('获取可编辑文件/说明','Editable source / instructions')}[key] || key)).join('')+
      '<a href="catalog/entries/'+encodeURIComponent(e.id)+'.json" target="_blank" rel="noopener noreferrer">'+safe(tr('供 AI 使用的单项 JSON','Single-entry JSON for AI'))+' ↗</a></div>'+
      '<div class="ora-detail-rights"><p>'+safe(tr('第三方素材归原权利人；署名或免费展示不等于再分发授权。如对展示有异议，可联系撤除或更正。','Third-party materials belong to their rights holders. Attribution and free access do not imply redistribution rights. Request removal or correction if you object.'))+'</p><a href="https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=asset-removal.yml" target="_blank" rel="noopener noreferrer">'+safe(tr('联系撤除 / 更正','Request removal / correction'))+' ↗</a></div>'+
      '<button type="button" id="ora-copy-brief">'+safe(tr('复制给 AI 的使用说明','Copy AI usage brief'))+'</button>'+
      '<p class="ora-community-prompt"><a href="https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=catalog-correction.md" target="_blank" rel="noopener noreferrer">'+safe(tr('反馈此资产 / 纠错','Suggest an improvement / correction'))+' ↗</a> · <a href="https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/new?template=submit-asset.yml" target="_blank" rel="noopener noreferrer">'+safe(tr('推荐另一份优秀资产','Recommend another asset'))+' ↗</a></p>'+
      (related.length?'<div class="ora-related"><h3>'+safe(tr('关联资产','Related asset'))+'</h3><a href="asset.html?id='+encodeURIComponent(related[0].id)+'">'+safe(related[0].title)+' →</a></div>':'')+
      '</aside></div>';
    window.ORA_COMMUNITY?.mount(e.id);
    document.getElementById('ora-copy-execution')?.addEventListener('click',async ()=>{
      if(!exec)return;
      const sections=[['Inputs',exec.inputs],['Outputs',exec.outputs],['Requirements',exec.requirements],
        ['Steps',exec.steps],['Checks',exec.checks]];
      const content=['Skill: '+e.title,'Original: '+(e.links?.source||''),
        'Source reviewed: '+(exec.source_checked_on||''),'Source-only notes: not independently tested.']
        .concat(sections.flatMap(([label,field])=>[label+':',...(local(field)||[]).map(x=>'- '+x)])).join('\n');
      const button=document.getElementById('ora-copy-execution');
      try{await navigator.clipboard.writeText(content);button.textContent=tr('已复制','Copied');}
      catch(_){button.textContent=tr('无法复制，请打开源文件','Clipboard unavailable; open original');}
    });
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
  function render() {if(!catalog)return;prepareFilters();renderFeaturedSites();renderGrid();renderSkills();renderDetail();}
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
