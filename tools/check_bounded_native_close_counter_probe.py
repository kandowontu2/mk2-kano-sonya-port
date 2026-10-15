"""Exact health census plus physical-port validation for close counter policy."""
from types import FunctionType
import json
import check_bounded_native_counterkick_probe as prior
BASE=prior.prior.ROOT/'audit_bounded_native_close_counter_runtime'
scope=dict(vars(prior),BASE=BASE,__file__=__file__)
main=FunctionType(prior.main.__code__,scope)
def physical():
    counts={'highkick':0,'lowkick':0,'released':0}
    with (BASE/'run.log').open() as stream:
        for line in stream:
            if not line.startswith('MK2_BOUNDED_PHYSICAL '):continue
            r=dict(prior.RX.findall(line));a=int(r['in0'],16);b=int(r['in2'],16)
            if r['press']=='highkick':
                assert a&0x40==0 and b&2!=0;counts['highkick']+=1
            elif r['press']=='lowkick':
                assert b&2==0 and a&0x40!=0;counts['lowkick']+=1
            else:
                assert a&0x40!=0 and b&2!=0;counts['released']+=1
    assert counts['lowkick']>0 and counts['released']>0
    out=BASE/'physical_port_check.json';assert not out.exists()
    out.write_text(json.dumps(dict(physicalPortCommandsAgree=True,counts=counts,
        highKickBranchExercised=counts['highkick']>0,fullGoalComplete=False),indent=2)+'\n')
    print(json.dumps(counts))
if __name__=='__main__':
    main();physical()
