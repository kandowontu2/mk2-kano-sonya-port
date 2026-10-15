"""Correct preflight duration to the stricter actual 120-field limit."""
import prepare_bounded_native_stance_bounds_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.prior.ROOT/'audit_bounded_native_stance_bounds_short_preparation'
source=old.old.previous.source
assert source.count("assert '1800' in TAIL and '2400' in TAIL")==1
source=source.replace("assert '1800' in TAIL and '2400' in TAIL","assert 'if age>=120 then' in TAIL and '2400' in TAIL",1)
assert source.count('maximumLiveFields=1800')==1
source=source.replace('maximumLiveFields=1800','maximumLiveFields=120',1)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
