"""Full native kiss mixed output comparison, including terminal field396."""
import inspect
import qualify_bounded_kung_lao_split_pcm_digest as previous

def main():
    gate=inspect.getsource(previous.gate)
    for old,new in {
        'set(range(1,299)) and len(rows)==298':'set(range(1,397)) and len(rows)==396',
        'importedChannelsIdleFields=298':'importedChannelsIdleFields=396',
    }.items():
        assert gate.count(old)==1;gate=gate.replace(old,new)
    source=inspect.getsource(previous.main)
    for old,new in {
        'kung_lao_split_pcm_digest_checked':'kitana_kiss_pcm_digest_checked',
        'kung_lao_split_dcs_delivery_checked':'kitana_kiss_dcs_delivery_checked',
        'kung_lao_split_dcs_delivery_runtime':'kitana_kiss_dcs_delivery_runtime',
        'kung_lao_split_pcm_':'kitana_kiss_pcm_',
        'end-begin==299':'end-begin==396',
    }.items():
        assert old in source;source=source.replace(old,new)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::kiss_pcm_gate','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
