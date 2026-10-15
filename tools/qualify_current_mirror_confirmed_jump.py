"""Whole original earned chronology plus actual jump request/acceptance ledger."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_ring_spacing.py').read_text()
for old,new in (
 ('audit_current_sonya_mirror_ring_spacing','audit_current_mirror_confirmed_jump'),
 ("'24000'","'21000'"),('MIRROR_RING_SPACING_ATTEMPT','MIRROR_CONFIRMED_JUMP_ATTEMPT'),
 ("if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):","if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL','MIRROR_ACTION_CHANGE'):") ,
 ("specials=[r for r in rows.get('SPECIAL',[]) if r['stage']=='5' and r['move']=='ring']","specials=rows.get('MIRROR_JUMP_ACCEPTED',[])\nassert all(r['action'] in ('512','779','776') for r in specials)\nassert all(r['human_action'] in ('0','771','772') for r in attempts)"),
 ('ringSpacingRequests','neutralJumpRequests'),('nativeRingEntries','nativeJumpAcceptances')):
    assert old in code;code=code.replace(old,new)
exec(compile(code,__file__,'exec'),{'__file__':__file__})
