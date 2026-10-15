"""Same full admission/control gate, exact prior Portal prefix and owned uppers."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_natural_smoke.py').read_text()
changes={
    'audit_current_sonya_natural_smoke_runtime':'audit_current_sonya_natural_smoke_close_runtime',
    'audit_current_sonya_natural_smoke_checked':'audit_current_sonya_natural_smoke_close_checked',
    'audit_current_sonya_natural_smoke_preparation':'audit_current_sonya_natural_smoke_close_preparation',
    'audit_current_stock_pit_initialized_selector_sonya_p1_kitana_runtime':'audit_current_sonya_natural_smoke_runtime',
    "int(r['frame'])<17948":"int(r['frame'])<20697",
    'priorPhysicalPrefixUnchangedThrough=17947':'priorPhysicalPrefixUnchangedThrough=20696',
}
for old,new in changes.items():
    assert old in source,old
    source=source.replace(old,new)
old='proof=gate(rows)'
assert source.count(old)==1
source=source.replace(old,'''proof=gate(rows)
uppers=rows.get('PORTAL_UPPERCUT',[])
assert all(r['ids']=='18,4' for r in uppers)
owned=[r for r in uppers if r['a8']==r['own'] and r['a13']==r['main']]
portal_damage=[r for r in rows.get('DAMAGE',[]) if r['match']=='8']
proof.update(nativeOwnedPortalUppercuts=len(owned),
    portalOutgoingDamage=sum(int(r['before'])-int(r['after']) for r in portal_damage))''')
exec(compile(source,__file__+'::unchanged_full_native_admission_and_controls_gate','exec'))
