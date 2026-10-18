"""Inventory ordinary attack tags in audited campaigns, never infer unseen moves."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SYMBOLS=BASE/'mk2-rebuild-main/srcp/MAINEQU.ASM'
NORMALS=('act_hipunch','act_lopunch','act_hikick','act_medkick','act_rhouse',
         'act_sweep','act_uppercut','act_jupkick','act_juppunch','act_duckpunch',
         'act_duck_kickh','act_duck_kickl','act_flykick','act_flypunch')

def inventory(rows,actor,actions):
    counts=collections.Counter()
    for row in rows:
        if row['mode']=='2' and row['p1selected']==row['p1char']==str(actor):
            counts[int(row['p1action'])]+=1
    return {name:dict(action=actions[name],sampledFields=counts[actions[name]],
                     observed=counts[actions[name]]>0) for name in NORMALS}

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def main():
    actions={name:int(value,16) for name,value in re.findall(r'^(act_\w+)\s+\.set\s+([0-9a-fA-F]+)H',SYMBOLS.read_text(),re.M)}
    cases=[]
    for name,actor in [('stock_wolf_2219_kano_boss_guard',17),('stock_wolf_2219_sonya_campaign',18)]:
        flags=getattr(subprocess,'CREATE_NO_WINDOW',0)|getattr(subprocess,'BELOW_NORMAL_PRIORITY_CLASS',0)
        subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],check=True,
                       stdout=subprocess.DEVNULL,creationflags=flags)
        run=BASE/name
        with (run/'campaign.csv').open() as stream:result=inventory(csv.DictReader(stream),actor,actions)
        cases.append(dict(actor=actor,run=name,ordinaryAttackTags=result,
            unobserved=[key for key,value in result.items() if not value['observed']],
            pins={str(path):sha(path) for path in (run/'execution.json',run/'autoboot.lua',run/'campaign.csv',SYMBOLS)}))
    report=dict(scope='Sampled action tags in two finite campaigns, not command/hit/animation/recovery proof',
                cases=cases,allNormalsVerified=False,fullPortVerified=False)
    (PORT/'CAMPAIGN_NORMALS_2219.json').write_text(json.dumps(report,indent=2)+'\n')
    for case in cases:print(case['actor'],'unobserved ordinary tags:',', '.join(case['unobserved']))

if __name__=='__main__':main()
