"""Track original CSS actor, not newly constructed battle actors of same ID."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_css_teardown_preparation'
out=sync.ROOT/'audit_bounded_css_teardown_owner_preparation';assert not out.exists();out.mkdir()
source=(old/'teardown.lua').read_text()
source=source.replace('local photo_draws,pose_draws=0,0','local photo_draws,pose_draws,css_pose_actor=0,0,0')
before='and src>=0x10000000 and src<0x11000000 then pose_draws=pose_draws+1 end'
after="""and src>=0x10000000 and src<0x11000000 then
  if not exit_at then css_pose_actor=actor end
  if actor==css_pose_actor then pose_draws=pose_draws+1 end
 end"""
assert source.count(before)==1;source=source.replace(before,after)
source=source.replace("'cssphotos=%d addedposes=%d exitframe=%d',photo_draws,pose_draws,exit_at or -1","'cssphotos=%d addedposes=%d exitframe=%d cssactor=%08X',photo_draws,pose_draws,exit_at or -1,css_pose_actor")
lua=out/'owner.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/teardown.lua',out.name+'/owner.lua').replace(sync.sha(old/'teardown.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_css_teardown_{fighter}_p{side}_runtime',f'audit_bounded_css_teardown_owner_{fighter}_p{side}_runtime')
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,originalSelectionActorOnly=True,rawMedia=False)))
