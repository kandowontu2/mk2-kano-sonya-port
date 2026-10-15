"""Retain complete scalar rejoin gates for the opposite physical slot."""
from pathlib import Path
parent=Path(__file__).with_name('qualify_bounded_secondary_rejoin_roster_ready.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))"
assert wrapper.count(marker)==1
namespace=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),namespace)
source=namespace['source']
for before,after in [
 ('audit_bounded_secondary_rejoin_roster_ready_checked','audit_bounded_secondary_rejoin_p2_checked'),
 ('_p1_runtime','_p2_runtime'),
 ("r['slot']=='2'","r['slot']=='1'"),
 ('Two P1 secondary finishers','Two P2 secondary finishers')]:
    assert before in source
    source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=namespace['prior']))
