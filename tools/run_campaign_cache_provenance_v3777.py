"""Unmodified3680, original3485 cold P2 controls; diagnose cache corruption only.

No state assistance or art/audio files. Six old PNG sinks are suppressed;
read taps log actual lookup/cache provenance. Not a campaign acceptance gate.
"""
import hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3778_campaign_cache_provenance'
LUA=ROOT/'mk2ks_campaign_cache_provenance_v3776.lua'
def run():
    need(not OUT.exists(),'Fresh immutable diagnostic leaf')
    candidate=ROOT/current.NAME
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p)for p in build['input_hashes']}|{candidate/'build-info.json',candidate/'mkport_candidate.exe',
      candidate/'roms/mk2ks/mk2ks.mdata',LUA,Path(__file__).resolve(),ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'}
    for leaf in ('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Exact compiled inputs')
    need(pins[str(candidate/'mkport_candidate.exe')]=='BF5D90F90E6A254C4BCB63B4C0D3974C08DF9F28A817BD35A6F86FE68ABE6A41','Actual3680 unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Inherited compression')
    for p in (LUA,Path(__file__).resolve(),ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'):
        dest=OUT/'input_sources'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    (OUT/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
      MK2KS_TWO_PLAYER='0',MK2KS_CAMPAIGN_OUT=str(OUT),MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='zoning',
      MK2KS_BOSS_PHYSICAL_POLICY='shao_ring_retreat')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat',
      '-inipath',str(OUT),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','4500',
      '-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(LUA)]
    with (OUT/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        (OUT/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print('Actual3680 read-only provenance pid='+str(process.pid),flush=True)
        with (OUT/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                need('hex='not in line,'No encoded raster persisted');log.write(line)
                if line.startswith('MK2_CACHE_PROVENANCE_')and 'SUPPRESSED'not in line or line.startswith('MK2_NAT_CAMPAIGN_STAGE '):
                    log.flush();print(line.strip(),flush=True)
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged')
    return dict(terminalExitCode=code,diagnosticOnly=True,candidate=current.NAME,input_hashes=pins,
      fullPortAcceptance=False,scope=__doc__,actualRasterFiles=[str(p)for p in OUT.rglob('*.png')],actualAudioFiles=[str(p)for p in OUT.rglob('*.wav')])
if __name__=='__main__':
    try:report=run()
    except Exception as e:report=dict(error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    if OUT.exists()and not(OUT/'result.json').exists():(OUT/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report.get('terminalExitCode')==0 else 1)
