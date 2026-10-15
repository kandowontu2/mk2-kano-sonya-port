"""Four observed physical-victim native calls: table/priority/owner/port sequence."""
import inspect
import qualify_bounded_kitana_kiss_effect_dispatch as previous

def main():
    source=inspect.getsource(previous.gate)
    before="if tag=='MK2_VOICE_SELECTOR_CUE' and int(r['cue'],16) in (0xa3,0xa5,0xa4)";assert source.count(before)==1
    source=source.replace(before,"if tag=='MK2_VOICE_SELECTOR_CUE'")
    before="    assert [int(r['cue'],16) for _,r in selected]==[0xa3,0xa5,0xa4]";assert source.count(before)==1
    source=source.replace(before,"    assert len(selected)==4\n    cues=[int(r['cue'],16) for _,r in selected]\n    assert cues[0] in (0xb7,0x85) and cues[1] in (0x20,0x21) and cues[2]==0x96 and cues[3] in (0x1f,0x22)")
    before='zip(selected,(211+side,211+side,351+side))';assert source.count(before)==1
    source=source.replace(before,'zip(selected,(75+side,149+side,165+side,207+side))')
    main_source=inspect.getsource(previous.main)
    changes={'audit_bounded_kitana_kiss_effect_dispatch_checked':'audit_bounded_kung_lao_split_victim_dispatch_checked',
        'audit_bounded_kitana_kiss_voice_choice_checked':'audit_bounded_kung_lao_split_voice_packets_checked',
        'kitana_kiss_voice_priority_runtime':'kung_lao_split_voice_runtime',
        "if tag=='MK2_VOICE_SELECTOR_CUE' and r['cue']=='A3'":"if tag=='MK2_VOICE_SELECTOR_CUE'"}
    for before,after in changes.items():assert main_source.count(before)==1;main_source=main_source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::actual_victim_dispatches','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
