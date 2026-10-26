/* Optional GitHub-verified feedback: activate only after Discussions + giscus are configured. */
(() => {
  'use strict';
  const mountPoint=document.getElementById('ora-community');
  if(!mountPoint)return;
  let activeId='';
  const settings=fetch('config/community.json',{cache:'no-cache'})
    .then(r=>r.ok?r.json():null).catch(()=>null);
  async function mount(id) {
    if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id))return;
    const config=await settings;
    if(!config || config.enabled!==true ||
       config.repo!=='OpenResearchAssets/openresearchassets.github.io' ||
       !/^R_[a-zA-Z0-9_-]+$/.test(config.repo_id||'') ||
       !/^DIC_[a-zA-Z0-9_-]+$/.test(config.category_id||''))return;
    const language=document.documentElement.lang==='en'?'en':'zh-CN';
    const key=id+'|'+language;
    if(key===activeId)return;
    activeId=key;
    mountPoint.hidden=false;
    mountPoint.innerHTML='<h2>'+ (language==='en'?'Appreciate or discuss this asset':'喜欢这份资产？参与讨论')+
      '</h2><p>'+(language==='en'?'Reactions and comments are handled through GitHub Discussions. GitHub sign-in required.':'点赞与评论通过 GitHub Discussions 进行，需要 GitHub 账号登录。')+'</p><div class="giscus"></div>';
    const script=document.createElement('script');
    script.src='https://giscus.app/client.js';
    Object.assign(script.dataset,{
      repo:config.repo,repoId:config.repo_id,
      category:config.category||'General',categoryId:config.category_id,
      mapping:'specific',term:'ora-asset:'+id,strict:'1',
      reactionsEnabled:'1',emitMetadata:'0',inputPosition:'bottom',
      theme:'light',lang:language,loading:'lazy'
    });
    script.crossOrigin='anonymous';
    script.async=true;
    script.onerror=()=>{mountPoint.hidden=true;};
    mountPoint.appendChild(script);
  }
  window.ORA_COMMUNITY={mount};
})();