"""Original earned-win/damage/wrap fault gates, actual secondary native entries."""
from pathlib import Path
parent=Path(__file__).with_name('qualify_bounded_own_finishers_header_binding.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=context['prior']))"
assert wrapper.count(marker)==1
namespace=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),namespace)
source=namespace['source']
for before,after in [
 ('audit_bounded_own_finishers_p1_checked','audit_bounded_secondary_finishers_p1_checked'),
 ('audit_bounded_own_finisher_dispatch_{fighter}_p1_runtime','audit_bounded_secondary_finisher_{fighter}_p1_runtime'),
 ("a['variant']=='1'","a['variant']=='2'"),
 ("{'kano':'FFFAAE00','sonya':'FFFAB200'}","{'kano':'FFD86600','sonya':'FFD7B000'}"),
 ('Two P1 owned primary finishers','Two P1 owned secondary finishers')]:
    assert before in source
    source=source.replace(before,after)
exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=namespace['context']['prior']))
