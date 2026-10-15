"""Normal-input wrong history/far/ineligible arena fixtures, no forcing."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_stage_rejections_preparation';assert not out.exists()
out.mkdir()
for fighter in ('kano','sonya'):
 for side in (1,2):
  for label,arena,case in [('wrong',1,'wrong_command'),('far',1,'far'),('arena0',0,'positive')]:
   runner=(base/'run_kano_p1.ps1').read_text()
   runner=runner.replace("MK2KS_STAGE_WINNER='kano'",f"MK2KS_STAGE_WINNER='{fighter}'").replace("MK2KS_STAGE_SIDE='1'",f"MK2KS_STAGE_SIDE='{side}'")
   runner=runner.replace("MK2KS_STAGE_ARENA='1'",f"MK2KS_STAGE_ARENA='{arena}'").replace("MK2KS_STAGE_CASE='positive'",f"MK2KS_STAGE_CASE='{case}'")
   runner=runner.replace('audit_current_native_tomb_kano_p1_runtime',f'audit_current_native_stage_reject_{fighter}_p{side}_{label}_runtime')
   (out/f'run_{fighter}_p{side}_{label}.ps1').write_text(runner)
print('Prepared12physical rejection fixtures, shared existing Lua/no media/build copies')
