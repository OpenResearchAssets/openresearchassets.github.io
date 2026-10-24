(() => {
  const shared = [
    ['scientific','无法仅凭外观判断科学内容正确','核对原始数据、图中标签、坐标轴、结论和 caption，缺少证据时保留待核验状态。','Scientific fidelity needs evidence','Check the underlying data, axes, claims and caption against original evidence.','High'],
    ['hierarchy','核心结论不够突出','明确主旨，调整字号和空间层次，减少竞争性的标题与图例。','The central takeaway is not prominent','Emphasize one primary message and reduce competing labels.','High'],
    ['legibility','最终版面可能难以阅读','嵌入真正的论文 PDF 按最终尺寸检查，放大关键文字或简化细节。','Hard to read at final size','Check in the compiled paper at actual size; enlarge essential labels.','High'],
    ['aesthetics','配色、对齐和间距不一致','控制配色与字阶，统一对齐和间距，使视觉编码有固定含义。','Inconsistent color, spacing or alignment','Use a focused palette, type hierarchy and meaningful alignment.','Medium'],
    ['coherence','图表与正文或 caption 可能不一致','对照正文核对术语、图号、面板和数值，标记无法验证的项目。','Possible figure–caption inconsistency','Cross-check terms, panel references and values against the manuscript.','High']
  ];
  const specific = {
    teaser:[
      ['story','主题过多，主线不清','突出问题、关键变化和证据，方法细节移到方法图。','Too many competing ideas','Show the problem, transformation and primary evidence.','High'],
      ['comparison','比较的条件不够公平或明确','尽可能统一视角、裁切及尺度，标记对应条件。','Comparison conditions are unclear','Match viewpoint, crop and scale where feasible; label conditions.','High'],
      ['impact','缺乏鲜明视觉焦点','突出最重要的证据或对象，减少不必要的周边装饰。','No recognizable focal point','Promote the strongest evidence and remove unnecessary decoration.','Medium']],
    method:[
      ['flow','信息流或计算关系不清','逐一核对模块输入、输出、条件及反馈方向。','Ambiguous information flow','Check inputs, outputs, conditions and feedback arrows.','High'],
      ['modules','模块堆叠或文字重复','合并重复步骤，让每个模块表达一个不同的职责。','Dense or repetitive modules','Merge redundant boxes and shorten labels.','Medium'],
      ['legend','颜色和图形含义未定义','为形状、颜色和符号提供统一说明。','Undefined colors or symbols','Add consistent legend semantics.','Medium']],
    results:[
      ['units','指标单位或比较设置缺失','补充单位、分母、样本量和基线条件，并检查坐标刻度。','Missing units or settings','Define units, denominators, sample size and baseline conditions.','High'],
      ['uncertainty','必要的误差或不确定性说明缺失','根据真实数据提供合适的置信区间或方差说明；不凭空补数字。','Missing uncertainty context','Use justified variance or confidence information from actual data.','High'],
      ['chart','图型或坐标尺度误导比较','选用易于比较的图型与统一尺度，必要的截断应说明。','Misleading chart encodings','Use shared scales and clearly disclose any truncation.','High']],
    table:[
      ['emphasis','重要比较难以定位','合理分组，统一数值精度，克制地突出关键结果。','Key comparisons are hard to find','Group methods and metrics with consistent precision.','Medium'],
      ['definition','表注或指标定义不完整','说明指标、符号、箭头和缺失值含义。','Undefined metrics or symbols','Define metrics, arrows, abbreviations and missing values.','High'],
      ['density','表格过密或超出页面宽度','减少冗余列，按真正的 PDF 排版尺寸检查。','Too dense at publication size','Trim redundant columns and inspect the final-size table.','Medium']],
    paper:[
      ['evidence','核心论点缺乏直接图表证据','建立论点—证据—图表对应关系，优先展示最关键的实验证据。','Important claims lack visible evidence','Map claims to figures, tables and source evidence.','High'],
      ['redundancy','多个图表重复表达相同内容','保留最能证明主张的图表，将空间让给独立证据。','Repeated visual evidence','Merge or remove redundant visuals.','High'],
      ['layout','全文排版与阅读顺序不稳定','检查编译后的浮动体位置、图表比例、caption 和页面留白。','Uneven layout and reading rhythm','Inspect compiled pages, figure order, captions and spacing.','Medium']]
  };
  const select=document.querySelector('#artifact-type');
  const nameInput=document.querySelector('#artifact-name');
  const wrap=document.querySelector('#audit-questions');
  const report=document.querySelector('#audit-report');
  const tr=(zh,en)=>window.ORA_I18N?.t(zh,en)??zh;
  const rows=()=>[...shared,...specific[select.value]];
  const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let last='';
  function draw(preserve=false){
    const checked=preserve?new Set([...wrap.querySelectorAll('input:checked')].map(x=>x.value)):new Set();
    wrap.innerHTML='';
    rows().forEach(([id,zh,fixZh,en,fixEn,severity])=>{
      const label=document.createElement('label');label.className='audit-question';
      const input=document.createElement('input');input.type='checkbox';input.value=id;input.checked=checked.has(id);input.setAttribute('aria-label',tr(zh,en));
      const content=document.createElement('span');const strong=document.createElement('strong');strong.textContent=tr(zh,en);
      const small=document.createElement('small');small.textContent=`${tr(severity==='High'?'较高优先级':'一般优先级',severity+' priority')} · ${tr(fixZh,fixEn)}`;
      content.append(strong,small);label.append(input,content);wrap.append(label);
    });
    report.hidden=true;
  }
  function generate(){
    const selected=new Set([...wrap.querySelectorAll('input:checked')].map(x=>x.value));
    const issues=rows().filter(row=>selected.has(row[0]));
    const name=nameInput.value.trim()||tr('未命名科研素材','Untitled research artifact');
    const type=select.selectedOptions[0].text;
    last=`# ${tr('科研设计自查报告','Research design self-review')}\n\n${tr('对象','Artifact')}: ${name}\n${tr('类型','Type')}: ${type}\n${tr('评估方式','Review')}: ${tr('用户手动选择问题；未使用 AI 自动审查','User-selected checklist; not automatic AI verification')}\n\n`+(issues.length?issues.map((r,i)=>`${i+1}. [${tr(r[5]==='High'?'较高':'一般',r[5])}] ${tr(r[1],r[3])}\n   ${tr('修改建议','Suggested action')}: ${tr(r[2],r[4])}\n`).join('\n'):tr('没有选择问题；这不意味着质量审核已通过。','No issues selected. This is not a verified quality pass.')+'\n')+`\n${tr('下一步：核对原始科学证据，在最终论文 PDF 尺寸下确认每项修改。','Next: verify source evidence and check the final-size publication PDF.')}\n`;
    const title=issues.length?tr(`已标记 ${issues.length} 项问题`,`${issues.length} selected issues`):tr('没有勾选问题','No issues selected');
    report.innerHTML='<h3>'+escapeHTML(title)+'</h3>'+(issues.length?'<ol>'+issues.map(r=>'<li><strong>'+escapeHTML(tr(r[1],r[3]))+'</strong><br>'+escapeHTML(tr(r[2],r[4]))+'</li>').join('')+'</ol>':'<p>'+escapeHTML(tr('未发现问题不代表已通过审核，还需要实际检查图表。','This is not a verified quality pass.'))+'</p>')+'<button id="copy-report" type="button">'+escapeHTML(tr('复制 Markdown 报告','Copy Markdown review'))+'</button>';
    report.hidden=false;
    document.querySelector('#copy-report').addEventListener('click',async()=>{
      const b=document.querySelector('#copy-report');
      try{await navigator.clipboard.writeText(last);b.textContent=tr('已复制','Copied to clipboard')}
      catch{b.textContent=tr('无法直接复制，请从下方复制','Clipboard unavailable — copy below');const pre=document.createElement('pre');pre.textContent=last;pre.style.whiteSpace='pre-wrap';report.append(pre)}
    });
  }
  select.addEventListener('change',()=>draw());
  document.querySelector('#generate-report').addEventListener('click',generate);
  document.querySelector('#clear-review').addEventListener('click',()=>{nameInput.value='';draw()});
  window.addEventListener('ora-language-change',()=>draw(true));
  draw();
})();
