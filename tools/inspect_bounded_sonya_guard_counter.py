"""Preserve the same natural-selection and target-presence census gate."""
import inspect
import inspect_bounded_sonya_natural_counter as previous

def main():
    source=inspect.getsource(previous.main)
    assert source.count('audit_bounded_sonya_natural_counter_runtime')==1
    source=source.replace('audit_bounded_sonya_natural_counter_runtime','audit_bounded_sonya_guard_counter_runtime')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::initial_guard_probe','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
