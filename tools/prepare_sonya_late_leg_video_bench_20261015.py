"""Keep proven early/Kitana inputs; test the same guard/leg policy at10/11."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_late_leg_bench_20261015_preparation'
assert not OUT.exists()
base=ROOT/'video_sonya_complete_bench_20261015_preparation'
source=(base/'campaign.lua').read_text()
old="   if fighter=='sonya' and side==2 and other.roster==4 and stage==9 then\n"
new="   if fighter=='sonya' and side==2 and ((other.roster==4 and stage==9) or (other.roster==5 and stage==10) or (other.roster==10 and stage==11)) then\n"
assert source.count(old)==1
source=source.replace(old,new,1)
source=source.replace("log('KITANA_LEG_PLAN',string.format('stage=9 gap=%d human_action=%d cpu_action=%d health=%d,%d',gap", "log('LATE_LEG_PLAN',string.format('stage=%d gap=%d human_action=%d cpu_action=%d health=%d,%d',stage,gap",1)
assert ':write_' not in source and 'io.open' not in source
OUT.mkdir();lua=OUT/'campaign.lua';lua.write_text(source)
runner=(base/'run.py').read_text().replace('video_sonya_complete_bench_20261015','video_sonya_late_leg_bench_20261015')
(OUT/'run.py').write_text(runner)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
(OUT/'preparation.json').write_text(json.dumps(dict(sourceSHA256=sha(lua),runnerSHA256=sha(OUT/'run.py'),baseSourceSHA256=sha(base/'campaign.lua'),physicalScope='Only add native Mileena stage10 and Scorpion stage11 to guarded close-leg policy that earned Kitana KOs. Identical prior0..9 physical prefix, existing boss/ending controls conserved.',gameUnchanged=True,guestWrites=False,media=False),indent=2))
print(OUT)
