"""Stage7 counterpart of the strict stage6 physical/native chronology gate."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_short_leg.py').read_text()
changes={
    'audit_current_sonya_p2_baraka_short_leg':'audit_current_sonya_p2_kano_short_leg',
    'audit_current_sonya_p2_baraka_ring_finish20_runtime':'audit_current_sonya_p2_baraka_short_leg_runtime',
    '50237':'93226',
    'SONYA_BARAKA_SHORT_LEG_PLAN':'SONYA_KANO_SHORT_LEG_PLAN',
    'SONYA_BARAKA_DAMAGE':'SONYA_KANO_DAMAGE',
    "r['ids']=='3,18'":"r['ids']=='17,18'",
    "r['stage']=='6'":"r['stage']=='7'",
    "r['stage']=='7':":"r['stage']=='8':",
    'ownBarakaRoundWins':'ownKanoRoundWins',
    'paidBarakaAttempts':'paidKanoAttempts',
    'stage7Observed':'stage8Observed',
    'stage7=result':'stage8=result',
    'plannedLegChords':'plannedLegChords',
}
# Stage advancement replacement must precede round-stage replacement.
source=source.replace("elif tag=='STAGE' and r['stage']=='7':", "elif tag=='STAGE' and r['stage']=='8':")
changes.pop("r['stage']=='7':")
for old,new in changes.items():
    assert old in source, old
    source=source.replace(old,new)
old="[(t,r) for t,r in rows if int(r['frame'])<=93226]"
assert source.count(old)==1
source=source.replace(old,"[(t,r) for t,r in rows if int(r['frame'])<=93226 and t!='SONYA_KANO_DAMAGE']")
source=source.replace("prefixExactlyPreservedThrough=93226,", "prefixExactlyPreservedThrough=93226, excludedOnlyNewPassiveDamageTag='SONYA_KANO_DAMAGE',")
exec(compile(source,__file__,'exec'))
