/* Findings: editorial overview + focused ranking, based exclusively on sourced snapshots.
 * A preview never claims to show the whole ranking. Every numeric signal has its own unit.
 */
(() => {
  'use strict';
  const root=document.getElementById('findings-feeds');
  if(!root)return;
  const search=document.getElementById('findings-search');
  const status=document.getElementById('findings-status');
  const updated=document.getElementById('findings-updated');
  const heading=document.getElementById('findings-title');
  const filters=[...document.querySelectorAll('.findings-filter')];
  const PREVIEW_COUNT=3;
  const order=['papers','github','skills','workflows'];
  const definitions={
    papers:{
      kicker:'HUGGING FACE / PAPERS',name:['论文趋势','Trending papers'],
      intro:['Hugging Face 近期热议的论文。关注研究问题与方法，不把社区投票等同于学术影响力。',
             'Papers gaining attention on Hugging Face. Community votes are not citations or research quality.'],
      metric:['社区投票','HF upvotes'],measure:['社区投票，不是引用数','Community votes, not citations'],
      source:['论文趋势榜','Paper trending feed'],symbol:'↗'
    },
    github:{
      kicker:'GITHUB / WEEKLY',name:['GitHub 趋势','GitHub Trending'],
      intro:['GitHub 官方周榜：观察近期快速获得开发者关注的项目。榜单排名与本周新增 Star 都来自原站。',
             'GitHub’s weekly trending repositories. Ranking and weekly star gains come from the source.'],
      metric:['本周新增 Stars','Stars this week'],measure:['本周新增，不是累计总星数','Weekly gain, not lifetime stars'],
      source:['GitHub 周榜','GitHub weekly list'],symbol:'★'
    },
    skills:{
      kicker:'AGENT / SKILLS',name:['热门 Skills','Agent Skills'],
      intro:['追踪近期出现的 Agent Skills。如果来源为 GitHub Search，数字是累计 Stars，不是安装量。',
             'Newly discovered Agent Skills. With GitHub Search as the source, numbers are total stars, not installs.'],
      metric:['累计 Stars','Total stars'],measure:['近 60 天创建的仓库 · 累计 Stars','Repositories created in the last 60 days · total stars'],
      source:['Skills 来源','Skill source'],symbol:'✳'
    },
    workflows:{
      kicker:'RESEARCH / WORKFLOWS',name:['工作流发现','Workflow discoveries'],
      intro:['寻找近期发布的研究及 Agent 工作流。以 GitHub 搜索结果作为发现线索，未经可用性验证。',
             'Recently created research and agent workflows. GitHub search signals, not verified workflow performance.'],
      metric:['累计 Stars','Total stars'],measure:['近 60 天创建的仓库 · 累计 Stars','Repositories created in the last 60 days · total stars'],
      source:['工作流来源','Workflow source'],symbol:'⇄'
    }
  };
  const fallback={
    papers:'https://huggingface.co/papers/trending',
    github:'https://github.com/trending?since=weekly',
    skills:'https://github.com/search?q=topic%3Aagent-skills&type=repositories',
    workflows:'https://github.com/search?q=research+workflow&type=repositories'
  };
  const t=(zh,en)=>document.documentElement.lang==='en'?en:zh;
  const h=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const external=x=>{
    try{const u=new URL(String(x||''));return u.protocol==='https:'&&u.hostname?u.href:'';}
    catch(_){return '';}
  };
  const number=n=>Number.isInteger(n)&&n>=0?
    new Intl.NumberFormat(document.documentElement.lang==='en'?'en-US':'zh-CN').format(n):'';
  const dateString=value=>{
    const ms=Date.parse(value||'');
    return Number.isFinite(ms)?new Intl.DateTimeFormat(
      document.documentElement.lang==='en'?'en-US':'zh-CN',
      {year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}
    ).format(ms):'';
  };
  const model={snapshot:null,feed:'all',query:'',failure:false};
  const countItems=feed=>Array.isArray(feed?.items)?feed.items.length:0;
  const termMatches=(item,words)=>words.every(word=>
    [item.title,item.subtitle,item.author,item.badge].join(' ').toLowerCase().includes(word));
  const isSearch=()=>Boolean(model.query.trim());
  function metric(item) {
    if(!Number.isInteger(item.value)||item.value<0)return null;
    const value=number(item.value);
    switch(item.metric){
      case 'upvotes':return {value,unit:t('社区投票','HF upvotes'),symbol:'▲',kind:'votes'};
      case 'total installs':return {value,unit:t('累计安装','Total installs'),symbol:'↓',kind:'installs'};
      case 'stars gained this week':return {value:'+'+value,unit:t('本周新增 Stars','Stars this week'),symbol:'★',kind:'stars'};
      case 'total stars':return {value,unit:t('累计 Stars','Total stars'),symbol:'★',kind:'stars'};
      default:return null;
    }
  }
  function fresh(feed) {
    const suffix=feed?.fetched_at ? ' · '+dateString(feed.fetched_at)+' UTC' : '';
    if(feed?.status==='stale')return t('最近成功快照（本轮采集失败）','Last valid snapshot (refresh failed)')+suffix;
    if(feed?.status==='ok')return t('来源已更新','Source refreshed')+suffix;
    return t('暂无可用快照','No verified snapshot yet');
  }
  function itemMarkup(item,index,focused,key) {
    const url=external(item.url);
    if(!url||!item.title)return '';
    const m=metric(item);
    const date=key==='papers'&&/^\d{4}-\d\d-\d\d/.test(item.badge||'')?dateString(item.badge):'';
    const subtitle=item.subtitle?h(item.subtitle):'';
    const metricBlock=m
      ?'<div class="findings-item-metric findings-metric-'+m.kind+'" aria-label="'+h(m.value+' '+m.unit)+'">'+
        '<span class="findings-metric-symbol" aria-hidden="true">'+h(m.symbol)+'</span>'+
        '<span class="findings-metric-value">'+h(m.value)+'</span>'+
        '<span class="findings-metric-unit">'+h(m.unit)+'</span></div>'
      :'<div class="findings-item-metric findings-metric-missing"><span>'+h(t('指标未公开','Metric unavailable'))+'</span></div>';
    return '<article class="findings-item'+(focused?' findings-item-expanded':'')+'">'+
      '<div class="findings-item-rank" aria-label="'+h(t('原始排名','Original rank'))+' '+(index+1)+'">'+
      String(index+1).padStart(2,'0')+'</div>'+
      '<div class="findings-item-content"><h4><a href="'+h(url)+'" target="_blank" rel="noopener noreferrer nofollow">'+
      h(item.title)+' <span aria-hidden="true">↗</span></a></h4>'+
      (subtitle?'<p class="findings-item-summary">'+subtitle+'</p>':'')+
      '<div class="findings-item-byline">'+
      (item.author?'<span>'+h(item.author)+'</span>':'')+
      (date?'<span>'+h(t('发表：','Published: ')+date)+'</span>':'')+
      '</div></div>'+metricBlock+'</article>';
  }
  function emptyMessage(feed,filtered) {
    const pending=feed?.status==='pending';
    return '<div class="findings-empty"><strong>'+h(filtered?
      t('没有匹配的条目','No matching records'):
      pending?t('等待首次采集','Awaiting first collection'):t('目前无法获取该来源','Source currently unavailable'))+'</strong>'+
      '<p>'+h(filtered?t('换个关键词试试，或切换其他榜单。','Try another keyword or source.'):
      t('可以直接打开原始来源查看，本站不会生成假榜单。','Open the original source instead; no rankings are invented here.'))+'</p></div>';
  }
  const desc=feed=>{
    if(feed.source==='GitHub Search')return t(
      '通过 GitHub Search 发现最近 60 天创建的相关仓库，按累计 Stars 排序；不是官方 Trending 或安装榜。',
      'GitHub Search: repositories created in the last 60 days, ordered by total stars. Not an official trending or install ranking.');
    if(feed.source==='Skills.sh')return t(
      '来自 Skills.sh 趋势榜，展示真实安装量；与 GitHub Stars 不能直接比较。',
      'Skills.sh trending results and their install counts. Not comparable to GitHub stars.');
    if(feed.source==='GitHub Trending')return t(
      '官方周榜排名；如有数字，表示本周新增 Stars，不是仓库总星数。',
      'Official weekly ranking. Numeric values represent stars gained this week, not lifetime totals.');
    if(feed.source==='Hugging Face Papers')return t(
      'Hugging Face 社区趋势排序；票数衡量社区关注，不代表引用量。',
      'Hugging Face community trending order. Upvotes reflect attention, not citations.');
    return t('来源和热度口径详见原站。','Check original source for metric definitions.');
  };
  function panel(key,feed,focused,words){
    const def=definitions[key];
    const url=external(feed.url)||fallback[key];
    const allItems=Array.isArray(feed.items)?feed.items:[];
    const matched=allItems.map((item,index)=>({item,index})).filter(({item})=>termMatches(item,words));
    const overview=!focused&&!words.length;
    const visible=overview?matched.slice(0,PREVIEW_COUNT):matched;
    const total=allItems.length;
    const header='<div class="findings-feed-head"><div class="findings-feed-ident">'+
      '<span class="findings-feed-kicker">'+h(def.kicker)+'</span>'+
      '<h3>'+h(t(...def.name))+'</h3>'+
      '<p class="findings-feed-intro">'+h(t(...def.intro))+'</p></div>'+
      '<div class="findings-feed-count" aria-label="'+h(t('已收录 '+total+' 条',''+total+' recorded'))+'">'+
      '<strong>'+h(String(total))+'</strong><span>'+h(t('条记录','records'))+'</span></div></div>';
    const note='<div class="findings-feed-context">'+
      '<p class="findings-feed-explainer">'+h(desc(feed))+'</p>'+
      '<div class="findings-feed-status">'+h(fresh(feed))+'</div></div>';
    const items=visible.length?visible.map(({item,index})=>itemMarkup(item,index,focused,key)).join(''):
      emptyMessage(feed,Boolean(words.length));
    const more=(overview&&total>PREVIEW_COUNT)
      ?'<button class="findings-feed-more" type="button" data-open-feed="'+key+'">'+
        h(t('查看完整 '+total+' 条趋势','Explore all '+total+' findings'))+' <span aria-hidden="true">→</span></button>'
      :'';
    const bottom='<div class="findings-feed-bottom">'+more+
      '<a class="findings-source-link" href="'+h(url)+'" target="_blank" rel="noopener noreferrer nofollow">'+
      h(t('访问原始榜单','Original source'))+' ↗</a></div>';
    const focusedHead=focused?
      '<div class="findings-focus-top"><button type="button" class="findings-back" data-open-feed="all">'+
      '← '+h(t('返回发现总览','All findings'))+'</button>'+
      '<span>'+h(t('完整榜单 · 各来源独立排名','Complete feed · Source-specific ranking'))+'</span></div>':'';
    const linkContext=focused?'<aside class="findings-focus-guide" aria-label="'+h(t('阅读提示','Reading guide'))+'">'+
      '<div class="findings-guide-label">'+h(t('如何阅读这份榜单','HOW TO READ THIS FEED'))+'</div>'+
      '<h4>'+h(t(...def.name))+'</h4><p>'+h(desc(feed))+'</p>'+
      '<dl><div><dt>'+h(t('数据来源','Source'))+'</dt><dd>'+h(feed.source||t('未验证','Unavailable'))+'</dd></div>'+
      '<div><dt>'+h(t('条目数量','Records'))+'</dt><dd>'+h(String(total))+'</dd></div>'+
      '<div><dt>'+h(t('更新时间','Last refreshed'))+'</dt><dd>'+h(dateString(feed.fetched_at)||t('暂无','Unavailable'))+'</dd></div></dl>'+
      '<a href="'+h(url)+'" target="_blank" rel="noopener noreferrer nofollow">'+h(t('打开来源网站','Visit original source'))+' ↗</a>'+
      '<p class="findings-guide-warning">'+h(t('趋势信号不代表人工精选，也不建议直接执行未经审查的第三方代码。',
        'Popularity is not an editorial endorsement. Review third-party code before running it.'))+'</p></aside>':'';
    return '<section class="findings-feed'+(focused?' findings-feed-focused':'')+'" id="feed-'+key+'" aria-label="'+h(t(...def.name))+'">'+
      focusedHead+header+note+
      '<div class="findings-feed-body"><div class="findings-ranking">'+items+'</div>'+linkContext+'</div>'+
      bottom+'</section>';
  }
  function render(){
    const feedMap=model.snapshot?.feeds||{};
    const words=model.query.toLowerCase().trim().split(/\s+/).filter(Boolean);
    const focused=model.feed!=='all';
    const keys=focused?[model.feed]:order;
    const total=keys.reduce((sum,key)=>sum+countItems(feedMap[key]),0);
    const matched=keys.reduce((sum,key)=>sum+(Array.isArray(feedMap[key]?.items)?feedMap[key].items.filter(item=>termMatches(item,words)).length:0),0);
    root.classList.toggle('is-focused',focused);
    root.classList.toggle('is-searching',Boolean(words.length));
    root.innerHTML=keys.map(key=>panel(key,feedMap[key]||{status:'pending',items:[]},focused,words)).join('');
    heading.textContent=focused?t('完整趋势榜单','Full source ranking'):t('趋势观察台','Trend desk');
    const visible=(!focused&&!words.length)?Math.min(PREVIEW_COUNT,countItems(feedMap.papers))+
      Math.min(PREVIEW_COUNT,countItems(feedMap.github))+
      Math.min(PREVIEW_COUNT,countItems(feedMap.skills))+
      Math.min(PREVIEW_COUNT,countItems(feedMap.workflows)):matched;
    status.textContent=words.length
      ?t('匹配 '+matched+' 条 · 搜索范围包括完整快照，不限于首页预览',
        matched+' matches · Search covers all snapshot entries, not only the preview')
      :focused
        ?t('当前展示 '+visible+' 条 · 来源独立排序，无跨平台综合评分',
          visible+' records · Original source ranking, no cross-platform score')
        :t('四个独立来源 · 每栏精选预览最多 '+PREVIEW_COUNT+' 条 · 共 '+total+' 条已采集',
          'Four independent feeds · Up to '+PREVIEW_COUNT+' previews each · '+total+' sourced records total');
    updated.textContent=model.snapshot?.generated_at
      ?t('最近采集：','Last checked: ')+dateString(model.snapshot.generated_at)+' UTC'
      :t('等待真实数据快照','Awaiting a verified snapshot');
    filters.forEach(button=>{const active=button.dataset.feed===model.feed;
      button.classList.toggle('is-current',active);button.setAttribute('aria-pressed',String(active));});
  }
  function setFeed(value,historyAction=true){
    const next=order.includes(value)?value:'all';
    model.feed=next;
    if(historyAction){
      const u=new URL(location.href);
      if(next==='all')u.searchParams.delete('feed');else u.searchParams.set('feed',next);
      if(u.href!==location.href)window.history.pushState(null,'',u.pathname+u.search+u.hash);
    }
    render();
    const headingTarget=document.querySelector('.findings-shell');
    if(headingTarget&&headingTarget.getBoundingClientRect().top<-100)
      headingTarget.scrollIntoView({behavior:'auto',block:'start'});
  }
  filters.forEach(button=>button.addEventListener('click',()=>setFeed(button.dataset.feed)));
  root.addEventListener('click',event=>{
    const button=event.target.closest('button[data-open-feed]');
    if(button&&root.contains(button))setFeed(button.dataset.openFeed);
  });
  search.addEventListener('input',()=>{model.query=search.value;render();});
  window.addEventListener('ora-language-change',render);
  window.addEventListener('popstate',()=>setFeed(new URLSearchParams(location.search).get('feed'),false));
  model.feed=order.includes(new URLSearchParams(location.search).get('feed'))?
    new URLSearchParams(location.search).get('feed'):'all';
  render();
  fetch('data/findings.json',{cache:'no-cache'})
    .then(r=>{if(!r.ok)throw Error('Findings HTTP '+r.status);return r.json();})
    .then(data=>{
      if(data.schema_version!=='1'||!data.feeds||typeof data.feeds!=='object')throw Error('Invalid Findings snapshot');
      model.snapshot=data;render();
    }).catch(err=>{
      console.warn('OpenResearchAssets Findings:',err);model.failure=true;model.snapshot={feeds:{},generated_at:null};render();
      status.textContent=t('暂时无法读取快照，请打开各平台的原始榜单。',
        'Snapshot unavailable. Browse the original feeds directly.');
    });
})();