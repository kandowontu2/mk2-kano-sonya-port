"""Finite actual opaque component contact lines; not displayed-scene parity."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
BASE=ROOT/'audit_bounded_native_stance_bounds_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def main():
    terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    groups=collections.defaultdict(list)
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            if line.startswith('MK2_BOUNDED_STANCE_PART '):
                r=dict(RX.findall(line));groups[int(r['frame']),int(r['slot'])].append(r)
    assert len(groups)==8 and {int(r['id']) for rows in groups.values() for r in rows}=={17,18}
    observations=[]
    for (frame,slot),rows in sorted(groups.items()):
        assert [int(r['part']) for r in rows]==list(range(len(rows)))
        assert all(int(r['opaque'])>0 and int(r['bits'])>0 for r in rows)
        # Native cache offsets are subtracted from the physical object origin.
        sole=max(int(r['y'])-int(r['dy'])+int(r['bottom']) for r in rows)
        stage=int(rows[0]['stage_floor'])
        assert sole==stage+4,'Opaque bottom does not match five-pixel inclusive native contact line'
        observations.append(dict(frame=frame,slot=slot,id=int(rows[0]['id']),
            action=rows[0]['action'],opaqueComponentSole=sole,stageBaseline=stage,
            soleBelowStagePixels=sole-stage,components=len(rows)))
    result=dict(passed=True,nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        finiteOpaqueComponentContactLines=observations,
        observedBothTrueIdsMatchConfiguredNativeContactLine=True,
        allSamplesAreReadyStandingPoses=False,
        currentStockControlCompared=False,displayedFramePixelsBound=False,
        graphicalSoleParityAccepted=False,fullGoalComplete=False,
        sourceSync=sync.verify(),logSha256=sync.sha(BASE/'run.log'),checkerSha256=sync.sha(Path(__file__)))
    out=BASE/'opaque_contact_check.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,opaqueSoleRows=sorted({r['opaqueComponentSole'] for r in observations}),
        observations=len(observations),graphicalSoleParityAccepted=False)))
if __name__=='__main__':main()
