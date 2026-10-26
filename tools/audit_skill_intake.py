#!/usr/bin/env python3
"""Validate curated SKILL.md source metadata and maintain a dated offline audit report.
This neither fetches upstream resources nor executes third-party skills.
"""
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
catalog=json.loads((ROOT/'catalog/index.json').read_text(encoding='utf-8'))
entries=sorted(
    (e for e in catalog['entries']
     if e.get('execution',{}).get('scope')=='source-metadata-reviewed-not-executed'),
    key=lambda e:e['id'])
if len(entries)<13:
    raise SystemExit('Too few inspected individual skills in catalog')
lines=["# 独立 Skill 来源记录审计 / Individual Skill Source Audit","","> 本报告核对的是**本站登记的上游文件和操作摘要元数据**，不是重新访问 GitHub、执行第三方技能或验证其效果。 / This validates saved source metadata, not live remote status or skill performance.","","| 资产 ID | 母仓库 | 官方 SKILL.md 文件 | Blob SHA 前缀 | 核验日 |","|---|---|---|---|---|"]
for e in entries:
    x=e['execution']
    c=e['curation']
    source=e.get('links',{}).get('source','')
    root='https://github.com/'+c['github_repo']+'/blob/main/'
    if not (c.get('track')=='popular' and c.get('type')=='skill' and
            c.get('star_scope')=='parent-repository' and
            source.startswith(root) and source.endswith('/SKILL.md')):
        raise SystemExit('Incorrect upstream source / star scope: '+e['id'])
    if not re.fullmatch(r'[a-f0-9]{40}',x.get('source_file_sha','')):
        raise SystemExit('Missing blob SHA: '+e['id'])
    if not re.fullmatch(r'20\d{2}-\d{2}-\d{2}',x.get('source_checked_on','')):
        raise SystemExit('Missing checked date: '+e['id'])
    for field in ('inputs','outputs','requirements','steps','checks'):
        if not all(isinstance(x.get(field,{}).get(lang),list)
                   and len(x[field][lang])>0
                   and all(isinstance(item,str) and item.strip() for item in x[field][lang])
                   for lang in ('zh','en')):
            raise SystemExit('Invalid bilingual execution guidance '+e['id']+' '+field)
    path=source[len(root):]
    lines.append('| `{}` | `{}` | `{}` | `{}` | {} |'.format(
        e['id'],c['github_repo'],path,x['source_file_sha'][:12],x['source_checked_on']))
lines+=["",f"**登记完整的独立 Skill：{len(entries)} 条 / Inspected individual skills: {len(entries)}.**","",
"核验命令：`python3 tools/audit_skill_intake.py --check`。首次生成或更新：`python3 tools/audit_skill_intake.py`。","",
"限制：须阅读上游原始文件与许可证并核对最新改动。静态 SHA 能记录检查时的具体版本，不保证项目现在未变化。",""]
output='\n'.join(lines)
destination=ROOT/'docs/SKILL_INTAKE_AUDIT.md'
if args.check:
    if not destination.exists() or destination.read_text(encoding='utf-8')!=output:
        raise SystemExit('STALE: docs/SKILL_INTAKE_AUDIT.md')
    print('PASS: locally audited',len(entries),'source inspected SKILL.md entries')
else:
    destination.write_text(output,encoding='utf-8')
    print('Generated docs/SKILL_INTAKE_AUDIT.md')
