"""Physical guard release and settled Down chord; no native state edits."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_settled_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p1_subzero_guard_release_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="local ready=grounded and human.flags&0x1c==0 and human.body&0x0c==0 and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)"
new="local ready=grounded and (human.flags&0x1c==0 or ((human.action==1792 or human.action==1793) and human.flags&0x18==0)) and human.body&0x0c==0 and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)"
assert source.count(old)==1
source=source.replace(old,new)
old="human.action==770 and sl_loop and sl_main==human.main and sl_loop>=sl_down and frame-sl_loop<=2 and(not sl_pulse or frame-sl_pulse>=64)"
new="human.action==770 and frame-sl_down>=33 and(not sl_pulse or frame-sl_pulse>=64)"
assert source.count(old)==1
source=source.replace(old,new).replace('gap,sl_loop,human.hp','gap,sl_loop or -1,human.hp')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_subzero_settled_leg_runtime','audit_current_sonya_p1_subzero_guard_release_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Physical guard release / Down33 LP+Block; 180sec/320MiB/10MiB; no media')
