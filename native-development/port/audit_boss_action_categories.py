"""Source-only boss dispatch compatibility audit; not boss runtime proof."""
import hashlib
import json
from pathlib import Path
import re
import zipfile
from inventory_character_tables import source_tables
from prepare_game_candidate import ZIP
from boss_category_source import integrate,category

PORT=Path(__file__).resolve().parent;SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
boss=(SRC/'MKBOSS.ASM').read_text()
with zipfile.ZipFile(ZIP) as archive:
    original=archive.read('mk2-rebuild-main/src/MKBOSS.ASM').decode('cp437').replace('\r\n','\n')
assert boss.rstrip()==integrate(original).rstrip()
tables=source_tables(boss)
dispatch={name:[value for row in tables[name]['rows'] for value in row['values']]
          for name in ('goro_catagory_jumps','kahn_catagory_jumps')}
assert all(len(values)==9 for values in dispatch.values())
equates=(SRC/'MAINEQU.ASM').read_text()
entries=(('KANOMOV.ASM','ks_kano_ball',2),('SONYAMOV.ASM','ks_sonya_square',2),
         ('KSPROJ.ASM','ks_kano_knife',0),('KSPROJ.ASM','ks_sonya_ring',0),
         ('KSBLADE.ASM','ks_kano_blade',1),('KSCHOKE.ASM','ks_kano_choke',2),
         ('KSLEG.ASM','ks_sonya_leg',2),('KSBIKE.ASM','ks_sonya_bike',2))
cases=[]
for filename,label,expected in entries:
    text=(SRC/filename).read_text()
    body=text.split('\n'+label+'\n',1)[1]
    token=re.search(r'movi\s+(\w+),a1\s+calla init_special_act',body)[1]
    if not token.lower().endswith('h'):
        token=re.search(r'(?m)^'+token+r'\s+\.set\s+(\w+)',text+'\n'+equates)[1]
    action=int(token[:-1],16)
    classified=category(17 if label.startswith('ks_kano') else 18,action)
    cases.append(dict(move=label,action=f'{action:04X}',rawCategory=action>>8,currentCategory=classified,
        expectedCategory=expected,categoryMatches=classified==expected,
        currentBossRoutes={name:values[classified] for name,values in dispatch.items()}))
report=dict(scope='Current entry tags versus unchanged original boss category dispatch',
    bossSourceSHA256=hashlib.sha256((SRC/'MKBOSS.ASM').read_bytes()).hexdigest().upper(),
    cases=cases,allEntryCategoriesMatch=all(case['categoryMatches'] for case in cases),
    runtimeBossBehaviorVerified=False,releaseReady=False)
(PORT/'BOSS_ACTION_CATEGORY_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
