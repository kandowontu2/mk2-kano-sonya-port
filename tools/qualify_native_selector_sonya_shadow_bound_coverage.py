"""Actual complete drawing admission and bicycle masked horizontal-store replay.

This qualifies observer coverage and finite native write provenance, not full
shadow geometry, audio waveform, all-contact choreography, or the entire port.
"""
import copy
import hashlib
import json
import re
import struct
from pathlib import Path
import capture_native_selector_sonya_choice_shadow_bound_loader as capture
import qualify_native_selector_sonya_choice_av_checkpoint as prior
import qualify_native_selector_sonya_choice_av_observed_bound as phases

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_bound_coverage_checked'


def gate(text,guest):
    ledger=prior.capture.choices.native_state
    whole=ledger.gate(text,guest)
    choices=prior.capture.choices.choices_gate(text,guest,whole['schedule'])
    physical=ledger.original.rounds.rows(text,'FIELD')
    by={(r['frame'],r['slot']):r for r in physical}
    expected=set()
    for f in range(1818,3618):
        a,b=by[f,1],by[f,2]
        if (a['mode']==b['mode']==2 and a['states']==b['states']=='1,0' and a['valid']==b['valid']==1 and
            a['id']==17 and b['id']==18 and a['owner']==a['actor'] and b['owner']==b['actor']):expected.add(f)
    rows=ledger.rows(text,'MK2_HPHASE_POST_FIELD')
    posts={(int(r['frame']),int(r['slot'])):r for r in rows}
    need(len(posts)==len(rows)==3034 and set(posts)=={(f,s) for f in expected for s in (1,2)},
         'Every independently expected actual draw-complete frame, no zero/partial coverage pass')
    numeric_hex={'actor','main','owner','vx','vy','gravity','flags','body','trail'}
    for (f,s),r in posts.items():
        target=by[f+1,s]
        need(r['writes']=='0' and r['assistance']=='none' and
             all(int(r[k],16 if k in numeric_hex else 10)==target[k]
                 for k in ('actor','main','owner','id','action','y','floor','vx','vy','gravity','flags','body','trail','hp','mode')) and
             int(r['roster'])==(17 if s==1 else 18) and int(r['state'])==(1 if s==1 else 0),
             'Every actual draw-complete word agrees with independent next pre-field')
        need(int(r['floor'])==82-(s-1),'Actual per-character floors, not shared Kano-only height')
    begins=ledger.rows(text,'MK2_HPHASE_SHADOW_BEGIN')
    bk={(int(r['frame']),int(r['slot'])):r for r in begins}
    need(len(bk)==len(begins)==len(posts) and set(bk)==set(posts),'Every admitted owned native shadow call')
    for key,r in bk.items():
        need(all(r[k]==posts[key][k] for k in ('actor','main','owner','id','pose','body')) and
             r['pc']=='FF801080' and r['mask']=='FFFF','Actual executing shadow eligibility and final own pose')
    binds=ledger.rows(text,'MK2_SONYA_SHADOW_BIND')
    need(binds==[dict(count='1',human='17',cpu='18',writes='0',assistance='none')],
         'Actual explicit environment interceptor executed once, not inferred from source')
    entries=ledger.rows(text,'MK2_HPHASE_CPU_NATIVE_ENTRY')
    routines=dict(ring=0xffffb400,square=0xffffca00,bicycle=0xfff9a400,leg=0xfff80800)
    need(len(entries)==10 and {r['kind'] for r in entries}==set(routines),'All actual later Sonya move entry kinds')
    for r in entries:
        at=routines[r['kind']]
        need(int(r['entry'],16)==at and int(r['pc'],16)==at+16 and int(r['opcode'],16)==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0] and
             r['mask']=='FFFF' and r['actor']==r['owner']=='010350A0' and r['main']=='0106BF30' and r['id']==r['roster']=='18' and
             r['state']=='0' and int(r['frame']) in expected,'Real owned native move entry, opcode and drawing context')
    return dict(passed=True,wholeNativeHealthState=whole,actualChoices=choices,expectedDrawingFrames=len(expected),
                actualDrawingFields=len(posts),actualOwnedShadowCalls=len(begins),actualCPUEntries=len(entries),
                wholeShadowGeometryAccepted=False,fullPortAcceptance=False)


