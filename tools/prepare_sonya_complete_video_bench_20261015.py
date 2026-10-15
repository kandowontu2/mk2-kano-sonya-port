"""Extend the actually cleared Kitana controller to the earned own ending."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_complete_bench_20261015_preparation'
assert not OUT.exists()
prior=ROOT/'video_sonya_kitana_leg_bench_20261015_preparation/campaign.lua'
proof=json.loads((ROOT/'video_sonya_kitana_leg_bench_20261015/qualification.json').read_text())
assert proof['passed'] and proof['proof']['nextMileenaFight']['frame']=='107749'
source=prior.read_text()
stop="\nemu.register_frame(function()\n if p:read_u16(0x01061b30)==10 and p:read_u16(0x010601d0)==2 then\n"
assert source.count(stop)==1
source=source[:source.index(stop)]
source=source.replace('frame>=150000','frame>=200000').replace('maximum_fields=150000','maximum_fields=200000')
assert ':write_' not in source and ':snapshot(' not in source and ':pixels(' not in source and 'io.open' not in source
OUT.mkdir();lua=OUT/'campaign.lua';lua.write_text(source)
runner=(ROOT/'tools/run_sonya_kitana_leg_video_bench_20261015.py').read_text()
runner=runner.replace('video_sonya_kitana_leg_bench_20261015','video_sonya_complete_bench_20261015')
runner=runner.replace('>300','>360').replace('wall300','wall360').replace("'-str','2800'","'-str','3800'")
# This runner is in a preparation subdirectory, one level deeper than tools.
runner=runner.replace('Path(__file__).resolve().parent.parent','Path(__file__).resolve().parent.parent')
ast.parse(runner);(OUT/'run.py').write_text(runner)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
(OUT/'preparation.json').write_text(json.dumps(dict(sourceSHA256=sha(lua),runnerSHA256=sha(OUT/'run.py'),priorSourceSHA256=sha(prior),kitanaProofSHA256=sha(ROOT/'video_sonya_kitana_leg_bench_20261015/qualification.json'),changedScope='Only remove native stage10 diagnostic stop and extend host deadline; physical controls and native ending observers unchanged.',physicalInputsOnly=True,media=False,frameCap=200000,wholeCampaignUnproven=True),indent=2))
print(OUT)
