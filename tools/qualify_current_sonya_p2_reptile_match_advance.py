"""Strict successful Reptile paid attempt into native Baraka3 fight."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_match_advance.py').read_text()
changes=[('audit_current_sonya_p2_kunglao_leg_spacing','audit_current_sonya_p2_reptile_hk_early_retreat'),('audit_current_sonya_p2_kunglao_match_advance','audit_current_sonya_p2_reptile_match_advance'),('23056','47550'),('26394','50238'),('24150','48536'),('25870','49728'),("start['stage']=='3'","start['stage']=='5'"),("start['cpu']=='0:0'","start['cpu']=='9:9'"),("advance['stage']=='4'","advance['stage']=='6'"),("advance['cpu']=='1:1'","advance['cpu']=='3:3'"),("r['stage']=='3' and r['id']","r['stage']=='5' and r['id']"),("frame='25000'","frame='49000'"),('sameAttemptKungLaoCleared','sameAttemptReptileCleared'),('nextNativeLiuKangFight','nextNativeBarakaFight')]
for old,new in changes:
    assert old in source,old
    source=source.replace(old,new)
exec(compile(source,__file__+'::strict_native_match','exec'))
