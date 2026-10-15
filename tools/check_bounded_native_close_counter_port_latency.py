"""Physical port reads precede this callback's overrides by one frame."""
import json
import check_bounded_native_close_counter_probe as prior
def main():
    previous=None;counts={'highkick':0,'lowkick':0,'released':0};checked=0
    with (prior.BASE/'run.log').open() as stream:
        for line in stream:
            if not line.startswith('MK2_BOUNDED_PHYSICAL '):continue
            r=dict(prior.prior.RX.findall(line))
            if previous and int(r['frame'])==int(previous['frame'])+1:
                press=previous['press'];a=int(r['in0'],16);b=int(r['in2'],16)
                assert (a&0x40==0)==(press=='highkick')
                assert (b&2==0)==(press=='lowkick')
                counts[press if press in ('highkick','lowkick') else 'released']+=1;checked+=1
            previous=r
    assert checked>1700 and counts['lowkick']>0 and counts['released']>0
    report=dict(passed=True,adjacentPhysicalFieldsChecked=checked,counts=counts,
        inputLatencyFields=1,highKickBranchExercised=counts['highkick']>0,
        previousZeroLatencyAssertionRejected=True,privateInterruptionAccepted=False,
        fullGoalComplete=False)
    out=prior.BASE/'physical_port_latency_check.json';assert not out.exists()
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
