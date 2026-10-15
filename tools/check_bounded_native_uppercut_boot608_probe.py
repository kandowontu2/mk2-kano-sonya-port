"""Same bounded stream checks, actual naturally selected Sonya case."""
import inspect
import check_bounded_native_uppercut_probe as prior
source=inspect.getsource(prior.main)
before="Natural opponent was Baraka (3), not Sonya; no private cue launched"
assert source.count(before)==1
source=source.replace(before,'Natural Sonya opponent present, but no private cue launched')
assert source.count("set(cpu_ids)=={'3'}")==1
source=source.replace("set(cpu_ids)=={'3'}","set(cpu_ids)=={'18'}")
scope=dict(vars(prior),BASE=prior.sync.ROOT/'audit_bounded_native_uppercut_boot608_runtime',__file__=__file__)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
