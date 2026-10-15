"""Input-only Kitana strategy test before another large campaign recording."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_kitana_leg_bench_20261015_preparation'
assert not OUT.exists()
oldpath=ROOT/'video_sonya_early_ladder_20261015_preparation/campaign.lua'
assert hashlib.sha256(oldpath.read_bytes()).hexdigest().upper()=='360CF4F2AFB65296445C11D4FFDC8ADE88A71747EEDA44592D43406708FBD051'
old=oldpath.read_text()
source=old[:old.index('-- Stream every native video frame.')]
source=source.replace('frame>=200000','frame>=150000').replace('maximum_fields=200000','maximum_fields=150000')
marker="   if leg_tactic and other.roster==18 then\n"
assert source.count(marker)==1
policy='''   if fighter=='sonya' and side==2 and other.roster==4 and stage==9 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    if not k9_last or frame-k9_last~=1 then k9_leg=nil;k9_retry=-1000;k9_guard=-1000 end
    k9_last=frame
    local blocking=human.action==1792 or human.action==1793
    local ready=height<=8 and (blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==263)
    if other.action==4 or other.action==8 or other.action==10 or other.action==16 then k9_guard=frame+32 end
    if k9_leg and frame-k9_leg<12 then
     local age=frame-k9_leg
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif height>8 then
     press('Block');if gap<105 and frame%6<3 then press('High Kick')end
    elseif cpu_height>15 then
     press('Down');press('Block')
    elseif gap>110 and (frame<k9_guard or other.flags&0x10~=0) then
     press('Down');press('Block')
    elseif ready and gap<110 and frame-k9_retry>=40 then
     k9_leg=frame;k9_retry=frame;press('Down')
     log('KITANA_LEG_PLAN',string.format('stage=9 gap=%d human_action=%d cpu_action=%d health=%d,%d',gap,human.action,other.action,human.hp,other.hp))
    elseif ready and gap>100 and cpu_height<=8 then
     press(forward)
    else press('Down');press('Block')end
'''
source=source.replace(marker,policy+marker.replace('   if ','   elseif ',1),1)
source='local k9_last,k9_leg,k9_retry,k9_guard=nil,nil,-1000,-1000\n'+source
source+='''
emu.register_frame(function()
 if p:read_u16(0x01061b30)==10 and p:read_u16(0x010601d0)==2 then
  local h,c=sample(2),sample(1)
  if h and c and h.id==18 and h.roster==18 and c.roster==5 and p:read_u16(slots[2].state)==1 and p:read_u16(slots[1].state)==0 then
   log('KITANA_BENCH_COMPLETE','native_stage=10 human=18:18 cpu=5:5 no_guest_writes=true')
   manager.machine:exit()
  end
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source and ':pixels(' not in source and 'io.open' not in source
OUT.mkdir();(OUT/'campaign.lua').write_text(source)
(OUT/'preparation.json').write_text(json.dumps(dict(sourceSHA256=hashlib.sha256((OUT/'campaign.lua').read_bytes()).hexdigest().upper(),changedScope='Stage9 only, physically close under grounded projectile guard, ordinary D/LP+Block leg chord; no health/AI/difficulty/RNG/state changes.',frameCap=150000,video=False,audio=False,positiveOutcomeRequired='Native same-paid Kitana win and Mileena stage10 live fighter; an observed entry alone is insufficient'),indent=2))
print(OUT)
