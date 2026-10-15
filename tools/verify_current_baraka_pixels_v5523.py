"""Exact current fourteen-phase Baraka head/body pixels and native foreground.

Original1014 complete physical contract is separate and retained. Reconstruct
every native source byte, dispatch and actual display flip; no fuzzy match,
best-field search, proxies, state writes or ignored blood/foreground pixels.
"""
import concurrent.futures,datetime,inspect,json,re,struct,traceback
from pathlib import Path
from collections import defaultdict
import numpy as np
import current_baraka_source_contract_v5521 as model
import verify_current_cage_sections_v5509 as transport

ROOT,need,sha=model.ROOT,model.need,model.sha
PARENT=ROOT/'audit_v5520_current_cage_sections_qualified_progress/progress.json'
BASE=ROOT/'audit_v5524_current_baraka_pixels_ram'
OUT=ROOT/'audit_v5525_current_baraka_pixels_progress'
LUA=ROOT/'mk2ks_current_baraka_ram_v5522.lua'
COMPLETED=[]
digest=lambda raw:transport.model.original.assets.sha(raw)
save=transport.save


def rows(log,tag):
    return transport.rows(log.replace('MK2_CURRENT_BARAKA_SCENE_','MK2_CURRENT_CAGE_SCENE_'),tag)


