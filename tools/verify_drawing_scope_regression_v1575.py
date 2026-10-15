"""Actual immutable drawing scopes plus in-memory rejection regressions; no guest edits."""
import hashlib,json,re
from pathlib import Path
import verify_native_floor_campaign_v1571 as before
import verify_native_floor_campaign_v1573 as after

ROOT=after.ROOT
OUT=ROOT/'audit_v1575_drawing_scope_regression_checked'

def verify():
    pins={};actual=[];rejected=[]
    for name in ('audit_v1564_native_arenas_kano_p1','audit_v1564_native_arenas_sonya_p2',
                 'audit_v1568_floor_geometry_smoke_kano_p2','audit_v1568_floor_geometry_smoke_sonya_p1'):
        folder=ROOT/name;result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        assert result['exit_code']==0 and result['assistance']=='none'
        log=folder/'run.log';original=after.digest(log);count=0;first=None;ordinary=[]
        with log.open(encoding='utf-8-sig') as stream:
            for line in stream:
                match=re.match(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',line)
                if not match:continue
                if match[1].startswith(('FLOOR_','SHADOW_')):
                    after.drawing_scope(match[2],result['human_slot'],result['player'])
                    count+=1
                    if first is None:first=line
                else:ordinary.append(line)
        assert count>100 and first is not None
        # Reproduce the retained checker failure using the first real row,
        # then require the successor to accept exactly that unchanged row.
        try:before.parse(first)
        except ValueError as error:assert str(error)=='Invalid actual drawing row scope'
        else:raise AssertionError('Preserved failure did not reproduce')
        assert after.parse(first,result['human_slot'],result['player'])==[]
        normal=''.join(ordinary)
        assert before.parse(normal)==after.parse(normal,result['human_slot'],result['player'])
        assert after.digest(log)==original
        pins[str(log)]=original;pins[str(folder/'result.json')]=after.digest(folder/'result.json')
        actual.append(dict(folder=name,actualDrawingRowsChecked=count,ordinaryRowsUnchanged=len(ordinary),
                           originalFailureReproduced=True))
        mutations={
            'guest_write':first.replace('writes=0','writes=1',1),
            'assisted':first.replace('assistance=none','assistance=guest',1),
            'other_valid_slot':first.replace('human_slot='+str(result['human_slot']),'human_slot='+str(3-result['human_slot']),1),
            'other_valid_fighter':first.replace('fighter='+result['player'],'fighter='+('sonya' if result['player']=='kano' else 'kano'),1),
            'invalid_slot':first.replace('human_slot='+str(result['human_slot']),'human_slot=3',1),
            'missing_scope':first.replace(' writes=0','',1),
            'duplicate_scope':first.rstrip()+' writes=0',
            'suffix_scope':first.replace('writes=0','writes=0junk',1),
        }
        for label,text in mutations.items():
            match=re.match(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$',text)
            try:after.parse(text,result['human_slot'],result['player'])
            except ValueError:rejected.append(name+':'+label)
            else:raise AssertionError('Bad scope accepted: '+label)
    for module in (before,after):pins[str(Path(module.__file__).resolve())]=after.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=after.digest(Path(__file__))
    return dict(passed=True,actualCaptures=actual,inMemoryCounterexamplesRejected=rejected,
                drawingScopeMustMatchActualPhysicalSlotAndFighter=True,
                noCaptureOrGameChanged=True,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
