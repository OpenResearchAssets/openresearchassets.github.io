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

SOURCES=('papers','github','skills','workflows')

def check_snapshot(path:Path)->None:
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data.get('schema_version')=='1','Unexpected schema version'
    assert set(data['feeds'])==set(SOURCES),'Expected four distinct sources'
    assert data.get('generated_at') is None or re.fullmatch(r'\d{4}-\d\d-\d\dT.+Z',data['generated_at'])
    for key,feed in data['feeds'].items():
        assert feed['status'] in ('pending','ok','stale','unavailable'),(key,'unsupported source state')
        assert isinstance(feed['items'],list) and len(feed['items'])<=(40 if key=='papers' else 14)
        assert collector.valid_url(feed['url']), (key,'invalid source URL')
        if feed['status'] in ('ok','stale'):
            assert feed['items'] and feed['fetched_at'], (key,'no audited source snapshot')
        if feed['status']=='ok':
            assert feed['metric_note'] and feed['source']
        for value in feed['items']:
            assert value.get('title') and value.get('url'),(key,'incomplete item')
            assert collector.valid_url(value['url']), (key,'untrusted item URL')
            assert len(value['title'])<=210 and len(value.get('subtitle',''))<=780 and len(value.get('detail',''))<=2600
            assert 'value' not in value or (type(value['value']) is int and value['value']>=0)
            if value.get('summary_source'):
                assert value['summary_source'] in ('paper abstract','repository README')
            for translated_field in ('title_zh','subtitle_zh','detail_zh'):
                if translated_field in value:
                    assert isinstance(value[translated_field],str) and len(value[translated_field])<=3000
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
