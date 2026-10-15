"""Exact original control plus one passive host exit callback; full298 pixels."""
import copy,inspect,sys
import qualify_bounded_kung_lao_split_pixels as previous

def control_gate(current,old):
    tags={tag for tag,r in old};filtered=[r for r in current if r[0] in tags]
    expected=copy.deepcopy(old)
    terminals=[r for tag,r in expected if tag=='BOUNDED_TERMINAL'];assert len(terminals)==1
    assert expected[-1][0]=='RESULT'
    final=expected[-1][1];assert final['frame']==terminals[0]['frame']
    extra=copy.deepcopy(terminals[0]);extra['frame']=str(int(extra['frame'])+1)
    final['frame']=str(int(final['frame'])+1)
    expected.insert(len(expected)-1,('BOUNDED_TERMINAL',extra))
    assert filtered==expected

def main(side):
    source=inspect.getsource(previous.main)
    changes={'audit_bounded_kung_lao_split_pixels_p':'audit_bounded_kung_lao_split_pixels_flush_callback_p',
        'audit_bounded_kung_lao_split_descriptors_checked':'audit_bounded_kung_lao_split_all_descriptors_checked',
        'kung_lao_split_pixels_runtime':'kung_lao_split_pixels_final_flush_runtime',
        'assert sum(expected.values())==126':'assert sum(expected.values())==(354 if side==1 else 352)',
        "assert [r for r in states(folder,fighter,side) if r[0] in tags]==old":"control_gate(states(folder,fighter,side),old)",
        'originalControlUnchanged=True':'originalControlThroughNativeTerminalUnchanged=True,passiveHostExitCallbackDelta=1'}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace.update(__file__=__file__,control_gate=control_gate)
    exec(compile(source,__file__+'::exact_passive_flush_callback','exec'),namespace);namespace['main'](side)

if __name__=='__main__':main(int(sys.argv[1]))
