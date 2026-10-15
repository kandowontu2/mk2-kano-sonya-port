"""Preserve earned0..11 prefix; extend close guard/leg to Raiden and Shang."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_raiden_leg_bench_20261015_preparation'
assert not OUT.exists()
base=ROOT/'video_sonya_late_leg_bench_20261015_preparation'
source=(base/'campaign.lua').read_text()
old=" or (other.roster==10 and stage==11)) then\n"
new=" or (other.roster==10 and stage==11) or (other.roster==7 and stage==12) or (other.roster==6 and stage==14)) then\n"
assert source.count(old)==1
source=source.replace(old,new,1)
assert ':write_' not in source and 'io.open' not in source
OUT.mkdir();lua=OUT/'campaign.lua';lua.write_text(source)
(OUT/'run.py').write_text((base/'run.py').read_text().replace('video_sonya_late_leg_bench_20261015','video_sonya_raiden_leg_bench_20261015'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
(OUT/'preparation.json').write_text(json.dumps(dict(sourceSHA256=sha(lua),runnerSHA256=sha(OUT/'run.py'),baseSourceSHA256=sha(base/'campaign.lua'),physicalScope='Only add native Raiden12/Shang14 to guarded close-leg strategy; all0..11 physical inputs and existing bosses/ownending observers unchanged.',gameUnchanged=True,guestWrites=False,media=False),indent=2))
print(OUT)
