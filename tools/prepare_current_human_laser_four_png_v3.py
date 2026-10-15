"""Prepare only: post-flash burst and observe, never route, post-finish CSS."""
import hashlib
import json
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
base=root/'audit_current_human_laser_four_png_v2_preparation'
out=root/'audit_current_human_laser_four_png_v3_preparation'
assert not out.exists()
s=(base/'campaign.lua').read_text()
assert s.count('if mode==4 and frame>700')==1
assert s.count('if css[n]and mode==4 then')==1
assert s.count('pending[frame+4]=label')==1
s=s.replace('if mode==4 and frame>700','if not started and mode==4 and frame>700')
s=s.replace('if css[n]and mode==4 then','if not started and css[n]and mode==4 then')
s=s.replace('pending[frame+4]=label',"pending[frame+(label=='burst'and 12 or 4)]=label")
assert ':pixels(' not in s and ':write_' not in s and s.count('screen:snapshot(')==1
out.mkdir()
lua=out/'campaign.lua';lua.write_text(s)
sha=hashlib.sha256(lua.read_bytes()).hexdigest().upper()
runner=(base/'run.ps1').read_text().replace('audit_current_human_laser_four_png_v2_runtime','audit_current_human_laser_four_png_v3_runtime').replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace('FB1DF9F2635B08AA7EE50B21CEF19DE7C122E969E16258E56047429BFE9643B6',sha)
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sha,
  exactDiff=['Initial physicalCSSrouting and input disabled once actualfinisherENTRY has occurred; post-finishCSS is observe-only.', 'BurstPNG scheduled atactualowned6B43+12fields, not+4, after intentionalsource2delay+6fieldflash. Otherphase/images/inputs/bounds unchanged.'],
  executedV2Retained=True,v2Error='No native selector route during transient paidCSS; do not qualify error-free run or gamebug from this controller error.',
  scope='Four bounded actualPNGs and native ownedscene/nextpaidCSS composition, not allallocationretirement or heardaudio.',
  limits='8000fields180sec320MiB10MiB/4PNG256KiB',fullPortAccepted=False),indent=2))
print(out,sha)
