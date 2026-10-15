"""Four genuine added-character Tomb role cases, not every stage branch."""
import inspect,json
import verify_native_source_sync as sync
import qualify_current_native_tomb_case as base

def main():
    source=sync.verify()
    out=sync.ROOT/'audit_current_native_tomb_roles_checked';assert not out.exists()
    results={}
    original=inspect.getsource(base.gate)
    for fighter in ('kano','sonya'):
        for side in (1,2):
            label=f'{fighter}_p{side}'
            folder=sync.ROOT/f'audit_current_native_tomb_{label}_runtime'
            reportpath=sync.ROOT/f'audit_current_native_tomb_{label}_checked/report.json'
            report=json.loads(reportpath.read_text());assert report['passed'] and not report['fullPortAcceptance']
            terminal=json.loads((folder/'terminal.json').read_text());assert terminal==report['terminal']
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert sync.sha(folder/'run.log')==report['logSHA256']
            code=original.replace("r['side']=='1'",f"r['side']=='{side}'")
            if fighter=='sonya':
                code=code.replace("r['winner']=='kano'","r['winner']=='sonya'").replace("'17,18'","'18,17'")
                code=code.replace("=='17'","=='TEMP'").replace("=='18'","=='17'").replace("=='TEMP'","=='18'")
            context=dict(vars(base));exec(compile(code,__file__+'::'+label,'exec'),context)
            proof=context['gate'](base.load(folder/'run.log'))
            assert proof==report['scene']
            results[label]=dict(scene=proof,terminal=terminal,reportSHA256=sync.sha(reportpath),logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,sourceSync=source,cases=results,bothAddedPerformersBothSlots=True,
                allTombBranchesAccepted=False,fullStageFinisherAcceptance=False,fullPortAcceptance=False,
                scope='Four fresh current native Tomb role cases: Kano/Sonya performers in both physical slots against the other true added actor, earned322damage/twoKO matches, native paid rematch/command/action,801continuous scene fields and1100followthrough. Not complete random/held/pressed/mirror/stock victim branches, rendered/audio/Pit/campaign/release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,currentTombRoleCases=4,fullPortAcceptance=False)))

if __name__=='__main__':main()