def verify_pixels(log,images,buffers,gfx_streams,source_image,reference,fighter,guest,_faults=True):
    dmas=rows(log,'DMA');cutoffs=rows(log,'CUTOFF')
    need([d['serial']for d in dmas]==list(range(1,len(dmas)+1)),'Complete ordered native Baraka foreground ledger')
    records={}
    for key,(raw,r)in gfx_streams.items():
        first,offset=int(r['first']),int(r['offset'])
        need(offset//8==first and raw==source_image[first:first+len(raw)],'Every actual whole native head/body/blood/foreground graphics stream source-exact: '+key)
        records[key]=dict(offset=offset,data=raw.hex())
    replay=transport.raster.Replay(ROOT,defaultdict(list),records,{})
    replay.words=np.empty((512,512),np.uint16);replay.body=np.zeros((512,512),np.uint8)
    replay.shadow=np.zeros((512,512),bool);replay.projected=np.zeros((512,512),bool)
    native=model.original.records(log,'MK2_ROLLING_HEAD_V1003')
    action=next(r for tag,r in model.original.records(log,'MK2_STOCK_HEAD_V921')if tag=='ACTION')
    assets=reference['by_source'];identity=17 if fighter=='kano'else 18
    shots=[r for tag,r in native if tag=='POSE_SNAPSHOT'and int(r['source'],16)in assets]
    owned=[r for tag,r in native if tag=='DMA'and int(r['source'],16)in assets]
    need(len(shots)==14,'Every actually presented native head rotation and body collapse')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    results=[];faults=[];owners={}
    for shot in shots:
        filename=f"head_pose_{shot['actor_pose']}_{shot['frame']}.png"
        found=[r for r in cutoffs if r['filename']==filename];need(len(found)==1,'One exact native flip per owned head/body picture')
        cutoff=found[0];raw,vr=buffers[filename,'VRAM'];colors,meta=buffers[filename,'PALETTE']
        need(all(meta[k]==vr[k]for k in('filename','frame','age','flip_frame','start','control','tap','pc','mask'))and
             int(meta['frame'])==int(meta['flip_frame'])==cutoff['frame']and meta['pc']=='FF8168E0'and meta['mask']=='FFFF',
             'Actual native framebuffer/palette/display-start association')
        image=images[filename]
        scan=transport.display.check_latch(image,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16))
        source=int(shot['source'],16);asset=assets[source]
        candidates=[d for d in owned if int(d['frame'])<=cutoff['frame']and int(d['source'],16)==source and
                    (int(d['y'])>>8)==(scan['row']>>8)]
        need(candidates,'Actual front-page owned head/body dispatch exists')
        latest=max(int(d['frame'])for d in candidates);selected=[d for d in candidates if int(d['frame'])==latest]
        need(len(selected)==1 and cutoff['frame']-latest in(0,1),'Actual latest native component; no frame/location search')
        original=selected[0]
        fields={'source':16,'command':16,'palette':16,'x':10,'y':10,'width':10,'height':10,'cursor':16}
        found=[d for d in dmas if d['frame']==latest and all(d[k]==int(original[k],base)for k,base in fields.items())]
        need(len(found)==1,'Own component exactly identified in the full ordered ledger')
        target=found[0]
        need(target['queue_match']==1 and target['queue_frame']==latest and target['id']==identity and
             target['actor']==int(original['fifo_actor'],16)and target['pose']==int(original['fifo_pose'],16)and
             tuple(asset['size'])==(target['width'],target['height']),
             'True native head/body FIFO identity/actor/descriptor/dimensions')
        replay.words.fill(65535);replay.dma(dict(target,slot=1));opaque=replay.words!=65535
        need(int(opaque.sum())>10,'Actual nonempty complete owned component silhouette')
        relevant=[d for d in dmas if target['serial']<=d['serial']<=cutoff['serial']]
        composed=np.full((512,512),65535,np.uint16);ownership=np.zeros((512,512),np.int32);foreground={}
        for d in relevant:
            replay.words.fill(65535);replay.dma(dict(d,slot=1));written=replay.words!=65535
            if d is not target and (written&opaque).any():
                need(d['queue_match']==1 and d['queue_frame']==d['frame']and d['command']&15==2 and d['pc']==0xff804640,
                     'Each actual own-component occluder uses the original native FIFO/copy consumer: '+str(d))
                if d['source']in assets:
                    other=assets[d['source']]
                    need(other['fighter']==fighter and d['id']==identity and tuple(other['size'])==(d['width'],d['height'])and
                         d['palette']==d['bank']&0x7f00,'Occluding owned opposite head/body has true source/dimensions/identity/palette')
                    kind='own opposite head/body'
                elif d['palette']in(0x1c00,0x0400):
                    need(d['id']==d['pose']==d['body']==0 and d['bank']==(0x1c1c if d['palette']==0x1c00 else 0x0404)and
                         d['actor']!=target['actor']and d['actor']!=int(action['actor'],16)and
                         0xff800000<=d['cache']<=0xfffffff0 and d['cache']%8==0 and d['source']<0x0a000000,
                         'Actual original native blood/gore object type/palette/cache/source')
                    at=(d['cache']-0xff800000)//8
                    if d['palette']==0x1c00:
                        w,h,s,c=struct.unpack_from('<HHIH',guest,at);length=10
                    else:
                        w,h,dx,dy,s,c=struct.unpack_from('<HHhhIH',guest,at);length=14
                        pal_at=(0xffaf2a40-0xff800000)//8
                        need(guest[pal_at:pal_at+32]==stock[pal_at:pal_at+32]and struct.unpack_from('<H',stock,pal_at)[0]==15,
                             'Entire immutable native gore palette')
                        words=struct.unpack_from('<15H',stock,pal_at+2)
                        native_colors=[((((v>>10&31)<<3)|(v>>12&7))<<16)|((((v>>5&31)<<3)|(v>>7&7))<<8)|
                                       (((v&31)<<3)|(v>>2&7))for v in words]
                        need(list(struct.unpack('<32768I',colors)[0x401:0x40f])==native_colors[1:],'Every native gore RGB pen source-exact')
                    need(guest[at:at+length]==stock[at:at+length]and(w,h,s)==(d['width'],d['height'],d['source'])and
                         ((c&~0x30)|(d['command']&0x30)|0x8002)==d['command'],
                         'Every typed original native blood/gore source/dimension/format/flip word exact')
                    kind='source-ROM blood/gore'
                else:
                    need(d['id']==3 and d['actor']==int(action['actor'],16)and d['source']<0x0a000000,
                         'Other legitimate occluder is true original Baraka, never substituted victim art')
                    parts=transport.graphics.native_group(dict(pose=f"{d['pose']:08X}",facing=f"{d['command']&0x30:08X}"),b'',guest)
                    need(any((p['graphic'],p['width'],p['height'],p['command']|0x8002)==
                             (d['source'],d['width'],d['height'],d['command'])for p in parts),
                         'Actual stock Baraka pixels belong to its original native ROM pose')
                    kind='source-ROM Baraka'
                need(d['queue_size']==((d['height']<<16)|d['width'])and d['queue_command']>>16==d['command'],
                     'Every legitimate foreground object FIFO dimensions/command match actual hardware')
                foreground[d['serial']]=kind;owners.setdefault(kind,d['serial'])
            composed[written]=replay.words[written];ownership[written]=d['serial']
        actual=np.frombuffer(raw,'<u2').reshape(512,512);difference=int(np.count_nonzero(composed[opaque]!=actual[opaque]))
        need(difference==0,'Every complete native owned '+asset['kind']+' pose'+str(asset['pose'])+' pixel exact after source-owned foreground; differences='+str(difference))
        keep=opaque&(ownership==target['serial']);covered=opaque&~keep
        need(int(keep.sum())>10 and set(ownership[covered].tolist()).issubset(foreground),'Every covered original head/body pixel has a legitimate explicit native owner')
        yy,xx=np.where(opaque);row,col=scan['row'],scan['column']
        need(np.all((xx>=col)&(xx<col+400)&(yy>=row)&(yy<row+254)),'Entire emitted native head/body appears within actual scanout')
        words=np.frombuffer(colors,'<u4')[composed[opaque]&0x7fff]
        wanted=np.stack((words>>16&255,words>>8&255,words&255),axis=1).astype(np.uint8)
        need(np.array_equal(image[yy-row,xx-col],wanted),'Every source-owned head/body/foreground pixel has exact displayed hardware RGB')
        if _faults:
            def reject(label,check):
                try:check()
                except ValueError as error:faults.append(dict(kind=asset['kind'],pose=asset['pose'],label=label,rejectedBy=str(error)))
                else:raise ValueError('Accepted actual Baraka RAM counterexample: '+label)
            bad=composed.copy();bad[yy[0],xx[0]]^=1
            reject('one actual native component pen corrupted',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'All original component pens exact'))
            bad=image.copy();bad[yy[0]-row,xx[0]-col,0]^=1
            reject('one actual displayed component RGB corrupted',lambda:transport.display.check_latch(bad,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
            if covered.any():
                cy,cx=np.where(covered);bad=composed.copy();bad[cy[0],cx[0]]^=1
                reject('actual legitimate foreground omitted/corrupted',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'All actual native occlusion pens exact'))
        results.append(dict(filename=filename,kind=asset['kind'],pose=asset['pose'],frame=cutoff['frame'],age=cutoff['age'],nativeDMAFrame=latest,
          originalOpaquePixels=int(opaque.sum()),ownVisiblePixels=int(keep.sum()),ownedNativeOccludedPixels=int(covered.sum()),nativeOccluders=foreground,
          orderedDMAsThroughFlip=len(relevant),**scan))
    need({(r['kind'],r['pose'])for r in results}=={(k,p)for k in('head','body')for p in range(7)},'All seven source-owned head rotations and collapse poses')
    owner_faults=[]
    if _faults:
        for kind,serial in owners.items():
            d=next(d for d in dmas if d['serial']==serial)
            line=next(line for line in log.splitlines()if line.startswith('MK2_CURRENT_BARAKA_SCENE_DMA ')and f' serial={serial} 'in line)
            changed,n=re.subn(r' id=\d+ ',f" id={1 if d['id']!=1 else 0} ",line,count=1);need(n==1 and changed!=line,'Effective actual native foreground identity fault')
            try:verify_pixels(log.replace(line,changed,1),images,buffers,gfx_streams,source_image,reference,fighter,guest,False)
            except ValueError as error:owner_faults.append(dict(kind=kind,serial=serial,rejectedBy=str(error)))
            else:raise ValueError('Accepted full original native foreground identity counterexample')
    return dict(passed=True,parts=results,effectiveActualRAMFaults=faults,effectiveActualNativeForegroundOwnerFaults=owner_faults,
      wholeNativeScanoutPixels=sum(r['pixels']for r in results),sourceBoundNativeGFXStreams=len(records),
      everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact=True,continuousWholeSceneAndAllArtisticContextsAccepted=False)


def record_faults(log,result,guest,payload,reference,images,ram,contract):
    positive=contract(log,result,guest,payload,reference,images,ram);out=[]
    def reject(label,pattern,replacement,count=1):
        changed,n=re.subn(pattern,replacement,log,count=count,flags=re.M)
        need(n>=1 and (count==0 or n==1)and changed!=log,'Effective actual native-record fault: '+label)
        try:contract(changed,result,guest,payload,reference,images,ram)
        except ValueError as error:out.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Actual original Baraka counterexample accepted: '+label)
    reject('proxy victim',r'ids=3,(17|18)',r'ids=3,1')
    reject('non-native health writer',r'pc=FF836700',r'pc=FF838860')
    reject('native action missing',r'^MK2_STOCK_HEAD_V921_ACTION .*\n','')
    reject('native wrap missing',r'^MK2_STOCK_HEAD_V921_WRAP .*\n','')
    reject('original native Block hold missing',r'^MK2_STOCK_HEAD_V921_INPUT .*button=Block\n','',count=0)
    reject('actual High Punch missing',r'^MK2_STOCK_HEAD_V921_INPUT .*button=High_Punch\n','',count=0)
    for label,tag,key in(('foreign owner','QUEUE','owner'),('wrong victim main','QUEUE','main'),('foreign native ID','QUEUE','id'),('unbound FIFO','DMA','queue_match')):
        reject(label,r'(^MK2_ROLLING_HEAD_V1003_'+tag+r' .*source=0F6[0-9A-F]+ .*?'+key+r'=)[0-9A-F]+',r'\g<1>0')
    body=next(s for s,a in reference['by_source'].items()if a['fighter']==result['player']and a['kind']=='body')
    reject('floating actual body',r'(^MK2_ROLLING_HEAD_V1003_DMA .*source='+f'{body:08X}'+r' .*?y=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('wrong actual stage floor',r'(^MK2_ROLLING_HEAD_V1003_QUEUE .*source='+f'{body:08X}'+r' .*?stageY=)(-?\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('wrong native dimensions',r'(^MK2_ROLLING_HEAD_V1003_DMA .*source=0F6[0-9A-F]+ .*?width=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('native owned palette missing',r'^MK2_ROLLING_HEAD_V1003_PALETTE_DUMP .*\n','')
    reject('one genuine head/body snapshot missing',r'^MK2_ROLLING_HEAD_V1003_POSE_SNAPSHOT .*source=0F6[0-9A-F]+ .*\n','')
    need(contract(log,result,guest,payload,reference,images,ram)==positive,'Complete actual Baraka positive restored after native-record counterexamples')
    return out


source=inspect.getsource(transport.capture)
changes={
 'Cage victim context':'Baraka victim context',
 "MK2KS_STOCK_KILLER='cage',MK2KS_STOCK_COMMAND='ddff_lp'":"MK2KS_STOCK_KILLER='baraka',MK2KS_STOCK_COMMAND='bbbb_hp'",
 'MK2_CURRENT_CAGE_RAM_':'MK2_CURRENT_BARAKA_RAM_',
 "killer='cage',command='ddff_lp'":"killer='baraka',command='bbbb_hp'",
 'native_torso_gfx.bin':'native_death_gfx.bin',
 'source-PNG torso graphics exact':'source-PNG head/body graphics exact',
 'actualNativeSectionPixelsAndScanout':'actualNativeHeadBodyPixelsAndScanout',
 'all six complete native section scanouts':'all fourteen complete native head/body scanouts',
}
for before,after in changes.items():
    need(source.count(before)==1,'Whole native capture; only killer command/observer/owned GFX/result labels change: '+before)
    source=source.replace(before,after,1)
scope=dict(transport.__dict__,model=model,ROOT=ROOT,BASE=BASE,LUA=LUA,COMPLETED=COMPLETED,digest=digest,
           verify_pixels=verify_pixels,record_faults=record_faults,__file__=__file__)
exec(compile(source,__file__+'.entire5509_native_RAM_capture_Baraka_original1014_contract','exec'),scope)
capture=scope['capture']


def run():
    guest=model.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Qualified full-scope Cage frontier retained')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    payload=(ROOT/model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for p in(Path(__file__),Path(model.__file__),Path(transport.__file__),LUA,ROOT/'mk2ks_current_cage_ram_v5509.lua',
             ROOT/'mk2ks_rolling_head_display_v1003.lua',ROOT/'mk2ks_stock_head_victim_v921.lua'):
        pins[str(p.resolve())]=sha(p)
    reference,gfx=model.source_art(guest,payload,pins);model.physical_contract();image=transport.source_graphics(payload,pins)
    need(all(sha(p)==h for p,h in pins.items()),'Every current/public/source/art/evidence input stable before native capture')
    first=capture(('kano',1),guest,payload,gfx,reference,pins,image)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=[first]+list(pool.map(lambda s:capture(s,guest,payload,gfx,reference,pins,image),[('sonya',1),('kano',2),('sonya',2)]))
    for p in BASE.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every current/public/source/art/native evidence pin stable after actual matrix')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
      parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: current true-ID Baraka decapitation victims both characters/player slots; full original physical controller/damage/BBBB+HP/Block/parser/palette/FIFO/seven-head-seven-body/floor/retirement contract; entire original900/1014 source-PNG art and56 exact native whole scanouts with all emitted head/body pixels and individually source-ROM-owned foreground',
      cases=cases,independentSourceArtReference=reference,currentNormalBarakaBothVictimsBothSlotsAccepted=True,
      actualRequestedRAMDisplayCallbacks=sum(len(c['actualDisplayHeaders'])for c in cases),
      effectiveActualNativeRecordFaults=sum(len(c['effectiveActualNativeRecordFaults'])for c in cases),
      effectiveActualRAMFaults=sum(len(c['actualNativeHeadBodyPixelsAndScanout']['effectiveActualRAMFaults'])for c in cases),
      effectiveActualNativeForegroundOwnerFaults=sum(len(c['actualNativeHeadBodyPixelsAndScanout']['effectiveActualNativeForegroundOwnerFaults'])for c in cases),
      exactWholeNativeScanoutPixels=sum(c['actualNativeHeadBodyPixelsAndScanout']['wholeNativeScanoutPixels']for c in cases),
      newNativeBoots=4,newBuilds=0,newDeletedFiles=0,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
      nativeAutomaticTerminalPNGs=sum(len(c['nativeAutomaticTerminalPNGs'])for c in cases),newInputHashes=pins,
      publicPlayableChanged=False,refreshedReleaseZIP=False,allFinishersVictimsArenasAndCostumesAccepted=False,
      completeBarakaAudioAccepted=False,continuousWholeSceneRasterAccepted=False,fullPortAcceptance=False)


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable current Baraka pixel checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
