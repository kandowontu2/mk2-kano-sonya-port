"""Preserve earned stage/identity/input chronology; do not imply a campaign clear."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_ring_spacing.py').read_text()
for old,new in (
 ('mirror_ring_spacing','mirror_jumpkick'),("'24000'","'21000'"),
 ('MIRROR_RING_SPACING_ATTEMPT','MIRROR_JUMPKICK_ATTEMPT'),
 ("specials=[r for r in rows.get('SPECIAL',[]) if r['stage']=='5' and r['move']=='ring']","specials=[r for r in rows.get('STATE',[]) if r.get('stage')=='5' and r.get('action')=='1025']"),
 ('ringSpacingRequests','jumpKickRequests'),('nativeRingEntries','sampledAirKickStates')):
    assert old in code;code=code.replace(old,new)
exec(compile(code,__file__,'exec'),{'__file__':__file__})
