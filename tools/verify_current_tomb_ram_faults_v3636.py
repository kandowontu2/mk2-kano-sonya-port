"""Qualified actual Tomb sprite/projection/shadow metadata faults, not new captures."""
import copy
import json
import subprocess
from collections import defaultdict
from pathlib import Path

import current_tomb_ram_model_v3629 as model
import run_current_tomb_ram_v3633 as capture
import inspect_native_shadow_rows_v635 as shadow
from verify_cpu_pair_display_v635_v3 import group

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v3637_current_native_tomb_ram_faults_checked'


def parts_and_ground(groups,guest,payload):
    parts=defaultdict(list)
    for row in groups['FLOOR_QUEUE_PART']:parts[row['frame'],row['cursor']].append(row)
    transforms={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE_TRANSFORM']}
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    need(len(queues)==len(groups['FLOOR_QUEUE'])and set(queues)==set(transforms),
         'Exact original FIFO/transform inventory')
    for key,q in queues.items():
        expected=group(q,payload,guest);observed=parts[key]
        need(len(observed)==len(expected)and all(all(p[k]==v for k,v in e.items())
             for p,e in zip(observed,expected)), 'Actual FIFO component offsets/source equal original ROM composites')
        t=transforms[key]
        need(t['floor']==q['floor']==t['stageY']-({17:134,18:135}[q['id']]),
             'Actual own fighter floor equals native stage minus original source anchor')
        part=expected[q['part']];signed=model.erase.short
        x,y=signed(t['world']),signed(t['world']>>16)
        if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
        x-=part['dx'];y-=part['dy'];command=q['command']>>16
        if command&16:x+=part['width']-1
        if command&32:y+=part['height']-1
        x+=signed(t['display']);y+=signed(t['display']>>16)
        need((q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),
             'Actual original camera/cache/native flip projection')
    return len(queues)


def shadow_contract(groups,buffers):
    shadow.data=lambda _: (groups,buffers,None,None,{})
    proof=shadow.inspect(None)
    need(proof['rowStreamVerified']and not proof['failures']and not proof['oversized_rows'],
         'Every actual native compressed row/source/cadence/black pen/XY shadow copy')
    return proof


def main():
    need(not OUT.exists(),'Fresh immutable qualified actual-metadata proof')
    source=capture.OUT/'report.json';report=json.loads(source.read_text())
    need(report['passed']and report['currentActualEarnedKanoP1TombWholeSceneRenderShadowEraseAccepted']
         and not report['fullPortAcceptance'], 'Actual terminal current continuous source/render proof')
    for file,wanted in report['inputHashes'].items():need(sha(file)==wanted,'Current source/capture unchanged')
    guest,_,payload,_,_=capture.stage.inventory.current.expected_current();pins={}
    image=capture.source_graphics(payload,pins);groups=defaultdict(list);buffers={}
    for line in (capture.CASE/'run.log').open(encoding='utf-8-sig'):
        parsed=model.parse(line)
        if not parsed:continue
        kind,row=parsed
        if kind=='FLOOR_CPU':continue
        groups[kind].append(row)
        if kind=='FLOOR_GFX':
            need(bytes.fromhex(row['data'])==image[row['first']:row['first']+row['bytes']],
                 'Actual graphics bytes remain independently ROM/source bound')
            buffers[row['key']]=row
    projections=parts_and_ground(groups,guest,payload);shadows=shadow_contract(groups,buffers)
    need(projections==report['nativeScene']['sourceBoundProjections']and
         shadows['checked_copies']==report['nativeScene']['nativeShadowCopies'],
         'Exact live-rendered projection/shadow inventory')
    faults=[]
    cases=[('original-art offset','FLOOR_QUEUE_PART',0,'dx',1,parts_and_ground),
           ('own floor anchor','FLOOR_QUEUE_TRANSFORM',0,'floor',1,parts_and_ground),
           ('native camera projection','FLOOR_QUEUE_TRANSFORM',0,'display',1,parts_and_ground),
           ('native shadow source','SHADOW_COMPONENT',0,'first_source',1,shadow_contract)]
    # Test the actual projected DMA coordinate, not descriptive world-y alone.
    first_event=groups['SHADOW_COMPONENT'][0]['event']
    index=next(i for i,r in enumerate(groups['FLOOR_DMA'])if r['event']==first_event)
    cases.extend([('native shadow black pen','FLOOR_DMA',index,'color',1,shadow_contract),
                  ('native shadow row coordinate','FLOOR_DMA',index,'y',1,shadow_contract)])
    for label,kind,index,field,delta,check in cases:
        changed=copy.deepcopy(groups);row=changed[kind][index];before=row[field];row[field]+=delta
        try:
            if check is parts_and_ground:check(changed,guest,payload)
            else:check(changed,buffers)
        except (ValueError,AssertionError)as error:
            faults.append(dict(label=label,kind=kind,frame=row['frame'],event=row.get('event'),
                               field=field,before=before,after=row[field],rejectedBy=str(error)))
        else:raise ValueError('Changed actual native metadata accepted: '+label)
        parts_and_ground(groups,guest,payload);shadow_contract(groups,buffers)
    for file,wanted in report['inputHashes'].items():need(sha(file)==wanted,'Faults never changed captured game/evidence')
    pins[str(source)]=sha(source);pins[str(Path(__file__).resolve())]=sha(__file__)
    pins[str(capture.CASE/'run.log')]=sha(capture.CASE/'run.log')
    value=dict(passed=True,candidate=capture.stage.NAME,actualSourceBoundProjections=projections,
               actualNativeShadowCopies=shadows['checked_copies'],qualifiedActualMetadataFaults=faults,
               positiveContractRestoredAfterEveryFault=True,newRuntimeOrRasterVRAMAudioCopies=0,
               stageAudioFidelityAccepted=False,allVictimMirrorBranchAcceptance=False,
               fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();file=OUT/'report.json';file.write_text(json.dumps(value,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact qualified fault report')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','qualifiedActualMetadataFaults')},indent=2))


if __name__=='__main__':main()