def horizontal(text,guest):
    ledger=prior.capture.choices.native_state
    fields=prior.phase_source.bicycle.state.original.rows(text,'FIELD')
    by={r['frame']:r for r in fields}
    rows=[r for r in ledger.rows(text,'MK2_SONYA_HORIZONTAL_STORE') if r['slot']=='2' and 3191<=int(r['frame'])<=3252]
    need(rows,'Whole actual bicycle horizontal-write inventory')
    signatures={0xff8040b0:(0xff804090,(0x0983,0x00c0)),
                0xff805630:(0xff805610,(0xb062,0x0090)),
                0xff805580:(0xff805560,(0xb282,0x0040)),
                0xff8285b0:(0xff828590,(0xb2e9,0x0040))}
    # The two original move/update stores below are bound to whole current cold
    # source as well; record their complete surrounding instruction bytes.
    sources={}
    for pc in sorted({int(r['pc'],16) for r in rows}):
        offset=(pc-128-0xff800000)//8
        sources[f'{pc:08X}']=guest[offset:offset+16].hex().upper()
        if pc in signatures:
            at,words=signatures[pc]
            need(struct.unpack_from('<2H',guest,(at-0xff800000)//8)==words,'Whole actual native store instruction signature')
    need(set(sources)=={'FF8040B0','FF805630','FF83CCD0','FF805580','FF80F700','FF8285B0'},'Exact original horizontal store sites')
    count=0;boundary=[]
    for f in range(3191,3253):
        values={'x':by[f]['xraw'],'vx':by[f]['vx']}
        for r in (r for r in rows if int(r['frame'])==f):
            kind=r['kind'];at=int(r['at'],16);offset=0x80 if kind=='x' else 0x40
            bit=at-(0x010350a0+offset)
            need(kind in ('x','vx') and bit in (0,16) and r['actor']==r['owner']=='010350A0' and r['main']=='0106BF30' and
                 r['id']=='18' and r['action']==('0303' if f==3191 else '0204' if f<3211 else '0611') and
                 r['writes']=='0' and r['assistance']=='none','Each actual native word-store address and bicycle owner')
            need(int(r['before'],16)&65535==(values[kind]>>bit)&65535 and
                 int(r['xraw'],16)==values['x'] and int(r['vx'],16)==values['vx'],
                 'Every pre-store native word, including high-half writes, agrees with replay')
            mask=int(r['mask'],16);data=int(r['data'],16)
            need(mask==65535 and data<=65535,'Exact native16-bit callback writes, no invented merged32-bit event')
            values[kind]=(values[kind]&~(mask<<bit))|((data&mask)<<bit)
            count+=1
            if r['pc']=='FF805630':
                need(kind=='x' and bit==16 and r['a2']==r['actor'] and r['a0']==r['a3']=='0000003C' and
                     data==int(r['left'])==60 and r['a4']=='00000000' and values['x']&65535==32768,
                     'Actually executing stock left-boundary clamp preserves fractional coordinate')
                boundary.append(f)
        need(values==dict(x=by[f+1]['xraw'],vx=by[f+1]['vx']),
             'All actual native masked x/vx stores exactly explain next complete field')
    need(boundary and boundary[0]==3232,'Original failing edge now directly traced, not waived')
    return dict(passed=True,first=3191,last=3252,sourceBoundMaskedStores=count,
                actualNativeClampFrames=boundary,nativeInstructionWindows=sources,
                allHorizontalFieldsExplainedByNativeStores=True,allStoreOperandRegistersCaptured=False,
                wholeBicycleContactsAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable native coverage/store qualification')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY];report=json.loads((folder/'result.json').read_text())
    need(report['passed'] and held['process'].poll()==report['nativeExit']==0 and held['identity']==report['nativeTerminal']['actualWindowsIdentity'] and
         held['identity']['ProcessId']==44988 and held['identity']['createdUnix']==1791753882.5997791,'Original corrected capture terminal, no replay')
    OUT.mkdir()
    try:
        positive=gate(text,state['guest']);movement=horizontal(text,state['guest'])
        raster=prior.raster_model.rasters(images,report['actualScenes'])
        pins=dict(report['inputHashes'])
        for p in (Path(__file__),Path(prior.__file__),Path(phases.__file__),Path(capture.__file__),
                  *(p for p in folder.rglob('*') if p.is_file())):
            key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No historical pin changed');pins[key]=h
        need(all(sha(p)==h for p,h in pins.items()),'All actual current sources/evidence unchanged')
        value=dict(passed=True,actualNativeIdentity=held['identity'],coverage=positive,horizontal=movement,
                   wholeOriginalRasterDigests=raster,inputHashes=pins,wholeShadowGeometryAccepted=False,
                   waveformAccepted=False,fullPortAcceptance=False,faultQualificationPending=True,
                   goalStatus='active',requirements=json.loads(capture.PARENT.read_text())['requirements'] if hasattr(capture,'PARENT') else
                       json.loads(capture.previous.PARENT.read_text())['requirements'],
                   newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
        prior.capture.choices.current.prior.save(OUT/'report.json',value)
        print('PASS every actual drawing admission and full masked bicycle horizontal-store replay; full geometry/operand faults/audio open',flush=True)
        return value
    except Exception as error:
        prior.capture.choices.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),fullPortAcceptance=False,newNativeGames=0))
        raise
