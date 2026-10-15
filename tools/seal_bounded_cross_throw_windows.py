"""Four bounded windows; no broader choreography or whole-port promotion."""
import json
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_cross_throw_windows_sealed';assert not out.exists()
    cases={};pins={}
    for fighter in ('sonya','kano'):
        reports=[]
        for phase,lo,hi in (('opening',114,144),('landing',145,176)):
            kind='queued' if (fighter,phase)==('sonya','opening') else 'viewport'
            checked=sync.ROOT/f'audit_bounded_{fighter}_{kind}_throw_{phase}_checked/report.json'
            report=json.loads(checked.read_text());assert report['passed']
            assert report['fighter']==fighter and report['phase']==phase
            assert report['firstSourceAge']==lo and report['lastSourceAge']==hi
            assert report['nativeDrawFields']==hi-lo+1 and report['opaquePixels']>100000
            assert report['identicalQualifiedGameplay'] and report['bothVideoBuffersCovered']
            terminal=report['terminal']
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes']<320*1024*1024 and terminal['rawMedia']=='none'
            runtime=sync.ROOT/f'audit_bounded_{fighter}_{kind}_throw_{phase}_runtime'
            assert sync.sha(runtime/'run.log')==report['logSha256']
            assert sync.sha(sync.ROOT/'tools'/('qualify_bounded_'+kind+'_throw_footprints.py'))==report['checkerSha256']
            if kind=='viewport':
                assert report['visibleMismatchRejected'] and report['visiblePixels']+report['opaquePixelsOutsideActualViewport']==report['opaquePixels']
            pins[str(checked)]=sync.sha(checked)
            pins[str(runtime/'run.log')]=report['logSha256']
            reports.append(report)
        assert sum(r['nativeDrawFields'] for r in reports)==63
        cases[fighter]=dict(drawFields=63,sourceAgeRange=[114,176],
            opaqueComponentPixels=sum(r['opaquePixels'] for r in reports),
            visibleComponentPixels=sum(r.get('visiblePixels',r['opaquePixels']) for r in reports),
            offscreenComponentPixels=sum(r.get('opaquePixelsOutsideActualViewport',0) for r in reports),
            peakWorkingSetBytes=max(r['terminal']['peakWorkingSetBytes'] for r in reports))
    report=dict(passed=True,cases=cases,pins=pins,sourceSync=sync.verify(),
        sealSha256=sync.sha(Path(__file__)),scope='Both P1 cross-added throw windows, ages114..176, each native body-component opaque pixel',
        entireThrowAnimationAccepted=False,allSlotsVictimsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases=cases)))

if __name__=='__main__':main()
