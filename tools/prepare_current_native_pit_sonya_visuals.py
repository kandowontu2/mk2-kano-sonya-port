"""Reciprocal bounded Pit visuals, reuse pinned actual controller/observer."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_visual_preparation'
out=sync.ROOT/'audit_current_native_pit_sonya_visual_preparation';assert not out.exists()
runner=(base/'run.ps1').read_text()
runner=runner.replace("MK2KS_STAGE_WINNER='kano'","MK2KS_STAGE_WINNER='sonya'").replace("MK2KS_STAGE_SIDE='1'","MK2KS_STAGE_SIDE='2'")
runner=runner.replace('audit_current_native_pit_visual_kano_p1_runtime','audit_current_native_pit_visual_sonya_p2_runtime')
out.mkdir();(out/'run.ps1').write_text(runner)
print('Prepared reciprocal SonyaP2/KanoP1 three Pit PNGs; same pinned Lua,512KiB cap')
