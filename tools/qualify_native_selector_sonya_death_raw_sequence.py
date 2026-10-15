"""Native47752 raw death-effect sequence, not universal victim-art acceptance.

First object has observed constructor, eight four-field descriptors, complete
native candidate/FIFO inventory and explicit removal. Second has eleven
five-field descriptors; address reuse later is quarantined, not death-effect
lifetime evidence. Complete source/record/RGB/audio equality preserves the
previous finite proofs without claiming their corruption tests were rerun.
"""
import copy
import hashlib
import json
import struct
import traceback
from collections import Counter
from pathlib import Path
import capture_native_selector_sonya_death_raw_lifetime as capture
import capture_native_selector_sonya_throw_late_views as previous
import qualify_native_selector_sonya_throw_late_lifetime as checkpoint

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_death_raw_sequence_checked'
VIEWS=ROOT/'audit_native_selector_sonya_death_raw_actual_views.json'
TAG='MK2_DEATH_RAW_'
rows=checkpoint.scope['rowset']


def source_gate(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    ranges=((0xffa0d9d0,0xffa0ecf0),(0xff83acb0,0xff83b390),
        (0xff838d80,0xff838f60),(0xff83e8f0,0xff83eb00),
        (0xff83f610,0xff83f650),(0xff8093e0,0xff8096d0),
        (0xff840450,0xff840600),(0xff840940,0xff840d00),
        (0xff804000,0xff8045d0))
    for lo,hi in ranges:
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Entire original native constructor/animation/retirement/raw renderer source')
    return [[hex(a),hex(b)] for a,b in ranges]


def raw_gate(groups,guest):
    source_gate(guest)
    def hx(r,k):return int(r[k],16)
    need({k:len(v) for k,v in groups.items()}==dict(CONSTRUCT=2,FIELD=539,CANDIDATE=484,QUEUE=452,REMOVE=1,RESULT=1),
         'Whole actual raw callback inventory')
    allrows=sorted((r for rs in groups.values() for r in rs),key=lambda r:int(r['sequence']))
    need([int(r['sequence']) for r in allrows]==list(range(1,1480)), 'Complete unaliased raw callback sequence')
    need(all(r['writes']=='0' and r['assistance']=='none' for r in allrows),'Only passive raw evidence')
    constructors=groups['CONSTRUCT'];subject=0x01034e90
    definitions={'first':(3024,0x01038c70,0xffa0e060,0x4d00,9,0xffa0ea10,8,4),
                 'second':(3108,0x01039ae0,0xffa0e3b0,0xb948,10,0xffa0eb30,11,5)}
    native_tables={}
    for r,(kind,(birth,actor,entry,opcode,subjectreg,table,n,period)) in zip(constructors,definitions.items(),strict=True):
        need(r['kind']==kind and int(r['frame'])==birth and hx(r,'actor')==hx(r,'a8')==actor and
             hx(r,'subject')==hx(r,'a'+str(subjectreg))==subject and hx(r,'entry')==entry and
             hx(r,'pc')==entry+16 and hx(r,'opcode')==opcode and r['mask']=='FFFF' and
             r['id']=='0' and r['pose']=='00000000' and r['body']=='0000' and actor!=subject,
             'True Sonya subject and distinct native raw-constructor return register binding')
        need(hx(r,'opcode')==struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0],
             'Actual executing original constructor return opcode')
        a=(table-0xff800000)//8
        values=list(struct.unpack_from('<'+('I'* (9 if kind=='first' else 13)),guest,a))
        descriptors=[d for d in values if d]
        need(len(descriptors)==n and values[8 if kind=='first' else 5]==0 and
             (kind=='first' or values[12]==0), 'Original native descriptor table and terminators')
        native_tables[kind]=descriptors
        need(hx(r,'a5')==hx(r,'descriptor')==descriptors[0], 'Native actual constructor descriptor input')
    reuse=[r for r in groups['FIELD'] if r['kind']=='second' and int(r['frame'])>=3438]
    need(len(reuse)==177 and int(reuse[0]['frame'])==3438 and reuse[0]['descriptor']=='FFC0D790' and
         reuse[0]['graphic']=='04003766' and reuse[0]['facing']=='9008' and reuse[0]['vx']=='00000000',
         'Explicit later pool-address reuse boundary; never a continuing victim object claim')
    first_fields=[r for r in groups['FIELD'] if r['kind']=='first']
    second_fields=[r for r in groups['FIELD'] if r['kind']=='second' and int(r['frame'])<3438]
    need([int(r['frame']) for r in first_fields]==list(range(3024,3056)) and
         [int(r['frame']) for r in second_fields]==list(range(3108,3438)), 'Every observed pre-reuse raw field')
    for kind,fs in (('first',first_fields),('second',second_fields)):
        birth,actor,_,_,_,_,n,period=definitions[kind]
        for r in fs:
            ordinal=min((int(r['frame'])-birth)//period,n-1)
            need(hx(r,'actor')==actor and hx(r,'subject')==subject and int(r['birth'])==birth and
                 hx(r,'descriptor')==native_tables[kind][ordinal] and r['id']=='0' and r['pose']=='00000000' and
                 r['body']=='0000' and r['type']=='0', 'Native complete raw descriptor cadence and distinct actor lifetime')
            offset=(hx(r,'descriptor')-0xff800000)//8
            need(hx(r,'size')==struct.unpack_from('<I',guest,offset)[0] and
                 hx(r,'graphic')==struct.unpack_from('<I',guest,offset+8)[0], 'Exact native raw size/graphic descriptor words')
        first=fs[0]
        need((first['xraw'],first['yraw'])==(('013E0000','00B80000') if kind=='first' else ('01740000','00B00000')),
             'Actual native original floor-effect setup coordinates')
    active={k:[r for r in groups[k] if r['kind']=='first' or int(r['frame'])<3438] for k in ('CANDIDATE','QUEUE')}
    candidates=active['CANDIDATE'];queues=active['QUEUE']
    ckeys={(r['kind'],r['frame']):r for r in candidates}
    need(len(ckeys)==len(candidates),'No duplicate active raw render field')
    need([int(r['frame']) for r in candidates if r['kind']=='first']==list(range(3025,3057)) and
         [int(r['frame']) for r in queues if r['kind']=='first']==list(range(3025,3057)),
         'Every first raw native candidate and FIFO through last pre-retirement draw')
    for tag,rs in active.items():
        entry,opcode=(0xff8042a0,0x4d42) if tag=='CANDIDATE' else (0xff804410,0x0981)
        for r in rs:
            birth,actor,*_=definitions[r['kind']]
            need(hx(r,'entry')==entry and hx(r,'pc')==entry+16 and hx(r,'opcode')==opcode and r['mask']=='FFFF' and
                 hx(r,'actor')==hx(r,'a0')==actor and hx(r,'subject')==subject and int(r['birth'])==birth and
                 r['a3']=='00000000' and r['a7']=='00000000' and r['body']=='0000' and r['pose']=='00000000' and
                 r['id']=='0' and hx(r,'a9')==hx(r,'size') and hx(r,'a11')==hx(r,'graphic') and
                 hx(r,'a12')==hx(r,'facing')<<16, 'Actual native raw renderer opcode/object/size/source/facing registers')
            need(hx(r,'descriptor') in native_tables[r['kind']], 'No reused-address descriptor admitted as death rendering')
            if tag=='QUEUE':
                c=ckeys.get((r['kind'],r['frame']))
                need(c is not None and int(c['sequence'])<int(r['sequence']) and
                     all(r[k]==c[k] for k in ('actor','descriptor','size','graphic','facing','xraw','yraw','a1','a9','a11','a12')),
                     'Every actual native FIFO record follows its same-field raw candidate and physical source')
    retirement=groups['REMOVE'][0]
    need(retirement['kind']=='first' and retirement['removal']=='actor_retire' and int(retirement['frame'])==3056 and
         retirement['birth']=='3024' and hx(retirement,'actor')==hx(retirement,'a0')==hx(retirement,'a8')==0x01038c70 and
         hx(retirement,'subject')==subject and retirement['entry']=='FF840450' and retirement['pc']=='FF840460' and
         retirement['opcode']=='0D5F' and retirement['mask']=='FFFF' and retirement['a9']=='FFA0EB10' and
         retirement['descriptor']=='FFC06E50' and retirement['a13']=='0106D400', 'Explicit original first-object terminator and native retirement')
    need(groups['RESULT'][0]['objects']=='2', 'Native original observer terminal object count')
    return dict(firstConstructor=constructors[0],secondConstructor=constructors[1],firstRetirement=retirement,
        firstDescriptorFields=32,secondPreReuseFields=330,nativeDescriptors=native_tables,
        observedActiveRawCandidates=len(candidates),observedActiveRawFIFORecords=len(queues),
        firstRawNativeRetirementObserved=True,secondRawNativeRetirementObserved=False,
        laterReusedAddressFieldsQuarantined=len(reuse),reuseBoundary=reuse[0],
        wholeRawPixelGeometryModelAccepted=False,allVictimArtAccepted=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable raw-sequence report')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    old_folder,old_text,old_images=previous.RAM_CASES[previous.KEY]
    oldmeta=json.loads((old_folder/'result.json').read_text())
    transport=json.loads((capture.OUT/'report.json').read_text())
    parent=json.loads((checkpoint.OUT/'report.json').read_text())
    need(transport['passed'] and parent['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         previous.NATIVE_HANDLES[previous.KEY]['process'].poll()==0 and held['identity']==transport['actualNativeIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==(47752,38752,1791758680.7186718),
         'Exact original native47752 terminal handle and completed source-qualified11004')
    pins=dict(transport['inputHashes'])
    for p,digest in parent['inputHashes'].items():
        need(p not in pins or pins[p]==digest,'No frozen parent input changed');pins[p]=digest
    need(all(sha(p)==d for p,d in pins.items()),'Every complete current native/source/evidence hash')
    def original_records(value):
        return [s for s in value.splitlines() if s.startswith('MK2_') and not s.startswith((TAG,'MK2_HPHASE_RGB_DIGEST '))]
    old,new=original_records(old_text),original_records(text)
    need(old==new and len(old)>270532,'Complete previous observed native records, not counts alone')
    groups={k:rows(text,TAG+k) for k in ('CONSTRUCT','FIELD','CANDIDATE','QUEUE','REMOVE','RESULT')}
    positive=raw_gate(groups,state['guest']);faults=[]
    trials=[('subject','CONSTRUCT',0,'subject','010396C0'),('constructor_actor','CONSTRUCT',0,'a8','01034E90'),
        ('constructor_descriptor','CONSTRUCT',0,'a5','FFC06B40'),('descriptor_cadence','FIELD',0,'descriptor','FFC06B40'),
        ('descriptor_size','FIELD',0,'size','000F0062'),('graphic_source','FIELD',0,'graphic','0460CB77'),
        ('raw_pose','FIELD',0,'pose','FF033840'),('candidate_source','CANDIDATE',0,'a11','0460CB77'),
        ('queue_actor','QUEUE',0,'a0','01034E90'),('retirement_actor','REMOVE',0,'a0','01039AE0'),
        ('retirement_terminator','REMOVE',0,'a9','FFA0EB30'),('retirement_frame','REMOVE',0,'frame','3057')]
    for name,tag,i,key,value in trials:
        bad=copy.deepcopy(groups);need(bad[tag][i][key]!=value,'Effective raw corruption');bad[tag][i][key]=value
        try:raw_gate(bad,state['guest'])
        except (ValueError,AssertionError) as error:faults.append(dict(name=name,rejectedBy=str(error)))
        else:raise ValueError('Raw sequence corruption accepted '+name)
    need(raw_gate(groups,state['guest'])==positive and len(faults)==12,'Whole positive restored after all12 effective raw faults')
    rasters=checkpoint.scope['original'].rasters.rasters(images,meta['actualScenes'])
    need(len(rasters)==67,'All67 native RGB callbacks full-digest checked')
    bystage={(r['stage'],r['frame']):r for r in meta['actualScenes']}
    need(len(bystage)==67,'Unique native capture stage/frame')
    for r in oldmeta['actualScenes']:
        newr=bystage.get((r['stage'],r['frame']))
        need(newr is not None and images[newr['imageKey']].tobytes()==old_images[r['imageKey']].tobytes(),
             'Every whole previous42 native raster unchanged, despite extra callback ordinals')
    views=json.loads(VIEWS.read_text())
    need(views['passed'] and views['actualNativeIdentity']==held['identity'] and
         views['originalIdentityRevalidatedBeforeAndAfter'] and [r['index'] for r in views['actualViewedCallbacks']]==[38,42,44,45,46,55,56,62],
         'Eight actually reviewed bound native raw-transition rasters')
    for r in views['actualViewedCallbacks']:
        actual=rasters[r['index']]
        need(r['header']==actual['header'] and r['SHA256']==actual['header']['sha256'] and
             r['nativeRGBSHA256']==actual['nativeRGBSHA256'] and r['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],
             'Every actual viewed raw transition bound to complete original pixels')
    audio,oldaudio=capture.AUDIO[capture.KEY],previous.AUDIO[previous.KEY]
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom','expectedROM','audioGuestObserved'):
        need(audio[key]==oldaudio[key],'Whole actual PCM/DAC/ROM bytes and headers equal source-qualified parent')
    need(len(audio['pcmChunks'])==len(audio['dacChunks'])==1645,'Whole original native audio callback inventory')
    for path in (Path(__file__),VIEWS,checkpoint.OUT/'report.json',capture.OUT/'report.json',
        ROOT/'tools/read_native_selector_sonya_death_raw_frames.py',ROOT/'tools/read_native_selector_sonya_death_raw_frames_remote.py',
        *(p for p in folder.rglob('*') if p.is_file())):
        p=str(path.resolve());d=sha(p);need(p not in pins or pins[p]==d,'Immutable additional evidence');pins[p]=d
    need(all(sha(p)==d for p,d in pins.items()),'Complete final input hash inventory')
    result=dict(passed=True,goalStatus='active',scope=__doc__,actualNativeIdentity=held['identity'],
        rawSequence=positive,actualRawFaultsRejected=faults,wholeOriginalNativeRecordsUnchanged=len(old),
        wholePrevious42NativeRGBFramesIdentical=True,wholeCurrentRGBCallbacks=67,actualViews=views,
        wholePCM_DAC_ROMBytesAndHeadersIdentical=True,completeStereoFrames=1645*960,
        wholePCM_SHA256=hashlib.sha256(b''.join(audio['pcmChunks'])).hexdigest().upper(),
        parentFiniteGeometryAndAudioByCompleteInputOutputEquality=True,parentFaultsRerun=False,
        wholeSourceRanges=source_gate(state['guest']),requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        secondRawRemovalAndFullArtStillOpen=True,fullPortAcceptance=False,inputHashes=pins,
        publicPlayableChanged=False,newNativeGamesDuringQualification=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS raw constructor/cadence/source/FIFO/removal,12 faults,67 RGB and complete parent/native/audio equivalence',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve raw sequence rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
