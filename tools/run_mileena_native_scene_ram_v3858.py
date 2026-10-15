"""3836 actual swallowing victim full-scene replay; RAM-only native targets.

Retain3625 integer CPU/DMA/shift/scanout model. Source-bound palettes support
actual stock Mileena as well as true17/18, never relabel stock as added IDs.
First diagnostic is KanoP1. Exact pixels are not aesthetic/full-port acceptance.
"""
import hashlib,json,os,re,shutil,struct,subprocess,sys,traceback
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import current_tomb_ram_model_v3625 as model
import run_current_tomb_ram_v3626 as original
import verify_current_ground_shadow_v1859 as graphics
import verify_native_mileena_victim_data_v3819 as data
from verify_finish_display_v798 import raster as finish_format

# Imported modules extend/rebind legacy parser sets at import time. Bind the
# complete original observer schema explicitly after imports, not by luck.
model.raster.base.HEX |= finish_format.HEX | {'entry','frame_table','descriptor','field','before','a0','a1','a3','a7','b14','b10','parent','cursor','row','size','xy','p1','p2','main1','main2'}

ROOT=original.ROOT
NAME='diagnostic_v3836_native_mileena_rom_identity'
OBSERVER=ROOT/'mk2ks_mileena_native_scene_ram_v3853.lua'
CASE=ROOT/'audit_v3859_mileena_kano_p1_native_scene_ram'
OUT=ROOT/'audit_v3860_mileena_native_scene_observed'
REVIEW=ROOT/'art_review_mileena_v3861'
need,sha=original.need,original.sha
PALETTES=[]

def native_palette(q,actual,guest,ids,side):
    hero=q['id'];need(q['slot']==side and q['id']==q['roster'] and hero in(5,17,18),'True native FIFO character/palette owner')
    alternate=bool(q['body']&64)
    if hero in(17,18):
        off=(0xf1500 if hero==17 else 0xf1600)if alternate else(0xfda00 if hero==17 else 0xfdb00)
        need(struct.unpack_from('<H',guest,off)[0]==65,'Added native palette transparent plus64')
    else:
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
    return bytes(image)

