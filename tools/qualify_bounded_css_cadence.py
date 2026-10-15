"""Compare actual selected border cadence/coverage with adjacent stock portraits."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def rows(folder):
    result={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            tag=line.split()[0][7:]
            result.setdefault(tag,[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return result

def gate(cadence,identity,neighbor):
    windows=[]
    for first,last,wanted in ((54,70,identity),(78,94,neighbor),(224,260,identity)):
        window=[r for r in cadence if first<=int(r['age'])<=last]
        assert len(window)==last-first+1 and all(r['roster']==wanted for r in window)
        assert all(int(r['border'])==(1064 if int(r['age'])%8 in (1,2,3,4) else 0) for r in window)
        assert len({r['posehash'] for r in window})>=3
        windows.append(dict(firstAge=first,lastAge=last,roster=wanted,distinctCharacterRegionSignatures=len({r['posehash'] for r in window})))
    return windows

out=sync.ROOT/'audit_bounded_css_cadence_checked';assert not out.exists()
proof_path=sync.ROOT/'audit_bounded_current_ui_review_checked/report.json'
proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
for fighter,identity,neighbor in (('kano','17','1'),('sonya','18','9')):
    for side in (1,2):
        key=f'{fighter}P{side}'
        folder=sync.ROOT/f'audit_bounded_css_cadence_{fighter}_p{side}_runtime'
        base=sync.ROOT/f'audit_bounded_current_ui_select_{fighter}_p{side}_runtime'
        assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        assert not (folder/'stderr.log').read_text().strip()
        assert not list((folder/'snap').rglob('*.png'))
        actual=rows(folder);old=rows(base)
        for tag in ('SELECT','INPUT','FIELD','CSS','EXIT','LIVE','RESULT'):assert actual[tag]==old[tag],tag
        windows=gate(actual['CADENCE'],identity,neighbor);faults=[]
        for fault in ('frozen_border','thin_border','frozen_character_region'):
            bad=copy.deepcopy(actual['CADENCE'])
            window=[r for r in bad if 224<=int(r['age'])<=260]
            for r in window:
                if fault=='frozen_border':r['border']='1064'
                elif fault=='thin_border' and r['border']=='1064':r['border']='532'
                elif fault=='frozen_character_region':r['posehash']=window[0]['posehash']
            try:gate(bad,identity,neighbor)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted')
        results[key]=dict(windows=windows,rejectedFaults=faults,physicalGameplayPrefixUnchanged=True,terminal=terminal,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),priorProofSHA256=sync.sha(proof_path),checkerSHA256=sync.sha(Path(__file__)),borderOnFields=4,borderOffFields=4,litBorderPixels=1064,scope='Selected top-row portraits and character-region animation over three stable windows per slot. Not every pixel alignment, whole transition teardown or full integration.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,stockMatchedBlink=True,movingCharacterRegion=True)))
