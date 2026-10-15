"""Original split victim gender/packed cue/priority and every observed port pair."""
import inspect
import qualify_bounded_kitana_kiss_voice_packets as previous

def main():
    source=inspect.getsource(previous.voice_gate)
    changes={'age=180 if side==1 else 181':'age=76 if side==1 else 77',
        "steps[0]['a0']=='00000002' and steps[0]['a1']=='32343638'":"steps[0]['a0']=='00000001' and steps[0]['a1']=='8585B8B7'",
        'base=0x38 if ident==18 else (0x32 if side==1 else 0x34)':'base=0xb7 if ident==18 else 0x85',
        "steps[1]['a0']==steps[2]['a0']=='00000002'":"steps[1]['a0']==steps[2]['a0']=='00000001'",
        'assert cue in (base,base+1)':'assert cue==base',
        'nativeVariantCount=2':'nativeVariantCount=1'}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    main_source=inspect.getsource(previous.main)
    changes={'audit_bounded_kitana_kiss_voice_packets_checked':'audit_bounded_kung_lao_split_voice_packets_checked',
        'kitana_kiss_voice_priority_runtime':'kung_lao_split_voice_runtime',
        "sync.ROOT/(f'audit_bounded_{fighter}_kitana_kiss_finisher_runtime' if side==1 else f'audit_bounded_p2_{fighter}_kitana_kiss_finisher_runtime')":"sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_finisher_runtime'",
        "int(end['frame'])-ready==396":"int(end['frame'])-ready==299"}
    for before,after in changes.items():assert main_source.count(before)==1;main_source=main_source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::native_split_voice_packets','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
