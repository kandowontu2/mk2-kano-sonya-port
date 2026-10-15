"""Keep state composite victim field separate from victim-name log header."""
from pathlib import Path
parent=Path(__file__).with_name('qualify_bounded_own_finishers_p1.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=prior))"
assert wrapper.count(marker)==1
context=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),context)
source=context['source']
before="assert r['victim']=='kitana' and r['side']=='2' and r['killer']==fighter"
assert source.count(before)==1
source=source.replace(before,"assert re.search(r' victim=kitana side=2 killer='+fighter+r' ',line)")
exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=context['prior']))