def run():
    need(not CASE.exists()and not OUT.exists()and not REVIEW.exists(),'Fresh immutable diagnostic/review leaves')
    # Retained positive tests use the unchanged original helper before adapting
    # only the palette contract to the independently declared actual stock ID.
    positive=original.positive_control()
    model.check_owned_body_palette=native_palette
    base_guest,_,base_payload,_,_=data.old.expected_current()
    candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    pins={};image=sources(payload,pins)
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    need(sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
         hashlib.sha256(guest).hexdigest().upper()==build['expected_guest_sha256'],'Exact actual3836 build and independently reconstructed whole guest')
    files={Path(p)for p in build['input_hashes']}|{Path(p)for p in pins}|{
        OBSERVER,Path(__file__).resolve(),candidate/'build-info.json',candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',
        ROOT/'mk2ks_native_tomb_display_v2062.lua',ROOT/'mk2ks_mileena_earned_fixed_v3824.lua',ROOT/'mk2ks_cache_provenance_mileena_fixed_v3823.lua',
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
    env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(CASE),MK2KS_CAMPAIGN_SIDE='1',MK2KS_PROVENANCE_MIN_FRAME='0',
        MK2KS_STAGE_SIDE='1',MK2KS_STAGE_WINNER='kano',MK2KS_STAGE_OUT=str(CASE))
    cmd=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
        '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
        '-inipath',str(CASE),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
        '-nothrottle','-str','150','-snapsize','400x254','-cfg_directory',str(CASE/'cfg'),'-nvram_directory',str(CASE/'nvram'),
        '-snapshot_directory',str(CASE/'snap'),'-autoboot_script',str(OBSERVER)]
    scene=model.Model(guest,payload,image);transport=model.Transport();errors=[];visible=[];ram_guest=None;phase_images={};last_rgb=None
    with(CASE/'stderr.log').open('wb')as stderr,subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr)as process:
        (CASE/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd),indent=2)+'\n')
        print('Actual3836 native swallowing RAM scene pid='+str(process.pid),flush=True)
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
                                poses={q['pose']for q in scene.groups['FLOOR_QUEUE']if q['frame']==frame-1 and q['slot']==1 and 0xffd61000<=q['pose']<0xffd611c0}
                                for pose in poses:
                                    if pose not in phase_images:phase_images[pose]=(frame,rgb.copy())
                            log.write('MK2_TOMB_RAM_PIXELS_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(rgb.tobytes())+'\n')
                    except Exception as error:
                        if not errors:errors.append(dict(header=header,error=repr(error),traceback=traceback.format_exc()))
                else:
                    need(not re.match(b'^[A-F0-9]{1000}',binary),'No raw native raster/VRAM encoded data on disk')
                    line=binary.decode('utf-8');log.write(line)
                    if not errors:
                        try:scene.line(line)
                        except Exception as error:errors.append(dict(line=line.rstrip(),error=repr(error),traceback=traceback.format_exc()))
                    if re.match(r'^MK2_NAT_CAMPAIGN_FLOOR_(BEGIN|RETIRED|RESULT) ',line)or re.match(r'^MK2_MILEENA_V3784_(ACTION|RESULT) ',line):log.flush();print(line.strip(),flush=True)
        code=process.wait()
    terminal=dict(exit_code=code,candidate=NAME,fighter='kano',side=1,assistance='none',guest_writes=0,ramGuestSHA256=ram_guest,
        observedRGBFields=len(visible),modelExactFields=len(scene.records),modelErrors=errors,input_hashes=pins,
        rawRasterVRAMAudioROMCopiesWritten=0,fullPortAcceptance=False)
    for filename,value in(('result.json',terminal),('buffer_digests.json',transport.records),('visible_digests.json',visible),('continuous_scene_records.json',scene.records),('palette_checks.json',PALETTES)):
        (CASE/filename).write_text(json.dumps(value,indent=2)+'\n')
    need(all(sha(p)==h for p,h in pins.items()),'All actual inputs unchanged')
    log=(CASE/'run.log').read_text();stderr=(CASE/'stderr.log').read_text()
    need(code==0 and not errors and ram_guest==model.digest(guest)and not re.search(r'LUA ERROR|stack traceback|Fatal error|WRONG CHECKSUMS|might not run correctly',log+stderr,re.I),'Actual terminal and unweakened continuous native model')
    need(len(scene.groups['FLOOR_BEGIN'])==len(scene.groups['FLOOR_RETIRED'])==len(scene.groups['FLOOR_RESULT'])==1,'One actual native swallowing victim/removal/completed window')
    begin=scene.groups['FLOOR_BEGIN'][0];retired=scene.groups['FLOOR_RETIRED'][0];result=scene.groups['FLOOR_RESULT'][0]
    need(begin['id']==17 and begin['entry']==0xff9e7d70 and retired['entry']==0xff838f60 and retired['id']==17 and
        retired['actor']==begin['actor']and retired['main']==begin['main']and retired['victim_health']==0,'Actual true Kano original victim task/owner/native disappearance')
    need([r['frame']for r in scene.records]==list(range(begin['origin']+1,retired['frame']+31))and result['snapshots']==len(scene.records),'Every consecutive native field through disappearance plus30')
    need(set(phase_images)=={0xffd61000+i*64 for i in range(7)},'All seven actual owned swallowing poses visible')
    later=[r for r in scene.records if r['frame']>=retired['frame']+3]
    need(later and all(r['body']['1']['pixels']==0 for r in later),'Actual victim erased by native display passes, no persistent body pixels')
    need(scene.pre_count==len(scene.groups['FLOOR_PRE_FRAME'])and scene.flip_count==len(scene.groups['FLOOR_LATCH'])and
         scene.loads==scene.fills>0 and scene.palette_checks>0 and not scene.events and not scene.raw and not scene.rgb,'No omitted native target/shift/palette event')
    # One explicitly essential native QA contact sheet, not an ordinary raster
    # capture archive. No changes to source sprites or runtime game graphics.
    REVIEW.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(REVIEW)],capture_output=True).returncode==0,'Review leaf compressed before write')
    atlas=Image.new('RGB',(800,4*278));draw=ImageDraw.Draw(atlas)
    frames=list(sorted(phase_images.items()))+[(0,(scene.records[-1]['frame'],last_rgb))]
    for i,(pose,(frame,rgb))in enumerate(frames):
        x,y=(i%2)*400,(i//2)*278;atlas.paste(Image.fromarray(rgb),(x,y+24));draw.text((x+4,y+5),f'{pose:08X} native frame {frame}',fill='white')
    atlas.save(REVIEW/'kano-native-swallowing-review.png')
    return dict(passed=True,candidate=NAME,actualKanoP1ContinuousNativeSceneAccepted=True,
        origin=begin['origin'],nativeDisappearance=retired['frame'],exactFields=len(scene.records),exactRGBPixels=len(scene.records)*400*254,
        nativeShiftTransfers=scene.transfers,nativePaletteChecks=scene.palette_checks,sourceGraphicsStreams=len(scene.buffers),
        rejectedActualPixelTargetFaults=scene.counterexamples,retainedOriginalPositiveControl=positive,
        actualPhaseFrames={f'{p:08X}':v[0]for p,v in phase_images.items()},finalVictimPixels=later[-1]['body']['1']['pixels'],
        rawRasterVRAMAudioROMCopiesWritten=0,essentialNativeReviewPNGsWritten=1,
        palettePhysicalIds=sorted({r['id']for r in PALETTES}),sourceFIFOProjectionShadowQualificationPending=True,
        aestheticArtAcceptance=False,allContextsAcceptance=False,campaignAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite evidence')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','retainedOriginalPositiveControl')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
