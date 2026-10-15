"""Scalar target census; positive overlap is not waveform qualification."""
import json
from pathlib import Path
import check_bounded_native_retained_tap as prior
BASE=prior.ROOT/'audit_bounded_native_lowkick24_runtime'
def main():
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    data=prior.scan(BASE)
    assert data['retained']==1 and data['fields']<=1800
    overlaps=[f for f in data['hits'] if f in data['active'] or f-1 in data['active']]
    report=dict(nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        scalarFields=data['fields'],actualPrivateCommands=data['cues'],
        activeOwnerFrames=len(data['active']),incomingSonyaDamageFrames=data['hits'],
        potentialDamageDuringVoiceFrames=overlaps,privateInterruptionAccepted=False,
        fullGoalComplete=False,sourceSync=prior.sync.verify(),
        limitation='Scalar target census only; no direct health-write instruction or audible output acceptance',
        hashes={str(p):prior.sync.sha(p) for p in (BASE/'run.log',Path(__file__))})
    out=BASE/'scalar_target_check.json';assert not out.exists()
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sourceSync','hashes')}))
if __name__=='__main__':main()
