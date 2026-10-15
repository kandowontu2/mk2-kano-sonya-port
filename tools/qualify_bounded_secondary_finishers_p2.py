"""Same secondary earned mechanics/fault gate in actual P2 execution."""
from pathlib import Path
parent=Path(__file__).with_name('qualify_bounded_secondary_finishers_p1.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=namespace['context']['prior']))"
assert wrapper.count(marker)==1
context=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),context)
source=context['source']
for before,after in [
 ('audit_bounded_secondary_finishers_p1_checked','audit_bounded_secondary_finishers_p2_checked'),
 ('audit_bounded_secondary_finisher_{fighter}_p1_runtime','audit_bounded_secondary_finisher_{fighter}_p2_runtime'),
 (' victim=kitana side=2 killer=',' victim=kitana side=1 killer='),
 ('Two P1 owned secondary finishers','Two P2 owned secondary finishers')]:
    assert before in source
    source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=context['namespace']['context']['prior']))
