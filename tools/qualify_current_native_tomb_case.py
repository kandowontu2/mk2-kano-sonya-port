"""Earned native Tomb admission and continuous finite scalar followthrough."""
import copy,json,re
import verify_native_source_sync as sync

def load(path):
    text=path.read_text();assert 'LUA ERROR' not in text
    rows={}
    for line in text.splitlines():
        if line.startswith('MK2_STAGE_'):
            rows.setdefault(line.split()[0][10:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows

def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['side']=='1' and r['winner']=='kano' for records in rows.values() for r in records)
    assert [(r['match'],r['arena'],r['ids']) for r in rows['MATCH']]==[('1','0','17,18'),('2','1','17,18')]
    for match in ('1','2'):
        damage=[r for r in rows['DAMAGE'] if r['match']==match]
        assert sum(int(r['before'])-int(r['after']) for r in damage)==322
        assert sum(r['after']=='0' for r in damage)==2
        assert all(r['pc']=='FF836700' and int(r['before'])>int(r['after']) for r in damage)
        window=next(r for r in rows['WINDOW'] if r['match']==match)
        assert window['kos']=='2' and window['damage']=='322'
    action=[r for r in rows['ENTRY'] if r['entry']=='FF8BDFE0'];assert len(action)==1
    action=action[0];assert action['arena']=='1' and action['id']=='17'
    command=rows['COMMAND'];assert len(command)==1 and command[0]['arena']=='1'
    assert int(action['frame'])==int(command[0]['frame'])+42
    fields=rows['FIELD'];by={int(r['age']):r for r in fields}
    assert len(by)==len(fields) and all(age in by for age in range(801))
    for age in range(801):
        row=by[age];assert int(row['frame'])==int(action['frame'])+age
        if row['own']!='00000000':assert row['id']=='17'
        if row['victim']!='00000000':assert row['victim_id']=='18'
    assert by[0]['own']==action['a8'] and by[0]['main']==action['a13']
    result=rows['RESULT'][0]
    assert result['matches']=='2' and result['kos']=='2' and result['damage']=='322' and result['action_arena']=='1'
    assert int(result['frame'])-int(action['frame'])>=1100 and not rows.get('HOST_BOUND')
    return dict(actionFrame=int(action['frame']),consecutiveSceneFields=801,followthroughFields=int(result['frame'])-int(action['frame']))

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_tomb_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_tomb_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');proof=gate(rows)
    bad=copy.deepcopy(rows);bad['FIELD'][0]['id']='1'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Proxy Kano accepted')
    bad=copy.deepcopy(rows);bad['DAMAGE'].pop(0)
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Unearned admission accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,scene=proof,
                proxyIdentityRejected=True,missingEarnedDamageRejected=True,
                logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
                scope='Current genuine KanoP1/SonyaP2 Tomb after two native full-health two-KO matches and paid rematch: native command/action,801consecutive scalar scene fields and1100followthrough. No whole raster/audio, all Tomb branches, Pit/secret/endings or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,currentNativeTomb=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
