/* GitHub Issues are the sole source of Community submissions, never the curated catalog. */
(() => {
  'use strict';
  const grid=document.getElementById('community-grid');
  if (!grid) return;
  const status=document.getElementById('community-status'), more=document.getElementById('community-more');
  const search=document.getElementById('community-search'), kind=document.getElementById('community-kind'), sort=document.getElementById('community-sort');
  const API='https://api.github.com/repos/OpenResearchAssets/openresearchassets.github.io/issues';
  const issueBase='https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/';
  const t=(zh,en)=>document.documentElement.lang==='en'?en:zh;
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const sourceUrl=value=>{try{const u=new URL(String(value||'').trim());return ['http:','https:'].includes(u.protocol)?u.href:'';}catch(_){return '';}};
  const clean=value=>String(value||'').replace(/<!--[\s\S]*?-->/g,'').replace(/[*_]/g,'').trim();
  const section=(body,part)=>{
    const chunks=String(body||'').split(/^###\s+/m).slice(1);
    const found=chunks.find(x=>x.split(/\r?\n/,1)[0].toLowerCase().includes(part.toLowerCase()));
    return found?found.split(/\r?\n/).slice(1).join('\n').trim():'';
  };
  const classify=raw=>{
    const v=raw.toLowerCase();
    if(v.includes('figure')||v.includes('科研配图')||v.includes('论文图'))return 'visual';
    if(v.includes('website')||v.includes('项目主页'))return 'website';
    if(v.includes('editable')||v.includes('可编辑'))return 'editable';
    if(v.includes('workflow'))return 'workflow';
    if(v.includes('skill')||v.includes('工具'))return 'skill';
    return 'other';
  };
  const labels={
    visual:['科研配图','Research figure','◇'],website:['项目主页','Project site','⌘'],
    editable:['可编辑素材','Editable asset','⬡'],skill:['Skill / Tool','Skill / Tool','✳'],
    workflow:['工作流','Workflow','⇄'],other:['社区投稿','Community submission','✦']
  };
  const state={items:[],curated:new Map(),page:1,loading:false,lastPage:false,error:false};
  const dateText=date=>{const ts=Date.parse(date||'');return Number.isFinite(ts)?
    new Intl.DateTimeFormat(document.documentElement.lang==='en'?'en-US':'zh-CN',{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}).format(ts):'';};
  const parseIssue=issue=>{
    if(!Number.isInteger(issue?.number)||issue.pull_request||!issue.title?.startsWith('[投稿]'))return null;
    const unwanted=new Set(['spam','hidden','do-not-display','invalid']);
    if((issue.labels||[]).some(x=>unwanted.has(String(typeof x==='string'?x:x.name).toLowerCase()))||issue.state_reason==='not_planned')return null;
    const user=issue.user?.login;
    if(!/^[a-z\d](?:[a-z\d-]{0,38})$/i.test(user||''))return null;
    const body=issue.body||'';
    if(!body.includes('### 资产类型 / Asset type')||!body.includes('### 官方来源 / Original source URL'))return null;
    const title=clean(section(body,'Asset title'))||clean(issue.title.slice(4))||t('未命名资产','Untitled asset');
    const details=clean(section(body,'Why is this asset worth sharing?'))||clean(section(body,'为什么值得分享或推荐'))||clean(section(body,'Why does it belong here?'))||clean(section(body,'为什么值得精选'));
    const match=section(body,'Original source URL').match(/https?:\/\/[^\s<>)\]]+/i);
    const source=sourceUrl(match?match[0]:'');
    return {
      number:issue.number,title:title.slice(0,180),description:details.replace(/\s+/g,' ').slice(0,360),
      topic:classify(section(body,'Asset type')),source,issueUrl:issueBase+issue.number,
      user,created:issue.created_at,closed:issue.state==='closed',
      likes:Number.isInteger(issue.reactions?.['+1'])?Math.max(0,issue.reactions['+1']):0,
      comments:Number.isInteger(issue.comments)?Math.max(0,issue.comments):0
    };
  };
  const listed=()=>{
    const words=(search.value||'').trim().toLowerCase().split(/\s+/).filter(Boolean),type=kind.value;
    return state.items.filter(x=>(type==='all'||x.topic===type)&&words.every(w=>
      [x.title,x.description,x.user,x.source].join(' ').toLowerCase().includes(w)))
      .sort((a,b)=>sort.value==='popular'?b.likes-a.likes||Date.parse(b.created)-Date.parse(a.created):
        sort.value==='discussion'?b.comments-a.comments||Date.parse(b.created)-Date.parse(a.created):
        Date.parse(b.created)-Date.parse(a.created));
  };
  const card=item=>{
    const [zh,en,symbol]=labels[item.topic]||labels.other;
    const selected=state.curated.get(item.number);
    const badge=selected?'<a class="ora-community-curated" href="asset.html?id='+encodeURIComponent(selected.id)+'">'+esc(t('已入选精选','Curated'))+' ↗</a>':
      item.closed?'<span class="ora-community-closed">'+esc(t('讨论已关闭','Discussion closed'))+'</span>':'';
    return '<article class="ora-community-entry">'+
      '<div class="ora-community-entry-icon" aria-hidden="true">'+esc(symbol)+'</div>'+
      '<div class="ora-community-entry-main">'+
      '<div class="ora-community-entry-top"><span class="ora-community-type">'+esc(t(zh,en))+'</span><span class="ora-community-number">#'+item.number+'</span>'+badge+'</div>'+
      '<h3><a href="'+item.issueUrl+'" target="_blank" rel="noopener noreferrer nofollow">'+esc(item.title)+' ↗</a></h3>'+
      (item.description?'<p class="ora-community-entry-description">'+esc(item.description)+'</p>':'')+
      '<div class="ora-community-entry-source">'+(item.source?'<a href="'+esc(item.source)+'" target="_blank" rel="noopener noreferrer nofollow">'+esc(t('原始来源（未经核实）','Original link (unverified)'))+' ↗</a>':'')+'</div>'+
      '<div class="ora-community-entry-foot">'+
      '<a class="ora-community-user" href="https://github.com/'+esc(item.user)+'" target="_blank" rel="noopener noreferrer"><img src="https://github.com/'+esc(item.user)+'.png?size=80" alt="" width="22" height="22" loading="lazy">@'+esc(item.user)+'</a>'+
      '<time datetime="'+esc(item.created)+'">'+esc(dateText(item.created))+'</time>'+
      '<div class="ora-community-reactions">'+
      '<a href="'+item.issueUrl+'" target="_blank" rel="noopener noreferrer nofollow" aria-label="'+esc(t('去 GitHub 点赞，当前 '+item.likes+' 赞','Like on GitHub; '+item.likes+' likes'))+'">👍 '+item.likes+' <span>'+esc(t('点赞','Like'))+'</span></a>'+
      '<a href="'+item.issueUrl+'#issuecomment-new" target="_blank" rel="noopener noreferrer nofollow" aria-label="'+esc(t(item.comments+' 条评论',item.comments+' comments'))+'">↳ '+item.comments+' <span>'+esc(t('讨论','Discuss'))+'</span></a></div></div></div></article>';
  };
  function render(){
    const result=listed();
    grid.innerHTML=result.length?result.map(card).join(''):
      '<div class="ora-community-empty"><span aria-hidden="true">✳</span><h3>'+
      esc(state.error&&!state.items.length?t('暂时无法读取 GitHub 投稿','GitHub submissions unavailable'):
        state.items.length?t('没有匹配的投稿','No matching submissions'):
        t('第一份社区投稿，等你来分享。','Be the first to contribute.'))+'</h3><p>'+
      esc(state.error?t('可能是 GitHub API 限流或网络问题。请直接在 GitHub 浏览。','The GitHub API may be rate-limited or unreachable. Browse GitHub directly.'):
        state.items.length?t('换一个关键词或筛选条件试试。','Try a different search or filter.'):
        t('任何人都能投稿并获得点赞；优质作品还可以进入精选。','Anyone can submit and collect likes; outstanding assets may be curated.'))+
      '</p><a href="'+(state.error?'https://github.com/OpenResearchAssets/openresearchassets.github.io/issues':'contribute.html')+'">'+
      esc(state.error?t('查看 GitHub Issues ↗','Open GitHub Issues ↗'):t('现在投稿 ↗','Submit an asset ↗'))+'</a></div>';
    status.textContent=state.error?t('GitHub 数据读取失败，当前已加载 '+state.items.length+' 项','GitHub request failed; '+state.items.length+' items previously loaded'):
      t('已加载 '+state.items.length+' 项社区投稿 · 筛选显示 '+result.length+' 项（来源：GitHub）',
        state.items.length+' community submissions loaded · '+result.length+' shown (GitHub)');
    more.hidden=state.lastPage||state.error;more.disabled=state.loading;
    more.textContent=state.loading?t('正在加载…','Loading…'):t('加载更多投稿 ↓','Load more submissions ↓');
  }
  async function loadPage(){
    if(state.loading||state.lastPage)return;
    state.loading=true;more.disabled=true;
    status.textContent=t('正在读取 GitHub 投稿…','Loading from GitHub…');
    try{
      const response=await fetch(API+'?state=all&per_page=100&page='+state.page,{headers:{Accept:'application/vnd.github+json'}});
      if(!response.ok)throw Error('GitHub API HTTP '+response.status);
      const result=await response.json();
      if(!Array.isArray(result))throw Error('Invalid GitHub API response');
      const seen=new Set(state.items.map(x=>x.number));
      for(const issue of result){const entry=parseIssue(issue);if(entry&&!seen.has(entry.number)){state.items.push(entry);seen.add(entry.number);}}
      state.page++;state.lastPage=result.length<100||state.page>5;
      state.error=false;
    }catch(error){state.error=true;console.warn('OpenResearchAssets Community:',error);}
    finally{state.loading=false;render();}
  }
  async function loadCurated(){
    try{
      const response=await fetch('catalog/index.json');
      if(!response.ok)return;
      const catalog=await response.json();
      for(const entry of catalog.entries||[]){
        const found=/^https:\/\/github\.com\/OpenResearchAssets\/openresearchassets\.github\.io\/issues\/(\d+)$/.exec(entry.submission?.issue_url||'');
        if(found&&!state.curated.has(Number(found[1])))state.curated.set(Number(found[1]),{id:entry.id});
      }
      render();
    }catch(error){console.warn('Curated linkage unavailable:',error);}
  }
  for(const el of [search,kind,sort])el.addEventListener(el===search?'input':'change',render);
  more.addEventListener('click',loadPage);
  window.addEventListener('ora-language-change',render);
  more.hidden=true;
  loadPage();
  loadCurated();
})();