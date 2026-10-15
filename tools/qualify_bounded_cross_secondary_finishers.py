"""Secondary counterpart retaining all primary earned/wrap/cache gates."""
from pathlib import Path
original=Path(__file__).with_name('qualify_bounded_cross_primary_finishers.py')
source=original.read_text()
changes={
    "'audit_bounded_cross_primary_finishers_checked'":"'audit_bounded_cross_secondary_finishers_checked'",
    "'FFFAAE00'":"'FFD86600'",
    "'FFFAB200'":"'FFD7B000'",
    'audit_bounded_cross_primary_finisher_{fighter}':'audit_bounded_cross_secondary_finisher_{fighter}',
    "'finiteCrossPrimaryMechanicsPassed'":"'finiteCrossSecondaryMechanicsPassed'",
    'four earned reciprocal added-victim primary fatalities':'four earned reciprocal added-victim secondary fatalities',
}
for before,after in changes.items():
    assert before in source,before
    source=source.replace(before,after)
marker='reports=[]'
assert source.count(marker)==1
source=source.replace(marker,"gate_source=gate_source.replace(\"a['variant']=='1'\",\"a['variant']=='2'\")\n"+marker)
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
