/* Offline smoke tests for the GitHub-Issues-backed Community page. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const source=fs.readFileSync(path.join(__dirname,'../js/community-page.js'),'utf8');
const issueUrl='https://github.com/OpenResearchAssets/openresearchassets.github.io/issues/';
const body=(title,type,why)=>[
  '### 资产类型 / Asset type',type,'',
  '### 作品名称 / Asset title',title,'',
  '### 官方来源 / Original source URL','https://example.org/source','',
  '### 为什么值得分享或推荐？/ Why is this asset worth sharing?',why
].join('\n');
const issue=(number,title,type,why,likes,comments,created)=>({
  number,title:'[投稿] '+title,state:'open',labels:[],
  body:body(title,type,why),user:{login:'researcher-'+number},
  created_at:created,reactions:{'+1':likes,total_count:likes},comments
});
const fixtures=[
  issue(18,'Robot & <script>alert(1)</script> teaser','高审美论文图 / Research figure','Clear composition & spatial evidence.',3,1,'2026-10-26T02:00:00Z'),
  issue(17,'Useful autonomous skill','高热度 Skill / Popular GitHub Skill','A repeatable research workflow.',20,5,'2026-10-25T04:00:00Z'),
  {...issue(16,'Spam','Research figure','Not reviewed',1000,200,'2026-10-25T00:00:00Z'),labels:[{name:'spam'}]},
  {...issue(15,'Not submitted','Research figure','Not reviewed',0,0,'2026-10-25T00:00:00Z'),title:'Ordinary issue'},
  {...issue(14,'A PR','Research figure','Not reviewed',0,0,'2026-10-25T00:00:00Z'),pull_request:{url:'https://api.github.com/example'}},
  {...issue(13,'Rejected','Research figure','Not reviewed',0,0,'2026-10-25T00:00:00Z'),state:'closed',state_reason:'not_planned'}
];
function setup(error=false){
  const listeners={};
  const control=(value='')=>({value,innerHTML:'',textContent:'',hidden:false,disabled:false,
    addEventListener(type,handler){this['on'+type]=handler;}});
  const nodes={
    'community-grid':control(),'community-status':control(),'community-more':control(),
    'community-search':control(),'community-kind':control('all'),'community-sort':control('new')
  };
  const document={documentElement:{lang:'zh-CN'},getElementById:id=>nodes[id]||null};
  const window={addEventListener:(event,handler)=>{listeners[event]=handler;}};
  const fetch=async url=>{
    if(url.startsWith('https://api.github.com/')){
      if(error)throw Error('Synthetic API outage');
      return {ok:true,json:async()=>fixtures};
    }
    if(url==='catalog/index.json')return {ok:true,json:async()=>({
      entries:[{id:'robot-teaser',submission:{issue_url:issueUrl+'18'}}]
    })};
    throw Error('Unrecognized fetch '+url);
  };
  vm.runInNewContext(source,{document,window,fetch,URL,Date,Intl,console:{warn(){}},Set},{filename:'community-page.js'});
  return{nodes,listeners,document};
}
const flush=()=>new Promise(setImmediate);
(async()=>{
  const{nodes,listeners,document}=setup();
  await flush();await flush();
  let html=nodes['community-grid'].innerHTML;
  assert.match(html,/researcher-18/);assert.match(html,/researcher-17/);
  assert.match(html,/👍 3/);assert.match(html,/👍 20/);assert.match(html,/↳ 5/);
  assert.ok(!html.includes('<script>alert(1)</script>'),'Raw script may not enter innerHTML');
  assert.match(html,/&lt;script&gt;/);
  for(const n of [16,15,14,13])assert.ok(!html.includes('researcher-'+n),'Unsafe/unrelated Issue must be excluded');
  assert.match(html,/asset.html\?id=robot-teaser/);
  assert.match(html,/Clear composition/,'Submission rationale from current form');
  assert.match(html,/原始来源（未经核实）/);
  assert.equal(nodes['community-more'].hidden,true);
  nodes['community-sort'].value='popular';nodes['community-sort'].onchange();
  html=nodes['community-grid'].innerHTML;
  assert.ok(html.indexOf('researcher-17')<html.indexOf('researcher-18'),'Popular uses actual plus-one count');
  nodes['community-kind'].value='visual';nodes['community-kind'].onchange();
  html=nodes['community-grid'].innerHTML;
  assert.match(html,/researcher-18/);assert.ok(!html.includes('researcher-17'));
  nodes['community-kind'].value='all';nodes['community-kind'].onchange();
  nodes['community-search'].value='autonomous';nodes['community-search'].oninput();
  html=nodes['community-grid'].innerHTML;
  assert.match(html,/researcher-17/);assert.ok(!html.includes('researcher-18'));
  nodes['community-search'].value='';nodes['community-search'].oninput();
  document.documentElement.lang='en';listeners['ora-language-change']();
  assert.match(nodes['community-grid'].innerHTML,/Original link \(unverified\)/);
  const offline=setup(true);await flush();await flush();
  assert.match(offline.nodes['community-status'].textContent,/GitHub/);
  assert.match(offline.nodes['community-grid'].innerHTML,/GitHub Issues/);
  assert.ok(!offline.nodes['community-status'].textContent.includes('0 community submissions loaded'));
  console.log('PASS: Community API data, sanitization, reactions, filters, sorting, curation link and error states');
})().catch(e=>{console.error(e);process.exitCode=1;});
