"""Actual native38516 complete raw sprite bulk reclamation and later reuse.

Native first effect retires3056; its address is reused3097 for another effect.
Native second effect remains active3108..3402, then original pool reset3403
returns it to the fixed-stride358-object free pool before3438 allocation.
Do not mistake unchanged stale descriptor words in a free record for a live
victim. No claim of every finisher, pixel-pen stream, campaign or full port.
"""
import copy
import json
import traceback
from pathlib import Path
import capture_native_selector_sonya_death_raw_pool as capture
import qualify_native_selector_sonya_death_raw_sequence as previous
import qualify_native_selector_sonya_death_raw_projection as projection

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_checked'
PREFIX='MK2_DEATH_DRAIN_'
FIRST,STRIDE,COUNT=0x0102d6f0,0x210,0x166
END=FIRST+STRIDE*COUNT
LISTS=('objects','layer1','layer2','freeObjects')


def data(text):
    return {k:previous.rows(text,PREFIX+k) for k in ('RESET_ENTER','RESET_COMPLETE','REUSE','FIELD_LISTS','MEMBER',
        'RESET_ENTER_LISTS','RESET_COMPLETE_LISTS','REUSE_LISTS')}


def gate(g,guest):
    previous.source_gate(guest)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff83f060,0xff83f210),(0xff8090b0,0xff809270)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Whole original native sprite pool reset/pop implementations')
    need({k:len(v) for k,v in g.items()}==dict(RESET_ENTER=1,RESET_COMPLETE=1,REUSE=2,FIELD_LISTS=591,MEMBER=1106,
        RESET_ENTER_LISTS=1,RESET_COMPLETE_LISTS=1,REUSE_LISTS=2), 'Complete actual native pool observer inventory')
    allrows=sorted((r for rs in g.values() for r in rs),key=lambda r:int(r['sequence']))
    need([int(r['sequence']) for r in allrows]==list(range(1,len(allrows)+1)) and
         all(r['writes']=='0' and r['assistance']=='none' for r in allrows), 'Every unaliased passive native pool record')
    expected_lists={}
    for tag in ('FIELD_LISTS','RESET_ENTER_LISTS','RESET_COMPLETE_LISTS','REUSE_LISTS'):
        for r in g[tag]:
            sets={}
            for k in LISTS:
                values=[] if r[k]=='-' else [int(v,16) for v in r[k].split(',')]
                need(len(values)==int(r[k+'Count'])==len(set(values)), 'Complete unique actual native linked-list nodes')
                if k=='freeObjects':
                    need(all(FIRST<=v<END and (v-FIRST)%STRIDE==0 for v in values) and
                         int(r[k+'Stop'],16) in (END,0x00fe0190), 'Only fixed-stride pool nodes and exact original sentinel')
                else:
                    need(all(0x01000000<=v<0x01100000 for v in values) and r[k+'Stop']=='00000000',
                         'Complete native active list with actual zero termination')
                sets[k]=set(values)
            active=sets['objects']|sets['layer1']|sets['layer2']
            need(sum(len(sets[k]) for k in LISTS[:3])==len(active) and not active&sets['freeObjects'],
                 'Native active sprite layers and free objects disjoint')
            members=[m for m in g['MEMBER'] if m['context']==tag and m['frame']==r['frame'] and
                     int(m['sequence'])>int(r['sequence']) and int(m['sequence'])<=int(r['sequence'])+2]
            need(len(members)==(1 if int(r['frame'])<3108 else 2), 'Every actually tracked raw address has its boundary membership')
            for m in members:
                a=int(m['actor'],16)
                need(m['kind'] in ('first','second') and a==({'first':0x01038c70,'second':0x01039ae0}[m['kind']]) and
                     m['subject']=='01034E90' and int(m['birth'])==({'first':3024,'second':3108}[m['kind']]) and
                     int(m['active'])==int(a in active) and int(m['free'])==int(a in sets['freeObjects']),
                     'Every tracked raw membership independently derived from complete actual native lists')
            expected_lists[tag,int(r['sequence'])]=sets
    need([int(r['frame']) for r in g['FIELD_LISTS']]==list(range(3024,3615)), 'All591 native fields through actual subsequent scene')
    for kind,birth in (('first',3024),('second',3108)):
        ms=[r for r in g['MEMBER'] if r['context']=='FIELD_LISTS' and r['kind']==kind]
        need([int(r['frame']) for r in ms]==list(range(birth,3615)), 'Continuous tracked raw-address field inventory')
        for r in ms:
            f=int(r['frame'])
            active=(f<3056 or 3097<=f<3403 or f>=3438) if kind=='first' else (f<3403 or f>=3438)
            need(int(r['active'])==int(active) and int(r['free'])==int(not active), 'Source-bound retirement/reset/reuse membership timeline')
            if kind=='second' and 3403<=f<3438:
                need(r['descriptor']=='FFC07500' and r['bulkReset']=='3403' and r['reused']=='-1',
                     'Free stale descriptor is quarantined until actual native allocation, never a live victim')
            if kind=='first' and 3097<=f<3403:
                need(r['descriptor']=='FFC09580', 'First retired address earlier reused for a distinct native effect')
    enter,done=g['RESET_ENTER'][0],g['RESET_COMPLETE'][0]
    for r,entry,opcode in ((enter,0xff83f060,0x5600),(done,0xff83f200,0x0960)):
        need(int(r['frame'])==3403 and int(r['entry'],16)==entry and int(r['pc'],16)==entry+16 and
             int(r['opcode'],16)==opcode and r['mask']=='FFFF' and
             int(r['opcode'],16)==int.from_bytes(guest[(entry-0xff800000)//8:(entry-0xff800000)//8+2],'little'),
             'Actual executing original bulk-reset entry and completion opcodes')
    need(int(enter['sequence'])<int(done['sequence']) and done['freeHead']==f'{FIRST:08X}' and done['a1']==f'{END:08X}',
         'Executing native pool reset starts at first record and terminates exactly at exclusive pool end')
    full=g['RESET_COMPLETE_LISTS'][0]
    need(full['objects']==full['layer1']==full['layer2']=='-' and full['freeObjectsStop']==f'{END:08X}' and
         [int(v,16) for v in full['freeObjects'].split(',')]==list(range(FIRST,END,STRIDE)),
         'Actual bulk reset clears all render lists and returns every358 original sprite in exact native order')
    for r,kind,actor in zip(g['REUSE'],('first','second'),(0x01038c70,0x01039ae0),strict=True):
        need(r['kind']==kind and int(r['frame'])==3438 and r['entry']=='FF809150' and r['pc']=='FF809160' and
             r['opcode']=='5642' and r['mask']=='FFFF' and int(r['actor'],16)==int(r['a0'],16)==actor and
             r['head']==r['next']==r['a2']==f'{actor+STRIDE:08X}',
             'Actual original native free-head pop consumes tracked address before zeroing/reinitializing it')
    return dict(nativeBulkResetFrame=3403,nativePoolRecordsReturned=COUNT,secondVictimActiveUntil=3402,
        secondVictimFreeFields=35,secondAddressActuallyReallocatedFrame=3438,firstRetiredFrame=3056,
        firstEarlierDistinctEffectReuseFrame=3097,continuousNativeListFields=591,trackedAddressMemberships=1106,
        secondRawCleanupAccepted=True,allOriginalPoolRecordsReturned=True,noDeathObjectPersistsThroughNextScene=True,
        allVictimArtAndFullPixelGeometryAccepted=False)


def execute(state):
    need(not OUT.exists(),'Immutable actual native raw pool qualification')
    parent=json.loads((previous.OUT/'report.json').read_text());pmodel=json.loads((projection.OUT/'report.json').read_text())
    transport=json.loads((capture.OUT/'report.json').read_text())
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());oldfolder,oldtext,oldimages=previous.capture.RAM_CASES[previous.capture.KEY]
    oldmeta=json.loads((oldfolder/'result.json').read_text())
    need(parent['passed'] and pmodel['passed'] and transport['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==transport['actualNativeIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==(38516,38752,1791759731.6919804),
         'Exact original terminal native38516 and complete source-qualified parents')
    pins=dict(transport['inputHashes'])
    for p,d in pmodel['inputHashes'].items():need(p not in pins or pins[p]==d,'No historical source input replaced');pins[p]=d
    def retained(value):return [s for s in value.splitlines() if s.startswith('MK2_') and
        not s.startswith((PREFIX,'MK2_DEATH_RAW_RESULT ','MK2_HPHASE_RGB_DIGEST '))]
    old,new=retained(oldtext),retained(text)
    need(old==new,'Entire old native physical/state/HP/audio/RAW/FIFO records identical, excluding only changed observer tap-count result')
    raw={k:previous.rows(text,previous.TAG+k) for k in ('CONSTRUCT','FIELD','CANDIDATE','QUEUE','REMOVE','RESULT')}
    need(raw['RESULT'][0]['taps']=='9' and raw['RESULT'][0]['sequence']=='1479' and raw['RESULT'][0]['objects']=='2',
         'Only original terminal observer tap count changes6->9, all other results remain bound')
    positive=gate(data(text),state['guest']);projection_positive=projection.gate(raw)
    g=data(text);faults=[]
    cases=[('reset_opcode','RESET_COMPLETE',0,'opcode','0961'),('reset_completion_end','RESET_COMPLETE',0,'a1','0105B960'),
        ('allocation_actor','REUSE',1,'a0','01034E90'),('allocation_head','REUSE',1,'head','01039CE0'),
        ('stale_death_marked_active','MEMBER',next(i for i,r in enumerate(g['MEMBER']) if r['kind']=='second' and r['frame']=='3403' and r['context']=='FIELD_LISTS'),'active','1'),
        ('free_pool_count','RESET_COMPLETE_LISTS',0,'freeObjectsCount','357'),('pool_sentinel','RESET_COMPLETE_LISTS',0,'freeObjectsStop','00000000'),
        ('first_reuse_frame','REUSE',0,'frame','3437'),('continuous_field_gap','FIELD_LISTS',20,'frame','3045')]
    for name,tag,i,key,value in cases:
        bad=copy.deepcopy(g);need(bad[tag][i][key]!=value,'Effective native pool corruption');bad[tag][i][key]=value
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError) as error:faults.append(dict(name=name,rejectedBy=str(error)))
        else:raise ValueError('Actual native pool corruption admitted '+name)
    need(gate(g,state['guest'])==positive and len(faults)==9,'All nine effective pool faults reject, complete positive restored')
    rasters=previous.checkpoint.scope['original'].rasters.rasters(images,meta['actualScenes'])
    need(len(rasters)==67 and meta['actualScenes']==oldmeta['actualScenes'] and
         all(images[r['imageKey']].tobytes()==oldimages[r['imageKey']].tobytes() for r in oldmeta['actualScenes']),
         'All67 original native RGB pixels/header identities unchanged; previous actual view proof retained by whole equality')
    audio,oldaudio=capture.AUDIO[capture.KEY],previous.capture.AUDIO[previous.capture.KEY]
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom','expectedROM','audioGuestObserved'):
        need(audio[key]==oldaudio[key],'Every entire actual native audio byte/header/source clock/ROM unchanged')
    for p in (Path(__file__),previous.OUT/'report.json',projection.OUT/'report.json',capture.OUT/'report.json',
              *(p for p in folder.rglob('*') if p.is_file())):
        p=str(p.resolve());d=sha(p);need(p not in pins or pins[p]==d,'Immutable actual native pool inputs');pins[p]=d
    need(all(sha(p)==d for p,d in pins.items()),'Entire current source/native/evidence hash inventory')
    value=dict(passed=True,actualNativeIdentity=held['identity'],nativeRawPool=positive,rawProjection=projection_positive,
        actualPoolFaultsRejected=faults,wholeOriginalNativeRecordsIdentical=len(old),whole67OriginalRGBFramesIdentical=True,
        wholePCM_DAC_ROMBytesAndHeadersIdentical=True,previousActualViewsRetainedByWholePixels=True,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],inputHashes=pins,goalStatus='active',
        fullPortAcceptance=False,fullRawPixelPenScanoutAcceptance=False,publicPlayableChanged=False,
        newNativeGamesDuringQualification=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual bulk sprite reset/free-list/reuse with nine faults, original raw projection and whole records/RGB/audio equality',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve exact native pool rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
