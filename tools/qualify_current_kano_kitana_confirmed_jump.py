"""Keep full earned current campaign gate; exact earlier route unchanged."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kitana_confirmed_jump_runtime'
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_bounded_compact_kano_campaign_p1_runtime/run.log')
cutoff=int(next(r for r in old['FIGHT'] if r['stage']=='3')['frame'])
for tag in set(rows)|set(old):
    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in old.get(tag,[]) if int(r['frame'])<cutoff],tag
code=Path(__file__).with_name('qualify_bounded_campaign_progress.py').read_text()
changes={"'audit_bounded_campaign_progress_checked'":"'audit_current_kano_kitana_confirmed_jump_checked'","for fighter in ('kano','sonya'):":"for fighter in ('kano',):",'for side in (1,2):':'for side in (1,):',"f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'":"'audit_current_kano_kitana_confirmed_jump_runtime'","result['frame']=='12000'":"result['frame']=='18000'",'contexts=4':'contexts=1'}
for before,after in changes.items():
    assert before in code;code=code.replace(before,after)
exec(compile(code,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
print('Exact prior route through',cutoff-1,'accepted jump markers',len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[])))
