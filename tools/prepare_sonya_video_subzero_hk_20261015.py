"""Prepare narrow physical SubZero successor; preserve executed failed video."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_subzero_hk_20261015_preparation'
assert not OUT.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
oldpath=ROOT/'video_sonya_full_20261015_preparation/campaign.lua'
old=oldpath.read_text()
currentpath=ROOT/'audit_current_sonya_p2_jax_standing_guard_preparation/campaign.lua'
assert sha(currentpath)=='8733AF20BDB2431C39D36F6ECCB1FC54ACFC6BB14E6753C3BDD4727221BD2E02'
current=currentpath.read_text()
begin="   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) then\n"
a=current.index(begin)
b=current.index("   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw')",a)
branch=current[a:b]
branch=branch.replace(begin,"   if fighter=='sonya' and side==2 and other.roster==8 and stage==1 then\n",1)
needle="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then\n"
assert old.count(needle)==1
lua=old.replace(needle,branch+needle.replace('   if ','   elseif ',1),1)
lua="local sh_last,sh_start,sh_retry=nil,nil,-1000\nlocal sr_start,sr_direction=nil,nil\n"+lua
lua=lua.replace('frame>=80000','frame>=120000').replace('maximum_fields=80000','maximum_fields=120000').replace('video_frames<=80000','video_frames<=120000')
assert ':write_' not in lua and 'read_range' not in lua and 'screen:snapshot' not in lua
OUT.mkdir();(OUT/'campaign.lua').write_text(lua)
runner=(ROOT/'video_sonya_full_20261015_preparation/run.py').read_text()
runner=runner.replace("OUT=ROOT/'video_sonya_full_20261015'", "OUT=ROOT/'video_sonya_subzero_hk_20261015'")
runner=runner.replace("LUA=ROOT/'video_sonya_full_20261015_preparation/campaign.lua'", "LUA=ROOT/'video_sonya_subzero_hk_20261015_preparation/campaign.lua'")
assert sha(oldpath) in runner
runner=runner.replace(sha(oldpath),sha(OUT/'campaign.lua'))
runner=runner.replace('frames<=80000','frames<=120000').replace('350*1024**2','450*1024**2').replace('wav350MiB','wav450MiB')
ast.parse(runner);(OUT/'run.py').write_text(runner)
(OUT/'preparation.json').write_text(json.dumps(dict(preparedNotRun=True,
 currentSubZeroSource=str(currentpath),currentSourceSHA256=sha(currentpath),
 executedVideoController=str(oldpath),executedVideoControllerSHA256=sha(oldpath),
 luaSHA256=sha(OUT/'campaign.lua'),runnerSHA256=sha(OUT/'run.py'),
 exactChangedPhysicalScope='Only actualSonyaP2 versusSubZero8 atstage1: currentqualified standingHK pressure/attackguard/retreatbelow90 and nativeD,F,LP Ringfinish<=33HP. Exact currentbranchbody retained and guard narrowedto8stage1. Every other historicalcontroller physicalbranch/paidcontinues/boss/ending/capture unchanged. Two local timingvariables groups isolated.',
 positiveCurrentSubZeroEvidence='audit_current_sonya_p2_subzero_match_advance_checked/report.json: earnedSubZero samepaid14594 rounds15397/16802 thenCage17315. Not a currentfullcampaignwin guarantee.',
 actualFailedPolicy='Executed currenthistoricalRingstrategy remainedSubZero1 through19losses by67482; failure is weakbotpolicy, notcharacteractivationdefect.',
 noGameMutation=True,currentFullCompletionAssumed=False,
 limits='120000frames600sec320/384/128MiB/WAV450MiB/video250MiB/text20MiB;4:3SAR127/150',currentClearReportSHA256=sha(ROOT/'audit_current_sonya_p2_subzero_match_advance_checked/report.json')),indent=2))
print(OUT,sha(OUT/'campaign.lua'),sha(OUT/'run.py'))
