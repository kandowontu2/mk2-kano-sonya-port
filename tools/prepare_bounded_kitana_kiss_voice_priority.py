"""Original earned kiss with scalar native voice/priority/packet observers."""
import inspect
import prepare_bounded_jax_arms_voice_priority as previous

def main():
    source=inspect.getsource(previous.main)
    assert source.count('jax_arms')==4
    source=source.replace('jax_arms','kitana_kiss')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::kiss_observer','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
