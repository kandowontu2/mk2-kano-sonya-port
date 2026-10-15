"""Find unpressed native Tomb mirror drops through ordinary command timing.

Every cold run earns full-health two-round wins and paid native arena advance,
then retains the full original input/801-field/1100-retirement contract. The
RNG register/state is never set. Actual initialized guests remain in RAM;
only compressed text, digest and source snapshots are written. A held result
is retained as held, not relabeled a drop or all-stage art/audio acceptance.
"""
import argparse,concurrent.futures,hashlib,json,os,re,shutil,subprocess,sys,traceback
from pathlib import Path
import verify_tomb_mirror_native_branches_v4357 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
NAME=native.runtime.old.NAME
DRIVER='mk2ks_tomb_mirror_random_timing_driver_ram_v4453.lua'
OBSERVER='mk2ks_tomb_mirror_random_timing_provenance_ram_v4454.lua'
OUT=ROOT/'audit_v4456_tomb_mirror_random_timing_search'
DEPENDENCIES=(DRIVER,OBSERVER,'mk2ks_current_stage_ram_driver_v3594.lua',
              'mk2ks_current_stage_provenance_v3595.lua')

def preflight():
    old=(ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua').read_text()
    actual=(ROOT/DRIVER).read_text()
    boundary="assert(load(source,'@complete3594_true_mirror_ram_only_4340','t',_ENV))()\n"
    need(old.count(boundary)==1,'One exact complete original driver execution')
    prefix=old[:old.index(boundary)].replace(
       ' "  -- The read-only audio observer sends the whole guest to verifier RAM.")',
       ' "  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\\n  _tomb_timing_guest(raw)")')
    need(actual.startswith(prefix) and actual.count("replace('frame-window>=65 then','frame-window>='..(65+delay)..' then')")==1,
         'Entire original mirror driver retained, only native command wait and RAM guest sink added')
    suffix=actual[len(prefix):]
    need(not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',suffix),
         'No RNG/health/identity/position/AI/register assistance')
    observer=(ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua').read_text().replace(
       "dofile('mk2ks_tomb_mirror_driver_ram_v4340.lua')",f"dofile('{DRIVER}')").replace(
       '@complete3595_true_mirror_pc_qualified_4341','@complete3595_true_mirror_pc_qualified_command_delay_4454')
    need((ROOT/OBSERVER).read_text()==observer,'Every original native branch/PC/actor/motion read retained')
    return dict(passed=True,physicalCommandWaitOnlyChanged=True,nativeRNGStateUntouched=True,
       originalHealthInput801Field1100CleanupContractRetained=True,
       driverSHA256=sha(ROOT/DRIVER),observerSHA256=sha(ROOT/OBSERVER),fullPortAcceptance=False)

def capture(fighter,side,delay,guest):
    folder=OUT/f'{fighter}_p{side}_delay{delay:02d}'
    need(not folder.exists(),'Fresh actual timing trial, never restart an executed leaf')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p).resolve() for p in build['input_hashes']}
    files.update((candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
       ROOT/'mk2/mk2-maincpu.bin',Path(__file__).resolve()))
    files.update(ROOT/n for n in DEPENDENCIES)
    for module in tuple(sys.modules.values()):
        p=getattr(module,'__file__',None)
        if p and Path(p).suffix=='.py' and Path(p).resolve().is_relative_to(ROOT/'tools'):files.add(Path(p).resolve())
    for leaf in ('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve() for p in files if p.is_file()};pins={str(p):sha(p) for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()) and
       sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982' and
       sha(candidate/'roms/mk2ks/mk2ks.mdata')=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',
       'Every actual3836 compiled source and playable byte bound')
    folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,
                         'Compress fresh capture before writes')
    frozen={}
    for p in files:
        if p.suffix in ('.lua','.py','.ps1','.json'):
            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);need(sha(dest)==pins[str(p)],'Exact source snapshot');frozen[str(p)]=str(dest)
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    (folder/'source_snapshot_paths.json').write_text(json.dumps(frozen,indent=2)+'\n')
    env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_ARENA='1',
       MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder),MK2KS_TOMB_COMMAND_DELAY=str(delay))
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
       '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
       '-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
       '-nothrottle','-str','900','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
       '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/OBSERVER)]
    guest_sha=None
    with (folder/'stderr.log').open('w',encoding='utf-8') as errors,subprocess.Popen(command,cwd=ROOT,env=env,
          stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict') as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print(f'{fighter}P{side} ordinary delay{delay}: native pid={process.pid}',flush=True)
        with (folder/'run.log').open('w',encoding='utf-8') as log:
            for line in process.stdout:
                if line.startswith('MK2_TOMB_TIMING_GUEST '):
                    row=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(row.pop('hex'))
                    need(guest_sha is None and row==dict(frame='1',bytes='1048576') and raw==guest,
                         'Every actual initialized native guest byte independently compared in RAM')
                    guest_sha=hashlib.sha256(raw).hexdigest().upper()
                    log.write('MK2_TOMB_TIMING_GUEST_DIGEST frame=1 bytes=1048576 sha256='+guest_sha+'\n')
                else:
                    need('hex=' not in line,'No encoded guest/raster/PCM persisted');log.write(line)
                    if line.startswith(('MK2_STAGE_COMMAND ','MK2_STAGE_PROVENANCE_BRANCH ','MK2_STAGE_RESULT ')):log.flush()
        code=process.wait()
    log=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
    meta=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,physicalCommandDelay=delay,
       guestSHA256=guest_sha,input_hashes=pins,assistance='none',guest_writes=0,cheats_enabled=False,
       rawRasterAudioROMBuildCopiesWritten=0,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    need(code==0 and guest_sha==hashlib.sha256(guest).hexdigest().upper() and
       not re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|WRONG CHECKSUMS|HOST_DEADLINE',log+errors,re.I),
       'Actual complete native terminal0, no fallback or runtime error')
    need(not any(p.suffix in ('.png','.wav','.bin','.exe','.mdata') for p in folder.rglob('*') if p.is_file()),
       'No raw media/ROM/new builds on disk')
    need(all(sha(p)==h for p,h in pins.items()),'Every executed source unchanged')
    checked=native.branch(log,guest,fighter,side)
    return dict(passed=True,capture=str(folder),fighter=fighter,side=side,physicalDelay=delay,nativeBranch=checked,
       originalEarnedContractPassed=True,noForcedNativeState=True,fullPortAcceptance=False)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),default='kano')
    parser.add_argument('--side',type=int,choices=(1,2),default=1)
    parser.add_argument('--first',type=int,default=1);parser.add_argument('--last',type=int,default=20)
    args=parser.parse_args();need(1<=args.first<=args.last<=80,'Finite declared ordinary timing range')
    report_path=OUT/f'search_{args.fighter}_p{args.side}_{args.first:02d}_{args.last:02d}.json'
    need(not report_path.exists(),'Fresh immutable search range')
    proof=preflight();guest=native.runtime.old.expected()
    OUT.mkdir(exist_ok=True)
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
         'Compress text search evidence before writes')
    trials=[]
    for first in range(args.first,args.last+1,4):
        delays=list(range(first,min(first+4,args.last+1)))
        need(all(not (OUT/f'{args.fighter}_p{args.side}_delay{d:02d}').exists() for d in delays),
             'Every new timing leaf unused')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda d:capture(args.fighter,args.side,d,guest),delays))
        for r in results:
            trials.append(r)
            print(json.dumps(dict(delay=r['physicalDelay'],nativeRandom=r['nativeBranch']['actualNativeRandomValue'],
               actualUnpressedNativeDrop=r['nativeBranch']['nativeDrop'],originalEarnedContractPassed=True)),flush=True)
        if any(r['nativeBranch']['nativeDrop'] for r in results):break
    found=[r for r in trials if r['nativeBranch']['nativeDrop']]
    report=dict(passed=True,sourcePreflight=proof,actualTrials=trials,nativeDropsFound=found,
       allStartedRunsActuallyTerminal=True,searchNotStatisticalRNGOrAIClaim=True,
       fullSceneRasterShadowAudioAccepted=False,allMirrorBranchContextsAccepted=False,fullPortAcceptance=False)
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(report=str(report_path),actualTrials=len(trials),actualNativeDropsFound=len(found)),indent=2),flush=True)

if __name__=='__main__':main()
