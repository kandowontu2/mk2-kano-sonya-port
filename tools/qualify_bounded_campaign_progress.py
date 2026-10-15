"""Natural victories/losses/paid reselects, never accept bounded stop as clear."""
import json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line and 'hex=' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            groups.setdefault(line.split()[0][17:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

out=sync.ROOT/'audit_bounded_campaign_progress_checked';assert not out.exists();results={}
for fighter in ('kano','sonya'):
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert not (folder/'stderr.log').read_text().strip()
        assert not any(p.suffix.lower() in ('.bin','.png','.wav') for p in folder.rglob('*') if p.is_file())
        rows=load(folder);identity='17' if fighter=='kano' else '18'
        assert len(rows['HOST_BOUND'])==len(rows['RESULT'])==1
        result=rows['RESULT'][0];assert result['frame']=='12000' and result['ending']==result['ending_completed']=='-1'
        assert rows['LIVE'] and all(r['human']==f'{identity}:{identity}' for r in rows['LIVE'])
        assert all(r['roster']==identity for r in rows['SELECT_ID'])
        stages=[int(r['stage']) for r in rows['STAGE']];assert stages==list(range(max(stages)+1))
        ownwins=[r for r in rows['WIN'] if int(r['slot'])==side]
        assert all(r['id']==identity and r['pc']=='FF8296B0' for r in ownwins)
        for r in ownwins:
            health=[int(v) for v in r['health'].split(',')];assert health[2-side]==0 and health[side-1]>0
        losses=rows.get('LOSS',[]);selects=rows['SELECT'];assert len(selects)==len(losses)+1
        for loss,selection in zip(losses,selects[1:]):
            assert int(selection['continue'])==int(loss['frame']) and int(selection['frame'])>int(loss['frame'])
        for stage in stages[1:]:
            prior=[r for r in ownwins if int(r['stage'])==stage-1 and int(r['frame'])<int(next(r['frame'] for r in rows['STAGE'] if int(r['stage'])==stage))]
            assert len({r['frame'] for r in prior})>=2
        results[f'{fighter}P{side}']=dict(terminal=terminal,observedStages=stages,completedOpponents=max(stages),nativeOwnWinReads=len(ownwins),paidContinueLosses=len(losses),actualSelections=len(selects),sampledTrueIdentityFields=len(rows['LIVE']),allReselectionsTrueIdentity=True,fullCampaignClear=False,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),scope='Four current cold physical campaigns bounded at12000 fields. Genuine round wins/stage advancement/paid losses/reselection. SonyaP2 did not clear first opponent. No bosses, ending, full audio/art or whole-port acceptance.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,fullCampaignClear=False)))
