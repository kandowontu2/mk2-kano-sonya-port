"""Re-execute exact rejection gates across all12 earned current role cases."""
import json
import verify_native_source_sync as sync
from qualify_current_native_stage_rejection import gate,load

def main():
    source=sync.verify();out=sync.ROOT/'audit_current_native_stage_rejections_checked';assert not out.exists()
    cases={}
    for fighter in ('kano','sonya'):
        for side in (1,2):
            for label in ('wrong','far','arena0'):
                name=f'{fighter}_p{side}_{label}'
                folder=sync.ROOT/f'audit_current_native_stage_reject_{name}_runtime'
                path=sync.ROOT/f'audit_current_native_stage_reject_{name}_checked/report.json'
                report=json.loads(path.read_text());terminal=json.loads((folder/'terminal.json').read_text())
                assert report['passed'] and terminal==report['terminal'] and terminal['exitCode']==0 and terminal['limitReason'] is None
                assert sync.sha(folder/'run.log')==report['logSHA256']
                proof=gate(load(folder/'run.log'),fighter,side,label);assert proof==report['rejection']
                cases[name]=dict(rejection=proof,terminal=terminal,logSHA256=report['logSHA256'],reportSHA256=sync.sha(path))
    report=dict(passed=True,sourceSync=source,cases=cases,bothAddedCharactersBothSlots=True,
                wrongHistoryRangeArenaRejectionsAccepted=True,deadPoolAcidFinisherAccepted=False,
                fullStageFinisherAcceptance=False,fullPortAcceptance=False,
                scope='Twelve current physical controller cases: true added performers/victims, native earned full-health two-KO matches and paid rematches, correct history/range/arena rejection branches, no stage action and clean next-screen return. Not every finish timing or stage/victim/raster/audio/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativeRejectionCases=12,fullPortAcceptance=False)))

if __name__=='__main__':main()
