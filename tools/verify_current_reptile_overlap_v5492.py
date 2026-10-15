"""Current physical Reptile victims: source-owned art plus ordered foreground.

Native blood is not an ignored mask: replay its actual ROM pixels, queue and
DMA registers up to the actual display flip, then require exact VRAM and RGB.
No threshold, chosen best field, guest writes, raw-media files or game build.
"""
import concurrent.futures, datetime, inspect, json, os, re, struct, subprocess, traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import current_reptile_victims_ram_v5467 as canonical
import current_reptile_victims_ram_v5477 as art
import current_reptile_victims_ram_v5480 as pixels
import inspect_current_cpu_knife_raster_v1975 as raster
import verify_move_phase_shadow_v5089 as graphics

ROOT,need,sha=canonical.ROOT,canonical.need,canonical.sha
PARENT=canonical.PARENT
BASE=ROOT/'audit_v5493_current_reptile_overlap_ram'
OUT=ROOT/'audit_v5494_current_reptile_overlap_progress'
LUA=ROOT/'mk2ks_current_reptile_overlap_v5492.lua'
COMPLETED=[]
HEX=set('source command palette pc cursor actor pose cache bank body queue_size queue_xy queue_command queue_palette'.split())


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if line.startswith('MK2_CURRENT_REPTILE_SCENE_'+tag+' '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            for k in r:
                if k not in ('filename','assistance'):r[k]=int(r[k],16 if k in HEX else 10)
            result.append(r)
    return result


def source_graphics(pins,expected_death):
    image=graphics.reconstruct(pins)
    # Original imported own death allocation, independently re-encoded first.
    image[0x1ec0000:0x1ec0000+len(expected_death)]=expected_death
    old=ROOT/graphics.native.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    new=ROOT/canonical.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    def block(p):
        return p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
    need(block(old)==block(new),'Entire current graphics ROM lane inventory matches independent reconstruction')
    pins[str(new)]=sha(new)
    return image


def verify_pixels(log,images,buffers,gfx_streams,source_image,reference,fighter,guest):
    dmas=rows(log,'DMA');cutoffs=rows(log,'CUTOFF')
    need(len(cutoffs)==3 and [r['age']for r in cutoffs]==[150,200,250],'All three actual native display cutoffs')
    need([r['serial']for r in dmas]==list(range(1,len(dmas)+1)),'Complete ordered passive native DMA ledger')
    records={}
    for key,(raw,r)in gfx_streams.items():
        first=int(r['first']);offset=int(r['offset'])
        need(offset//8==first and raw==source_image[first:first+len(raw)],
             'Every complete actual foreground/body/blood graphics stream equals independently reconstructed ROM')
        records[key]=dict(offset=offset,data=raw.hex())
    replay=raster.Replay(ROOT,defaultdict(list),records,{})
    replay.words=np.empty((512,512),np.uint16)
    replay.body=np.zeros((512,512),np.uint8)
    replay.shadow=np.zeros((512,512),bool)
    replay.projected=np.zeros((512,512),bool)
    assets={int(r['graphics'],16):r for r in reference['fighters'][fighter]['frames']}
    owned=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
           if line.startswith('MK2_DEATH_ART_V897_DMA ')]
    targets=[];negative=[]
    for cutoff in cutoffs:
        filename=cutoff['filename'];colors,meta=buffers[filename,'PALETTE'];raw,vr=buffers[filename,'VRAM']
        need(all(meta[k]==vr[k]for k in('filename','frame','age','flip_frame','start','control','tap','pc','mask'))and
             int(meta['frame'])==int(meta['flip_frame'])==cutoff['frame']and meta['pc']=='FF8168E0'and meta['mask']=='FFFF',
             'Whole actual hardware flip/palette/VRAM/display association')
        image=images[filename]
        scan=pixels.display.check_latch(image,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16))
        candidates=[d for d in owned if int(d['frame'])<=cutoff['frame']and
                    (int(d['y'])>>8)==(scan['row']>>8)and d['fifo_actor']==d['fifo_physical']]
        need(candidates,'Actual front-page owned body dispatch exists')
        latest=max(int(d['frame'])for d in candidates)
        candidates=[d for d in candidates if int(d['frame'])==latest]
        need(len(candidates)==1 and cutoff['frame']-latest in(0,1),'Latest front-page body; no frame/location search')
        original=candidates[0];source=int(original['source'],16);asset=assets[source]
        need(asset['kind']=='body','Actual source-owned headless-body descriptor')
        fields={'source':16,'command':16,'palette':16,'x':10,'y':10,'width':10,'height':10,'cursor':16}
        same=[d for d in dmas if d['frame']==latest and all(d[k]==int(original[k],base)for k,base in fields.items())]
        need(len(same)==1,'Original owned DMA exactly identified in complete foreground ledger')
        body=same[0]
        need(body['queue_match']==1 and body['queue_frame']==latest and body['actor']==int(original['fifo_physical'],16)and
             body['pose']==int(original['fifo_pose'],16)and (body['width'],body['height'])==tuple(asset['size']),
             'Actual physical victim FIFO owner/source/pose/dimensions preserved')
        relevant=[d for d in dmas if body['serial']<=d['serial']<=cutoff['serial']]
        composed=np.full((512,512),65535,np.uint16)
        ownership=np.zeros((512,512),np.int32)
        opaque=None;foreground={}
        for d in relevant:
            replay.words.fill(65535);replay.body.fill(0)
            replay.dma(dict(d,slot=1))
            written=replay.words!=65535
            if d is body:
                opaque=written.copy()
                need(int(opaque.sum())>100,'Complete source body contains native opaque pixels')
            overlap=written&opaque
            if d is not body and overlap.any():
                need(d['queue_match']==1 and d['queue_frame']==d['frame']and d['actor']!=body['actor']and
                     d['palette']==0x1c00 and d['bank']&0x7f00==0x1c00 and d['command']&15==2 and
                     d['source']<0x0a000000 and d['pc']==0xff804640,
                     'Every actual body occluder is genuine original stock blood, with native FIFO/actor/palette/consumer ownership')
                need(d['queue_size']==((d['height']<<16)|d['width']) and d['queue_command']>>16==d['command'],
                     'Original blood FIFO dimensions and pixel command bind to hardware')
                need(0xff800000<=d['cache']<=0xfffffff0 and d['cache']%8==0,'Actual blood uses original native ROM descriptor')
                at=(d['cache']-0xff800000)//8
                bw,bh,bx,by,bsource,bcommand=struct.unpack_from('<HHhhIH',guest,at)
                need((bw,bh,bsource)==(d['width'],d['height'],d['source'])and
                     bcommand&0x7000==d['command']&0x7000,'Actual blood pixels and dimensions come from original native descriptor')
                foreground[d['serial']]=d
            composed[written]=replay.words[written];ownership[written]=d['serial']
        actual=np.frombuffer(raw,'<u2').reshape(512,512)
        need(np.array_equal(composed[opaque],actual[opaque]),
             'Every original body pixel exactly equals own source or its actual subsequent source-ROM blood draw; no ignored occlusion')
        keep=opaque&(ownership==body['serial']);covered=opaque&~keep
        need(np.array_equal(composed[keep],actual[keep])and int(keep.sum())>100,
             'Every unoccluded owned body pixel remains source-exact')
        need(set(ownership[covered].tolist()).issubset(foreground),'All occluded pixels have individually source-bound native blood owners')
        row,col=scan['row'],scan['column']
        yy,xx=np.where(opaque)
        need(np.all((xx>=col)&(xx<col+400)&(yy>=row)&(yy<row+254)),'Complete original body is visible in native scanout')
        pal=np.frombuffer(colors,'<u4');words=pal[composed[opaque]&0x7fff]
        expected=np.stack((words>>16&255,words>>8&255,words&255),axis=1).astype(np.uint8)
        need(np.array_equal(image[yy-row,xx-col],expected),'Every original body or owned blood pixel has exact native hardware RGB')
        # Effective faults on real captured pixels/source/order, never guest mutations.
        def reject(label,fn):
            try:fn()
            except ValueError as error:negative.append(dict(age=cutoff['age'],label=label,rejectedBy=str(error)))
            else:raise ValueError('Actual overlap counterexample accepted: '+label)
        bad=composed.copy();bad[yy[0],xx[0]]^=1
        reject('one actual source-derived body pixel corrupted',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'Exact native body/source pen comparison'))
        bad=image.copy();bad[yy[0]-row,xx[0]-col,0]^=1
        reject('one actual displayed body RGB pixel corrupted',lambda:pixels.display.check_latch(bad,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
        if covered.any():
            cy,cx=np.where(covered);bad=composed.copy();bad[cy[0],cx[0]]=body['palette']|1
            reject('native blood overlap omitted or reordered',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'All original owned occlusion pixels exact'))
            owner=int(ownership[cy[0],cx[0]]);blood=foreground[owner]
            key=f"{blood['source']:08X}_{blood['command']:04X}_{blood['width']}_{blood['height']}"
            data,record=gfx_streams[key];changed=bytearray(data);changed[0]^=1
            reject('one actual native blood source byte corrupted',lambda:need(changed==source_image[int(record['first']):int(record['first'])+len(data)],'Whole source-ROM blood stream must be exact'))
        need(np.array_equal(composed[opaque],actual[opaque]),'Original positive restored after every effective actual RAM counterexample')
        targets.append(dict(filename=filename,age=cutoff['age'],frame=cutoff['frame'],nativeBodyDMAFrame=latest,
          bodyPose=asset['pose'],**scan,originalOpaquePixels=int(opaque.sum()),ownVisiblePixels=int(keep.sum()),
          sourceROMBloodOccludedPixels=int(covered.sum()),actualNativeBloodDraws=len(foreground),
          actualOrderedDMAsThroughFlip=len(relevant),everyOriginalOpaqueBodyAndNativeBloodPixelExact=True))
    return dict(passed=True,targets=targets,effectiveActualRAMFaults=negative,
      completeNativeSceneScanoutPixels=sum(r['pixels']for r in targets),sourceBoundNativeGFXStreams=len(records),
      boundedBodyAndNativeBloodOwnershipAccepted=True,wholeContinuousSceneOrAllArtisticContextsAccepted=False)


def capture(spec,guest,payload,expected_gfx,reference,pins,source_image):
    fighter,side=spec;folder=BASE/f'{fighter}_p{side}'
    need(not folder.exists(),'Fresh immutable current physical victim context')
    folder.mkdir(parents=True)
    for name in('cfg','nvram','snap'):(folder/name).mkdir()
    frozen=dict(pins);canonical.save(folder/'input_hashes_before.json',frozen)
    build=ROOT/canonical.current.NAME
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_PORT_ROOT=str(ROOT),MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_REPTILE_AUDIT_DIR=str(folder))
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
      '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','95','-snapsize','400x254',
      '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
    ram,images,headers,buffers,gfx={},{},[],{},{}
    with(folder/'stderr.log').open('w',encoding='utf-8')as err:
        proc=subprocess.Popen(command,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
        canonical.save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
        print(f'{fighter} P{side} actual native PID={proc.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as out:
            for line in proc.stdout:
                if line.startswith('MK2_CURRENT_REPTILE_RAM_'):
                    tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
                    need(len(raw)==int(r['bytes']),'Whole actual RAM transport buffer');r['sha256']=canonical.digest(raw)
                    if tag.endswith('_DATA'):
                        need(r['filename']not in ram,'Unique guest/death GFX');ram[r['filename']]=raw
                    elif tag.endswith('_GFX'):
                        need(r['filename']not in gfx,'Unique actual foreground source');gfx[r['filename']]=(raw,r)
                    elif tag.endswith(('_PALETTE','_VRAM')):
                        kind=tag.rsplit('_',1)[1];need((r['filename'],kind)not in buffers,'Unique palette/VRAM');buffers[r['filename'],kind]=(raw,r)
                    else:
                        need(tag.endswith('_RGB')and(r['width'],r['height'],len(raw))==('400','254',406400)and r['filename']not in images,'Whole unique native scanout')
                        images[r['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();headers.append(r)
                    out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
                else:need('hex='not in line,'No raw media persisted');out.write(line)
            code=proc.wait()
    log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
    need(code==0 and not error and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),'Warning-free terminal native run')
    need(ram.get('guest_maincpu.bin')==guest and ram.get('native_death_gfx.bin')==expected_gfx,'Whole actual initialized guest and source-derived death art exact')
    result=dict(exit_code=code,candidate=canonical.current.NAME,player=fighter,victim_slot=side,winner_slot=3-side,seconds=95,
      executable_sha256=canonical.current.EXE_SHA,payload_sha256=canonical.current.PAYLOAD_SHA,assistance='none',cheats_enabled=False,
      entireOriginal887PhysicalControllerRetained=True,input_hashes=frozen,nativePID=proc.pid)
    contract,contract_sha=art.physical_contract()
    state=contract(log,result,ram['guest_maincpu.bin'],ram['native_death_gfx.bin'],reference,images,guest,payload)
    faults=pixels.corrected_faults()(log,result,ram,reference,images,guest,payload,contract)
    print(f'{fighter} P{side} native terminal; physical/art/FIFO/ground/retirement and21 record faults pass; checking ordered foreground',flush=True)
    visual=verify_pixels(log,images,buffers,gfx,source_image,reference,fighter,guest)
    final=dict(passed=True,process=result,originalFullPhysicalArtContractSHA256=contract_sha,actualNativeContract=state,
      actualDisplayHeaders=headers,effectiveActualNativeRecordFaults=faults,actualNativeBodyBloodPixelsAndScanout=visual,
      allGuestGraphicsAndDisplayedFramesOnlyInRAM=True,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,audioAccepted=False,fullPortAcceptance=False)
    canonical.save(folder/'result.json',final)
    before=sha(folder/'run.log');cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True)
    need(cp.returncode==0 and sha(folder/'run.log')==before,'Lossless terminal trace compression')
    COMPLETED.append(final)
    print(f'{fighter} P{side} exact native body + source-ROM blood overlap and whole scanouts passed',flush=True)
    return final


def run():
    guest=canonical.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Current primary/audio prerequisite retained')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    payload=(ROOT/canonical.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for p in(LUA,Path(__file__).resolve(),Path(canonical.__file__),Path(art.__file__),Path(pixels.__file__),
             Path(graphics.__file__),Path(raster.__file__),Path(raster.base.__file__),Path(raster.scaling.__file__),
             ROOT/'tools/inspect_natural_arena_floor_v602.py',ROOT/'tools/verify_native_floor_display_v602.py',
             ROOT/'mk2ks_current_reptile_ram_v5483.lua',ROOT/'mk2ks_current_reptile_ram_v5480.lua',ROOT/'mk2ks_current_reptile_ram_v5470.lua',
             ROOT/'mk2ks_current_reptile_ram_v5467.lua',ROOT/'mk2ks_reptile_victim_v887.lua',ROOT/'mk2ks_reptile_death_grounding_v904.lua'):
        pins[str(p.resolve())]=sha(p)
    reference,expected_gfx=art.corrected_art(guest,payload,pins)
    image=source_graphics(pins,expected_gfx)
    stockpath=ROOT/'mk2/mk2-maincpu.bin';stock=bytearray(stockpath.read_bytes());pins[str(stockpath)]=sha(stockpath)
    offset=lambda address:(address-0xff800000)//8
    struct.pack_into('<I',stock,offset(0xff8c8a70),0xfffd4000)
    need(guest[offset(0xff8c81f0):offset(0xff8c9900)]==stock[offset(0xff8c81f0):offset(0xff8c9900)],'Entire original Reptile choreography; only typed victim table relocation')
    need(all(sha(p)==h for p,h in pins.items()),'All current/source/public pins stable before actual boot')
    first=capture(('kano',1),guest,payload,expected_gfx,reference,pins,image)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=[first]+list(pool.map(lambda spec:capture(spec,guest,payload,expected_gfx,reference,pins,image),[('kano',2),('sonya',1),('sonya',2)]))
    for p in BASE.rglob('*'):
        if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No raw media files');pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every current/source/public/evidence pin unchanged after matrix')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
      parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: current Reptile true-ID victims both characters/slots; complete original physical damage/head/body/palette/floor/FIFO/retirement gate; exact source-owned native blood overlap and12 whole scanouts; actual record and RAM counterexamples',
      cases=cases,independentSourcePNGNativeReference=reference,currentReptileVictimsBothSlotsAccepted=True,
      actualDisplayedFrameCallbacks=sum(len(c['actualDisplayHeaders'])for c in cases),
      effectiveActualNativeRecordFaults=sum(len(c['effectiveActualNativeRecordFaults'])for c in cases),
      effectiveActualPixelFaults=sum(len(c['actualNativeBodyBloodPixelsAndScanout']['effectiveActualRAMFaults'])for c in cases),
      exactWholeNativeScanoutPixels=sum(c['actualNativeBodyBloodPixelsAndScanout']['completeNativeSceneScanoutPixels']for c in cases),
      newNativeBoots=4,newBuilds=0,newDeletedFiles=0,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
      publicPlayableChanged=False,refreshedReleaseZIP=False,allFinisherContextsAccepted=False,allArenasAccepted=False,
      audioAccepted=False,continuousWholeSceneRasterAccepted=False,fullPortAcceptance=False,newInputHashes=pins)


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable native overlap checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();canonical.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
