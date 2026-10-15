"""Same failed controller, exact paired native action timeline."""
import json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load

def main():
    sync.verify();folder=sync.ROOT/'audit_current_native_deadpool_actions_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_deadpool_actions_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_deadpool_actions_preparation/stage.lua')
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    rows=load(folder/'run.log');fields=rows['ACID_ACTION_FIELD']
    assert len(fields)==402 and {(int(r['age']),int(r['slot'])) for r in fields}=={(a,s) for a in range(201) for s in (1,2)}
    assert all(r['id']==('17' if r['slot']=='1' else '18') and r['owner']==r['actor'] for r in fields)
    own={int(r['age']):r for r in fields if r['slot']=='1'}
    assert all(own[a]['native_action']=='1287' for a in range(7,62))
    assert all(own[a]['native_action']=='771' for a in range(62,201))
    prefix='MK2_STAGE_'
    actual=[l for l in (folder/'run.log').read_text().splitlines() if l.startswith(prefix) and not l.startswith(prefix+'ACID_ACTION_FIELD ')]
    old=[l for l in (sync.ROOT/'audit_current_native_deadpool_probe_kano_p1_runtime/run.log').read_text().splitlines() if l.startswith(prefix)]
    assert actual==old
    report=dict(passedObservationChecks=True,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),unchangedFailedController=True,
        pairedActionFields=402,normalThrowAges=[7,61],uppercutInputAges=[32,35],actualUppercutObserved=False,
        acidFinisherAccepted=False,fullPortAcceptance=False,scope='Exact failed probe plus201 paired native action fields; HP input overlaps actual native throw1287. No port-defect or acid-success claim.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passedObservationChecks=True,nativeThrowOverlapsHP=True,acidFinisherAccepted=False)))

if __name__=='__main__':main()
