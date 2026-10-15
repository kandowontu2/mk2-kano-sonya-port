"""Reuse transient scalar PCM observation for physical Kitana kiss replays."""
import inspect
import prepare_bounded_kung_lao_split_pcm_digest as previous

def main():
    source=inspect.getsource(previous.main)
    for old,new in {
        'kung_lao_split_dcs_delivery_preparation':'kitana_kiss_dcs_delivery_preparation',
        'kung_lao_split_pcm_digest_preparation':'kitana_kiss_pcm_digest_preparation',
        'kung_lao_split_dcs_delivery_runtime':'kitana_kiss_dcs_delivery_runtime',
        'kung_lao_split_pcm_':'kitana_kiss_pcm_',
    }.items():
        assert old in source; source=source.replace(old,new)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::kiss_pcm_preparation','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
