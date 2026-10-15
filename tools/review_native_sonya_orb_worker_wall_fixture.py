"""Preserve the real P2 wall fixture's expired finish window, not a pass."""
import gzip
import json
from pathlib import Path
import capture_native_sonya_orb_worker_wall as host
import review_native_sonya_orb_palette_runtime as shared

ROOT=host.ROOT
OUT=ROOT/'audit_native_sonya_orb_worker_wall_fixture_review'

def main():
    host.need(not OUT.exists(),'Fresh frozen fixture review')
    folder=ROOT/'audit_native_sonya_orb_worker_wall_p2'
    report=json.loads((folder/'report.json').read_text())
    text=gzip.open(folder/'run.log.gz','rt').read()
    host.need(report['passed'] and report['nativeExit']==0 and report['wholeGuestMatched'] and
              report['nativeRGBFrames']==0 and all(host.sha(p)==h for p,h in report['inputHashes'].items()),
              'Same actual terminal native test and every executed input conserved')
    command=shared.rows(text,'COMMAND_READY');modes=shared.rows(text,'MODE')
    host.need(len(command)==1 and command[0]['frame']=='3052' and command[0]['gap']=='300' and
              not shared.rows(text,'ENTRY') and not shared.rows(text,'HISTORY') and
              any(r['frame']=='3091' and r['mode']=='5' for r in modes),
              'Finish mode expires before the fixture schedules final High Kick at3094')
    paths=[Path(__file__),folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz',
           host.LUA,Path(host.__file__)]
    OUT.mkdir()
    result=dict(passed=True,fixtureFailurePreserved=True,gameplayAccepted=False,fullPortAcceptance=False,
        actualWindowsIdentity=report['actualWindowsIdentity'],physicalGapAtReady=300,
        physicallyObservedGap=304,commandReadyFrame=3052,finishExpiredFrame=3091,
        scheduledFinalHighKickFrame=3094,finalHighKickDelivered=False,actionEntered=False,
        parserRejectionProven=False,nativeExit=0,actualRGBFrames=0,
        nextAction='Successor physical controller begins retreat20fields earlier; do not extend game deadline or alter parser/positions/health.',
        inputHashes={str(p.resolve()):host.sha(p) for p in paths},goalStatus='active',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,fixtureFailure=True,parserRejected=False,deadline=3091,scheduledHK=3094)))

if __name__=='__main__':main()
