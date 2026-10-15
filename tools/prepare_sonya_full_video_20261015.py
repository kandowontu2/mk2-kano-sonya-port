"""Prepare current Sonya video from source-only expanded historical controller."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_full_20261015_preparation'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
expanded=OUT/'expanded_historical_controller.lua'
old=expanded.read_text()
assert not (OUT/'campaign.lua').exists()
start=old.index('-- Cold campaign, genuine losses/paid continues.')
body=old[start:]
lines=[]
removed=[]
for line in body.splitlines():
 if any(s in line for s in ['_campaign_emit(', '_campaign_guest(', 'local raw=p:read_range(']):
  removed.append(line);continue
 lines.append(line)
lua='\n'.join(lines)+'\n'
assert len(removed)==8
assert ':pixels(' not in lua and 'read_range' not in lua and ':write_' not in lua
assert 'io.open' not in lua and 'read_block' not in lua and 'snapshot' not in lua
lua=lua.replace("local function log(tag,value)\n", "local function log(tag,value)\n if (tag=='INPUT' and frame>=1690)or tag=='BOSS_HANDLER' then return end\n")
# Host-only frame cap; physical policy and every native observer remain unchanged.
site='emu.register_frame(function()\n frame=frame+1'
assert site in lua
lua=lua.replace(site,"emu.register_frame(function()\n if frame>=80000 then log('HOST_BOUND','maximum_fields=80000');manager.machine:exit();return end\n frame=frame+1",1)
kano=(ROOT/'video_kano_full_20261015_preparation/campaign.lua').read_text()
capture=kano[kano.index('-- Stream every native video frame.'):]
lua+=capture
(OUT/'campaign.lua').write_text(lua)
runner=(ROOT/'video_kano_full_20261015_preparation/run.py').read_text()
runner=runner.replace("OUT=ROOT/'video_kano_full_20261015'", "OUT=ROOT/'video_sonya_full_20261015'")
runner=runner.replace("LUA=ROOT/'video_kano_full_20261015_preparation/campaign.lua'", "LUA=ROOT/'video_sonya_full_20261015_preparation/campaign.lua'")
runner=runner.replace('8F48B1D550B0B12049B0AC823BDEC0437C8DE46CB566BDC6CBF23D017B460F87',sha(OUT/'campaign.lua'))
runner=runner.replace("final=OUT/'Kano_full_playthrough.mp4'", "final=OUT/'Sonya_full_playthrough.mp4'")
runner=runner.replace("MK2KS_TEST_FIGHTER='kano'", "MK2KS_TEST_FIGHTER='sonya'")
runner=runner.replace("MK2KS_CAMPAIGN_STRATEGY='zoning'", "MK2KS_CAMPAIGN_STRATEGY='guard_punish'")
runner=runner.replace("x['human']=='17:17'", "x['human']=='18:18'")
runner=runner.replace('True Kano throughout campaign','True Sonya throughout campaign')
runner=runner.replace("'-crf','20','-pix_fmt'", "'-crf','20','-vf','setsar=127/150','-pix_fmt'")
ast.parse(runner)
(OUT/'run.py').write_text(runner)
trace=(OUT/'offline_read_trace.txt').read_text().splitlines()
pins={p:sha(ROOT/p) for p in trace}
pins[str(expanded.relative_to(ROOT))]=sha(expanded)
(OUT/'preparation.json').write_text(json.dumps(dict(preparedNotRun=True,currentBuildExpected=True,historicalFullClearOnly=True,currentCompletionNotAssumed=True,
 historicalSource='mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua',historicalRun='audit_v5689_verified_subzero_sonya_p2_campaign/run.log.gz',historicalCompletionFrame=77819,
 offlineExpansion='Bundled standaloneLua interpreter executes string transformations only. Final load intercepted before any guest code; explicitreadtrace13files. No emulator launched for expansion; no historicalPython collector imported.',
 luaSHA256=sha(OUT/'campaign.lua'),runnerSHA256=sha(OUT/'run.py'),sourcePins=pins,removedRawAndSnapshotLines=removed,
 changes='Drop rawdump helper prefix and8rawRAM/snapshot call lines; filter diagnostic INPUT/BOSS_HANDLER text only, add host80000fieldbound and identicalstreamingobserver. All physical policy/nativefeedback/taps preserved.',
 limits='80000fields600sec/MAME320MiB/ffmpeg384MiB/host128MiB/WAV350MiB/video250MiB/text20MiB',
 authenticity='Must actually clear current ladder,bosses,ownending2pages. If not, do not label successful fullplaythrough. No health/difficulty/position/AI/state writes or staged opponents.',rawFrameDisk=False),indent=2))
print(OUT,sha(OUT/'campaign.lua'),sha(OUT/'run.py'))
