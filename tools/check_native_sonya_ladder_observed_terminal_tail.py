"""Distinguish observed last refill field from its unobserved planned end."""
import copy
import gzip
import hashlib
import json
import re
from pathlib import Path
import qualify_native_sonya_first_four_ladder_windows_paths as finite

ROOT, need, sha = finite.ROOT, finite.need, finite.sha
OUT=ROOT/'audit_native_sonya_first_four_ladder_observed_tail_checked'


def tail(rows):
    result=[]
    for slot,pc in (('1','FF9DEF40'),('2','FF9DEF70')):
        values=[q for q in rows if q['slot']==slot]
        need(len(values)==26 and values[0]['frame']=='355163' and values[0]['before']=='161' and
             values[0]['after']=='65535', 'Exact original final sentinel retained')
        for age,q in enumerate(values[1:]):
            need(q['pc']==pc and int(q['frame'])==355163+age and int(q['after'])==4+2*age and
                 int(q['before'])==(65535 if age==0 else 2+2*age), 'Every actually observed final physical-slot fill step')
        result.append(dict(slot=slot,startFrame=355163,observedEndFrame=355187,unobservedExpectedCompletionFrame=355242,
            actualStores=26,lastObservedHealth=52,complete=False))
    need(len(rows)==52,'Whole final two-slot recorded prefix retained')
    return result


def run():
    need(not OUT.exists(),'Fresh precise observed-terminal-tail receipt')
    path=finite.OUT/'report.json'; report=json.loads(path.read_text())
    need(report['passed'] and report['finiteFirstFourLadderProgressionAccepted'] and
         not report['fullTowerAccepted'] and not report['fullPortAcceptance'] and
         all(sha(p)==h for p,h in report['inputHashes'].items()), 'Original finite positive/107-fault proof and failed tower unchanged')
    folder=ROOT/'audit_native_paired_stumble_raiden_guard_ready'
    lines=gzip.open(folder/'run.log.gz','rt',encoding='utf-8').read().splitlines()
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',q)) for q in lines if q.startswith('MK2_NAT_CAMPAIGN_HEALTH ')]
    observed=[q for q in rows if int(q['frame'])>=355163]
    actual=tail(observed); faults=[]
    for field,value in [('frame','355188'),('after','54'),('pc','FF838860'),('slot','2')]:
        bad=copy.deepcopy(observed);bad[-2][field]=value
        try: tail(bad)
        except ValueError as error: faults.append(dict(field=field,rejectedBy=str(error)))
        else: raise ValueError('False observed end accepted')
    try: tail(observed[:-1])
    except ValueError as error: faults.append(dict(field='missing',rejectedBy=str(error)))
    else: raise ValueError('Missing native final store accepted')
    need(int(re.findall(r'frame=(\d+)',lines[-1])[0])==355187, 'Full received chronology ends at actual final observed field')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteFirstFourLadderProgressionAccepted=True,
        originalProgressionReceiptSHA256=sha(path),originalSemanticFaultsRejected=107,
        completeNativeRefillSequences=444,observedIncompleteTerminalRefills=actual,terminalTailFaultsRejected=faults,
        previousPartialEndFrameIsPredictedNotObserved=True,originalReportUnchanged=True,
        inputHashes={str(path):sha(path),str(folder/'run.log.gz'):sha(folder/'run.log.gz'),str(Path(__file__).resolve()):sha(__file__)},
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,original107FaultProofPreserved=True,tailFaultsRejected=len(faults),
        actualObservedFinalFrame=355187,fullPortAcceptance=False)),flush=True)


if __name__=='__main__': run()
