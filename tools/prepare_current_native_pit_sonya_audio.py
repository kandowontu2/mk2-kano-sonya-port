"""Reciprocal actual Pit sound observer, no changed game or media."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_audio_preparation'
out=sync.ROOT/'audit_current_native_pit_sonya_audio_preparation';assert not out.exists()
runner=(base/'run.ps1').read_text().replace("MK2KS_STAGE_WINNER='kano'","MK2KS_STAGE_WINNER='sonya'").replace("MK2KS_STAGE_SIDE='1'","MK2KS_STAGE_SIDE='2'")
runner=runner.replace('audit_current_native_pit_audio_kano_p1_runtime','audit_current_native_pit_audio_sonya_p2_runtime')
out.mkdir();(out/'run.ps1').write_text(runner)
print('Prepared SonyaP2 actual native Pit sound/channel trace; same pinned Lua/no media/caps')
