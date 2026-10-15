"""Use the actually successful Kano charge-recovery uppercut controls for Sonya.

Only final Shao controls change. All prior earned-ladder physical input bodies
and ending observers are retained. Four extra native read taps observe charge;
one existing owned-human write tap observes actual crouch-loop timing.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_shao_counter_bench_20261015_preparation'
assert not OUT.exists()
base=ROOT/'video_sonya_raiden_leg_bench_20261015_preparation'
source=(base/'campaign.lua').read_text()
kpath=ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation/campaign.lua'
kano=kpath.read_text()
start=kano.index('    if stage==16 then\n');end=kano.index('    elseif quiet then\n',start)
branch=kano[start:end]
oldstart=source.index('    if stage==16 then\n');oldend=source.index('    elseif quiet then\n',oldstart)
original=source[oldstart:oldend];source=source[:oldstart]+branch+source[oldend:]
locals='local cg_loop,cg_loop_main=nil,nil\nlocal cg_contact,cg_main,cg_down,cg_pulse=nil,nil,nil,nil\n'
source=locals+source
needle="      log('BOSS_ACTION',string.format("
assert source.count(needle)==1
added="      if current_stage==16 and data&0xffff==770 and cpu.PC.value==0xff82fa80 then cg_loop=frame;cg_loop_main=observed_main end\n"
source=source.replace(needle,added+needle,1)
tapstart=kano.index('for _,entry in ipairs({0xff9d20d0,0xff9d24c0,0xff9d26b0,0xff9d27f0})do\n')
observer=kano[tapstart:]
assert observer.endswith('end\n') and observer.count("h.id~=17")==1 and ':write_' not in observer
observer=observer.replace('h.id~=17','h.id~=18',1)
source+='\n'+observer
assert ':write_' not in source and ':pixels(' not in source and ':snapshot(' not in source and 'io.open' not in source
OUT.mkdir();lua=OUT/'campaign.lua';lua.write_text(source)
(OUT/'run.py').write_text((base/'run.py').read_text().replace('video_sonya_raiden_leg_bench_20261015','video_sonya_shao_counter_bench_20261015'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
(OUT/'preparation.json').write_text(json.dumps(dict(sourceSHA256=sha(lua),runnerSHA256=sha(OUT/'run.py'),baseSourceSHA256=sha(base/'campaign.lua'),successfulKanoControllerSHA256=sha(kpath),physicalScope='Only stage16: original16field backjump; crouch-block charge, release Block during measured recovery, fresh HP from actual owned native crouch loop. Same branch that earned Kano finalShao win. Four passive charge reads and one added scalar crouch observation; no game writes.',previousKintaroKOs=[159997,162275],wholeSonyaCampaignUnproven=True,media=False),indent=2))
print(OUT)
