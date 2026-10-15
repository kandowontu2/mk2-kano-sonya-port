"""Combine proven current early-ladder physical policy with historical late policy.

Preparation only. No guest writes, changed game, lowered difficulty, or wins
assumed from the preparation. Keep prior executed attempts immutable.
"""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_early_ladder_20261015_preparation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert not OUT.exists()
base=ROOT/'video_sonya_full_20261015_preparation/campaign.lua'
early=ROOT/'audit_current_sonya_p2_jax_standing_guard_preparation/campaign.lua'
assert sha(base)=='9F45F0657C0D174C5DD99405189AEE450AF7D01ED37A4D70F8D3D2E81AB9AC35'
assert sha(early)=='8733AF20BDB2431C39D36F6ECCB1FC54ACFC6BB14E6753C3BDD4727221BD2E02'
old=base.read_text();current=early.read_text()
start=current.index("   if leg_tactic and other.roster==18 then\n")
end=current.index("   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw')",start)
prefix=current[start:end]
# Identical bodies, but late-game victims use the historically completed
# Ring/guard policy instead of the early-ladder leg policy.
prefix=prefix.replace("   elseif fighter=='sonya' and side==2 and (other.roster==8", "   elseif stage<=8 and fighter=='sonya' and side==2 and (other.roster==8",1)
needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then\n"
assert old.count(needle)==1
replacement="   leg_tactic=stage<=8\n"+prefix+needle.replace('   if ','   elseif ',1)
lua=old.replace(needle,replacement,1)
locals='''local jgl_last,jgl_pulse=nil,nil
local jgl_until,jgl_jump=-1000,-1000
local kl_last,kl_pulse=nil,nil
local bl_last,bl_pulse=nil,nil
local kg_last,kg_leg,kg_retry,kg_upper,kg_guard=nil,nil,-1000,-1000,-1000
local mg_last,mg_leg,mg_retry,mg_upper,mg_guard=nil,nil,-1000,-1000,-1000
local sh_last,sh_start,sh_retry=nil,nil,-1000
local sr_start,sr_direction=nil,nil
'''
lua=locals+lua
lua=lua.replace('frame>=80000','frame>=200000').replace('maximum_fields=80000','maximum_fields=200000').replace('video_frames<=80000','video_frames<=200001')
assert ':write_' not in lua and 'read_range' not in lua and ':snapshot(' not in lua
# Undo proves all original code and late controls conserved, except host cap.
undo=lua[len(locals):].replace(replacement,needle,1).replace('frame>=200000','frame>=80000').replace('maximum_fields=200000','maximum_fields=80000').replace('video_frames<=200001','video_frames<=80000')
assert undo==old
OUT.mkdir();(OUT/'campaign.lua').write_text(lua)
runner=(ROOT/'video_sonya_subzero_hk_20261015_preparation/run.py').read_text()
runner=runner.replace('video_sonya_subzero_hk_20261015','video_sonya_early_ladder_20261015')
runner=runner.replace('D29AF0C4BA9EBE8BFA3C2BE4B8BF0DD94A354CFDB4DD2D916E053FF8F47EE42A',sha(OUT/'campaign.lua'))
runner=runner.replace('frames<=120000','frames<=200001').replace('450*1024**2','750*1024**2').replace('wav450MiB','wav750MiB').replace('250*1024**2','450*1024**2').replace('video250MiB','video450MiB').replace("'-str','2500'","'-str','3800'")
ast.parse(runner);(OUT/'run.py').write_text(runner)
(OUT/'preparation.json').write_text(json.dumps(dict(preparedNotRun=True,baseSHA256=sha(base),earlyPolicySHA256=sha(early),luaSHA256=sha(OUT/'campaign.lua'),runnerSHA256=sha(OUT/'run.py'),physicalScope='Current mirror/Lao/Liu legguard, SubZero/Cage/Reptile HK+Ring, Baraka/Kano shortleg, Jax standingguard+jump+shortleg at stages0..8; historical guard/Ring controls afterstage8; ordinary paid continues only.',undoToOriginalGate=True,guestWrites=False,bounds='200000 controller fields plus at most one exit video frame;600sec;MAME320MiB/encoder384MiB/host128MiB;WAV750MiB/MP4450MiB/text20MiB',completion='Actual entire current ladder, native boss wins and both own ending pages; no result assumed'),indent=2))
print(OUT,sha(OUT/'campaign.lua'))

if __name__=='__main__':pass
