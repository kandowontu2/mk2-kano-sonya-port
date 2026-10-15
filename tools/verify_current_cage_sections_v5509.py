"""Actual current Cage victims: complete physical contract and exact sections.

Retains original controller/state/grounding/retirement criteria. Separately
replays source-bound native foreground through the actual hardware flip.
Requested pixels/guest/GFX/VRAM/palettes stay in RAM; automatic -str PNGs are
explicitly accounted. No game build, proxy, guest assistance or public change.
"""
import concurrent.futures, datetime, json, os, re, struct, subprocess, traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import current_cage_torso_source_v5508 as model
import verify_move_phase_shadow_v5089 as graphics
import current_cpu_scene_ram_contract_v5363 as hud
import inspect_current_cpu_knife_raster_v1975 as raster
import verify_native_floor_display_v602 as display

ROOT,need,sha=model.ROOT,model.need,model.sha
PARENT=ROOT/'audit_v5507_current_reptile_overlap_qualified_progress/progress.json'
BASE=ROOT/'audit_v5510_current_cage_sections_ram'
OUT=ROOT/'audit_v5511_current_cage_sections_progress'
LUA=ROOT/'mk2ks_current_cage_ram_v5509.lua'
COMPLETED=[]
HEX=set('source command palette pc cursor actor pose cache bank body queue_size queue_xy queue_command queue_palette'.split())


def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def digest(raw):return model.original.assets.sha(raw)


def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if line.startswith('MK2_CURRENT_CAGE_SCENE_'+tag+' '):
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            for k in r:
                if k not in('filename','assistance'):r[k]=int(r[k],16 if k in HEX else 10)
            out.append(r)
    return out


def source_graphics(payload,pins):
    image=hud.patch_hud(graphics.reconstruct(pins),pins)
    old=ROOT/graphics.native.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    new=ROOT/model.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    def block(p):return p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
    need(block(old)==block(new),'Whole source-bound current native graphics lane inventory')
    pins[str(new)]=sha(new)
    for header,source,gfx in((0x160008,0x164000,0x1ec0000),(0x1b0008,0x1b1000,0x1f20000)):
        count=struct.unpack_from('<I',payload,header)[0]
        image[gfx:gfx+count]=payload[source:source+count]
    return image


