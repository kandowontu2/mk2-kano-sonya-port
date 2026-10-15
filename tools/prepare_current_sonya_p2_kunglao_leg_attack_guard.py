"""Physical leg policy: exclude native CPU attack flag from safe approach."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_verified_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_attack_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='safe=safe and other.flags&0x0c==0'
assert source.count(old)==1
source=source.replace(old,'safe=safe and other.flags&0x1c==0')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir()
lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_verified_leg_runtime','audit_current_sonya_p2_kunglao_leg_attack_guard_runtime')
(out/'run.ps1').write_text(runner)
(out/'policy-change.json').write_text(json.dumps(dict(base=str(base),baseSHA256=sync.sha(base/'campaign.lua'),newSHA256=sync.sha(lua),change='CPU safe mask 0x0c -> 0x1c; exclude active attack bit0x10',gameChanged=False,guestWrites=False,fullPortAccepted=False),indent=2)+'\n')
print('Prepared physical-only CPU attack-flag guard;90sec/320MiB/10MiB/no media')
