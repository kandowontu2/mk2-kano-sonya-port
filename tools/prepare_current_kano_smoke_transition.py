"""Same physical native secret/return driver, select actual Kano17 instead."""
import json
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_smoke_transition_batched_preparation'
out=sync.ROOT/'audit_current_kano_smoke_transition_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
assert sync.sha(lua)==sync.sha(base/'stage.lua')
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(
    'audit_current_sonya_smoke_transition_batched_runtime','audit_current_kano_smoke_transition_runtime')
old="$env:MK2KS_STAGE_WINNER='sonya'"
assert runner.count(old)==1
runner=runner.replace(old,"$env:MK2KS_STAGE_WINNER='kano'")
(out/'run.ps1').write_text(runner)
(out/'provenance.json').write_text(json.dumps(dict(sameDriverSHA256=sync.sha(lua),
    reference=base.name,onlyControlChoiceChanged='Select Kano17 rather than Sonya18',
    gameStateWrites=0,forcedRNG=False),indent=2))
print('Prepared actualKano17P1/Kitana4 route; same72-field physical cadence/return driver;28000fields/90sec/no media')
