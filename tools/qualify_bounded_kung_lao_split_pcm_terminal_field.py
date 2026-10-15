"""Actual sample-channel observer includes terminal field299, not just298."""
import inspect
import qualify_bounded_kung_lao_split_pcm_digest as previous

def main():
    source=inspect.getsource(previous.gate)
    for before,after in [('set(range(1,299)) and len(rows)==298','set(range(1,300)) and len(rows)==299'),
        ('importedChannelsIdleFields=298','importedChannelsIdleFields=299')]:
        assert source.count(before)==1;source=source.replace(before,after)
    main_source=inspect.getsource(previous.main).replace('audit_bounded_kung_lao_split_pcm_digest_checked','audit_bounded_kung_lao_split_pcm_terminal_field_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::full_channel_terminal_field','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
