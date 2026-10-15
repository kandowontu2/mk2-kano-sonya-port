"""Strict same-attempt Cage clear and real native Kung Lao next-fight gate."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_match_advance.py').read_text()
changes=[
 ('audit_current_sonya_p2_subzero_close_retreat','audit_current_sonya_p2_cage_early_retreat'),
 ('audit_current_sonya_p2_subzero_match_advance','audit_current_sonya_p2_cage_match_advance'),
 ('14594','20233'),('17315','23056'),('15397','21108'),('16802','22543'),
 ("start['stage']=='1'","start['stage']=='2'"),
 ("start['cpu']=='8:8'","start['cpu']=='2:2'"),
 ("r['stage']=='1' and r['slot']=='2'","r['stage']=='2' and r['slot']=='2'"),
 ("fight['stage']=='2'","fight['stage']=='3'"),
 ("fight['cpu']=='2:2'","fight['cpu']=='0:0'"),
 ("if r['stage']=='2'];assert fields","if r['stage']=='3'];assert fields"),
 ("r['cpu']=='2:2' and r['human_actor']","r['cpu']=='0:0' and r['human_actor']"),
 ('sameAttemptSubzeroCleared','sameAttemptCageCleared'),
 ('nextNativeCageFight','nextNativeKungLaoFight'),
 ("frame='16000',stage='1'","frame='22000',stage='2'")]
for before,after in changes:
    assert before in source,before
    source=source.replace(before,after)
exec(compile(source,__file__+'::same_attempt_gate','exec'))
