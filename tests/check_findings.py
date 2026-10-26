#!/usr/bin/env python3
"""Offline contract checks for Findings; no fabricated external source fixtures on site."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import update_findings as collector
import findings_enrichment as enrichment
import findings_offline_translate as offline
import findings_editorial_zh as editorial
import findings_zh_typography as typography
from unittest.mock import patch

SOURCES=('papers','github','skills','workflows')

def check_snapshot(path:Path)->None:
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data.get('schema_version')=='1','Unexpected schema version'
    assert set(data['feeds'])==set(SOURCES),'Expected four distinct sources'
    assert data.get('generated_at') is None or re.fullmatch(r'\d{4}-\d\d-\d\dT.+Z',data['generated_at'])
    if 'translation_coverage' in data:
        coverage=data['translation_coverage']
        assert isinstance(coverage['translated'],int)
        assert isinstance(coverage['total'],int)
        assert 0<=coverage['translated']<=coverage['total']
        assert coverage['total']==sum(len(f['items']) for f in data['feeds'].values())
    for key,feed in data['feeds'].items():
        assert feed['status'] in ('pending','ok','stale','unavailable'),(key,'unsupported source state')
        assert isinstance(feed['items'],list) and len(feed['items'])<=(100 if key=='papers' else 14)
        assert collector.valid_url(feed['url']), (key,'invalid source URL')
        if feed['status'] in ('ok','stale'):
            assert feed['items'] and feed['fetched_at'], (key,'no audited source snapshot')
        if feed['status']=='ok':
            assert feed['metric_note'] and feed['source']
        for value in feed['items']:
            assert value.get('title') and value.get('url'),(key,'incomplete item')
            assert collector.valid_url(value['url']), (key,'untrusted item URL')
            assert len(value['title'])<=210 and len(value.get('subtitle',''))<=780 and len(value.get('detail',''))<=6000
            assert 'value' not in value or (type(value['value']) is int and value['value']>=0)
            if value.get('summary_source'):
                assert value['summary_source'] in ('paper abstract','repository README')
            for translated_field in ('title_zh','subtitle_zh','detail_zh'):
                if translated_field in value:
                    assert isinstance(value[translated_field],str) and len(value[translated_field])<=8500
            assert value.get('metric') in ('upvotes','total installs','stars gained this week','total stars','position'),(key,'unsupported metric')
    print('PASS: Findings source provenance, freshness and safe metrics')

class FindingsCollectorTests(unittest.TestCase):
    def test_parse_github_trending(self):
        sample='''<main>
        <article class="Box-row">
        <h2 class="h3"><a href="/example-org/agent-workflows">example-org / agent-workflows</a></h2>
        <p class="col-9">Open research tools</p>
        <span>1,234 stars this week</span>
        </article><article class="Box-row">
        <h2><a href="/another/visual-skill">another / visual-skill</a></h2>
        <p>Figure workflows</p></article></main>'''
        values=collector.parse_github_trending(sample)
        self.assertEqual([x['title'] for x in values],['example-org/agent-workflows','another/visual-skill'])
        self.assertEqual(values[0]['value'],1234)
        self.assertEqual(values[0]['metric'],'stars gained this week')
        self.assertNotIn('value',values[1])
        self.assertEqual(values[0]['url'],'https://github.com/example-org/agent-workflows')

    def test_source_failure_does_not_invent_items(self):
        self.assertEqual(collector.fallback_feed('HF','https://huggingface.co/papers',None)['items'],[])
        old={'source':'HF','url':'https://huggingface.co/papers','items':[{'title':'Verified','url':'https://huggingface.co/papers/2601.12345'}],
             'fetched_at':'2026-10-26T00:00:00Z','status':'ok','metric_note':'HF upvotes'}
        saved=collector.fallback_feed('HF','https://huggingface.co/papers',old)
        self.assertEqual(saved['status'],'stale')
        self.assertEqual(saved['fetched_at'],old['fetched_at'])
        self.assertEqual(saved['items'],old['items'])

    def test_chinese_punctuation_preserves_versions_urls_code_and_decimals(self):
        cases = [
            ('模型改进. 下一步测试,效果更好!', '模型改进。下一步测试，效果更好！'),
            ('参数为v2.6.3,准确率96.3%. 接下来讨论.', '参数为v2.6.3，准确率96.3%。接下来讨论。'),
            ('我们记录1,200个样本,处理时间10:30,完毕.', '我们记录1,200个样本，处理时间10:30，完毕。'),
            ('代码在https://github.com/team/repo,详情见README.md. 继续.',
             '代码在https://github.com/team/repo，详情见README.md。继续。'),
            ('中文内容: 模型v1.2.3; 基础结论? 是的!',
             '中文内容：模型v1.2.3；基础结论？是的！'),
            ('引用package.json,访问README.md,然后执行测试.',
             '引用package.json，访问README.md，然后执行测试。'),
            ('English only. Keep 1.2, and URL https://example.com.', 
             'English only. Keep 1.2, and URL https://example.com.'),
        ]
        for original, expected in cases:
            with self.subTest(original=original):
                actual=typography.normalize_zh_typography(original)
                self.assertEqual(actual,expected)
                self.assertEqual(typography.normalize_zh_typography(actual),expected)

    def test_chinese_field_only_normalization(self):
        record={'title':'Model v2.6: Report', 'subtitle':'The model improves.',
                'title_zh':'模型v2.6: 研究报告',
                'subtitle_zh':'模型v2.6在这里. 进一步分析,没有问题.',
                'detail_zh':'准确率为96.3%,模型在github.com发布.'}
        feeds={'papers':{'items':[record]}}
        self.assertEqual(typography.normalize_translated_feeds(feeds),3)
        self.assertEqual(record['title_zh'],'模型v2.6：研究报告')
        self.assertEqual(record['subtitle_zh'],'模型v2.6在这里。进一步分析，没有问题。')
        self.assertEqual(record['detail_zh'],'准确率为96.3%，模型在github.com发布。')
        self.assertEqual(record['title'],'Model v2.6: Report')
        self.assertEqual(record['subtitle'],'The model improves.')
        self.assertEqual(typography.normalize_translated_feeds(feeds),0)

    def test_readme_extraction_is_sourced_and_clean(self):
        readme = "# Repository Overview\n\nThis research tool collects genuine papers and describes them with source citations.\n\n" \
                 "It supports reusable research workflows and has public experiment notes.\n\n" \
                 "```bash\nnever run arbitrary commands\n```"
        text = enrichment.clean_text(readme)
        self.assertIn("genuine papers", text)
        self.assertNotIn("never run arbitrary commands", text)

    def test_translation_caches_without_secret(self):
        feeds={'papers':{'status':'ok','items':[{'url':'https://huggingface.co/papers/2610.12345',
          'title':'Source paper title', 'detail':'A scientifically grounded source abstract sentence. ' * 5,
          'subtitle':'A scientifically grounded source abstract sentence.'}]}}
        old={'papers':{'items':[{'url':'https://huggingface.co/papers/2610.12345',
          'title':'Source paper title', 'title_zh':'原始论文题名',
          'detail':'A scientifically grounded source abstract sentence. ' * 5,
          'detail_zh':'一段有真实来源的中文论文摘要。'}]}}
        with patch.dict('os.environ',{'GOOGLE_TRANSLATE_API_KEY':''}):
            state,count=enrichment.add_translations(feeds,old,key='')
        self.assertEqual(state,'cached')
        self.assertGreaterEqual(count,2)
        self.assertEqual(feeds['papers']['items'][0]['title_zh'],'原始论文题名')
        self.assertTrue(feeds['papers']['items'][0]['subtitle_zh'])

    def test_offline_translation_and_source_exact_caching(self):
        class MockEngine:
            def __init__(self): self.calls=0
            def translate(self,value):
                self.calls+=1
                return '这是一段机器翻译的中文原始资料摘要，保留来源证据。'
        text='English research abstract about robot agents and visible planning.'
        paper={'url':'https://huggingface.co/papers/2610.00001','title':'Research on Agents',
               'detail':text,'subtitle':text[:30]}
        repo={'url':'https://github.com/author/project','title':'author/project',
              'subtitle':'An English GitHub repository for research automation and agents.'}
        feeds={'papers':{'status':'ok','items':[paper]},'github':{'status':'ok','items':[repo]}}
        engine=MockEngine()
        state,count=offline.add_offline_translations(feeds,{},translator=engine,seconds=1000)
        self.assertEqual(state,'offline_argos')
        self.assertEqual(count,3)
        self.assertTrue(offline.is_chinese(paper['title_zh']))
        self.assertTrue(offline.is_chinese(paper['subtitle_zh']))
        self.assertTrue(offline.is_chinese(repo['subtitle_zh']))
        self.assertEqual(engine.calls,3)
        old={k:{'items':[dict(v) for v in feed['items']]} for k,feed in feeds.items()}
        fresh={'papers':{'status':'ok','items':[{'url':paper['url'],'title':paper['title'],'detail':text}]},
               'github':{'status':'ok','items':[{'url':repo['url'],'title':repo['title'],
                         'subtitle':repo['subtitle']}]}}
        engine2=MockEngine()
        state,count=offline.add_offline_translations(fresh,old,translator=engine2,seconds=1000)
        self.assertEqual(state,'cached')
        self.assertEqual(engine2.calls,0)
        self.assertEqual(count,3)

    def test_chinese_source_is_translated_back_for_english_page(self):
        chinese='这是一套中文研究工具，能够组织多智能体流程并生成可追溯的实验报告。'
        entry={'title':'author/chinese-research', 'url':'https://github.com/author/chinese-research',
               'subtitle':chinese}
        feeds={'workflows':{'status':'ok','items':[entry]}}
        class Reverse:
            def translate(self,value):
                return 'A research tool for multi-agent workflows and traceable experimental reports.'
        with patch.object(offline,'load_translator',return_value=Reverse()):
            state,n=offline.add_offline_translations(feeds,{},translator=Reverse(),seconds=999)
        self.assertEqual(state,'offline_argos')
        self.assertEqual(n,1)
        self.assertEqual(entry['subtitle_zh'],chinese)
        self.assertIn('research tool',entry['subtitle_en'])

    def test_bilingual_readme_is_not_misclassified_as_chinese(self):
        mixed='An agent research tool for advanced workflows with a 中文 installation note.'
        self.assertFalse(offline.is_chinese(mixed))
        self.assertTrue(offline.is_chinese('这是一个有完整中文版描述的研究工作流'))

    def test_source_exact_chinese_review_override(self):
        original={'url':'https://github.com/example/workflow','title':'example/workflow',
                  'subtitle':'Public source workflow description', 'subtitle_zh':'机械翻译错误'}
        rule={'overrides':[{'url':original['url'],
                'source_title':original['title'],
                'source_subtitle':original['subtitle'],
                'subtitle_zh':'源文一致时才采用准确的中文表述。'}]}
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'reviewed.json'
            path.write_text(json.dumps(rule,ensure_ascii=False),encoding='utf-8')
            feeds={'workflows':{'items':[original]}}
            self.assertEqual(editorial.apply_editorial_chinese(feeds,path),1)
            self.assertEqual(original['subtitle_zh'],'源文一致时才采用准确的中文表述。')
            original['subtitle']='Upstream author changed the project description'
            self.assertEqual(editorial.apply_editorial_chinese(feeds,path),0)
            self.assertEqual(original['subtitle_zh'],'源文一致时才采用准确的中文表述。')
            # Runtime collector supplies new English text before this check;
            # stale wording must never replace a machine translation again.

    def test_missing_translate_key_never_creates_fake_zh(self):
        feeds={'skills':{'status':'ok','items':[{'url':'https://github.com/a/b',
          'subtitle':'A public skill without translated source information.'}]}}
        with patch.dict('os.environ',{'GOOGLE_TRANSLATE_API_KEY':''}):
            state,n=enrichment.add_translations(feeds,{},key='')
        self.assertEqual((state,n),('not_configured',0))
        self.assertNotIn('subtitle_zh',feeds['skills']['items'][0])

    def test_only_safe_sources(self):
        self.assertFalse(collector.valid_url('javascript:alert(1)'))
        self.assertFalse(collector.valid_url('https://not-github.com/repo','github.com'))
        self.assertEqual(collector.valid_url('https://github.com/a/b','github.com'),'https://github.com/a/b')
        with self.assertRaises(ValueError):
            collector.item(title='fake',url='javascript:alert(1)')

if __name__=='__main__':
    if '--snapshot' in sys.argv:
        check_snapshot(ROOT/'data/findings.json')
        sys.argv.remove('--snapshot')
    unittest.main(verbosity=1)
