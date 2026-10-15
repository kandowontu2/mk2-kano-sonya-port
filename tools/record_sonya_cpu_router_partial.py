"""Retain qualified observed choices without accepting a host-interrupted run."""
import json,copy
from collections import Counter
import verify_native_source_sync as sync
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_cpu_router_probe as prior

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_current_sonya_cpu_router_partial_observations';assert not out.exists()
    folder=sync.ROOT/'audit_current_sonya_cpu_router_probe_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==-1 and terminal['limitReason']=='wall_limit'
    assert 90<=terminal['elapsedSeconds']<91 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_cpu_router_probe_preparation/campaign.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=chronology.load(folder/'run.log');assert not rows.get('RESULT') and not rows.get('HOST_BOUND')
    decisions=prior.choices_gate(rows)
    bad=copy.deepcopy(rows);next(r for r in bad['CPU_MOVE'] if r['move']=='bicycle')['move']='ring'
    try:prior.choices_gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Wrong observed action target accepted')
    report=dict(observedEntryBindingsAccepted=True,completedRunAccepted=False,
        hostLimitStop=True,terminal=terminal,sourceSync=source_sync,
        lastRecordedFrame=max(int(r['frame']) for values in rows.values() for r in values),
        actualDecisions=decisions,actualCpuMoveEntries=dict(Counter(r['move'] for r in rows['CPU_MOVE'])),
        wrongDecisionTargetRejected=True,logSHA256=sync.sha(folder/'run.log'),
        fullCpuChoreographyAccepted=False,fullPortAcceptance=False,
        scope='Partial host-stopped cold natural Sonya18 CPU mirror probe: complete observed decision-to-entry bindings for19choices, including three bicycles; all four own special entries observed. No terminal callback/normal completion/recovery/stability/campaign or full-port acceptance inferred.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(observedBindingsAccepted=True,completedRunAccepted=False,actualDecisions=decisions)))

if __name__=='__main__':main()
