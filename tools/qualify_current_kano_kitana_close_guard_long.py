"""Full earned current campaign gate and exact prior productive prefix."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
rows=chronology.load(sync.ROOT/'audit_current_kano_kitana_close_guard_long_runtime/run.log')
old=chronology.load(sync.ROOT/'audit_current_kano_kitana_close_guard_runtime/run.log')
for tag in set(rows)|set(old):
    if tag in ('HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<18000]==[r for r in old.get(tag,[]) if int(r['frame'])<18000],tag
code=Path(__file__).with_name('qualify_current_kano_kitana_confirmed_jump.py').read_text().replace('kano_kitana_confirmed_jump','kano_kitana_close_guard_long')
code=code.replace("result['frame']=='18000'","result['frame']=='21000'")
code=code.replace("len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[]))","len(rows.get('KANO_CLOSE_NATIVE_UPPER',[]))")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
