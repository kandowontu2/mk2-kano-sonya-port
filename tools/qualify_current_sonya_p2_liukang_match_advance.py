"""Strict successful LiuKang paid attempt into native Reptile9 fight."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_match_advance.py').read_text()
changes=[('audit_current_sonya_p2_kunglao_leg_spacing','audit_current_sonya_p2_liukang_leg_spacing'),('audit_current_sonya_p2_kunglao_match_advance','audit_current_sonya_p2_liukang_match_advance'),('23056','39375'),('26394','44489'),('24150','40751'),('25870','43978'),("start['stage']=='3'","start['stage']=='4'"),("start['cpu']=='0:0'","start['cpu']=='1:1'"),("advance['stage']=='4'","advance['stage']=='5'"),("advance['cpu']=='1:1'","advance['cpu']=='9:9'"),("r['stage']=='3' and r['id']","r['stage']=='4' and r['id']"),("frame='25000'","frame='42000'"),('sameAttemptKungLaoCleared','sameAttemptLiuKangCleared'),('nextNativeLiuKangFight','nextNativeReptileFight')]
for old,new in changes:
    assert old in source,old
    source=source.replace(old,new)
exec(compile(source,__file__+'::strict_native_match','exec'))
