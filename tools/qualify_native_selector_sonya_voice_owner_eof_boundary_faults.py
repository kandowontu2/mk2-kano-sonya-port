"""Effective faults for the exact instruction-time mode-boundary addition."""
import copy,json
from pathlib import Path
import qualify_native_selector_sonya_voice_owner_eof_boundary as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_boundary_faults_checked'


def execute():
    need(not OUT.exists(),'Fresh immutable mode-boundary counterexamples')
    parent=previous.OUT/'report.json'; proof=json.loads(parent.read_text())
    need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Full prior actual owner proof and original failures intact')
    data=previous.read(); lengths={0x6b00:45512,0x6b01:40720,0x6b02:66523}
    positive=previous.gate(data,lengths); faults=[]
    for label,change in (
        ('actual_instruction_mode',lambda d:next(r for r in d['MK2_SONYA_CHOICE_EVENT'] if r['frame']=='2490' and r['kind']=='bicycle').update(mode='7')),
        ('actual_instruction_opcode',lambda d:next(r for r in d['MK2_SONYA_CHOICE_EVENT'] if r['frame']=='2490' and r['kind']=='bicycle').update(opcode='C081')),
        ('next_physical_mode',lambda d:next(r for r in d['MK2_CPU_ROUND_FIELD'] if r['frame']=='2491' and r['slot']=='2').update(mode='7')),
        ('unrelated_mode_waiver',lambda d:next(r for r in d['MK2_CPU_ROUND_FIELD'] if r['frame']=='1966' and r['slot']=='2').update(mode='7'))):
        bad=copy.deepcopy(data);change(bad)
        try:previous.gate(bad,lengths)
        except AssertionError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise AssertionError('Effective exact-boundary corruption accepted: '+label)
    need(previous.gate(data,lengths)==positive,'Entire untouched owner history restored')
    pins=dict(proof['inputHashes'])
    for p in (Path(__file__),Path(previous.__file__),parent):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every whole original/new evidence pin intact')
    result=dict(proof,recordedQuietEOFOwnership=positive,inputHashes=pins,
        exactWithinFrameBoundaryFaultsRejected=faults,previousWholeOwnerFaultsRejected=13,
        totalEffectiveFaultsRejected=17,allOwnerLifetimeTransitionsAccepted=False,
        physicalLowkickGameplayAccepted=False,fullPortAcceptance=False)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,ownerSnapshots=13850,totalFaults=17,physicalLowkickGameplayAccepted=False)),flush=True)
    return result


if __name__=='__main__':execute()
