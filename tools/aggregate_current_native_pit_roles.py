"""Recheck four earned current Pit roles; retain explicit coverage limits."""
import inspect,json
import verify_native_source_sync as sync
import qualify_current_native_pit_case as base

def main():
    source=sync.verify();out=sync.ROOT/'audit_current_native_pit_roles_checked';assert not out.exists()
    results={};original=inspect.getsource(base.gate)
    for fighter in ('kano','sonya'):
        for side in (1,2):
            label=f'{fighter}_p{side}';folder=sync.ROOT/f'audit_current_native_pit_longkick_{label}_runtime'
            path=sync.ROOT/f'audit_current_native_pit_longkick_{label}_checked/report.json'
            report=json.loads(path.read_text());terminal=json.loads((folder/'terminal.json').read_text())
            assert report['completedRunAccepted'] and report['currentPitSceneAccepted'] and report['terminal']==terminal
            assert sync.sha(folder/'run.log')==report['logSHA256']
            code=original.replace("r['side']=='1'",f"r['side']=='{side}'")
            if fighter=='sonya':
                code=code.replace("r['winner']=='kano'","r['winner']=='sonya'").replace("'17,18'","'18,17'")
                code=code.replace("=='17'","=='TEMP'").replace("=='18'","=='17'").replace("=='TEMP'","=='18'")
            context=dict(vars(base));exec(compile(code,__file__+'::'+label,'exec'),context)
            proof=context['gate'](base.load(folder/'run.log'));assert proof==report['scene']
            assert proof['nativePitActivated'] and proof['completeSceneFollowthrough']
            results[label]=dict(scene=proof,terminal=terminal,reportSHA256=sync.sha(path),logSHA256=report['logSHA256'])
    report=dict(passed=True,sourceSync=source,cases=results,bothAddedPerformersBothSlots=True,
                fullStageFinisherAcceptance=False,fullPortAcceptance=False,
                scope='Four real cross-added-character Pit performer/slot roles, seven earned full-health two-KO matches, native arena progression and commands,801 consecutive scene fields plus1100 followthrough. No complete raster/audio, stock/mirror victim matrix, all stages, campaign or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,currentPitRoleCases=4,fullPortAcceptance=False)))

if __name__=='__main__':main()
