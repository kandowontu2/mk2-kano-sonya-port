"""Actual11004 floor writes/body-skip instructions and six late native views.

Entire270532 original native records,30 original rasters and every whole
PCM/DAC/ROM byte/header compare exactly to38692. Extra observation does not
broaden finite geometry/audio scope. Raw replacement-object retirement is
still unobserved; the pool observer captured only actors with nonzero poses.
"""
import copy
import hashlib
import json
import re
import struct
import traceback
from collections import Counter
from pathlib import Path
import capture_native_selector_sonya_throw_late_views as capture
import qualify_native_selector_opposite_roles_checkpoint as original

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_throw_late_checkpoint_checked'
VIEWS=ROOT/'audit_native_selector_sonya_throw_late_actual_views.json'
GEOMETRY=capture.PARENT
AUDIO=ROOT/'audit_native_selector_opposite_roles_winner_pcm_checked/report.json'
rowset=original.rows


def native_gate(text,guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for start,stop in ((0xffa0dc60,0xffa0de70),(0xff838f60,0xff839090),
        (0xff804000,0xff8045d0),(0xff9054d0,0xff905930),(0xff83a070,0xff83a120)):
        lo,hi=(start-0xff800000)//8,(stop-0xff800000)//8
        need(guest[lo:hi]==stock[lo:hi],'Entire original actual reset/floor/hide/renderer branch source')
    bind=rowset(text,'MK2_LATE_THROW_BIND')
    need(len(bind)==2 and {int(r['slot']) for r in bind}=={1,2},'Both actual Main/actor passive tap bindings')
    owners={int(r['slot']):(int(r['actor'],16),int(r['main'],16)) for r in bind}
    for r in bind:
        a,m=owners[int(r['slot'])]
        need(int(r['floorAt'],16)==m+0x200 and int(r['bodyAt'],16)==a+0x160 and
             r['writes']=='0' and r['assistance']=='none','Each exact passive Main floor/body tap target')
    floor=rowset(text,'MK2_LATE_THROW_FLOOR_STORE')
    timeline=[(2433,1,81,81,0xff905590),(2433,1,81,0,0xff83a100),
        (2433,1,0,0,0xff83a100),(2433,1,0,81,0xff905630),
        (2433,2,82,82,0xff905870),(2433,2,82,0,0xff83a100),
        (2433,2,0,0,0xff83a100),(2433,2,0,82,0xff9058f0),
        (2961,1,81,73,0xffa0dd40)]
    need(len(floor)==len(timeline),'Every actual floor write, including reset transient zero/no-op stores')
    for r,(f,s,before,after,pc) in zip(floor,timeline,strict=True):
        a,m=owners[s]
        need((int(r['frame']),int(r['slot']),int(r['before'],16),int(r['after'],16),int(r['pc'],16))==
             (f,s,before,after,pc) and int(r['actor'],16)==int(r['owner'],16)==a and
             int(r['main'],16)==m and int(r['at'],16)==m+0x200 and
             int(r['id'])==(18 if s==1 else 17) and int(r['mask'],16)==65535 and
             int(r['data'],16)==after and int(r['floor'])==before and
             r['writes']=='0' and r['assistance']=='none',
             'Exact native actual floor-write identity/address/mask/pre-value/data/timeline')
        need((int(r['op0'],16),int(r['op1'],16))==struct.unpack_from('<2H',guest,(pc-32-0xff800000)//8),
             'Actual final instruction words at captured native floor-store PC')
    lowered=floor[-1];a,m=owners[1]
    need(lowered['op0']=='B00D' and lowered['op1']=='0200' and
         int(lowered['a0'],16)==73 and int(lowered['a8'],16)==a and int(lowered['a13'],16)==m,
         'Actually executing source-bound A0-to-Main floor store at FFA0DD20, not inferred alone')
    body=rowset(text,'MK2_LATE_THROW_BODY_STORE')
    need(len(body)==138,'Whole captured native body-write inventory')
    for r in body:
        s=int(r['slot']);a,m=owners[s]
        before,data,mask,after=(int(r[k],16) for k in ('before','data','mask','after'))
        need(int(r['actor'],16)==int(r['owner'],16)==a and int(r['main'],16)==m and
             int(r['at'],16)==a+0x160 and int(r['id'])==(18 if s==1 else 17) and mask==65535 and
             after==(before&(~mask&65535))|(data&mask) and int(r['body'],16)==before and
             r['writes']=='0' and r['assistance']=='none','Every passive actual body write and full masked result')
    hides=[r for r in body if r['frame']=='3028' and r['slot']=='1']
    need(len(hides)==1,'One actual final true Sonya body handoff')
    hide=hides[0]
    need((hide['before'],hide['after'],hide['pc'],hide['op0'],hide['op1'])==
         ('0016','0026','FF839090','B080','0160') and int(hide['a0'],16)==a and
         int(hide['a4'],16)==0x26 and hide['a7']=='FFA0E2B0',
         'Actual original hide branch/register result/uppercut-death continuation')
    skips=rowset(text,'MK2_LATE_THROW_BODY_SKIP_TEST')
    need(len(skips)==15840 and Counter(int(r['frame']) for r in skips)=={f:198 for f in range(3029,3109)},
         'All80 actual body-skip fields and all198 executing skip tests per field')
    for r in skips:
        need(r['slot']=='1' and (int(r['actor'],16),int(r['main'],16))==owners[1] and
             int(r['owner'],16)==a and int(r['a0'],16)==a and r['id']=='18' and
             (r['at'],r['pc'],r['opcode'],r['mask'],r['op0'],r['op1'])==
             ('FF804190','FF8041A0','1F47','FFFF','CA11','1F47') and
             int(r['a7'],16)==int(r['body'],16)==0x26 and r['pose']=='FF033840' and
             r['floor']=='73' and r['writes']=='0' and r['assistance']=='none',
             'Every actually executing native multipart skip test and true victim register/flag source')
    return dict(passed=True,actualNativeFloorWrites=floor,actualNativeBodyWrites=len(body),
        actualHideStore=hide,actualMultipartSkipTests=len(skips),actualSkipFrames=80,
        sourceFloorStoreInstructionNowObserved=True,sourceRendererSkipInstructionNowObserved=True,
        resetTransientFloorZeroStoresObserved=True,replacementActorAtHandoff=int(hide['a9'],16),
        replacementObjectGeometryOrRetirementAccepted=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual late-observation checkpoint')
    geometry=json.loads(GEOMETRY.read_text());audio=json.loads(AUDIO.read_text())
    transport=json.loads((capture.OUT/'report.json').read_text())
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    parent=capture.parent
    old_folder,old_text,old_images=parent.RAM_CASES[parent.KEY]
    old_meta=json.loads((old_folder/'result.json').read_text())
    old_held=parent.NATIVE_HANDLES[parent.KEY]
    need(geometry['passed'] and audio['passed'] and transport['passed'] and meta['passed'] and
         held['process'].poll()==meta['nativeExit']==0 and old_held['process'].poll()==old_meta['nativeExit']==0 and
         held['identity']==transport['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (11004,38752,1791757518.8894863) and geometry['actualNativeIdentity']==audio['actualNativeIdentity']==old_held['identity'],
         'Both original exact terminal native handles and independent source-qualified parents')
    pins=dict(transport['inputHashes'])
    for parent_pins in (geometry['inputHashes'],audio['inputHashes']):
        for path,digest in parent_pins.items():
            need(path not in pins or pins[path]==digest,'No historical source input silently replaced');pins[path]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Entire current source/evidence inventory')
    def existing(value):
        return [s for s in value.splitlines() if s.startswith('MK2_') and
            not s.startswith(('MK2_LATE_THROW_','MK2_HPHASE_RGB_DIGEST '))]
    old=existing(old_text);new=existing(text)
    need(len(old)==270532 and new==old,'Every entire original native record unchanged by additional passive observers')
    ledger=original.gate(text,state['guest']);positive=native_gate(text,state['guest'])
    faults=[]
    def corruption(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
            all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Effective actual observer corruption')
        return text.replace(line,changed,1)
    trials=[('floor_result',corruption('MK2_LATE_THROW_FLOOR_STORE','after','004A',frame=2961)),
        ('floor_target',corruption('MK2_LATE_THROW_FLOOR_STORE','at','0106BA50',frame=2961)),
        ('floor_mask',corruption('MK2_LATE_THROW_FLOOR_STORE','mask','FFFE',frame=2961)),
        ('floor_store_register',corruption('MK2_LATE_THROW_FLOOR_STORE','a0','00000048',frame=2961)),
        ('reset_transient_zero',corruption('MK2_LATE_THROW_FLOOR_STORE','after','0051',frame=2433,slot=1,before='0051',after='0000')),
        ('hide_result',corruption('MK2_LATE_THROW_BODY_STORE','after','0016',frame=3028,slot=1)),
        ('hide_result_register',corruption('MK2_LATE_THROW_BODY_STORE','a4','00000016',frame=3028,slot=1)),
        ('skip_register',corruption('MK2_LATE_THROW_BODY_SKIP_TEST','a7','00000016',frame=3029)),
        ('skip_opcode',corruption('MK2_LATE_THROW_BODY_SKIP_TEST','opcode','1F46',frame=3029)),
        ('skip_owner',corruption('MK2_LATE_THROW_BODY_SKIP_TEST','owner','010350A0',frame=3029))]
    for label,bad in trials:
        try:native_gate(bad,state['guest'])
        except (ValueError,AssertionError) as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual direct instruction/store corruption admitted '+label)
    need(len(faults)==10 and native_gate(text,state['guest'])==positive,'All10 actual observation faults reject and positive restored')
    rasters=original.rasters.rasters(images,meta['actualScenes'])
    need(len(rasters)==42 and meta['actualScenes'][:30]==old_meta['actualScenes'] and
         all(images[r['imageKey']].tobytes()==old_images[r['imageKey']].tobytes() for r in old_meta['actualScenes']),
         'All42 whole native pixel digests and every original30 raster unchanged')
    views=json.loads(VIEWS.read_text())
    host=next(r for r in original.identity.census_hosts() if r['ProcessId']==38752)
    need(views['passed'] and views['actualNativeIdentity']==held['identity'] and views['actualHostIdentity']==host and
         views['originalIdentityRevalidatedBeforeAndAfter'] and
         [r['index'] for r in views['actualViewedCallbacks']]==[30,34,35,36,37,41],
         'All six actually reviewed late native rasters and exact retained host')
    for r in views['actualViewedCallbacks']:
        actual=rasters[r['index']]
        need(r['header']==actual['header'] and r['SHA256']==actual['header']['sha256'] and
             r['nativeRGBSHA256']==actual['nativeRGBSHA256'] and
             r['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],
             'Every actual visual observation binds whole original native pixels')
    new_audio=capture.AUDIO[capture.KEY];old_audio=parent.AUDIO[parent.KEY]
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom','expectedROM','audioGuestObserved'):
        need(new_audio[key]==old_audio[key],'Every complete actual audio byte/header/source clock/ROM equals source-qualified original')
    need(len(new_audio['pcmChunks'])==len(new_audio['dacChunks'])==1645 and
         all(len(raw)==12582912 for raw in new_audio['rom'].values()),'Whole complete current PCM/DAC and both sound ROMs')
    for path in (Path(__file__),Path(capture.__file__),capture.LUA,GEOMETRY,AUDIO,VIEWS,capture.OUT/'report.json',
        ROOT/'tools/read_native_selector_sonya_throw_late_frames.py',ROOT/'tools/read_native_selector_sonya_throw_late_frames_remote.py',
        *(p for p in folder.rglob('*') if p.is_file())):
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No frozen source or evidence replaced');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Entire exact input inventory after faults and comparison')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],actualHostIdentity=host,
        wholeNativeHealthStateChoices=ledger,directNativeFloorBodySkipInstructions=positive,actualObserverFaultsRejected=faults,
        unchangedOriginalNativeRecords=len(old),unchangedOriginalRGBCallbacks=30,wholeOriginalRasters=rasters,
        actualReviewedLateViews=views,completeStereoFrames=1645*960,
        wholePCM_SHA256=hashlib.sha256(b''.join(new_audio['pcmChunks'])).hexdigest().upper(),
        wholePCM_DAC_ROMBytesAndHeadersIdenticalToSourceQualified38692=True,
        sourceWaveformModelByEntireInputOutputEquality=True,waveformFaultsRerunOn11004=False,
        finiteMainActorGeometryByEntireRecordAndCodeEquality=True,geometryFaultsRerunOn11004=False,
        sourceQualifiedGeometryReportSHA256=sha(GEOMETRY),sourceQualifiedAudioReportSHA256=sha(AUDIO),
        replacementBodyPresentAtHandoff=True,replacementObjectRetirementAccepted=False,
        poolObserverMissesZeroPoseRawObjects=True,fullVictimArtAcceptance=False,fullPortAcceptance=False,
        requirements=geometry['requirements'],remainingGroups=geometry['remainingGroups'],inputHashes=pins,
        publicPlayableChanged=False,newNativeGamesThisCapture=1,newNativeGamesDuringQualification=0,
        newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();capture.parent.previous.choices.current.prior.save(OUT/'report.json',value)
    print('PASS same11004 actual floor-store/skip instructions,six late views,whole270532-record/30RGB/PCM-DAC-ROM equivalence with10 faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual checkpoint failure')
        OUT.mkdir();capture.parent.previous.choices.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False))
        raise
