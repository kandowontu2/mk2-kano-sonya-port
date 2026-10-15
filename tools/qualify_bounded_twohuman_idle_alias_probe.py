"""Stock stance also shares native animation62; require actual stance0 ref."""
import qualify_bounded_twohuman_idle_masked_probe as prior
scope=dict(prior.scope)
source=prior.source
old='assert refs and set(refs).issubset({0,64})'
assert source.count(old)==1
source=source.replace(old,'assert 0 in refs and set(refs).issubset({0,62,64})')
scope['__file__']=__file__
scope['__name__']='qualified_alias_successor'
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
