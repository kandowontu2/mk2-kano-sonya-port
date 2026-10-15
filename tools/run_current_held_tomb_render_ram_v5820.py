"""Current5219 earned unpressed held mirror Tomb rendering in RAM.

All original3648 scene/FIFO/projection/owned-shadow/native-motion gates are
retained, with actual held-branch references and full4344 earned input gates.
No overrides, target anchors or native raster/VRAM/PCM/ROM copies on disk.
One full scene first; no full-stage/audio/port acceptance claim.
"""
import argparse,gzip,hashlib,inspect,json,os,re,shutil,subprocess,sys,time,traceback
from pathlib import Path
import numpy as np
import run_current_tomb_ram_matrix_v3648 as old
import run_tomb_mirror_audio_ram_v4350 as audio
import tomb_mirror_render_model_v4360 as model
import verify_tomb_mirror_contract_v4344 as native
import verify_tomb_mirror_native_branches_v4357 as branches
import current_payload_metadata_context_v5229 as current
import run_current_tomb_winner_mix_v5781 as timing
ROOT,need,sha=audio.ROOT,audio.need,audio.sha
NAME=current.NAME
OBSERVER=ROOT/'mk2ks_current_held_tomb_display_ram_v5821.lua'


original_contract_source=inspect.getsource(old.scene_contract)
contract_source=original_contract_source.replace("old=(reference/'run.log').read_text(encoding='utf-8-sig')", "with gzip.open(reference/'run.log.gz','rt')as reader:old=reader.read()",1)
scope=dict(old.__dict__);scope.update(model=model,native=native,gzip=gzip)
exec(compile(contract_source,'<entire3648_scene_contract_true_mirror_earned_gates>','exec'),scope)
scene_contract=scope['scene_contract']

def paths(fighter,side):
    need(fighter in ('kano','sonya')and side in (1,2),'Exact both true character/physical slot matrix')
    return ROOT/f'audit_v5822_current_held_tomb_{fighter}_p{side}_render_ram',ROOT/f'audit_v5823_current_held_tomb_{fighter}_p{side}_render_checked'


def controls():
    source=(ROOT/'mk2ks_native_tomb_display_v2062.lua').read_text()
    changes={"dofile('mk2ks_stage_branch_provenance_v1722.lua')":"dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')",
      "local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()":'MK2KS_TOMB_RAM_SAVE(file,raw)',
      'screen:snapshot(file)':'MK2KS_TOMB_RAM_PIXELS(file)'}
    for before,after in changes.items():
        need(source.count(before)==1,'Every original2062 observer sink/driver adaptation identified exactly once')
        source=source.replace(before,after)
    need(not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)|io\.open|snapshot\(',source),
         'Entire original observer retained read-only with no output disk sinks')
    wrapper=(ROOT/'mk2ks_native_tomb_ram_v3624.lua').read_text()
    need(wrapper.count('assert(count==1)')==3 and not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',wrapper),
         'Original full RAM sinks and no controls/guest/register writes')
    need(model.source==inspect.getsource(model.original.Model).replace(
      'len(self.ids)==2 and set(self.ids)=={17,18}','self.ids in ((17,18),(18,17),(17,17),(18,18))'),
      'Exactly one tuple admission change, all continuous raster gates intact')
    need(contract_source==inspect.getsource(old.scene_contract).replace("old=(reference/'run.log').read_text(encoding='utf-8-sig')", "with gzip.open(reference/'run.log.gz','rt')as reader:old=reader.read()",1),'Entire original scene/FIFO/shadow/ground/erase gates retained')
    current.expected()
    pre=json.loads((timing.source.OUT/'report.json').read_text())
    need(pre['passed']and all(sha(p)==h for p,h in pre['inputHashes'].items()),
         'Whole current original unpressed driver/source and immutable completed audio proof retained')
    expected=(ROOT/'mk2ks_tomb_mirror_display_ram_v4359.lua').read_text().replace(
      "dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')",
      "dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')").replace(
      '@complete3624_native_mirror_scene_RAM_sinks_4359',
      '@complete3624_native_held_mirror_scene_RAM_sinks_5821')
    expected+="emu.register_frame_done(function()\n if emu.time()>=890 then\n  print('MK2_CURRENT_TOMB_RENDER_DEADLINE writes=0 assistance=none')\n  manager.machine:exit()\n end\nend)\n"
    need(OBSERVER.read_text()==expected,'Entire native RGB/FIFO/DMA observer unchanged, only declared timing-driver target')
    return hashlib.sha256(source.encode()).hexdigest().upper()

