"""Natural Pit admission; distinguish capped attempts from complete scenes."""
import copy,json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load

def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['side']=='1' and r['winner']=='kano' for records in rows.values() for r in records)
    matches=rows['MATCH']
    assert [(int(r['match']),int(r['arena']),r['ids']) for r in matches]==[(i+1,i,'17,18') for i in range(len(matches))]
    assert 1<=len(matches)<=7
    for window in rows.get('WINDOW',[]):
        damage=[r for r in rows['DAMAGE'] if r['match']==window['match']]
        assert sum(int(r['before'])-int(r['after']) for r in damage)==322
        assert sum(r['after']=='0' for r in damage)==2
        assert all(r['pc']=='FF836700' and int(r['before'])>int(r['after']) for r in damage)
        assert window['kos']=='2' and window['damage']=='322'
    actions=[r for r in rows.get('ENTRY',[]) if r['entry']=='FF8BDDE0']
    assert len(actions)<=1
    if not actions:return dict(nativePitActivated=False,matches=len(matches))
    assert len(matches)==7 and len(rows['WINDOW'])==7
    action=actions[0];assert action['arena']=='6' and action['id']=='17'
    command=rows['COMMAND'];assert len(command)==1 and command[0]['arena']=='6'
    assert int(action['frame'])==int(command[0]['frame'])+42
    fields=rows.get('FIELD',[]);by={int(r['age']):r for r in fields}
    assert len(by)==len(fields)
    for age,row in by.items():
        assert int(row['frame'])==int(action['frame'])+age
        if row['own']!='00000000':assert row['id']=='17'
        if row['victim']!='00000000':assert row['victim_id']=='18'
    assert by[0]['own']==action['a8'] and by[0]['main']==action['a13']
    complete=bool(rows.get('RESULT')) and int(rows['RESULT'][0]['frame'])-int(action['frame'])>=1100
    if complete:assert all(age in by for age in range(801))
    return dict(nativePitActivated=True,matches=7,actionFrame=int(action['frame']),completeSceneFollowthrough=complete)

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_pit_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_pit_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    complete=terminal['exitCode']==0 and terminal['limitReason'] is None
    assert complete or (terminal['limitReason']=='wall_limit' and terminal['exitCode']!=0)
    assert terminal['elapsedSeconds']<=(90 if complete else 92)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_pit_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');proof=gate(rows)
    if proof['nativePitActivated']:
        bad=copy.deepcopy(rows);bad['FIELD'][0]['id']='1'
        try:gate(bad)
        except AssertionError:pass
        else:raise AssertionError('Proxy Kano accepted')
        bad=copy.deepcopy(rows);bad['DAMAGE'].pop(0)
        try:gate(bad)
        except AssertionError:pass
        else:raise AssertionError('Unearned stage admission accepted')
    report=dict(passedObservationChecks=True,completedRunAccepted=complete,sourceSync=source,terminal=terminal,scene=proof,
                currentPitSceneAccepted=complete and proof.get('completeSceneFollowthrough',False),
                logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
                scope='Physical standingHK/paid-rematch native arena progression to Pit6 with real KanoP1/SonyaP2; health-ledger322/twoKO windows and native Pit action if reached. Capped attempts never accepted as complete. No full raster/audio, all Pit branches/victims or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(completedRunAccepted=complete,scene=proof,fullPortAcceptance=False)))

if __name__=='__main__':main()
