/* Findings is a read-only, source-aware snapshot viewer. No combined fake score. */
(() => {
  'use strict';
  const root=document.getElementById('findings-feeds');
  if(!root)return;
  const search=document.getElementById('findings-search');
  const status=document.getElementById('findings-status');
  const updated=document.getElementById('findings-updated');
  const controls=[...document.querySelectorAll('.findings-filter')];
  const order=['papers','github','skills','workflows'];
  const titles={
    papers:['论文趋势','Trending papers','HUGGING FACE / PAPERS'],
    github:['GitHub 趋势','GitHub Trending','GITHUB / WEEKLY'],
    skills:['Agent Skills','Agent Skills','SKILLS / SIGNALS'],
    workflows:['研究工作流','Research workflows','WORKFLOWS / DISCOVERY']
  };
  const fallback={
    papers:'https://huggingface.co/papers/trending',
    github:'https://github.com/trending?since=weekly',
    skills:'https://skills.sh/trending',
    workflows:'https://github.com/search?q=research+workflow&type=repositories'
  };
  const t=(zh,en)=>document.documentElement.lang==='en'?en:zh;
  const escapeText=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const cleanUrl=x=>{
    try{
      const u=new URL(String(x||''),location.origin);
      return u.protocol==='https:' && u.hostname ? u.href : '';
    }catch(e){return '';}
  };
  const short=value=>{
    if(!Number.isFinite(value)||value<0)return '';
    return new Intl.NumberFormat(document.documentElement.lang==='en'?'en-US':'zh-CN',{notation:value>=10000?'compact':'standard',maximumFractionDigits:1}).format(value);
  };
  const formatDate=value=>{
    const time=Date.parse(value||'');
    if(!Number.isFinite(time))return '';
    return new Intl.DateTimeFormat(document.documentElement.lang==='en'?'en-US':'zh-CN',
      {year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}).format(time);
  };
  const model={snapshot:null,filter:'all',query:''};
  const metricText=(item,key)=>{
    const value=short(item.value);
    if(!value)return '';
    const metric=item.metric;
    if(metric==='upvotes')return '▲ '+value+' '+t('HF 投票','HF votes');
    if(metric==='total installs')return value+' '+t('累计安装','total installs');
    if(metric==='stars gained this week')return '+'+value+' '+t('本周 Stars','stars this week');
    if(metric==='total stars')return '★ '+value+' '+t('累计 Stars','total stars');
    return '';
  };
  const noData=feed=>{
    const stale=feed.status==='stale';
    return '<div class="findings-empty"><strong>'+escapeText(t('当前来源暂时不可用','This source is currently unavailable'))+'</strong>'+
      escapeText(stale?t('正在展示最近一次成功抓取的内容。','Last successfully fetched content is shown instead.'):
        t('没有可靠的公开条目可展示，可到原站查看。','No verified entries yet; please browse the original source.'))+'</div>';
  };
  const card=(item,index,key)=>{
    const url=cleanUrl(item.url);
    if(!url||!item.title)return '';
    const note=metricText(item,key);
    const badge=item.badge ? '<span class="findings-item-badge">'+escapeText(item.badge)+'</span>' : '';
    return '<article class="findings-item">'+
      '<div class="findings-item-head"><span class="findings-item-rank">'+String(index+1).padStart(2,'0')+'</span>'+badge+'</div>'+
      '<h4><a href="'+escapeText(url)+'" target="_blank" rel="noopener noreferrer nofollow">'+escapeText(item.title)+' ↗</a></h4>'+
      (item.subtitle?'<p class="findings-item-summary">'+escapeText(item.subtitle)+'</p>':'')+
      '<div class="findings-item-foot">'+(note?'<span class="findings-item-value">'+escapeText(note)+'</span>':'')+
      (item.author?'<span class="findings-item-creator">'+escapeText(item.author)+'</span>':'')+
      '</div></article>';
  };
  function render(){
    const feedMap=model.snapshot?.feeds||{};
    const query=model.query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible=0;
    root.classList.toggle('is-focused',model.filter!=='all');
    root.innerHTML=order.map(key=>{
      if(model.filter!=='all'&&model.filter!==key)return '';
      const feed=feedMap[key]||{items:[],status:'pending'};
      const sourceLink=cleanUrl(feed.url)||fallback[key];
      const entries=Array.isArray(feed.items)?feed.items.map((item,i)=>({item,originalIndex:i})).filter(({item})=>
        !query.length || query.every(word=>[item.title,item.subtitle,item.author,item.badge].join(' ').toLowerCase().includes(word))):[];
      visible+=entries.length;
      const label=t(titles[key][0],titles[key][1]);
      const stale=feed.status==='stale';
      const sourceName=feed.source||t('原始来源','Original source');
      const stamp=feed.fetched_at?formatDate(feed.fetched_at):'';
      const sourceState=stale?t('旧快照 / 来源未更新','Stale snapshot / source unavailable'):
        feed.status==='ok'?t('已更新','Updated'):
        t('待抓取','Pending collection');
      const header='<div class="findings-feed-head"><div><span class="findings-feed-kicker">'+
        escapeText(titles[key][2])+'</span><h3>'+escapeText(label)+'</h3><p>'+
        escapeText(feed.metric_note||t('原站信号 · 不等于编辑精选','Original-source signals, not editorial selection'))+
        '</p></div><a class="findings-feed-source" href="'+escapeText(sourceLink)+
        '" target="_blank" rel="noopener noreferrer nofollow">'+escapeText(sourceName)+' ↗</a></div>';
      const list=entries.length?entries.map(({item,originalIndex})=>card(item,originalIndex,key)).join(''):
        (feed.status==='ok'&&query.length?'<p class="findings-empty">'+
          escapeText(t('没有匹配的条目，请调整关键词。','No matching items; try another search.'))+'</p>':noData(feed));
      const sourceStatus='<div class="findings-feed-status">'+escapeText(sourceState+(stamp?' · '+stamp+' UTC':''))+'</div>';
      return '<section class="findings-feed" id="feed-'+key+'" aria-label="'+escapeText(label)+'">'+
        header+sourceStatus+list+'<a class="findings-feed-more" href="'+escapeText(sourceLink)+
        '" target="_blank" rel="noopener noreferrer nofollow">'+escapeText(t('在来源平台查看完整榜单','View the full original feed'))+' ↗</a></section>';
    }).join('');
    status.textContent=model.snapshot
      ?t('当前显示 '+visible+' 条来源记录 · 各榜单独立排名，数字不可跨平台比较',
          visible+' sourced entries shown · rankings and metrics are source-specific')
      :t('尚无已验证快照，自动采集正在初始化。','No verified snapshot yet. Automated collection is initializing.');
    const when=model.snapshot?.generated_at?formatDate(model.snapshot.generated_at):'';
    updated.textContent=when?t('最新抓取任务：','Latest collection attempt: ')+when+' UTC':
      t('等待第一份真实趋势快照','Awaiting first sourced trend snapshot');
  }
  controls.forEach(button=>button.addEventListener('click',()=>{
    model.filter=button.dataset.feed||'all';
    controls.forEach(x=>{const selected=x===button;x.classList.toggle('is-current',selected);x.setAttribute('aria-pressed',String(selected));});
    render();
  }));
  search.addEventListener('input',()=>{model.query=search.value;render();});
  window.addEventListener('ora-language-change',render);
  fetch('data/findings.json',{cache:'no-cache'}).then(r=>{
    if(!r.ok)throw Error('Findings snapshot HTTP '+r.status);
    return r.json();
  }).then(data=>{
    if(data.schema_version!=='1'||!data.feeds)throw Error('Invalid findings snapshot schema');
    model.snapshot=data;render();
  }).catch(err=>{
    console.warn('Findings source unavailable:',err);
    model.snapshot={generated_at:null,feeds:{}};
    render();
    status.textContent=t('暂时无法读取自动趋势快照，请直接通过各来源链接浏览。',
      'The findings snapshot is unavailable. Browse the original sources directly.');
  });
  render();
})();