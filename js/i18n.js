/* Chinese is the canonical authoring language. English is a complete secondary UI.
   All translations live alongside source text in markup and reference metadata. */
(() => {
  const supported = ['zh','en'];
  const fromURL = new URLSearchParams(window.location.search).get('lang');
  let saved = null;
  try { saved = window.localStorage.getItem('ora-lang'); } catch (_) {}
  let language = supported.includes(fromURL) ? fromURL : (supported.includes(saved) ? saved : 'zh');
  const toggle = document.querySelector('.lang-toggle');
  function apply() {
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-i18n-en]').forEach(el => {
      const texts = JSON.parse(el.getAttribute('data-i18n-' + language));
      const nodes = [...el.childNodes].filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
      if (nodes.length === texts.length) nodes.forEach((n,i) => { n.textContent = texts[i]; });
    });
    document.querySelectorAll('[data-i18n-attrs]').forEach(el => {
      const attrs = JSON.parse(el.getAttribute('data-i18n-attrs'));
      Object.entries(attrs).forEach(([name,values])=>el.setAttribute(name, values[language === 'zh' ? 1 : 0]));
    });
    if (toggle) {
      // Both languages stay visible. Highlight CURRENT language, never
      // present only the destination language as if it were the active one.
      toggle.innerHTML = '<span class="ora-lang-option'+(language==='zh'?' is-active':'')+
        '" lang="zh-CN">中文</span><span class="ora-lang-divider" aria-hidden="true">/</span>'+
        '<span class="ora-lang-option'+(language==='en'?' is-active':'')+'" lang="en">EN</span>';
      toggle.setAttribute('aria-label',language==='zh'
        ? '当前语言：中文。点击切换为 English' : 'Current language: English. Click to switch to 中文');
      toggle.setAttribute('title',language==='zh'
        ? '当前：中文 · 切换为 English' : 'Current: English · Switch to 中文');
      toggle.setAttribute('data-current-lang',language);
    }
    window.dispatchEvent(new CustomEvent('ora-language-change',{detail:{language}}));
  }
  window.ORA_I18N={get language(){return language}, t:(zh,en)=>language==='zh'?zh:en};
  toggle?.addEventListener('click',()=>{
    language = language === 'zh' ? 'en' : 'zh';
    try {window.localStorage.setItem('ora-lang',language)}catch (_){}
    apply();
  });
  apply();
})();
