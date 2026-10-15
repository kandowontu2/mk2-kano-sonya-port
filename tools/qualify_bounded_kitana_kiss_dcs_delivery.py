"""Same strict native delivery gate, for the kiss's twenty observed bytes."""
import inspect
import qualify_bounded_kung_lao_split_dcs_delivery as previous

def main():
    gate=inspect.getsource(previous.gate)
    assert gate.count('==102')==1
    gate=gate.replace('==102','==20')
    source=inspect.getsource(previous.main)
    substitutions={
        'audit_bounded_kung_lao_split_dcs_delivery_checked':'audit_bounded_kitana_kiss_dcs_delivery_checked',
        'audit_bounded_kung_lao_split_voice_packets_checked':'audit_bounded_kitana_kiss_voice_choice_checked',
        'kung_lao_split_dcs_delivery_runtime':'kitana_kiss_dcs_delivery_runtime',
        'kung_lao_split_voice_runtime':'kitana_kiss_voice_priority_runtime',
        'nativeBytesConsumed=102,nativeCommandPairs=51':'nativeBytesConsumed=20,nativeCommandPairs=10',
    }
    for old,new in substitutions.items():
        assert old in source; source=source.replace(old,new)
    namespace=dict(previous.__dict__); namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::kiss_delivery','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
