"""Same full packet gate with a genuinely changed high-byte counterexample."""
import inspect
import qualify_bounded_jax_arms_all_sound_bytes as previous

def main():
    source=inspect.getsource(previous.main)
    needle="('wrong_high_byte',0,'data','FF00')";assert source.count(needle)==1
    source=source.replace(needle,"('wrong_high_byte',0,'data','FFFF')")
    source=source.replace('audit_bounded_jax_arms_all_sound_bytes_checked','audit_bounded_jax_arms_all_sound_bytes_faultsafe_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::nonvacuous_fault','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
