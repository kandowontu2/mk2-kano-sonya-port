"""Original raw-object camera/clip/flip/FIFO equations, not pixel-pen proof.

TMS34010 ADDXY/SUBXY operate on signed packed sixteen-bit coordinates.
The original FF8042A0..FF804410 uses inclusive clip boundaries and separate
display-origin/flip additions. Native47752 already captured every candidate,
including rejected candidates: do not derive coverage from queues alone.
"""
import copy
import json
import traceback
from pathlib import Path
import qualify_native_selector_sonya_death_raw_sequence as parent

ROOT,need,sha=parent.ROOT,parent.need,parent.sha
OUT=ROOT/'audit_native_selector_sonya_death_raw_projection_checked'


def signed(value):
    value&=65535
    return value-65536 if value&32768 else value


def xy(value):return signed(value),signed(value>>16)


def packed(x,y):return (x&65535)|((y&65535)<<16)


def gate(groups):
    candidates=[r for r in groups['CANDIDATE'] if r['kind']=='first' or int(r['frame'])<3438]
    queues=[r for r in groups['QUEUE'] if r['kind']=='first' or int(r['frame'])<3438]
    qkeys={(r['kind'],r['frame']):r for r in queues}
    need(len(qkeys)==len(queues),'Unique complete raw native FIFO fields')
    expected=set();flips=0
    for r in candidates:
        h=lambda k:int(r[k],16)
        x,y=xy(h('a10'));cx,cy=xy(h('a4'))
        need(h('a10')==packed((h('xraw')>>16)-cx,(h('yraw')>>16)-cy),
             'Every native raw candidate is exact physical integer position minus original camera')
        width,height=xy(h('a9'));lowx,lowy=xy(h('a14'));highx,highy=xy(h('a13'))
        need(width>0 and height>0 and (lowx,lowy,highx,highy)==(0,0,400,254),
             'Original positive packed descriptor size and full native raw clip rectangle')
        visible=signed(x+width)>=lowx and signed(y+height)>=lowy and x<=highx and y<=highy
        key=r['kind'],r['frame']
        if not visible:continue
        expected.add(key);q=qkeys.get(key)
        need(q is not None,'Every original source-predicted visible raw candidate is queued')
        command=h('a12');dx=width-1 if command&(1<<20) else 0;dy=height-1 if command&(1<<21) else 0
        ox,oy=xy(h('a5'))
        need(int(q['a10'],16)==packed(x+dx+ox,y+dy+oy) and q['a2']==f'{packed(dx,dy):08X}',
             'Exact original raw flip-anchor plus packed native display origin at FIFO')
        flips+=bool(dx or dy)
    need(set(qkeys)==expected,'No rejected native raw candidate silently reaches FIFO')
    return dict(actualRawCandidates=len(candidates),actualRawQueues=len(queues),actualRawClipRejects=len(candidates)-len(queues),
        flippedQueuedFields=flips,everyPhysicalCameraProjectionExact=True,everyNativeClipDecisionExact=True,
        everyFlipDisplayAnchorExact=True,packedPixelsAndFinalScanoutAccepted=False)


def execute(state):
    need(not OUT.exists(),'Immutable original raw projection gate')
    report=json.loads((parent.OUT/'report.json').read_text());need(report['passed'],'Whole source-qualified actual raw sequence')
    folder,text,_=parent.capture.RAM_CASES[parent.capture.KEY]
    need(parent.capture.NATIVE_HANDLES[parent.capture.KEY]['process'].poll()==0,'Same original47752 genuinely terminal')
    groups={k:parent.rows(text,parent.TAG+k) for k in ('CANDIDATE','QUEUE')}
    positive=gate(groups);faults=[]
    for label,tag,key,value in (('camera','CANDIDATE','a4','FFFE0059'),('physical_x','CANDIDATE','xraw','013F0000'),
        ('candidate_x','CANDIDATE','a10','00BA00E7'),('clip_high','CANDIDATE','a13','00FE0191'),
        ('clip_low','CANDIDATE','a14','00000001'),('display_origin','CANDIDATE','a5','00000039'),
        ('flip_bit','CANDIDATE','a12','E9920000'),('queue_anchor','QUEUE','a10','00BA011F')):
        bad=copy.deepcopy(groups);need(bad[tag][0][key]!=value,'Effective raw projection fault');bad[tag][0][key]=value
        try:gate(bad)
        except (ValueError,AssertionError) as error:faults.append(dict(name=label,rejectedBy=str(error)))
        else:raise ValueError('Raw projection fault admitted '+label)
    need(len(faults)==8 and gate(groups)==positive,'Whole raw projection positive restored after eight effective faults')
    pins=dict(report['inputHashes'])
    for p in (Path(__file__),parent.OUT/'report.json',ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'):
        p=str(p.resolve());digest=sha(p);need(p not in pins or pins[p]==digest,'Unchanged raw projection source');pins[p]=digest
    need(all(sha(p)==d for p,d in pins.items()),'All full raw projection input hashes')
    result=dict(passed=True,actualNativeIdentity=report['actualNativeIdentity'],rawProjection=positive,actualProjectionFaultsRejected=faults,
        inputHashes=pins,goalStatus='active',requirements=report['requirements'],remainingGroups=report['remainingGroups'],
        fullPortAcceptance=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS original raw camera/clip/flip/display FIFO with eight effective faults',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve exact raw projection rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
