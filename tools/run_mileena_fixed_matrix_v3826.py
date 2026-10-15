"""Fresh3822, true Kano/Sonya victims in both physical player slots.

No state assistance or art/audio files. All taps explicitly retained.
Not campaign, raster art or full-port acceptance; actual native finisher path.
"""
import concurrent.futures,hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
current.NAME='diagnostic_v3822_native_mileena_victims'
LUA=ROOT/'mk2ks_mileena_fixed_guest_v3825.lua'
TRACE=ROOT/'mk2ks_cache_provenance_mileena_fixed_v3823.lua'
DRIVER=ROOT/'mk2ks_mileena_earned_fixed_v3824.lua'
def run(context):
    fighter,side=context
    OUT=ROOT/f'audit_v3827_mileena_{fighter}_p{side}_fixed'
    need(not OUT.exists(),'Fresh immutable diagnostic leaf')
    candidate=ROOT/current.NAME
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p)for p in build['input_hashes']}|{candidate/'build-info.json',candidate/'mkport_candidate.exe',
      candidate/'roms/mk2ks/mk2ks.mdata',LUA,TRACE,DRIVER,Path(__file__).resolve()}
    for leaf in ('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Exact compiled inputs')
    need(pins[str(candidate/'mkport_candidate.exe')]==build['executable_sha256'] and build['expected_guest_sha256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821','Actual compiled3822 matched to independent expected guest')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited compression')
    for p in (LUA,TRACE,DRIVER,Path(__file__).resolve()):
        dest=OUT/'input_sources'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    (OUT/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
      MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(OUT),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat',
      '-inipath',str(OUT),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','150',
      '-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(LUA)]
    with (OUT/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        (OUT/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print('Actual3822 read-only provenance pid='+str(process.pid),flush=True)
        with (OUT/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                need('hex='not in line,'No encoded raster persisted');log.write(line)
                if re.match(r'^MK2_MILEENA_V3784_(ACTION|FIRST_LIVE|RESULT|HK_RELEASE|APPROACH|HOST_EXIT) ',line)or re.match(r'^MK2_CACHE_V3823_(ROW|EATEN_TASK|DISAPPEAR|RETIRE|HOST_EXIT|RESULT) ',line):
                    log.flush();print(line.strip(),flush=True)
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged')
    report=dict(terminalExitCode=code,diagnosticOnly=True,candidate=current.NAME,input_hashes=pins,fighter=fighter,side=side,
      fullPortAcceptance=False,scope=__doc__,actualRasterFiles=[str(p)for p in OUT.rglob('*.png')],actualAudioFiles=[str(p)for p in OUT.rglob('*.wav')])
    need(not(OUT/'result.json').exists(),'Immutable result');(OUT/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items()if k!='input_hashes'}
if __name__=='__main__':
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:cases=list(pool.map(run,(('kano',1),('kano',2),('sonya',1),('sonya',2))))
        report=dict(cases=cases,terminal0=all(c['terminalExitCode']==0 for c in cases),fullPortAcceptance=False)
    except Exception as e:report=dict(error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out=ROOT/'audit_v3828_mileena_fixed_matrix_observed';need(not out.exists(),'Fresh immutable matrix observation');out.mkdir()
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report.get('terminal0')else 1)
