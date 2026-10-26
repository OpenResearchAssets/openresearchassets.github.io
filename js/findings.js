/* Findings: in-page, source-attributed research reading.
 * Translations are built server-side; no browser secrets or generated summaries.
 */
(() => {
 'use strict';
 const root=document.getElementById('findings-feeds');
 if(!root)return;
 const search=document.getElementById('findings-search'),status=document.getElementById('findings-status');
 const updated=document.getElementById('findings-updated'),heading=document.getElementById('findings-title');
 const tabs=[...document.querySelectorAll('.findings-filter')];
 const keys=['papers','github','skills','workflows'],PREVIEW=3,BATCH=8;
 const labels={
  papers:['论文趋势','Trending papers','HUGGING FACE / PAPERS'],
  github:['GitHub 趋势','GitHub Trending','GITHUB / WEEKLY'],
  skills:['热门 Skills','Agent Skills','AGENT / SKILLS'],
  workflows:['研究工作流','Research workflows','RESEARCH / WORKFLOWS']
 };
 const sources={
  papers:'https://huggingface.co/papers/trending',
  github:'https://github.com/trending?since=weekly',
  skills:'https://github.com/search?q=topic%3Aagent-skills&type=repositories',
  workflows:'https://github.com/search?q=research+workflow&type=repositories'
 };
 const zh=()=>document.documentElement.lang!=='en';
 const tr=(cn,en)=>zh()?cn:en;
 const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const safeUrl=value=>{try{const u=new URL(String(value||''));return u.protocol==='https:'&&u.hostname?u.href:''}catch{return ''}};
 const valueFormat=n=>Number.isInteger(n)&&n>=0?new Intl.NumberFormat(zh()?'zh-CN':'en-US').format(n):'';
 const date=value=>{const stamp=Date.parse(value||'');return Number.isFinite(stamp)?
   new Intl.DateTimeFormat(zh()?'zh-CN':'en-US',{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}).format(stamp):''};
 const state={data:null,filter:'all',query:'',limit:BATCH};
 const localized=(entry,key)=>zh()?(entry[key+'_zh']||entry[key]||''):(entry[key]||'');
 const words=()=>state.query.trim().toLowerCase().split(/\s+/).filter(Boolean);
 const match=(r,terms)=>terms.every(w=>[r.title,r.title_zh,r.subtitle,r.subtitle_zh,r.detail,r.detail_zh,r.author].join(' ').toLowerCase().includes(w));
 function description(key,feed){
   if(feed.source==='GitHub Search')return tr('GitHub 近期新建项目，按累计 Stars 排序；不是官方 Trending 榜或人工精选。',
     'New GitHub repositories ranked by lifetime stars; not official Trending or editorial picks.');
   if(feed.source==='Skills.sh')return tr('Skills.sh 趋势榜及累计安装量，不等于 GitHub Stars。','Skills.sh trending and installs, not GitHub stars.');
   if(key==='github')return tr('GitHub 官方周榜；数字是本周新增 Stars，而非累计数。',
     'Official GitHub weekly ranking; numbers mean stars gained this week, not lifetime totals.');
   return tr('Hugging Face 论文趋势与社区投票，关注度不等于引用数或研究质量。',
     'Hugging Face trending papers and community votes, not citations or a measure of quality.');
 }
 function metric(r){
   const v=valueFormat(r.value);if(!v)return '';
   const specs={
     upvotes:['▲',tr('社区票数','HF upvotes'),'votes'],
     'stars gained this week':['★',tr('本周新增 Stars','Weekly stars'),'stars'],
     'total stars':['★',tr('累计 Stars','Total stars'),'stars'],
     'total installs':['↓',tr('累计安装','Total installs'),'installs']
   };
   const spec=specs[r.metric];if(!spec)return '';
   const amount=r.metric==='stars gained this week'?'+'+v:v;
   return '<div class="findings-item-metric findings-metric-'+spec[2]+'" aria-label="'+esc(amount+' '+spec[1])+'">'+
     '<span class="findings-metric-symbol" aria-hidden="true">'+spec[0]+'</span>'+
     '<span class="findings-metric-value">'+esc(amount)+'</span>'+
     '<span class="findings-metric-unit">'+esc(spec[1])+'</span></div>';
 }
 function row(r,originalRank,key,focused){
   const url=safeUrl(r.url);if(!url||!r.title)return '';
   const title=localized(r,'title'),abstract=localized(r,'subtitle')||localized(r,'detail');
   const detail=localized(r,'detail'),showMore=detail&&detail.length>abstract.length+35;
   const original=zh()&&r.title_zh&&r.title_zh!==r.title?
     '<div class="findings-original-title">'+esc(r.title)+'</div>':'';
   const sourceName=r.summary_source==='repository README'?tr('原仓库 README 摘录','Repository README excerpt'):
     key==='papers'?tr('论文摘要','Paper abstract'):tr('项目来源描述','Project description');
   const expanded=showMore?'<details class="findings-entry-detail"><summary>'+
     esc(tr(key==='papers'?'阅读全文摘要':'阅读更完整的介绍',key==='papers'?'Read full abstract':'Read fuller description'))+
     ' <span aria-hidden="true">⌄</span></summary><div class="findings-entry-full"><span>'+
     esc(sourceName)+'</span><p>'+esc(detail)+'</p></div></details>':'';
   const published=key==='papers'&&/^\d{4}-\d\d-\d\d/.test(r.badge||'')?date(r.badge):'';
   const originalLabel=key==='papers'?tr('论文原文','Original paper'):tr('项目原站','Original repository');
   const translated=zh()?'<span class="findings-translation-note">'+esc(r.subtitle_zh||r.detail_zh?
     '自动译文 · 可切换英文校对':'原文 · 中文机器翻译未启用')+'</span>':'';
   return '<article class="findings-item'+(focused?' findings-item-expanded':'')+'">'+
     '<span class="findings-item-rank">'+String(originalRank+1).padStart(2,'0')+'</span>'+
     '<div class="findings-entry-body"><h4>'+esc(title)+'</h4>'+original+
     (abstract?'<p class="findings-item-summary">'+esc(abstract)+'</p>':'')+
     '<div class="findings-entry-meta">'+(published?'<span>'+esc(tr('发表于','Published'))+' '+esc(published)+'</span>':'')+
     (r.author?'<span>'+esc(r.author)+'</span>':'')+'<span>'+esc(sourceName)+'</span>'+translated+'</div>'+
     expanded+'<a class="findings-entry-source-link" href="'+esc(url)+
     '" target="_blank" rel="noopener noreferrer nofollow">'+esc(originalLabel)+' ↗</a>'+
     '</div>'+metric(r)+'</article>';
 }
 function panel(key,feed,focused,terms){
   const def=labels[key],all=Array.isArray(feed.items)?feed.items:[];
   const matching=all.map((r,index)=>({r,index})).filter(({r})=>match(r,terms));
   const overview=!focused&&!terms.length;
   const entries=matching.slice(0,overview?PREVIEW:focused?state.limit:matching.length);
   const sourceLink=safeUrl(feed.url)||sources[key];
   const stamp=feed.fetched_at?date(feed.fetched_at):'';
   const name=tr(def[0],def[1]);
   const head=(focused?'<div class="findings-focus-top"><button class="findings-back" type="button" data-open-feed="all">← '+
     esc(tr('返回发现总览','Back to overview'))+'</button><span>'+
     esc(tr('直接站内阅读 · 不必打开来源榜单','Read here · Source navigation optional'))+'</span></div>':'')+
     '<div class="findings-feed-head"><div class="findings-feed-ident">'+
     '<span class="findings-feed-kicker">'+esc(def[2])+'</span><h3>'+esc(name)+'</h3>'+
     '<p class="findings-feed-intro">'+esc(key==='papers'?
       tr('先看研究问题与摘要，再决定是否精读原文。','Read the research question and abstract before the paper.'):
       key==='github'?tr('了解项目用途及 README 摘录，再决定是否进入仓库。','Read project descriptions and README excerpts before visiting the repo.'):
       tr('快速理解能解决什么问题，谨慎审查后再使用。','See what it solves and review carefully before using.'))+
     '</p></div><div class="findings-feed-count"><strong>'+all.length+'</strong><span>'+
     esc(tr('条记录','records'))+'</span></div></div>';
   const context='<div class="findings-feed-context"><p class="findings-feed-explainer">'+esc(description(key,feed))+
     '</p><div class="findings-feed-status">'+esc(feed.status==='stale'?tr('旧快照 · 采集失败','Stale snapshot'):
       feed.status==='ok'?tr('已更新','Updated'):tr('待采集','Pending'))+
     (stamp?' · '+stamp+' UTC':'')+'</div></div>';
   const list=entries.length?entries.map(({r,index})=>row(r,index,key,focused)).join(''):
     '<div class="findings-empty"><strong>'+esc(terms.length?tr('暂无匹配结果','No matching records'):
       tr('该数据源暂不可用','Source unavailable'))+'</strong><p>'+
     esc(tr('请更改搜索关键词，或查看原始来源。','Try a different search or the original source.'))+'</p></div>';
   const loadMore=focused&&matching.length>entries.length?
     '<button class="findings-load-more" type="button" data-load-more="'+key+'">'+
       esc(tr('在这里再看 '+Math.min(BATCH,matching.length-entries.length)+' 条 · 还剩 '+(matching.length-entries.length)+' 条',
         'Read '+Math.min(BATCH,matching.length-entries.length)+' more here · '+(matching.length-entries.length)+' remaining'))+' ↓</button>':'';
   const guide=focused?'<aside class="findings-focus-guide"><div class="findings-guide-label">'+
     esc(tr('阅读这份榜单','ABOUT THE SOURCE'))+'</div><h4>'+esc(name)+'</h4><p>'+
     esc(description(key,feed))+'</p><dl>'+
     '<div><dt>'+esc(tr('数据来源','Source'))+'</dt><dd>'+esc(feed.source||'—')+'</dd></div>'+
     '<div><dt>'+esc(tr('收录条目','Records'))+'</dt><dd>'+all.length+'</dd></div>'+
     '<div><dt>'+esc(tr('来源快照日期','Snapshot date'))+'</dt><dd>'+esc(stamp||'—')+'</dd></div></dl>'+
     '<p>'+esc(tr('摘要/README 来自公开原站，自动翻译可能有术语误差。外部程序请先审查。',
       'Abstracts and README excerpts are sourced. Machine translation can be imperfect; review external code.'))+'</p>'+
     '<a href="'+esc(sourceLink)+'" target="_blank" rel="noopener noreferrer nofollow">'+
     esc(tr('打开原始榜单','Open original feed'))+' ↗</a></aside>':'';
   const footer='<div class="findings-feed-bottom">'+
     (overview&&all.length>PREVIEW?'<button class="findings-feed-more" type="button" data-open-feed="'+key+'">'+
       esc(tr('站内查看全部 '+all.length+' 条','Read all '+all.length+' here'))+' →</button>':'')+
     '<a class="findings-source-link" target="_blank" rel="noopener noreferrer nofollow" href="'+esc(sourceLink)+'">'+
     esc(tr('原始来源','Original source'))+' ↗</a></div>';
   return '<section class="findings-feed'+(focused?' findings-feed-focused':'')+'" id="feed-'+key+'">'+
     head+context+'<div class="findings-feed-body"><div class="findings-ranking">'+list+loadMore+
     '</div>'+guide+'</div>'+footer+'</section>';
 }
 function render(){
   const feeds=state.data?.feeds||{},focused=state.filter!=='all',terms=words(),list=focused?[state.filter]:keys;
   root.classList.toggle('is-focused',focused);root.classList.toggle('is-searching',Boolean(terms.length));
   document.body.classList.toggle('findings-reading',focused);
   root.innerHTML=list.map(k=>panel(k,feeds[k]||{items:[],status:'pending'},focused,terms)).join('');
   heading.textContent=focused?tr('深入发现','Explore in depth'):tr('趋势观察台','Trend desk');
   const total=list.reduce((sum,k)=>sum+(feeds[k]?.items?.length||0),0);
   const matched=list.reduce((sum,k)=>sum+(feeds[k]?.items||[]).filter(x=>match(x,terms)).length,0);
   status.textContent=terms.length?tr('匹配 '+matched+' 条来源记录；可站内展开介绍',
     matched+' matching records, descriptions available here'):
     focused?tr('已采集 '+total+' 条 · 在本站分批阅读',total+' sourced records · Read in batches here'):
     tr('四个独立来源 · 各预览前三条 · 介绍可站内展开',
       'Four sources · Top three previews each · Read details here');
   updated.textContent=state.data?.generated_at?
     tr('最近采集：','Last checked: ')+date(state.data.generated_at)+' UTC':
     tr('等待真实来源快照','Awaiting verified data');
   tabs.forEach(btn=>{const selected=btn.dataset.feed===state.filter;
     btn.classList.toggle('is-current',selected);btn.setAttribute('aria-pressed',String(selected));});
   const translation=document.getElementById('findings-translation');
   if(translation)translation.textContent=tr(
     state.data?.translation_status==='translated'||state.data?.translation_status==='cached'?
       '已包含自动中文译文 · 技术术语请核对原文':'自动中文翻译未配置 · 暂显示来源原文',
     state.data?.translation_status==='translated'||state.data?.translation_status==='cached'?
       'Automatic Chinese translations available':'Showing original descriptions');
 }
 function choose(value,modify=true){
   state.filter=keys.includes(value)?value:'all';state.limit=BATCH;
   if(modify){const u=new URL(location.href);
     if(state.filter==='all')u.searchParams.delete('feed');else u.searchParams.set('feed',state.filter);
     if(u.href!==location.href)history.pushState(null,'',u.pathname+u.search+u.hash);
   }
   render();const section=document.querySelector('.findings-shell');
   if(section&&section.getBoundingClientRect().top<-100)section.scrollIntoView({behavior:'auto',block:'start'});
 }
 tabs.forEach(btn=>btn.addEventListener('click',()=>choose(btn.dataset.feed)));
 root.addEventListener('click',ev=>{
   const pick=ev.target.closest('button[data-open-feed]');
   if(pick){choose(pick.dataset.openFeed);return}
   const more=ev.target.closest('button[data-load-more]');
   if(more){state.limit+=BATCH;render();}
 });
 search.addEventListener('input',()=>{state.query=search.value;state.limit=BATCH;render();});
 window.addEventListener('ora-language-change',render);
 window.addEventListener('popstate',()=>choose(new URLSearchParams(location.search).get('feed'),false));
 const queryFeed=new URLSearchParams(location.search).get('feed');
 state.filter=keys.includes(queryFeed)?queryFeed:'all';
 render();
 fetch('data/findings.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('Snapshot HTTP '+r.status);return r.json();})
   .then(d=>{if(d.schema_version!=='1'||!d.feeds)throw Error('Invalid Findings snapshot');state.data=d;render();})
   .catch(err=>{console.warn('Findings unavailable:',err);state.data={feeds:{}};render();
     status.textContent=tr('趋势快照暂时不可用，请通过原始来源访问。','Snapshot unavailable. Visit original feeds.');});
})();