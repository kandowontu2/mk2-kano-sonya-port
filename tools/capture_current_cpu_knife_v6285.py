"""Current native CPU knife: unchanged physical script, exact whole guest in RAM.

Natural process terminal is persisted before host semantics; failed observations
are drained on the same handle. No raw media, source-tree copy or new build.
"""
import datetime,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import capture_current_cmd_specials_v6261 as process_tools
import verify_current_kano_cpu_overlap_v1963 as original

ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v6286_current_native_cpu_knife_ram'
LUA=ROOT/'mk2ks_current_cpu_knife_ram_v6284.lua'
CHAIN=('mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_physical_p2_cpu_round_trace_v1940.lua',
       'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua','mk2ks_physical_p2_cpu_knife_trace_v1955.lua')


def capture():
 need(not FOLDER.exists(),'Fresh capture, no restart of executed/pending job')
 need(not process_tools.census(),'Actual native census empty before cold boot')
 guest=current.expected();build=ROOT/current.NAME
 prior_path=ROOT/'audit_v1963_current_kano_cpu_overlap_checked/report.json';prior=json.loads(prior_path.read_text())
 need(prior['passed'],'Existing whole independent CPU knife contact/lifecycle qualification')
 for name in CHAIN:
  p=ROOT/name;need(sha(p)==prior['inputHashes'][str(p.resolve())],'Whole original physical source unchanged: '+name)
  need(not re.search(r'write_u\d+|write_i\d+|:write_|load_?state|:reset\(|\.value\s*=(?!=)',p.read_text()),'No CPU/RNG/actor/HP injection')
 need(sha(original.__file__)==prior['inputHashes'][str(Path(original.__file__).resolve())],'Entire original independent knife gate unchanged')
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in (LUA,Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),
           Path(process_tools.__file__).resolve(),prior_path,*(ROOT/n for n in CHAIN),
           build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json'):
  pins[str(p.resolve())]=sha(p)
 FOLDER.mkdir();(FOLDER/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_ACCEPT_)',k)}
 env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='960',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_PAIR_APPROACH='guard_until_close')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
          '-samplepath',str(ROOT/'samples'),'-samples','-samplerate','48000','-artpath',str(ROOT/'artwork'),
          '-skip_gameinfo','-nocheat','-inipath',str(FOLDER),'-video','none','-sound','none','-nothrottle',
          '-noautoframeskip','-frameskip','0','-str','95','-cfg_directory',str(FOLDER/'cfg'),
          '-nvram_directory',str(FOLDER/'nvram'),'-snapshot_directory',str(FOLDER/'snap'),'-autoboot_script',str(LUA)]
 errors=[];proof=None;scenes=[];identity=None;started=time.time()
 with(FOLDER/'stderr.log').open('w',encoding='utf-8')as err:
  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')
  (FOLDER/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,startedUnix=started),indent=2)+'\n')
  print(json.dumps(dict(nativePID=process.pid,case=FOLDER.name)),flush=True)
  try:
   time.sleep(2);jobs=process_tools.census();(FOLDER/'live_census.json').write_text(json.dumps(jobs,indent=2)+'\n')
   matched=[j for j in jobs if j['ProcessId']==process.pid and j['ExecutablePath'] and
            Path(j['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve() and j['createdUnix']>=started]
   need(len(matched)==1,'Exact current executable/PID/creation identity, not a stale handle');identity=matched[0]
  except Exception as error:errors.append(repr(error))
  with gzip.open(FOLDER/'run.log.gz','wt',encoding='utf-8')as log:
   for line in process.stdout:
    try:
     if line.startswith(('MK2_KNIFE_RAM_RGB ','MK2_KNIFE_RAM_GUEST ')):
      f=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(f.pop('hex'));tag=line.split()[0]
      need(len(raw)==int(f['bytes']),'Complete actual RAM buffer');digest=hashlib.sha256(raw).hexdigest().upper()
      if tag.endswith('_GUEST'):
       need(proof is None and f==dict(frame='1',bytes='1048576')and raw==guest,'Whole current guest independently reconstructed and compared')
       proof=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      else:
       need(len(raw)==406400 and f['width']=='400'and f['height']=='254','Entire native RGB callback')
       scenes.append(dict(**f,sha256=digest))
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+digest+'\n')
     else:
      need('hex='not in line,'Never persist raw media/guest');log.write(line)
      if line.startswith(('MK2_P2CPU_COLD_LIVE ','MK2_CPU_PAIR_COMPLETE ','MK2_CPU_PAIR_INCOMPLETE ','MK2_CPU_PAIR_RESULT ')):
       values=dict(re.findall(r'(\w+)=([^\s]+)',line));print(json.dumps(dict(tag=line.split()[0],**{k:values[k]for k in('frame','cycle','cpu_id','id','vid','complete','follow_regain')if k in values})),flush=True)
    except Exception as error:errors.append(repr(error))
   code=process.wait()
  terminal=dict(pid=process.pid,exitCode=code,naturalTerminal=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),observationErrors=errors)
  (FOLDER/'native_terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
 need(not process_tools.census(),'Same native process naturally terminal and actual census empty')
 report=dict(passed=False,candidate=current.NAME,nativeExit=code,nativeIdentity=identity,proof=proof,actualScenes=scenes,
             inputHashes=pins,newBuilds=0,newZIPs=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,fullPortAcceptance=False)
 try:
  need(code==0 and identity and proof and not errors and not(FOLDER/'stderr.log').read_text().strip(),'Actual native terminal without host/runtime errors')
  need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged')
  with gzip.open(FOLDER/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
  report['independentSemantics']=original.verify(text,guest)
  report['passed']=True
 except Exception as error:report.update(error=repr(error),traceback=traceback.format_exc())
 (FOLDER/'result.json').write_text(json.dumps(report,indent=2)+'\n')
 for p in FOLDER.rglob('*'):
  if p.is_file():
   h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact terminal artifact losslessly compressed')
 print(json.dumps(dict(passed=report['passed'],nativeExit=code,error=report.get('error'),scenes=len(scenes),newBuilds=0)),flush=True)
 need(report['passed'],'Keep actual current CPU knife rejection; no weaker substitute')
 return report


if __name__=='__main__':
 capture()
