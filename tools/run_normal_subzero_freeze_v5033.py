"""Physical ordinary ice attempt and thaw/controls, exact RAM-only guest/GFX/RGB."""
import argparse,base64,hashlib,io,json,os,re,subprocess,traceback
from pathlib import Path
from PIL import Image
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
LUA='mk2ks_normal_subzero_freeze_v5031.lua'

def capture(fighter,side):
 folder=ROOT/f'audit_v5034_normal_subzero_{fighter}_p{side}'
 need(not folder.exists(),'Fresh actual ordinary-freeze attempt')
 guest=native.expected();gfx=native.expected_gfx();build=ROOT/native.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 controllers=[ROOT/LUA,ROOT/'mk2ks_stock_fatality_v1021.lua']
 for p in[*controllers,Path(__file__),Path(native.__file__),build/'build-info.json',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata']:
  pins[str(p.resolve())]=sha(p)
 code='\n'.join(p.read_text()for p in controllers)
 need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=))',code),'Only physical input and read-only taps')
 need(all(sha(p)==h for p,h in pins.items()),'Exact immutable compiled inputs')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compress before proof')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',MK2KS_STOCK_COMMAND='ddff_lp',MK2KS_STOCK_GAP='168')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
  '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0',
  '-nothrottle','-str','80','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
  '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
 proof_guest=proof_gfx=None;scenes=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
  print(f'{fighter} P{side} actual ordinary-freeze attempt pid={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_NORMAL_FREEZE_GUEST ','MK2_NORMAL_FREEZE_GFX ','MK2_NORMAL_FREEZE_RGB ')):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     digest=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
     if tag.endswith('_GUEST'):
      need(proof_guest is None and fields==dict(frame='1',bytes='1048576')and raw==guest,'Every actual guest byte compared in RAM')
      proof_guest=dict(bytes=len(raw),sha256=digest,executableSHA256=native.EXE_SHA,everyActualByteComparedInRAM=True,rawGuestFilesWritten=0)
      (folder/'guest_memory_proof.json').write_text(json.dumps(proof_guest,indent=2)+'\n')
     elif tag.endswith('_GFX'):
      need(proof_gfx is None and fields==dict(frame='1',bytes='18976')and raw==gfx,'Every actual owned GFX byte compared in RAM')
      proof_gfx=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      (folder/'gfx_memory_proof.json').write_text(json.dumps(proof_gfx,indent=2)+'\n')
     else:
      need(len(raw)==406400 and fields['width']=='400'and fields['height']=='254'and fields['bytes']=='406400','Actual full native RGB field')
      scenes.append(dict(stage=fields['stage'],frame=int(fields['frame']),width=400,height=254,bytes=406400,sha256=digest,rawMediaFilesWritten=0))
      png=io.BytesIO();Image.frombytes('RGB',(400,254),raw,'raw','BGRX').save(png,format='PNG')
      print('MK2_NORMAL_FREEZE_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
      (folder/'rgb_memory_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
     log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in fields.items())+' sha256='+digest+'\n');log.flush()
    else:
     need('hex='not in line,'Never persist raw guest/GFX/RGB/audio bytes')
     log.write(line)
     if re.search(r'_(FIRST_LIVE|ICE_REQUEST|PROJECTILE_SETUP|END|NO_LIVE_ROUND|RESULT) ',line):print(line.strip(),flush=True)
  native_exit=process.wait()
 log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()
 rows=[dict(re.findall(r'(\w+)=([^\s]+)',line),tag=line.split()[0])for line in log.splitlines()if line.startswith(('MK2_NORMAL_FREEZE_','MK2_STOCK_HEAD_V921_'))and '_DIGEST 'not in line]
 meta=dict(nativeExit=native_exit,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
           actualScenes=scenes,inputHashes=pins,fullPortAcceptance=False,normalFreezeAccepted=False,fullArtAcceptance=False,
           fullAudioAcceptance=False,nativeFloorShadowCoverageAccepted=False,rawGuestMediaAudioFilesWritten=0)
 (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
 need(native_exit==0 and proof_guest and proof_gfx and all(sha(p)==h for p,h in pins.items()),'Actual terminal transport and immutable inputs')
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|CACHE_OVERWRITE |INVALID_ACTOR ',log+err,re.I),'No callback/error/overrun/invalid actor')
 fields=[r for r in rows if r['tag']=='MK2_NORMAL_FREEZE_FIELD'];ends=[r for r in rows if r['tag']=='MK2_NORMAL_FREEZE_END']
 need(len(fields)==701 and len(ends)==1 and [r['stage']for r in scenes]==['before','ice','wait','after_controls'],
      'Every actual ordinary live field and four requested RGB stages retained')
 meta.update(passed=True,fieldCount=len(fields),end=ends[0],actualVictimActions=sorted({r['action']for r in fields}),
             actualVictimBanks=sorted({r['bank']for r in fields}),nativeIceRequestObserved=any(r['tag']=='MK2_NORMAL_FREEZE_ICE_REQUEST'for r in rows),
             finalVictim=fields[-1])
 return meta

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya','kitana','liu_kang'));parser.add_argument('--side',required=True,type=int,choices=(1,2));args=parser.parse_args()
 out=ROOT/f'audit_v5035_normal_subzero_{args.fighter}_p{args.side}_observed'
 need(not out.exists(),'Fresh terminal ordinary-freeze report')
 try:report=capture(args.fighter,args.side)
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False,normalFreezeAccepted=False)
 out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress terminal proof')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
