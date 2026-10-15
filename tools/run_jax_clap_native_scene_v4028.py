"""3836 earned Jax head-clap, complete native continuous scenes.

Retain3625 integer CPU/DMA/shift/scanout model. Source-bound palettes support
actual stock Jax and true17/18 including their source-owned headless
palettes. All four physical contexts; no forced AI/health/roster or pixels.
"""
import hashlib,json,os,re,shutil,struct,subprocess,sys,traceback
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import current_tomb_ram_model_v3625 as model
import run_current_tomb_ram_v3626 as original
import verify_current_ground_shadow_v1859 as graphics
import verify_native_mileena_victim_data_v3819 as data
import build_native_death_art_v900 as death_art
from verify_finish_display_v798 import raster as finish_format

# Imported modules extend/rebind legacy parser sets at import time. Bind the
# complete original observer schema explicitly after imports, not by luck.
model.raster.base.HEX |= finish_format.HEX | {'entry','frame_table','descriptor','field','before','a0','a1','a3','a7','b14','b10','parent','cursor','row','size','xy','p1','p2','main1','main2'}

ROOT=original.ROOT
model.raster.base.HEX |= set(re.findall(r'(\w+)=%\d*X',(ROOT/'mk2ks_native_tomb_display_v2062.lua').read_text()))
NAME='diagnostic_v3836_native_mileena_rom_identity'
OBSERVER=ROOT/'mk2ks_jax_clap_native_scene_ram_v4019.lua'
OUT=ROOT/'audit_v4030_jax_clap_native_scene_observed'
REVIEW=ROOT/'art_review_jax_clap_v4031'
need,sha=original.need,original.sha
PALETTES=[]
PALETTE_ROUTES={}
QUEUE_ROUTES={}

