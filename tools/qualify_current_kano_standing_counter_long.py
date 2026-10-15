"""Exact productive prefix plus original native earned-stage gate."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
new=chronology.load(sync.ROOT/'audit_current_kano_standing_counter_long_runtime/run.log')
old=chronology.load(sync.ROOT/'audit_current_kano_kitana_standing_counter_runtime/run.log')
for tag in set(new)|set(old):
    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in new.get(tag,[]) if int(r['frame'])<18000]==[r for r in old.get(tag,[]) if int(r['frame'])<18000],tag
code=Path(__file__).with_name('qualify_current_kano_kitana_confirmed_jump.py').read_text().replace('kano_kitana_confirmed_jump','kano_standing_counter_long')
code=code.replace("if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):","if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','KANO_STANDING_ACTION'):")
code=code.replace("result['frame']=='18000'","result['frame']=='21000'")
code=code.replace("len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[]))","len([r for r in rows.get('KANO_STANDING_ACTION',[]) if r['action']=='259'])")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
