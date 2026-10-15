"""Actual current remaining Tomb slots: qualified art/ground/shadow/input faults.

No new capture or altered game. Recompute original component projection and
shadow contracts from the terminal live source-replay logs, then reject actual
row/identity/control changes and restore the positive data after every fault.
"""
import copy
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

import run_current_tomb_ram_matrix_v3648 as current
import verify_current_tomb_ram_faults_v3636 as geometry

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3653_current_tomb_matrix_faults_checked'


def mutate_native(log,tag,field,transform):
    prefix='MK2_STAGE_'+tag+' '
    lines=log.splitlines()
    index=next(i for i,line in enumerate(lines)if line.startswith(prefix))
    row=dict(re.findall(r'(\w+)=([^\s]+)',lines[index]));before=row[field];after=transform(before)
    old=field+'='+before
    need(old in lines[index]and before!=after,'One actual native record field selected')
    lines[index]=lines[index].replace(old,field+'='+after,1)
    return '\n'.join(lines),dict(tag=tag,frame=int(row['frame']),field=field,before=before,after=after)


def verify_case(fighter,side,guest,payload,image):
    folder,output=current.case_paths(fighter,side);file=output/'report.json'
    report=json.loads(file.read_text())
    need(report['passed']and report['fighter']==fighter and report['side']==side and
         report['sampledFrames']==537 and not report['fullPortAcceptance'],
         'Actual terminal current true-character/physical-slot rendering proof')
    log=(folder/'run.log').read_text();groups=defaultdict(list);buffers={}
    for line in log.splitlines():
        parsed=current.model.parse(line)
        if not parsed:continue
        kind,row=parsed
        if kind=='FLOOR_CPU':continue
        groups[kind].append(row)
        if kind=='FLOOR_GFX':
            need(bytes.fromhex(row['data'])==image[row['first']:row['first']+row['bytes']],
                 'Actual graphics bytes independently source-bound')
            buffers[row['key']]=row
    projections=geometry.parts_and_ground(groups,guest,payload)
    shadows=geometry.shadow_contract(groups,buffers)
    need(projections==report['nativeScene']['sourceBoundProjections']and
         shadows['checked_copies']==report['nativeScene']['nativeShadowCopies'],
         'Original terminal live source/render inventory exactly retained')
    first=groups['SHADOW_COMPONENT'][0]['event']
    index=next(i for i,r in enumerate(groups['FLOOR_DMA'])if r['event']==first)
    vectors=[('original-art offset','FLOOR_QUEUE_PART',0,'dx',geometry.parts_and_ground),
             ('own floor anchor','FLOOR_QUEUE_TRANSFORM',0,'floor',geometry.parts_and_ground),
             ('camera projection','FLOOR_QUEUE_TRANSFORM',0,'display',geometry.parts_and_ground),
             ('shadow source','SHADOW_COMPONENT',0,'first_source',geometry.shadow_contract),
             ('shadow black pen','FLOOR_DMA',index,'color',geometry.shadow_contract),
             ('shadow row coordinate','FLOOR_DMA',index,'y',geometry.shadow_contract)]
    faults=[]
    for label,kind,index,field,contract in vectors:
        changed=copy.deepcopy(groups);row=changed[kind][index];before=row[field];row[field]+=1
        try:
            if contract is geometry.parts_and_ground:contract(changed,guest,payload)
            else:contract(changed,buffers)
        except (ValueError,AssertionError)as error:
            faults.append(dict(label=label,kind=kind,frame=row['frame'],event=row.get('event'),
                               field=field,before=before,after=row[field],rejectedBy=str(error)))
        else:raise ValueError('Changed actual native geometry/art/shadow accepted')
        geometry.parts_and_ground(groups,guest,payload);geometry.shadow_contract(groups,buffers)
    native=current.native.check_log(log,fighter,side,1,'positive',guest=guest)
    for label,tag,field,transform,wanted in (
        ('wrong cold true identity','BOOT','own_id',lambda value:str(35-int(value)),
         'True native IDs from cold boot'),
        ('wrong physical selected identity','SELECT_ID','actual',lambda value:str(35-int(value)),
         'Wrong selected native ID'),
        ('proxy/rematch identity','MATCH','ids',lambda value:','.join(reversed(value.split(','))),
         'Proxy/rematch identity'),
        ('discontinuous earned health','DAMAGE','after',lambda value:str(int(value)+1),
         'Native two full-health KO damage chains')):
        changed,details=mutate_native(log,tag,field,transform)
        try:current.native.check_log(changed,fighter,side,1,'positive',guest=guest)
        except ValueError as error:
            need(str(error)==wanted,'Actual input/identity fault reaches intended original gate')
            faults.append(dict(label=label,**details,rejectedBy=str(error)))
        else:raise ValueError('Changed actual native input/identity/health accepted')
        current.native.check_log(log,fighter,side,1,'positive',guest=guest)
    for path,wanted in report['inputHashes'].items():need(sha(path)==wanted,'Actual executed source/evidence unchanged')
    return dict(fighter=fighter,side=side,truePhysicalIDs=report['truePhysicalIDs'],
                actualSourceBoundProjections=projections,actualNativeShadowCopies=shadows['checked_copies'],
                nativeInputState=native,qualifiedActualFaults=faults,
                positivesRestoredAfterEveryFault=True,sourceReport=str(file),sourceReportSHA256=sha(file))


def main():
    need(not OUT.exists(),'Fresh immutable matrix counterexample evidence')
    matrix_path=current.OUT/'report.json';matrix=json.loads(matrix_path.read_text())
    need(matrix['passed']and matrix['currentBothCharactersBothPhysicalSlotsNativeTombRenderShadowEraseAccepted'],
         'Actual complete current remaining-slot matrix')
    guest,_,payload,_,_=current.stage.inventory.current.expected_current();pins={}
    image=current.source_graphics(payload,pins)
    cases=[verify_case(fighter,side,guest,payload,image)for fighter,side in current.CASES]
    for case in cases:
        path=Path(case['sourceReport']);pins[str(path)]=case['sourceReportSHA256']
        report=json.loads(path.read_text())
        for file,wanted in report['inputHashes'].items():pins[file]=wanted
    pins[str(matrix_path)]=sha(matrix_path);pins[str(Path(__file__).resolve())]=sha(__file__)
    pins[str(Path(geometry.__file__))]=sha(geometry.__file__)
    value=dict(passed=True,candidate=current.stage.NAME,cases=cases,
               qualifiedActualMetadataInputIdentityHealthFaults=sum(len(r['qualifiedActualFaults'])for r in cases),
               newRuntimeOrRasterVRAMAudioPlayableCopies=0,stageAudioFidelityAccepted=False,
               allStockNewMirrorVictimBranchAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();file=OUT/'report.json';file.write_text(json.dumps(value,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact matrix qualified-fault report')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes')},indent=2))


if __name__=='__main__':main()
