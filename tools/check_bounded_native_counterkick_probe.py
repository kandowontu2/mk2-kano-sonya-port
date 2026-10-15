"""Exact native health writes compared with preceding real owner snapshots."""
import json,re
from pathlib import Path
import check_bounded_native_retained_tap as prior
BASE=prior.ROOT/'audit_bounded_native_counterkick_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def main():
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    data=prior.scan(BASE);owners={};damage=[];health_count=0;retained=False
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(RX.findall(line))
            if tag=='MK2_VOICE_OWNER':owners[int(r['slot'])]=r
            elif tag=='MK2_BOUNDED_HEALTH_TAPS_TERMINAL':retained=r['retained']=='2'
            elif tag=='MK2_BOUNDED_HEALTH_WRITE':
                health_count+=1;before=int(r['before']);value=int(r['data'],16);mask=int(r['mask'],16)
                after=(before&(~mask&0xffff))|(value&mask)
                if 0<before<=166 and after<before:
                    slot=int(r['slot']);owner=owners.get(slot)
                    gap=float(r['seconds'])-float(owner['seconds']) if owner else None
                    damage.append(dict(frame=int(r['frame']),seconds=r['seconds'],slot=slot,
                        before=before,after=after,pc=r['pc'],
                        precedingOwner=owner,observationGapSeconds=gap,
                        precedingOwnerActive=bool(owner and owner['actor']!='00000000')))
    assert retained and health_count>0 and data['retained']==1
    overlap=[r for r in damage if r['precedingOwnerActive']]
    result=dict(nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        actualPrivateCommands=data['cues'],healthWriteEvents=health_count,
        actualNativeDamage=damage,potentialVoiceInterruptionWrites=overlap,
        privateInterruptionAccepted=False,fullGoalComplete=False,
        limitation='Preceding owner observation is not event-time owner/output qualification',
        sourceSync=prior.sync.verify(),logSha256=prior.sync.sha(BASE/'run.log'))
    out=BASE/'health_write_check.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(nativeExit=0,healthWriteEvents=health_count,damageWrites=len(damage),
        potentialVoiceInterruptionWrites=len(overlap),actualPrivateCommands=data['cues'],
        potentialFrames=[r['frame'] for r in overlap])))
if __name__=='__main__':main()