def verify_pixels(log,images,buffers,gfx_streams,source_image,reference,fighter,guest):
    dmas=rows(log,'DMA');cutoffs=rows(log,'CUTOFF')
    need([r['serial']for r in dmas]==list(range(1,len(dmas)+1)),'Complete ordered actual native foreground ledger')
    records={}
    for key,(raw,r)in gfx_streams.items():
        first,offset=int(r['first']),int(r['offset'])
        need(offset//8==first and raw==source_image[first:first+len(raw)],'Every actual native foreground graphics stream source-exact: '+key)
        records[key]=dict(offset=offset,data=raw.hex())
    replay=raster.Replay(ROOT,defaultdict(list),records,{})
    replay.words=np.empty((512,512),np.uint16);replay.body=np.zeros((512,512),np.uint8)
    replay.shadow=np.zeros((512,512),bool);replay.projected=np.zeros((512,512),bool)
    native=model.original.records(log,'MK2_CAGE_TORSO_V979')
    actions=model.original.records(log,'MK2_STOCK_HEAD_V921')
    action=next(r for tag,r in actions if tag=='ACTION')
    identity=17 if fighter=='kano'else 18
    assets=reference['by_source']
    shots=[r for tag,r in native if tag=='POSE_SNAPSHOT'and int(r['source'],16)in assets]
    owned=[r for tag,r in native if tag=='DMA'and int(r['source'],16)in assets]
    need(len(shots)==6,'All six originally dispatched owned section poses')
    results=[];faults=[]
    for shot in shots:
        filename=f"torso_pose_{shot['actor_pose']}_{shot['frame']}.png"
        found=[r for r in cutoffs if r['filename']==filename]
        need(len(found)==1,'One exact native flip per presented owned section')
        cutoff=found[0];raw,vr=buffers[filename,'VRAM'];colors,meta=buffers[filename,'PALETTE']
        need(all(meta[k]==vr[k]for k in('filename','frame','age','flip_frame','start','control','tap','pc','mask'))and
             int(meta['frame'])==int(meta['flip_frame'])==cutoff['frame']and meta['pc']=='FF8168E0'and meta['mask']=='FFFF',
             'Actual full section framebuffer/palette/native flip association')
        image=images[filename]
        scan=display.check_latch(image,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16))
        source=int(shot['source'],16);asset=assets[source];pose=asset['group']
        # All components of this exact section, from the actual front page.
        candidates=[d for d in owned if int(d['frame'])<=cutoff['frame']and int(d['fifo_pose'],16)==pose and
                    int(d['source'],16)in assets and (int(d['y'])>>8)==(scan['row']>>8)]
        need(candidates,'Actual front-page section dispatch exists')
        latest=max(int(d['frame'])for d in candidates)
        selected=[d for d in candidates if int(d['frame'])==latest]
        expected={s for s,a in assets.items()if a['name']==fighter and a['group']==pose}
        need(cutoff['frame']-latest in(0,1)and {int(d['source'],16)for d in selected}==expected and len(selected)==len(expected),
             'Entire current owned section; no best-frame/location/partial-component search')
        fields={'source':16,'command':16,'palette':16,'x':10,'y':10,'width':10,'height':10,'cursor':16}
        targets=[]
        for original in selected:
            same=[d for d in dmas if d['frame']==latest and all(d[k]==int(original[k],base)for k,base in fields.items())]
            need(len(same)==1,'Each complete section component identified in ordered native ledger')
            d=same[0];part=assets[d['source']]
            need(d['queue_match']==1 and d['queue_frame']==latest and d['id']==identity and d['pose']==pose and
                 d['actor']==int(original['fifo_actor'],16)and tuple(part['size'])==(d['width'],d['height']),
                 'Each native section FIFO owner/identity/source/group/dimension exact')
            targets.append(d)
        start=min(d['serial']for d in targets)
        relevant=[d for d in dmas if start<=d['serial']<=cutoff['serial']]
        target_serials={d['serial']for d in targets}
        opaque=np.zeros((512,512),bool);target_masks={}
        # Decode the target silhouettes first, then every later native draw.
        for d in targets:
            replay.words.fill(65535);replay.body.fill(0);replay.dma(dict(d,slot=1))
            mask=replay.words!=65535;need(int(mask.sum())>10,'Every dispatched owned component has genuine visible source pixels')
            opaque|=mask;target_masks[d['serial']]=mask
        composed=np.full((512,512),65535,np.uint16);ownership=np.zeros((512,512),np.int32)
        foreground={}
        for d in relevant:
            replay.words.fill(65535);replay.body.fill(0);replay.dma(dict(d,slot=1));written=replay.words!=65535
            if d['serial']not in target_serials and (written&opaque).any():
                need(d['queue_match']==1 and d['queue_frame']==d['frame']and d['command']&15==2 and d['pc']==0xff804640,
                     'Actual section occluder retains original native FIFO and DMA consumer: '+str(d))
                if d['source']in assets:
                    other=assets[d['source']]
                    need(other['name']==fighter and d['id']==identity and d['pose']==other['group']and
                         tuple(other['size'])==(d['width'],d['height'])and d['palette']==d['bank']&0x7f00,
                         'Occluding opposite section has own current descriptor/group/identity/palette')
                    owner_kind='own other section'
                elif d['palette']==0x1c00:
                    need(d['actor']not in {t['actor']for t in targets}and d['bank']&0x7f00==0x1c00 and
                         d['source']<0x0a000000 and 0xff800000<=d['cache']<=0xfffffff0 and d['cache']%8==0,
                         'Every blood occluder uses actual original native ROM object/palette/source')
                    at=(d['cache']-0xff800000)//8
                    w,h,s,c=struct.unpack_from('<HHIH',guest,at)
                    need((w,h,s)==(d['width'],d['height'],d['source'])and c&0x7000==d['command']&0x7000,
                         'Original ten-byte blood descriptor binds dimensions and source')
                    owner_kind='source-ROM blood'
                else:
                    need(d['id']==2 and d['actor']==int(action['actor'],16)and d['source']<0x0a000000,
                         'Other occluder is actual original Cage, never a foreign substituted body')
                    native_parts=graphics.native_group(dict(pose=f"{d['pose']:08X}",facing=f"{d['command']&0x30:08X}"),b'',guest)
                    need(any((p['graphic'],p['width'],p['height'],p['command'])==
                             (d['source'],d['width'],d['height'],d['command']&0x7fff)for p in native_parts),
                         'Actual stock Cage component belongs to original ROM native pose')
                    owner_kind='source-ROM Cage'
                need(d['queue_size']==((d['height']<<16)|d['width'])and d['queue_command']>>16==d['command'],
                     'Occluding native object FIFO dimensions/command bind to actual hardware')
                foreground[d['serial']]=owner_kind
            composed[written]=replay.words[written];ownership[written]=d['serial']
        actual=np.frombuffer(raw,'<u2').reshape(512,512)
        mismatches=int(np.count_nonzero(composed[opaque]!=actual[opaque]))
        need(mismatches==0,'Every complete owned section pixel source-exact after individually owned native foreground; differences='+str(mismatches))
        keep=opaque&np.isin(ownership,list(target_serials));covered=opaque&~keep
        need(int(keep.sum())>100 and set(ownership[covered].tolist()).issubset(foreground),
             'All occluded section pixels have explicit source-bound native owners')
        yy,xx=np.where(opaque);row,col=scan['row'],scan['column']
        need(np.all((xx>=col)&(xx<col+400)&(yy>=row)&(yy<row+254)),'Complete emitted section appears within actual native scanout')
        words=np.frombuffer(colors,'<u4')[composed[opaque]&0x7fff]
        wanted=np.stack((words>>16&255,words>>8&255,words&255),axis=1).astype(np.uint8)
        need(np.array_equal(image[yy-row,xx-col],wanted),'All own section and legitimate foreground pixels have exact actual RGB')
        def reject(label,check):
            try:check()
            except ValueError as error:faults.append(dict(pose=asset['pose'],label=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted actual section RAM counterexample: '+label)
        for target in targets:
            ty,tx=np.where(target_masks[target['serial']]);bad=composed.copy();bad[ty[0],tx[0]]^=1
            reject('one source-derived component pen corrupted',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'Every dispatched component pen exact'))
        bad=image.copy();bad[yy[0]-row,xx[0]-col,0]^=1
        reject('one actual presented section RGB pixel corrupted',lambda:display.check_latch(bad,raw,colors,int(meta['start'],16),int(meta['control'],16),int(meta['tap'],16)))
        if covered.any():
            cy,cx=np.where(covered);bad=composed.copy();bad[cy[0],cx[0]]^=1
            reject('actual legitimate foreground omitted or corrupted',lambda:need(np.array_equal(bad[opaque],actual[opaque]),'Every legitimate occlusion pen exact'))
        results.append(dict(filename=filename,pose=asset['pose'],frame=cutoff['frame'],age=cutoff['age'],nativeDMAFrame=latest,
          components=len(targets),originalOpaquePixels=int(opaque.sum()),ownVisiblePixels=int(keep.sum()),
          ownedNativeOccludedPixels=int(covered.sum()),nativeOccluders=foreground,orderedDMAsThroughFlip=len(relevant),**scan))
    need({r['pose']for r in results}=={0,1,2,3,5,6},'Every originally dispatched native section phase accepted, not unused pose4')
    return dict(passed=True,sections=results,effectiveActualRAMFaults=faults,
      wholeNativeScanoutPixels=sum(r['pixels']for r in results),sourceBoundNativeGraphicsStreams=len(records),
      everyEmittedOwnedSectionPixelAndLegitimateForegroundExact=True,continuousSceneAndAllArtisticContextsAccepted=False)


def record_faults(log,result,guest,payload,reference,images,ram,contract):
    positive=contract(log,result,guest,payload,reference,images,ram);out=[]
    def reject(label,pattern,replacement,count=1):
        changed,n=re.subn(pattern,replacement,log,count=count,flags=re.M)
        need(n>=1 and (count==0 or n==1)and changed!=log,'Effective actual native-record counterexample: '+label)
        try:contract(changed,result,guest,payload,reference,images,ram)
        except ValueError as error:out.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Actual physical counterexample accepted: '+label)
    reject('proxy victim',r'ids=2,(17|18)',r'ids=2,1')
    reject('non-native health writer',r'pc=FF836700',r'pc=FF838860')
    reject('missing native action',r'^MK2_STOCK_HEAD_V921_ACTION .*\n','')
    reject('missing native wrap',r'^MK2_STOCK_HEAD_V921_WRAP .*\n','')
    reject('missing genuine LP command',r'^MK2_STOCK_HEAD_V921_INPUT .*button=Low_Punch\n','')
    reject('wrong native main57',r'(index=)00000039',r'\g<1>00000000',count=0)
    for label,tag,key in(('wrong actual section owner','QUEUE','owner'),('wrong section main','QUEUE','main'),
                          ('foreign section ID','QUEUE','id'),('unbound actual FIFO','DMA','queue_match')):
        # Limit these to a genuinely owned torso source rather than earlier Cage frames.
        wanted=r'(^MK2_CAGE_TORSO_V979_'+tag+r' .*source=0F9[0-9A-F]+ .*?'+key+r'=)[0-9A-F]+'
        reject(label,wanted,r'\g<1>0')
    reject('wrong native width',r'(^MK2_CAGE_TORSO_V979_DMA .*source=0F9[0-9A-F]+ .*?width=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    lower=next(s for s,a in reference['by_source'].items()if a['name']==result['player']and a['pose']==6)
    reject('floating actual grounded lower section',r'(^MK2_CAGE_TORSO_V979_DMA .*source='+f'{lower:08X}'+r' .*?y=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('wrong grounded lower stage floor',r'(^MK2_CAGE_TORSO_V979_QUEUE .*source='+f'{lower:08X}'+r' .*?stageY=)(-?\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('section palette absent',r'^MK2_CAGE_TORSO_V979_PALETTE_DUMP .*\n','')
    reject('one native section snapshot absent',r'^MK2_CAGE_TORSO_V979_POSE_SNAPSHOT .*source=0F9[0-9A-F]+ .*\n','')
    need(contract(log,result,guest,payload,reference,images,ram)==positive,'Actual native positive restored after record counterexamples')
    return out


def capture(spec,guest,payload,expected_gfx,reference,pins,source_image):
    fighter,side=spec;folder=BASE/f'{fighter}_p{side}'
    need(not folder.exists(),'Fresh immutable current physical Cage victim context')
    folder.mkdir(parents=True)
    for name in('cfg','nvram','snap'):(folder/name).mkdir()
    frozen=dict(pins);save(folder/'input_hashes_before.json',frozen)
    build=ROOT/model.current.NAME
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_PORT_ROOT=str(ROOT),MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),
      MK2KS_REPTILE_AUDIT_DIR=str(folder),MK2KS_STOCK_KILLER='cage',MK2KS_STOCK_COMMAND='ddff_lp',MK2KS_STOCK_GAP='64')
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
      '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','95','-snapsize','400x254',
      '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
    ram,images,headers,buffers,gfx={},{},[],{},{}
    with(folder/'stderr.log').open('w',encoding='utf-8')as err:
        proc=subprocess.Popen(command,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
        save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
        print(f'{fighter} P{side} actual native PID={proc.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as out:
            for line in proc.stdout:
                if line.startswith('MK2_CURRENT_CAGE_RAM_'):
                    tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
                    need(len(raw)==int(r['bytes']),'Whole actual RAM transport buffer');r['sha256']=digest(raw)
                    if tag.endswith('_DATA'):
                        need(r['filename']not in ram,'Unique actual initialized guest/GFX/palettes');ram[r['filename']]=raw
                    elif tag.endswith('_GFX'):
                        need(r['filename']not in gfx,'Unique actual native foreground source');gfx[r['filename']]=(raw,r)
                    elif tag.endswith(('_PALETTE','_VRAM')):
                        kind=tag.rsplit('_',1)[1];need((r['filename'],kind)not in buffers,'Unique native palette/VRAM');buffers[r['filename'],kind]=(raw,r)
                    else:
                        need(tag.endswith('_RGB')and(r['width'],r['height'],len(raw))==('400','254',406400)and r['filename']not in images,'Whole unique actual native scanout')
                        images[r['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();headers.append(r)
                    out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
                else:need('hex='not in line,'No raw game media persisted');out.write(line)
            code=proc.wait()
    log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
    process=dict(exit_code=code,candidate=model.current.NAME,player=fighter,victim_slot=side,winner_slot=3-side,seconds=95,
      executable_sha256=model.current.EXE_SHA,payload_sha256=model.current.PAYLOAD_SHA,assistance='none',cheats_enabled=False,
      killer='cage',command='ddff_lp',target_gap=64,entireOriginal921PhysicalControllerRetained=True,input_hashes=frozen,nativePID=proc.pid)
    save(folder/'terminal.json',process)
    need(code==0 and not error and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),'Warning-free native terminal0')
    need(ram.get('guest_maincpu.bin')==guest and ram.get('native_torso_gfx.bin')==expected_gfx,'Whole actual initialized guest and independent source-PNG torso graphics exact')
    contract,contract_sha=model.physical_contract()
    state=contract(log,process,guest,payload,reference,images,ram)
    final=dict(passed=False,process=process,originalFullPhysicalArtContractSHA256=contract_sha,actualNativeContract=state,actualDisplayHeaders=headers,
      requestedGuestGFXVRAMRGBPalettesOnlyInRAM=True,audioAccepted=False,fullPortAcceptance=False)
    save(folder/'physical.json',final)
    faults=record_faults(log,process,guest,payload,reference,images,ram,contract)
    print(f'{fighter} P{side} terminal0; original physical damage/parser/sections/FIFO/floor/cleanup gate and {len(faults)} record faults passed',flush=True)
    visual=verify_pixels(log,images,buffers,gfx,source_image,reference,fighter,guest)
    auto=[]
    for p in folder.rglob('*'):
        if p.is_file():
            need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No raw game buffers written')
            if p.suffix.lower()=='.png':
                need(p.relative_to(folder).as_posix()=='snap/mk2ks/0000.png'and Image.open(p).size==(400,254),'Only native -str automatic terminal screenshot')
                auto.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
    need(len(auto)==1,'One accurately accounted native automatic terminal PNG')
    final.update(passed=True,effectiveActualNativeRecordFaults=faults,actualNativeSectionPixelsAndScanout=visual,nativeAutomaticTerminalPNGs=auto)
    save(folder/'result.json',final)
    before=sha(folder/'run.log');cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True)
    need(cp.returncode==0 and sha(folder/'run.log')==before,'Lossless terminal native trace compression')
    COMPLETED.append(final);print(f'{fighter} P{side} all six complete native section scanouts and source-owned foreground passed',flush=True)
    return final


def run():
    guest=model.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Qualified full-scope additive frontier remains active')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    payload=(ROOT/model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for p in(LUA,Path(__file__),Path(model.__file__),Path(model.original.__file__),Path(graphics.__file__),Path(hud.__file__),
             Path(raster.__file__),Path(raster.base.__file__),Path(raster.scaling.__file__),Path(display.__file__),
             ROOT/'tools/inspect_natural_arena_floor_v602.py',ROOT/'mk2ks_stock_head_victim_v921.lua',ROOT/'mk2ks_cage_torso_display_v979.lua'):
        pins[str(p.resolve())]=sha(p)
    reference,expected_gfx=model.source_art(guest,payload,pins);model.physical_contract();image=source_graphics(payload,pins)
    need(all(sha(p)==h for p,h in pins.items()),'All current/source/public/evidence pins stable before native capture')
    first=capture(('kano',1),guest,payload,expected_gfx,reference,pins,image)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=[first]+list(pool.map(lambda s:capture(s,guest,payload,expected_gfx,reference,pins,image),[('sonya',1),('kano',2),('sonya',2)]))
    for p in BASE.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All current/source/public/native evidence immutable at final gate')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
      parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual current true-ID Cage torso-rip victims both characters/player slots; entire original physical controller/state/FIFO/palettes/floor/retirement gate, all28 source-PNG components/native grammar, six complete section poses per case and explicitly source-owned native foreground through actual flip',
      cases=cases,independentSourceArtReference=reference,currentCageSectionsBothVictimsBothSlotsAccepted=True,
      actualRequestedRAMDisplayCallbacks=sum(len(c['actualDisplayHeaders'])for c in cases),
      effectiveActualNativeRecordFaults=sum(len(c['effectiveActualNativeRecordFaults'])for c in cases),
      effectiveActualRAMFaults=sum(len(c['actualNativeSectionPixelsAndScanout']['effectiveActualRAMFaults'])for c in cases),
      exactWholeNativeScanoutPixels=sum(c['actualNativeSectionPixelsAndScanout']['wholeNativeScanoutPixels']for c in cases),
      newNativeBoots=4,newBuilds=0,newDeletedFiles=0,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
      nativeAutomaticTerminalPNGs=sum(len(c['nativeAutomaticTerminalPNGs'])for c in cases),newInputHashes=pins,
      publicPlayableChanged=False,refreshedReleaseZIP=False,allFinisherContextsAccepted=False,allArenasAccepted=False,
      completeAudioAccepted=False,continuousWholeSceneRasterAccepted=False,fullPortAcceptance=False)


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable current Cage checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourceArtReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