def palette_trace(line,guest):
    """Bind palette state to actual instruction/queue order, not pose guesses."""
    if line.startswith('MK2_STOCK_HEAD_V921_PALETTE '):
        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        hero=int(r['id']);flags=int(r['flags'],16)
        table=struct.unpack_from('<I',guest,(0xff90c840-0xff800000)//8)[0]
        expected=struct.unpack_from('<I',guest,(table-0xff800000)//8+hero*8+(4 if flags&64 else 0))[0]
        need(int(r['pc'],16)==0xff90c8e0 and int(r['pointer'],16)==expected and r['writes']=='0' and r['assistance']=='none','Actual original headless palette fetch and exact source table row')
        PALETTE_ROUTES[int(r['actor'],16)]=expected
    parsed=model.parse(line)
    if parsed and parsed[0]=='FLOOR_QUEUE':
        q=parsed[1]
        QUEUE_ROUTES[(q['frame'],q['actor'],q['part'])]=PALETTE_ROUTES.get(q['actor'])

def positive_control():
    stage=original.stage;old=json.loads(stage.OLD_REPORT.read_text())
    need(old['passed']and sha(stage.REFERENCE/'run.log')==old['inputHashes'][str(stage.REFERENCE/'run.log')],'Retained source-qualified native log')
    _,guest,_,_,_=stage.inventory.current.expected_current()
    payload=(ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata').read_bytes()
    pins={};scene=model.Model(guest,payload,original.source_graphics(payload,pins))
    for line in(stage.REFERENCE/'run.log').open(encoding='utf-8-sig'):
        parsed=model.parse(line)
        if parsed:
            kind,row=parsed
            if kind in('FLOOR_BASE','FLOOR_SHIFT_DATA','FLOOR_PRE_FRAME','FLOOR_LATCH','FLOOR_HELD'):
                file=stage.REFERENCE/row['file'];need(sha(file)==old['inputHashes'][str(file)],'Source-bound retained native RAM control');scene.raw[row['file']]=file.read_bytes();pins[str(file)]=sha(file)
            if kind=='FLOOR_DISPLAY':
                file=stage.REFERENCE/row['palette_file'];need(sha(file)==old['inputHashes'][str(file)],'Source-bound retained palette');scene.raw[row['palette_file']]=file.read_bytes();pins[str(file)]=sha(file)
            if kind=='FLOOR_SNAP':
                file=stage.REFERENCE/'snap'/row['file'];need(sha(file)==old['inputHashes'][str(file)],'Source-bound retained RGB');scene.rgb[row['file']]=np.asarray(Image.open(file).convert('RGB'));pins[str(file)]=sha(file)
        scene.line(line)
        if len(scene.records)==3:break
    # A snapshot callback follows the next pass's PRE event: the actual three
    # flips8173..75 yield snapshots8174..76, with four PREs8173..76. No PRE
    # target is ignored or used to re-anchor; all four are independently exact.
    need([r['frame']for r in scene.groups['FLOOR_PRE_FRAME']]==[8173,8174,8175,8176]and
        [r['frame']for r in scene.records]==[8174,8175,8176]and scene.pre_count==4 and scene.flip_count==3 and
        scene.loads==scene.fills==3 and scene.transfers==381 and scene.palette_checks==8,'Exact retained native chronology: four pre-pass targets, three displayed fields')
    pins[str(stage.OLD_REPORT)]=sha(stage.OLD_REPORT);pins[str(stage.REFERENCE/'run.log')]=sha(stage.REFERENCE/'run.log')
    return dict(passed=True,frames=3,exactPreBuffers=4,nativeShiftTransfers=381,paletteChecks=8,
        rejectedActualPixelTargetFaults=scene.counterexamples,transport=original.protocol_control(),inputHashes=pins)

def native_palette(q,actual,guest,ids,side):
    hero=q['id'];need(q['slot']==side and q['id']==q['roster'] and hero in(11,17,18),'True native FIFO character/palette owner; actual Jax and own17/18')
    alternate=bool(q['body']&64)
    if hero in(17,18):
        off=(0xf1500 if hero==17 else 0xf1600)if alternate else(0xfda00 if hero==17 else 0xfdb00)
        need(struct.unpack_from('<H',guest,off)[0]==65,'True own normal/alternate palette, transparent plus64')
    else:
        pointer=QUEUE_ROUTES[(q['frame'],q['actor'],q['part'])]
        if pointer is None:
            table=0xff907b30 if alternate else 0xff907910
            pointer=struct.unpack_from('<I',guest,(table-0xff800000)//8+hero*4)[0]
        need(0xff800000<=pointer<0x100000000 and pointer%16==0,'Original native stock palette table pointer')
        off=(pointer-0xff800000)//8
    count=struct.unpack_from('<H',guest,off)[0]
    need(2<=count<=256 and off+2+count*2<=len(guest),'Whole native palette extent')
    raw=struct.unpack_from('<'+str(count)+'H',guest,off+2)
    expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<d for s,d in((10,16),(5,8),(0,0)))for c in raw],dtype=np.uint32)
    bank=q['bank']&0x7f00
    need(len(actual)==32768 and np.array_equal(actual[bank:bank+count],expected),'Entire true native stock/own normal/alternate palette, no dim/recolour')
    PALETTES.append(dict(id=hero,slot=side,alternate=alternate,count=count,bank=bank,pointer=0xff800000+off*8))
    return PALETTES[-1]

def sources(payload,pins):
    graphics.NAME=NAME
    image=bytearray(original.source_graphics(payload,pins))
    need(payload[0x1f6000:0x1f6004]==b'KME1','Own swallowing native graphics header')
    # Independent encoder/data proof checks exact extents and every packed pen.
    k,s=22952,25352
    image[0x1f80000:0x1f80000+k]=payload[0x122000:0x122000+k]
    image[0x1f80000+k:0x1f80000+k+s]=payload[0x154000:0x154000+s]
    for header,magic,wanted_source,wanted_dest in((0x160000,b'KDH1',0x164000,0x1ec0000),(0x180000,b'KIF1',0x184000,0x1ee0000)):
        need(payload[header:header+4]==magic,'Actual dedicated native death/inflation source header')
        source,count,dest=struct.unpack_from('<III',payload,header+4)
        need((source,dest)==(wanted_source,wanted_dest)and count>0 and source+count<=len(payload)and dest+count<=len(image),'Whole independent native graphics upload range')
        image[dest:dest+count]=payload[source:source+count]
    need(payload[0x1c3800:0x1c3804]==b'KSP1','Dedicated native split source header')
    first,count,second,last,dest=struct.unpack_from('<5I',payload,0x1c3804)
    need((first,second,dest)==(0x172000,0x1bc000,0x1f60000) and 0<count<=0xe000 and 0<last<=0x4000,'Whole independent native split upload ranges')
    image[dest:dest+count]=payload[first:first+count]
    image[dest+count:dest+count+last]=payload[second:second+last]
    return bytes(image)

class SplitModel(model.Model):
    """Extend only native slot3 accounting; retain the whole integer replay."""
    def snapshot(self,snap):
        self.replay_events()
        latch=self.groups['FLOOR_LATCH'][-1] if self.groups['FLOOR_LATCH'] else None
        selected=bool(latch and latch['snapshot']==snap['frame'])
        target=latch if selected else self.groups['FLOOR_HELD'][-1]
        body=self.flips[latch['event']][1] if selected else self.replay.body
        display=self.groups['FLOOR_DISPLAY'][-1]
        bound=model.check_latch(self.rgb[snap['file']],self.raw[target['file']],self.raw[display['palette_file']],target['start'],target['control'],target['tap'])
        row,col=bound['row'],bound['column'];secondary=int((body[row:row+254,col:col+400]==3).sum())
        super().snapshot(snap)
        self.records[-1]['nativeSecondarySplitPixels']=secondary

def run(fighter,side):
    CASE=ROOT/f'audit_v4029_jax_clap_{fighter}_p{side}_native_scene_ram'
    identity={'kano':17,'sonya':18,'liu_kang':1,'kitana':4}[fighter]
    reference=identity in(1,4)
    need(fighter in('kano','sonya'),'True own victim contexts only, no relabelled stock runs')
    count=7
    PALETTES.clear()
    PALETTE_ROUTES.clear();QUEUE_ROUTES.clear()
    need(not CASE.exists()and not OUT.exists(),'Fresh immutable diagnostic leaves')
    # Retained positive tests use the unchanged original helper before adapting
    # only the palette contract to the independently declared actual stock ID.
    positive=positive_control()
    model.check_owned_body_palette=native_palette
    base_guest,_,base_payload,_,_=data.old.expected_current()
    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    original_rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    code_lo=(0xff90c800-0xff800000)//8;code_hi=(0xff90c8f0-0xff800000)//8
    expected_code=bytearray(original_rom[code_lo:code_hi])
    struct.pack_into('<I',expected_code,(0xff90c840-0xff90c800)//8,0xff800000+0xfa900*8)
    need(guest[code_lo:code_hi]==expected_code and guest[0xfa900:0xfa900+17*8]==original_rom[(0xff90c900-0xff800000)//8:(0xff90c900-0xff800000)//8+17*8],'Whole original headless selector code and all seventeen stock palette rows; only declared table extension')
    body_offset=0xfaa00+(identity-17)*14*20
    need(guest[body_offset:body_offset+7*20]==payload[0x160400+(identity-17)*14*20:0x160400+(identity-17)*14*20+7*20],'All seven true own headless-body native descriptors equal actual payload')
    phase_targets=set(death_art.GROUPS[fighter])
    need(len(phase_targets)==count,'Seven original animation-group pointers, not their native descriptors')
    for i,pointer in enumerate(death_art.GROUPS[fighter]):
        at=(pointer-0xfe800000)//8
        need(struct.unpack_from('<2I',payload,at)==(0xff800000+(body_offset+i*20)*8,0),'Every actual original own group points to its exact corresponding native headless descriptor and sentinel')
    pins=dict(positive['inputHashes']);image=sources(payload,pins)
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    need(sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
         hashlib.sha256(guest).hexdigest().upper()==build['expected_guest_sha256'],'Exact actual3836 build and independently reconstructed whole guest')
    files={Path(p)for p in build['input_hashes']}|{Path(p)for p in pins}|{
        OBSERVER,Path(__file__).resolve(),candidate/'build-info.json',candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',
        ROOT/'mk2ks_native_tomb_display_v2062.lua',ROOT/'mk2ks_stock_fatality_v1021.lua',ROOT/'mk2ks_stock_extended_earned_ram_v3958.lua',
        ROOT/'art_reference_mileena_v3801/reference.json',ROOT/'art_native_mileena_v3810/kano-swallowing.png',ROOT/'art_native_mileena_v3810/sonya-swallowing.png',
        ROOT/'audit_v3847_native_mileena_fix_full_scope_checkpoint/checkpoint.json'}
    for module in list(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):files.add(Path(file).resolve())
    for leaf in('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/leaf).glob('*'))
    pins.update({str(p.resolve()):sha(p)for p in files if p.is_file()})
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Every actual compiled input unchanged')
    CASE.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(CASE)],capture_output=True).returncode==0,'Inherited capture compression before writes')
    for p in files:
        if p.is_file()and p.suffix in('.lua','.py','.ps1'):
            target=CASE/'input_sources'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);need(sha(target)==sha(p),'Exact hierarchy source snapshot')
    (CASE/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(CASE),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0',
        MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='fff_lp_release',MK2KS_STOCK_GAP='64',
        MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_OUT=str(CASE))
    cmd=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
        '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
        '-inipath',str(CASE),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
        '-nothrottle','-str','150','-snapsize','400x254','-cfg_directory',str(CASE/'cfg'),'-nvram_directory',str(CASE/'nvram'),
        '-snapshot_directory',str(CASE/'snap'),'-autoboot_script',str(OBSERVER)]
    scene=SplitModel(guest,payload,image);transport=model.Transport();errors=[];visible=[];ram_guest=None;phase_images={};last_rgb=None
    with(CASE/'stderr.log').open('wb')as stderr,subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr)as process:
        (CASE/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd),indent=2)+'\n')
        print(f'Actual3836 native Jax head-clap {fighter}P{side} RAM scene pid='+str(process.pid),flush=True)
        with(CASE/'run.log').open('w',encoding='utf-8')as log:
            for binary in iter(process.stdout.readline,b''):
                if binary.startswith((b'MK2_TOMB_RAM_BUFFER ',b'MK2_TOMB_RAM_PIXELS ')):
                    header=binary.decode('ascii').strip();row=dict(re.findall(r'(\w+)=([^\s]+)',header));encoded=process.stdout.readline().decode('ascii').strip()
                    try:
                        if binary.startswith(b'MK2_TOMB_RAM_BUFFER '):
                            raw=transport.decode(row,encoded)
                            if row['file']=='guest_maincpu.bin':need(raw==guest,'Whole actual initialized3836 guest in RAM');ram_guest=model.digest(raw)
                            elif not errors:scene.raw[row['file']]=raw
                            log.write('MK2_TOMB_RAM_BUFFER_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(raw)+'\n')
                        else:
                            need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Complete actual native RGB field')
                            words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                            rgb=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8);last_rgb=rgb
                            visible.append(dict(file=row['file'],rgbSHA256=model.digest(rgb.tobytes())))
                            if not errors:
                                scene.rgb[row['file']]=rgb
                                frame=int(re.search(r'_(\d+)\.png$',row['file']).group(1))
                                poses={q['pose']for q in scene.groups['FLOOR_QUEUE']if q['frame']==frame-1 and q['slot']==side and q['pose'] in phase_targets}
                                for pose in poses:
                                    if pose not in phase_images:phase_images[pose]=(frame,rgb.copy())
                            log.write('MK2_TOMB_RAM_PIXELS_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(rgb.tobytes())+'\n')
                    except Exception as error:
                        if not errors:errors.append(dict(header=header,error=repr(error),traceback=traceback.format_exc()))
                else:
                    need(not re.match(b'^[A-F0-9]{1000}',binary),'No raw native raster/VRAM encoded data on disk')
                    line=binary.decode('utf-8');log.write(line)
                    if not errors:
                        try:palette_trace(line,guest);scene.line(line)
                        except Exception as error:errors.append(dict(line=line.rstrip(),error=repr(error),traceback=traceback.format_exc()))
                    if re.match(r'^MK2_NAT_CAMPAIGN_FLOOR_(BEGIN|RETIRED|RESULT) ',line)or re.match(r'^MK2_STOCK_HEAD_V921_(ACTION|WRAP|RESULT) ',line):log.flush();print(line.strip(),flush=True)
        code=process.wait()
    terminal=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,
        observedRGBFields=len(visible),modelExactFields=len(scene.records),modelErrors=errors,input_hashes=pins,
        rawRasterVRAMAudioROMCopiesWritten=0,fullPortAcceptance=False)
    for filename,value in(('result.json',terminal),('buffer_digests.json',transport.records),('visible_digests.json',visible),('continuous_scene_records.json',scene.records),('palette_checks.json',PALETTES)):
        (CASE/filename).write_text(json.dumps(value,indent=2)+'\n')
    need(all(sha(p)==h for p,h in pins.items()),'All actual inputs unchanged')
    log=(CASE/'run.log').read_text();stderr=(CASE/'stderr.log').read_text()
    need(code==0 and not errors and ram_guest==model.digest(guest)and not re.search(r'LUA ERROR|stack traceback|Fatal error|WRONG CHECKSUMS|might not run correctly',log+stderr,re.I),'Actual terminal and unweakened continuous native model')
    need(len(scene.groups['FLOOR_BEGIN'])==len(scene.groups['FLOOR_RETIRED'])==len(scene.groups['FLOOR_RESULT'])==1,'One actual native Jax action/match pointer teardown/completed window')
    begin=scene.groups['FLOOR_BEGIN'][0];retired=scene.groups['FLOOR_RETIRED'][0];result=scene.groups['FLOOR_RESULT'][0]
    state=scene.groups['FLOOR_STATE'][0];winner=3-side
    need(begin['id']==11 and begin['human_slot']==side and begin['entry']==0xff8c7820 and
        begin['actor']==state[f'p{winner}']and begin['main']==state[f'main{winner}']and state[f'roster{side}']==identity and
        retired['p1']==retired['p2']==0 and retired['victim_health']==0,'Actual true Jax winner, own victim and native both-pointer teardown')
    need([r['frame']for r in scene.records]==list(range(begin['origin']+1,retired['frame']+31))and result['snapshots']==len(scene.records),'Every consecutive native field through disappearance plus30')
    need(set(phase_images)==phase_targets,'All seven actual true-character native headless poses visible')
    later=[r for r in scene.records if r['frame']>=retired['frame']+3]
    need(later and all(not r['modeledFlip'] and r['rgbSHA256']==scene.records[retired['frame']-begin['origin']-1]['rgbSHA256'] for r in later),'Every post-retirement native scanout holds the exact last winner page; no later redraw or overlay')
    retirement_line=next(i for i,line in enumerate(log.splitlines()) if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RETIRED '))
    actual_actors={q['actor'] for q in scene.groups['FLOOR_QUEUE'] if q['slot'] in (side,3)}
    for i,line in enumerate(log.splitlines()):
        parsed=model.parse(line)
        if parsed and parsed[0]=='FLOOR_ALL_QUEUE' and parsed[1]['actor'] in actual_actors:
            need(i<retirement_line,'No physical or mirrored victim FIFO publication after native pointer teardown')
    need(scene.pre_count==len(scene.groups['FLOOR_PRE_FRAME'])and scene.flip_count==len(scene.groups['FLOOR_LATCH'])and
         scene.loads==scene.fills>0 and scene.palette_checks>0 and not scene.events and not scene.raw and not scene.rgb,'No omitted native target/shift/palette event')
    # One explicitly essential native QA contact sheet, not an ordinary raster
    # capture archive. No changes to source sprites or runtime game graphics.
    atlas=Image.new('RGB',(800,((count+2)//2)*278));draw=ImageDraw.Draw(atlas)
    frames=list(sorted(phase_images.items()))+[(0,(scene.records[-1]['frame'],last_rgb))]
    for i,(pose,(frame,rgb))in enumerate(frames):
        x,y=(i%2)*400,(i//2)*278;atlas.paste(Image.fromarray(rgb),(x,y+24));draw.text((x+4,y+5),f'{pose:08X} native frame {frame}',fill='white')
    atlas.save(REVIEW/f'{fighter}-p{side}-native-clap-review.png')
    return dict(passed=True,candidate=NAME,fighter=fighter,side=side,stockReferenceOnly=reference,actualContinuousNativeSceneAccepted=True,
        origin=begin['origin'],nativeBothPointerTeardown=retired['frame'],exactFields=len(scene.records),exactRGBPixels=len(scene.records)*400*254,
        nativeShiftTransfers=scene.transfers,nativePaletteChecks=scene.palette_checks,sourceGraphicsStreams=len(scene.buffers),
        rejectedActualPixelTargetFaults=scene.counterexamples,retainedOriginalPositiveControl=positive,
        actualPhaseFrames={f'{p:08X}':v[0]for p,v in phase_images.items()},finalVictimPixels=later[-1]['body'][str(side)]['pixels'],
        rawRasterVRAMAudioROMCopiesWritten=0,essentialNativeReviewPNGsWritten=1,
        palettePhysicalIds=sorted({r['id']for r in PALETTES}),sourceFIFOProjectionShadowQualificationPending=True,
        actualNativeHeldWinnerPageAfterPointersClear=True,postRetirementNewVictimFIFO=0,postRetirementNewRender=False,
        victimPixelsOnHeldWinnerPage=later[-1]['body'][str(side)]['pixels'],secondaryPixelsOnHeldWinnerPage=later[-1]['nativeSecondarySplitPixels'],
        allClearPixelsAfterPointersAccepted=False,stockHeldWinnerPageComparisonPending=True,
        aestheticArtAcceptance=False,allContextsAcceptance=False,campaignAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists()and not REVIEW.exists(),'Never overwrite evidence')
    REVIEW.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(REVIEW)],capture_output=True).returncode==0,'Review leaf compressed before writes')
    completed=[]
    try:
        for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
            # The original helper is restored for each retained control before
            # using the explicit true-stock palette function for the new run.
            from verify_finish_display_v798 import check_owned_body_palette
            model.check_owned_body_palette=check_owned_body_palette
            completed.append(run(fighter,side))
        report=dict(passed=True,cases=completed,fullPortAcceptance=False)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compression')
    report['completedContexts']=[dict(fighter=c['fighter'],side=c['side'],exactFields=c['exactFields'])for c in completed]
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='cases'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
