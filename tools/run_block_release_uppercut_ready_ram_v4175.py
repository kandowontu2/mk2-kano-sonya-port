"""Current3836 physical P2 ordinary uppercut; original2151 controller unchanged.

Only media sinks use RAM. Original2153 whole paired timeline/contact/recovery/
follow-up checker retained. A clean ordinary action is not full port acceptance.
"""
import hashlib,inspect,json,os,re,shutil,struct,subprocess,sys,traceback
from pathlib import Path
import run_sonya_guard_uppercut_ready_campaign_v4145 as current
import verify_current_human_uppercut_clean_v2153 as original
import run_current_clean_uppercut_ram_v4155 as prior

ROOT,need,sha=current.ROOT,current.need,current.sha
LUA='mk2ks_block_release_uppercut_ready_ram_v4174.lua'
FOLDER=ROOT/'audit_v4176_current_sonya_p2_block_release_uppercut_ready_ram'
OUT=ROOT/'audit_v4177_current_sonya_p2_block_release_uppercut_ready_checked'

def original_ram_boundary():
    old=(ROOT/'mk2ks_human_uppercut_clean_v2151.lua').read_text()
    actual=(ROOT/'mk2ks_clean_uppercut_ram_v4154.lua').read_text()
    helpers="""-- Only four original media sinks are replaced with RAM transport.
local function ramhex(raw)return (raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end))end
local function ramframe(screen,name)
 local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==400*254*4)
 print(string.format('MK2_UPPERCUT_RAM_FRAME filename=%s width=%d height=%d bytes=%d hex=%s',name,width,height,#raw,ramhex(raw)))
end
"""
    need(actual.count(helpers)==1,'One output-only RAM helper')
    restored=actual.replace(helpers,'',1)
    sink="  print('MK2_UPPERCUT_GUEST_RAM frame=1 bytes=1048576 hex='..ramhex(raw))"
    need(restored.count(sink)==1,'One full guest RAM transport')
    restored=restored.replace(sink,"  local file=assert(io.open(assert(os.getenv('MK2KS_HUMAN_ORDINARY_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()",1)
    for name in ('special_before.png','special_recovered.png','special_final.png'):
        a=f"ramframe(screen,'{name}')"
        need(restored.count(a)==1,'One native RGB transport: '+name)
        restored=restored.replace(a,f"screen:snapshot('{name}')",1)
    need(restored==old,'Entire original2151 cold selection, physical input, native observers and follow-up unchanged except four media sinks')
    original.restore_driver(restored)
    need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)|\bdofile\s*\(|\bload\s*\(|screen:snapshot|io.open',actual),'No guest assistance or persistent media sinks')

def boundary():
    original_ram_boundary()
    old=(ROOT/'mk2ks_clean_uppercut_ram_v4154.lua').read_text()
    changes=[("   elseif clean(own)and clean(victim)then", "   elseif clean(victim)and own.y==own.floor and own.vx==0 and own.vy==0 and own.gravity==0 and own.flags&0x1c==0 and own.body&4==0 and (clean(own)or own.action==0 or own.action==0x303 or own.action==0x701)then"),
      ('    settle=settle or frame','    settle=settle or frame\n    if frame-settle<120 then input(side,\'Down\');input(side,\'Block\')end'),
      ("pulse(side,'High Punch',age,6,3)\n   elseif move=='leg'", "pulse(side,'High Punch',age,1,3)\n   elseif move=='leg'"),
      ("if frame>=3000 and not ready then log('FAILED','reason=no_actual_match_ready')", "if frame>=3000 and not command then log('FAILED','reason=no_actual_guarded_command_ready')")]
    for a,b in changes:
        need(old.count(a)==1,'Unique original physical guard-release edit');old=old.replace(a,b,1)
    need(old==(ROOT/LUA).read_text(),'Only genuine Down/Block120field preparation, guarded readiness and HP1..3 physical timing change')

def verify_log(log,move,side):
    code=inspect.getsource(original.verify_log)
    edits=[("plan=[('Down',0,9),('High_Punch',6,3)]", "plan=[('Down',0,9),('High_Punch',1,3)]"),
      ("need(not any(result['command']-120<=row['frame']<result['command']for row in inputs),\n         'At least120actual fields of neutral physical input before Down/HP')",
       "need({(row['frame'],row['slot'],row['button']) for row in inputs if result['command']-120<=row['frame']<result['command']}=={(result['command']-at,side,button) for at in range(1,121) for button in ('Down','Block')}, 'Exactly120actual fields of physical Down/Block before releasing Block and HP1..3')")]
    for a,b in edits:
        need(code.count(a)==1,'Unique original whole verifier physical-plan adaptation');code=code.replace(a,b,1)
    scope=dict(vars(original));exec(compile(code,__file__+'::original_whole_state_and_contact_grammar','exec'),scope)
    return scope['verify_log'](log,move,side)

def main():
    need(not FOLDER.exists() and not OUT.exists(),'Fresh immutable leaves')
    boundary()
    guest=current.expected()
    native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    first=(0xff870dc0-0xff800000)//8;last=(0xff871030-0xff800000)//8
    need(guest[first:last]==native[first:last],'Entire original HUMAN uppercut routine unchanged in current3836')
    for address,words in ((0xff870e30,(0x1b89,)),(0xff870f50,(0x09c1,0x0107)),(0xff871000,(0xc080,0x73f0,0xff83))):
        need(struct.unpack_from('<'+'H'*len(words),native,(address-0xff800000)//8)==words,'Original HUMAN28/action107/native attack signature')
    candidate=ROOT/current.NAME
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files=set(map(Path,build['input_hashes']))|{candidate/'build-info.json',candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',ROOT/LUA,ROOT/'mk2ks_human_uppercut_clean_v2151.lua',ROOT/'mk2ks_human_special_matrix_v3.lua',ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'art_reference_mileena_v3801/reference.json',Path(__file__).resolve()}
    for module in tuple(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path and Path(path).suffix=='.py' and Path(path).resolve().is_relative_to(ROOT/'tools'):files.add(Path(path))
    for leaf in ('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    pins={str(p.resolve()):sha(p) for p in files if p.is_file()}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'All actual compiled inputs unchanged')
    need(pins[str((candidate/'mkport_candidate.exe').resolve())]=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982' and pins[str((candidate/'roms/mk2ks/mk2ks.mdata').resolve())]=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24','Exact current3836 executable/payload')
    FOLDER.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(FOLDER)],capture_output=True).returncode==0,'Capture compressed before writes')
    snapshots={}
    for path,digest in pins.items():
        p=Path(path);need(p.is_relative_to(ROOT),'Workspace input only')
        if p.suffix in ('.lua','.py','.ps1','.json'):
            dest=FOLDER/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            need(sha(dest)==digest,'Exact frozen source');snapshots[path]=str(dest)
    (FOLDER/'source_snapshot_paths.json').write_text(json.dumps(snapshots,indent=2)+'\n')
    (FOLDER/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_HUMAN_ORDINARY_OUT=str(FOLDER),MK2KS_HUMAN_SPECIAL_MOVE='uppercut_sonya',MK2KS_HUMAN_SPECIAL_SIDE='2',MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='sub_zero')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),'-artpath',str(ROOT/'artwork'),'-samplepath',str(ROOT/'samples'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(FOLDER),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254','-cfg_directory',str(FOLDER/'cfg'),'-nvram_directory',str(FOLDER/'nvram'),'-snapshot_directory',str(FOLDER/'snap'),'-autoboot_script',str(ROOT/LUA)]
    frames=[];proof=None
    with (FOLDER/'stderr.log').open('w',encoding='utf-8') as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict') as process:
        (FOLDER/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print('Clean native P2 uppercut started pid='+str(process.pid),flush=True)
        with (FOLDER/'run.log').open('w',encoding='utf-8') as log:
            for line in process.stdout:
                if line.startswith(('MK2_UPPERCUT_GUEST_RAM ','MK2_UPPERCUT_RAM_FRAME ')):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper()
                    if line.startswith('MK2_UPPERCUT_GUEST_RAM '):
                        need(proof is None and raw==guest and h['frame']=='1' and h['bytes']=='1048576','Every byte of actual initialized guest compared independently in RAM')
                        proof=dict(h,everyActualByteComparedInRAM=True,guestDumpFilesWritten=0,executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],captureSourceSHA256=sha(__file__),transportSourceSHA256=sha(ROOT/LUA))
                        (FOLDER/'guest_memory_proof.json').write_text(json.dumps(proof,indent=2)+'\n')
                        tag='MK2_UPPERCUT_GUEST_RAM_DIGEST '
                    else:
                        need(len(raw)==400*254*4 and h['width']=='400' and h['height']=='254' and int(h['bytes'])==len(raw),'Complete actual RGB32 callback only in RAM')
                        frames.append(h);tag='MK2_UPPERCUT_RAM_FRAME_DIGEST '
                    log.write(tag+' '.join(f'{k}={v}' for k,v in h.items())+'\n');log.flush()
                    del raw
                else:
                    need('hex=' not in line,'No raw media in persistent log');log.write(line)
                    if line.startswith(('MK2_HSPECIAL_COMMAND ','MK2_HSPECIAL_RECOVERED ','MK2_HSPECIAL_FAILED ','MK2_HSPECIAL_RESULT ')):print(line.strip(),flush=True);log.flush()
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'Every executed input unchanged')
    meta=dict(exit_code=code,candidate=current.NAME,move='uppercut_sonya',side=2,air=False,victim='sub_zero',assistance='none',cheats_enabled=False,executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],input_hashes=pins,rawRasterFilesWritten=0,rawAudioFilesWritten=0,guestDumpFilesWritten=0,actualNativeFrameCallbacks=frames,passed=False,fullPortAcceptance=False)
    (FOLDER/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    need(code==0 and proof and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS',(FOLDER/'run.log').read_text()+(FOLDER/'stderr.log').read_text(),re.I),'Terminal runtime success')
    log=(FOLDER/'run.log').read_text()
    positive=verify_log(log,'uppercut_sonya',2)
    need([h['filename'] for h in frames]==['special_before.png','special_recovered.png','special_final.png'],'Original three native callbacks retained in RAM')
    faults={}
    def reject(name,changed):
        need(changed!=log,'Actual positive witness mutated')
        try:verify_log(changed,'uppercut_sonya',2)
        except Exception as error:faults[name]=str(error)
        else:raise AssertionError('Fault not rejected: '+name)
    for name,tag,old,new in (('wrong_own_identity','FIELD','id=18 ','id=17 '),('unexplained_health','FIELD','hp=161 ','hp=160 '),('wrong_native_entry_pc','EVENT','pc=FF870DD0 ','pc=FF870DE00 '),('wrong_command_button','INPUT','button=Down','button=Up')):
        lines=log.splitlines();index=next(i for i,line in enumerate(lines) if line.startswith('MK2_HSPECIAL_'+tag+' ') and old in line and (tag!='FIELD' or 'slot=2 ' in line) and (tag!='INPUT' or 'slot=2 ' in line))
        lines[index]=lines[index].replace(old,new,1);reject(name,'\n'.join(lines)+'\n')
    lines=[line.replace('action=263','action=262') if line.startswith('MK2_HSPECIAL_FIELD ') and 'slot=2 ' in line and 'action=263' in line else line for line in log.splitlines()]
    reject('cpu106_cannot_substitute_human107','\n'.join(lines)+'\n')
    allpins=dict(pins)
    for p in FOLDER.rglob('*'):
        if p.is_file():allpins[str(p.resolve())]=sha(p)
    need(not any(p.suffix in ('.bin','.png','.wav') for p in FOLDER.rglob('*') if p.is_file()),'No new native media dump files')
    return dict(passed=True,positive=positive,actualFaultsRejected=faults,inputHashes=allpins,fullGuestAcceptedInRAM=True,originalWholeStateContactRecoveryFollowupGrammarRetained=True,physicalPreparation='Down+Block120 then Down9/HP1..3; no guest assistance',fullMoveArtGroundShadowAudioAccepted=False,fullPortAcceptance=False,scope='One current3836 true SonyaP2 physical block-release uppercut versus passive SubZero8; not a live CPU strategy, full move art/audio/shadow or whole tower proof.')

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