def preflight(guest,payload,image):
    digest=controls()
    for ids in ((17,18),(18,17),(17,17),(18,18)):
        need(model.Model(guest,payload,image,ids).ids==ids,'Exact declared actual slot tuple')
    rejected=[]
    for ids in ((17,1),(1,17),(18,0),(17,),(17,18,17)):
        try:model.Model(guest,payload,image,ids)
        except ValueError:rejected.append(ids)
        else:raise ValueError('Proxy/invalid physical IDs admitted')
    need(len(rejected)==5,'All invalid/proxy tuples rejected')
    return dict(observerSHA256=digest,modelSHA256=model.MODEL_SOURCE_SHA256,
      sceneContractSHA256=hashlib.sha256(contract_source.encode()).hexdigest().upper(),
      earnedContractSHA256=native.CONTRACT_SHA256,rejectedProxyTuples=rejected)

def run(fighter,side):
    CASE,OUT=paths(fighter,side)
    need(not CASE.exists()and not OUT.exists(),'Fresh immutable current5219 native mirror scene')
    identity=17 if fighter=='kano'else 18;ids=(identity,identity)
    matrixpath=ROOT/'audit_v5786_current_enabled_tomb_winner_mix_checked/report.json'
    matrix=json.loads(matrixpath.read_text())
    need(matrix['passed']and matrix['actualCurrentBothCharactersBothSidesHeldTombEnabledWinnerMixAccepted'],
         'Actual complete current four-case unpressed native state/audio proof')
    case=next(c for c in matrix['cases']if c['fighter']==fighter and c['physicalSlot']==side)
    branch_reference=case['sourceQualifiedNativeBranch']
    need(not branch_reference['nativeDrop']and branch_reference['nativeMotion']['continuousArena1MotionCallbacks']>400,
         'Exactly the real original held branch, no drop or pressed substitution')
    reference=Path(case['capture'])
    need(sha(reference/'run.log.gz')==matrix['inputHashes'][str(reference/'run.log.gz')],
         'Frozen actual current same-role native controls reference')
    guest=current.expected();candidate=ROOT/NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    graphics_pins={};image=old.source_graphics(payload,graphics_pins);proof=preflight(guest,payload,image)
    retained=json.loads((ROOT/'audit_v3635_current_native_tomb_ram_checked/report.json').read_text())
    need(retained['passed']and retained['retainedOriginalPositiveControl']['passed'],'Original source-perfect raster positive control retained')
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p)for p in build['input_hashes']}|{OBSERVER,Path(__file__).resolve(),Path(model.__file__),
      candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',matrixpath,
      ROOT/'mk2ks_native_tomb_display_v2062.lua',ROOT/'mk2ks_native_tomb_ram_v3624.lua',
      ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua',ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua',
            timing.source.OUT/'report.json',
      ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',ROOT/'mk2ks_current_stage_provenance_v3595.lua',
      reference/'run.log.gz',reference/'result.json',ROOT/'audit_v3635_current_native_tomb_ram_checked/report.json'}
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path and Path(path).resolve().is_relative_to(ROOT/'tools'):files.add(Path(path).resolve())
    files.update(Path(p)for p in graphics_pins)
    for directory in ('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/directory).glob('*'))
    before={str(p.resolve()):sha(p)for p in files if p.is_file()}
    need(all(before[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items())and
      sha(candidate/'mkport_candidate.exe')==build['executable_sha256']==current.EXE_SHA and
      sha(candidate/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256']==current.PAYLOAD_SHA,
      'Exact actual3836 executable/payload and complete compiled source manifest')
    CASE.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(CASE)],capture_output=True).returncode==0,'Compress diagnostic text before writes')
    (CASE/'input_hashes_before.json').write_text(json.dumps(before,indent=2)+'\n')
    # Complete exact input hashes bind existing originals; no source-tree duplicates.
    scene=model.Model(guest,payload,image,ids);transport=model.Transport();errors=[];rgb_records=[];ram_guest=None
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(CASE))
    cmd=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(CASE),
      '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','900',
      '-snapsize','400x254','-cfg_directory',str(CASE/'cfg'),'-nvram_directory',str(CASE/'nvram'),
      '-snapshot_directory',str(CASE/'snap'),'-autoboot_script',str(OBSERVER)]
    with(CASE/'stderr.log').open('wb')as stderr,subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)as process:
        (CASE/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd,startedUnix=time.time(),hostPID=os.getpid(),hostSource=__file__),indent=2)+'\n')
        print(f'{fighter.capitalize()}P{side} true mirror complete native scene RAM pid={process.pid}',flush=True)
        with gzip.open(CASE/'run.log.gz','wt',encoding='utf-8')as log:
            for binary in iter(process.stdout.readline,b''):
                if binary.startswith((b'MK2_TOMB_RAM_BUFFER ',b'MK2_TOMB_RAM_PIXELS ')):
                    header=binary.decode('ascii').strip();row=dict(re.findall(r'(\w+)=([^\s]+)',header))
                    encoded=process.stdout.readline().decode('ascii').strip()
                    try:
                        if binary.startswith(b'MK2_TOMB_RAM_BUFFER '):
                            raw=transport.decode(row,encoded)
                            if row['file']=='guest_maincpu.bin':need(raw==guest,'Every actual initialized current5219 guest byte verified in RAM');ram_guest=model.digest(raw)
                            elif not errors:scene.raw[row['file']]=raw
                            log.write('MK2_TOMB_RAM_BUFFER_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(raw)+'\n')
                        else:
                            need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and
                              row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Complete exact actual native RGB transfer')
                            words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                            rgb=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
                            rgb_records.append(dict(file=row['file'],rgbSHA256=model.digest(rgb.tobytes())))
                            if not errors:scene.rgb[row['file']]=rgb
                            log.write('MK2_TOMB_RAM_PIXELS_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(rgb.tobytes())+'\n')
                    except Exception as error:
                        if not errors:errors.append(dict(header=header,error=repr(error),traceback=traceback.format_exc()))
                elif binary.startswith(b'MK2_TOMB_TIMING_GUEST '):
                    row=dict(re.findall(r'(\w+)=([^\s]+)',binary.decode('ascii')))
                    raw=bytes.fromhex(row.pop('hex'))
                    need(row==dict(frame='1',bytes='1048576') and raw==guest,
                      'Every additional actual timing-driver guest byte verified in RAM, never persisted')
                    log.write('MK2_TOMB_TIMING_GUEST_DIGEST frame=1 bytes=1048576 sha256='+model.digest(raw)+'\n')
                else:
                    need(not re.match(b'^[A-F0-9]{1000}',binary),'No encoded native raster/VRAM/ROM transport on disk')
                    line=binary.decode('utf-8')
                    if not errors:
                        try:scene.line(line)
                        except Exception as error:errors.append(dict(line=re.sub(r'\bdata=[^\s]+','data=RAM_ONLY',line.rstrip()),error=repr(error),traceback=traceback.format_exc()))
                    # Validate all complete native graphics streams in RAM; persist
                    # only a source-bound digest, not a new sprite/ROM copy.
                    if re.search(r'\bdata=',line):
                        data=re.search(r'\bdata=([^\s]+)',line).group(1)
                        line=re.sub(r'\bdata=[^\s]+','data_sha256='+hashlib.sha256(bytes.fromhex(data)).hexdigest().upper(),line)
                    log.write(line)
                    if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and len(scene.records)%100==0 and scene.records:
                        print(f'{fighter.capitalize()}P{side} mirror {len(scene.records)} whole fields exact; {scene.transfers} native erase transfers',flush=True)
        code=process.wait()
    with gzip.open(CASE/'run.log.gz','rt')as reader:text=reader.read()
    stderr=(CASE/'stderr.log').read_text()
    terminal=dict(captureCompleted=True,exit_code=code,candidate=NAME,fighter=fighter,side=side,truePhysicalIDs=ids,
      guest_writes=0,assistance='none',cheats_enabled=False,input_hashes=before,ramGuestSHA256=ram_guest,
      observedRGBFields=len(rgb_records),modelExactFields=len(scene.records),modelErrors=errors,
      executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],rawImageAudioVRAMROMCopiesWritten=0,fullPortAcceptance=False)
    (CASE/'result.json').write_text(json.dumps(terminal,indent=2)+'\n')
    (CASE/'buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\n')
    (CASE/'visible_digests.json').write_text(json.dumps(rgb_records,indent=2)+'\n')
    (CASE/'continuous_scene_records.json').write_text(json.dumps(scene.records,indent=2)+'\n')
    need(code==0 and not errors and ram_guest==model.digest(guest)and not re.search(
      r'LUA ERROR|Lua error|stack traceback|Fatal error|WRONG CHECKSUMS|might not run correctly|MK2_CURRENT_TOMB_RENDER_DEADLINE',text+stderr,re.I),
      'Actual terminal, whole current5219 guest and entire continuous native scene model')
    need(not list(CASE.rglob('*.png'))and not list(CASE.rglob('*.wav'))and not list(CASE.rglob('*.bin')),
      'No raw native image/audio/VRAM/ROM files created')
    contract=scene_contract(scene,text,guest,payload,fighter,side,reference,ids)
    branch=branches.branch(text,guest,fighter,side)
    need(not branch['nativeDrop']and branch==branch_reference,
      'Exact actual independently-qualified unpressed held phase, not a random or pressed drop')
    palettes={n:sorted({bool(q['body']&64)for q in scene.groups['FLOOR_QUEUE']if q['slot']==n})for n in(1,2)}
    need(palettes=={1:[False],2:[True]},'Normal native mirror selection gives exactly P1normal/P2alternate, no forced flags')
    need(all(sha(file)==h for file,h in before.items()),'Every actual executed relevant input byte unchanged')
    pins=dict(before)
    for p in CASE.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    return dict(passed=True,candidate=NAME,fighter=fighter,side=side,truePhysicalIDs=ids,inputHashes=pins,
      actualCurrentHeldMirrorNativeTombWholeRenderPaletteShadowEraseAccepted=True,
      sourcePreflight=proof,nativeScene=contract,nativeBranch=branch,nativeMirrorPaletteSelectors=palettes,
      sampledFrames=len(scene.records),exactRGBPixels=len(scene.records)*400*254,
      continuousExactPreBuffers=scene.pre_count,continuousExactFlips=scene.flip_count,
      nativeShiftLoads=scene.loads,nativeShiftFills=scene.fills,nativeShiftTransfers=scene.transfers,
      exactCPUWrites=scene.cpu_count,fullPhysicalPaletteChecks=scene.palette_checks,
      actualPixelFaultsRejected=scene.counterexamples,oneInitialBaseOnly=True,laterTargetsNeverUsedAsAnchors=True,
      allMirrorBranchesAndSlotsAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,
      rawImageAudioVRAMROMCopiesWritten=0,publicPlayableOrReleaseChanged=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    CASE,OUT=paths(args.fighter,args.side)
    try:report=run(args.fighter,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite actual native scene result');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','nativeScene','nativeBranch')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
