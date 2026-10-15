"""Native damage interrupts reverse; actual retry/store/ordinary controls required."""
import copy
import json
import re
import qualify_bounded_current_morph_hits as prior
import verify_native_source_sync as sync


def gate(rows,target,side):
    proof=prior.gate(rows,target,side)
    begins=rows['RESTORE_BEGIN']
    assert len(begins)==2
    attack=rows['ATTACK'];assert len(attack)==1
    first,retry=int(begins[0]['frame']),int(begins[1]['frame'])
    assert int(attack[0]['frame'])==first+2 and int(attack[0]['slot'])==3-side
    assert first<proof['hitFrame']<retry<proof['returnFrame']
    assert proof['returnFrame']==retry+12
    assert all(r['pc']=='FFA16310' and int(r['id'])==(17 if target=='kano' else 18) for r in begins)
    assert any(r['action']=='0107' and int(r['slot'])==3-side and first<=int(r['frame'])<=proof['hitFrame'] for r in rows['PAIR'])
    return dict(proof,reverseInterrupted=True,nativeRetryFrame=retry,originalRetryToStoreFields=12)


if __name__=='__main__':
    out=sync.ROOT/'audit_bounded_current_morph_reverse_attacks_checked';assert not out.exists()
    results={}
    for target in ('kano','sonya'):
        for side in (1,2):
            folder=sync.ROOT/f'audit_bounded_current_morph_reverse_attack_{target}_p{side}_runtime'
            terminal=json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode']==0 and terminal['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
            rows={}
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_HUMAN_SHANG_'):
                    rows.setdefault(line.split()[0].removeprefix('MK2_HUMAN_SHANG_'),[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            proof=gate(rows,target,side)
            broken=copy.deepcopy(rows);broken['RESTORE_BEGIN']=broken['RESTORE_BEGIN'][:1]
            try:gate(broken,target,side)
            except AssertionError:pass
            else:raise AssertionError('Missing actual reverse retry accepted')
            results[target+str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),missingRetryRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),fullPortAcceptance=False,
        scope='Four current real40damage native uppercut interruptions during reverse transformation; actual added IDs retained through hit, native restore retry/original12field store/ordinary controls/clean paired physics. No KO, forward timing, CPU or whole art/audio/port acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=4,fullPortAcceptance=False)))
