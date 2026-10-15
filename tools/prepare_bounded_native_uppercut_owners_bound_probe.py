"""Allow the explicit passive tap; preserve rejected first preparation."""
import inspect
import prepare_bounded_native_uppercut_owners_probe as owners
prior=owners.prior
prior.OUT=prior.ROOT/'audit_bounded_native_uppercut_owners_bound_preparation'
source=inspect.getsource(prior.main)
assert source.count("'install_write_tap',")==1
source=source.replace("'install_write_tap',",'',1)
assert prior.TAIL.count('install_write_tap(')==1
assert 'return data' not in prior.TAIL
scope=dict(vars(prior))
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':
    scope['main']()
