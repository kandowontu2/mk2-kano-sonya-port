"""Whole existing earned progression gate plus true uppercut ownership."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
rows=chronology.load(sync.ROOT/'audit_current_kano_kunglao_crouch_counter_runtime/run.log')
assert all(r['actor']==r['owner'] and r['id']=='17' and r['pc']=='FF870DD0' for r in rows.get('KANO_KUNGLAO_NATIVE_UPPER',[]))
code=Path(__file__).with_name('qualify_current_kano_kunglao_early_counter.py').read_text().replace('kano_kunglao_early_counter','kano_kunglao_crouch_counter')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
