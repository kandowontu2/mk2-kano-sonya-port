"""Remaining physical acid role cases; same observer/controller, no media."""
import verify_native_source_sync as sync

sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_gate_hold_preparation'
out=sync.ROOT/'audit_current_native_deadpool_roles_preparation'
assert not out.exists()
out.mkdir()
runner=(base/'run.ps1').read_text()
for fighter,side in [('sonya',1),('kano',2),('sonya',2)]:
    text=runner.replace('audit_current_native_deadpool_gate_hold_kano_p1_runtime',
                        f'audit_current_native_deadpool_gate_hold_{fighter}_p{side}_runtime')
    text=text.replace("$env:MK2KS_STAGE_WINNER='kano'",f"$env:MK2KS_STAGE_WINNER='{fighter}'")
    text=text.replace("$env:MK2KS_STAGE_SIDE='1'",f"$env:MK2KS_STAGE_SIDE='{side}'")
    (out/f'run_{fighter}_p{side}.ps1').write_text(text)
print('Prepared remaining three roles; same pinned Lua, physical selection only')
