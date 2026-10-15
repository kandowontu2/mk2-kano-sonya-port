"""Actual off-top native uppercut and rejection tests; immutable captures stay unchanged."""
import copy,json,re
from pathlib import Path
from collections import defaultdict
import verify_native_uppercut_screen_cull_v1589 as cull

ROOT=cull.arena.ROOT;OUT=ROOT/'audit_v1592_native_screen_cull_checked'

def verify():
    pins={};folder=ROOT/'audit_v1564_native_arenas_kano_p1';log=folder/'run.log'
    before=cull.arena.campaign.digest(log)
    diagnostic=ROOT/'audit_v1587_kano_native_visibility_diagnostic/report.json';old=json.loads(diagnostic.read_text())
    assert old['diagnosticCompleted']and old['exactSavedFrames']==302 and len(old['visibilityFailures'])==1
    for path,wanted in old['inputHashes'].items():assert cull.arena.campaign.digest(Path(path))==wanted;pins[path]=wanted
    pins[str(diagnostic)]=cull.arena.campaign.digest(diagnostic)
    record=old['visibilityFailures'][0];groups=defaultdict(list);frame=record['frame']-1
    assert record['frame']==44376 and record['arena']==8
    assert record['wholeVRAMMismatches']==record['displayedMismatches']==record['shadowMismatches']==0
    record=dict(next(r for r in old['records']if r['frame']==record['frame']))
    record['body']={int(key):value for key,value in record['body'].items()}
    hex_fields=cull.arena.native.raster.HEX|{'op','before0','before1','before','after','first_source','row'}
    str_fields=cull.arena.native.raster.STR|{'register'}
    with log.open(encoding='utf-8-sig')as stream:
        for line in stream:
            match=re.match(r'^MK2_NAT_CAMPAIGN_(FLOOR_QUEUE|FLOOR_QUEUE_DISPATCH|SHADOW_COMPONENT) ',line)
            if not match:continue
            at=int(re.search(r'\bframe=(\d+)',line)[1])
            if not frame-2<=at<=frame:continue
            cull.arena.campaign.drawing_scope(line,1,'kano')
            row=dict(re.findall(r'(\w+)=([^\s]+)',line))
            for key,value in row.items():
                if key not in str_fields:row[key]=int(value,16 if key in hex_fields else 10)
            groups[match[1]].append(row)
    guest,_,payload=cull.arena.native.grab.expected_guest()
    report=cull.prove(groups,record,1,17,guest,payload)
    rejected=[]
    for label in('not_uppercut','wrong_owner','grounded_hidden_body','part_source_changed','camera_inside_screen','missing_part'):
        altered=copy.deepcopy(groups)
        if label=='not_uppercut':
            for row in altered['FLOOR_QUEUE']:
                if row['slot']==1:row['action']=4
        else:
            for row in altered['SHADOW_COMPONENT']:
                if row['slot']!=1 or row['frame']!=frame:continue
                if label=='wrong_owner':row['owner']+=16
                elif label=='grounded_hidden_body':row['y']=row['floor']
                elif label=='part_source_changed':row['first_source']+=8
                elif label=='camera_inside_screen':row['cameraY']=-1000
            if label=='missing_part':altered['SHADOW_COMPONENT']=[r for r in altered['SHADOW_COMPONENT']if not(r['slot']==1 and r['frame']==frame and r['component']==1)]
        try:cull.prove(altered,record,1,17,guest,payload)
        except (AssertionError,ValueError):rejected.append(label)
        else:raise AssertionError('Invalid screen-cull condition accepted: '+label)
    assert len(rejected)==6 and cull.arena.campaign.digest(log)==before
    pins[str(log)]=before
    for module in(cull,cull.layout):pins[str(Path(module.__file__).resolve())]=cull.arena.campaign.digest(Path(module.__file__))
    pins[str(Path(__file__).resolve())]=cull.arena.campaign.digest(Path(__file__))
    return dict(passed=True,actualNativeUppercutCull=report,inMemoryCounterexamplesRejected=rejected,
                capturesAndGameUnchanged=True,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)


