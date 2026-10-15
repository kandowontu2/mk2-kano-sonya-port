"""Current5219 full1600-field earned Friendship scene, no media/source copies.

Compare every actual snapshot-rendered RGB byte against the retained original
source-qualified raster/palette/shadow/erase reference, preserving its whole
gate and real pixel counterexamples. Keep native terminal evidence even after
host comparison errors; never stop/restart a child on an observation failure.
"""
import argparse,gzip,hashlib,json,os,re,subprocess,traceback
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_current_friendship_snapshot_pixels_v3579 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_friendship_scene_v6244.lua'
PARENT=ROOT/'audit_v6243_current_default_launcher_progress/progress.json'

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def digest(raw):return hashlib.sha256(raw).hexdigest().upper()

def run(fighter,side):
 folder=ROOT/f'audit_v6246_current_{fighter}_friendship_scene_p{side}'
 need(not folder.exists(),'Fresh immutable current full-scene evidence')
 guest=current.expected();original.control_source()
 reference,window,refs,pins=original.reference(fighter,side)
 # Preflight actual retained complete references before launching native game.
 for row in refs:
  path=Path(row['path']);need(sha(path)==row['wanted'],'Exact source-qualified complete reference exists')
  pins[str(path)]=row['wanted']
 build=ROOT/current.NAME;metadata=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
 files=[LUA,Path(__file__).resolve(),Path(current.__file__),Path(original.__file__),PARENT,
        build/'build-info.json',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata']
 files += [ROOT/n for n in original.LUA]
 files += [ROOT/'mk2ks_native_friendship_probe_v788.lua',ROOT/'mk2ks_current_friendship_extended_audio_v2687.lua',
           ROOT/'mk2ks_current_friendship_extended_wins_v2688.lua']
 files += list((ROOT/'samples/mk2ks').glob('*.wav'))
 for p in files:pins[str(p.resolve())]=sha(p)
 pins.update(metadata['input_hashes'])
 need(all(sha(p)==h for p,h in pins.items()),'Every reference/control/compiled/voice input exact')
 parent=json.loads(PARENT.read_text());need(parent['passed']and len(parent['remaining'])==5,'Full original scope retained')
 folder.mkdir();save(folder/'inputs.json',pins)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_FRIEND_WINNER=fighter,MK2KS_FRIEND_SIDE=str(side),MK2KS_FRIEND_CASE='positive',
            MK2KS_FRIEND_GAP='160',MK2KS_FRIEND_OBSERVATION='1600')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-nocheat','-skip_gameinfo',
  '-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
  '-nothrottle','-str','180','-snapsize','400x254','-cfg_directory',str(folder/'cfg'),
  '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 verified=[];mismatches=[];faults=[];errors=[];guests=0;wi=None
 with(folder/'stderr.log').open('wb')as stderr,subprocess.Popen(command,cwd=ROOT,env=env,
      stdout=subprocess.PIPE,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)as process:
  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process.pid)+"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
  census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  if census.returncode==0 and census.stdout.strip():wi=json.loads(census.stdout)
  save(folder/'process.json',dict(pid=process.pid,command=command,actualWindowsIdentity=wi))
  print(f'{fighter} P{side}: current full Friendship PID={process.pid}',flush=True)
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in iter(process.stdout.readline,b''):
    try:
     if line.startswith(b'MK2_CURRENT_FRIEND_GUEST '):
      h=dict(re.findall(r'(\w+)=([^\s]+)',line.decode('ascii')));raw=bytes.fromhex(h['hex'])
      need(len(raw)==int(h['bytes'])==1048576 and raw==guest,'Entire actual independently reconstructed current guest')
      guests+=1;log.write('MK2_CURRENT_FRIEND_GUEST_DIGEST bytes=1048576 sha256='+digest(raw)+'\n')
     elif line.startswith(b'MK2_FSTREAM_PIXELS '):
      h=dict(re.findall(r'(\w+)=([^\s]+)',line.decode('ascii')))
      encoded=process.stdout.readline().strip()
      need(len(encoded)==int(h['bytes'])*2==400*254*8 and h['encoding']=='u32le_as_hex_numeric'and
           int(h['width'])==400 and int(h['height'])==254 and int(h['frame'])==window+len(verified)+1 and
           h['writes']=='0'and h['assistance']=='none','Whole actual consecutive unmodified RGB transport')
      words=np.frombuffer(bytes.fromhex(encoded.decode('ascii')),dtype='>u4').reshape(254,400)
      actual=np.stack([(words>>shift)&255 for shift in(16,8,0)],axis=2).astype(np.uint8)
      ref=refs[len(verified)];expected=np.asarray(Image.open(ref['path']).convert('RGB'))
      differing=int(np.count_nonzero(np.any(actual!=expected,axis=2)))
      if differing:mismatches.append(dict(frame=int(h['frame']),pixels=differing,
           firstYX=np.argwhere(np.any(actual!=expected,axis=2))[0].tolist()))
      elif not faults:faults=original.pixel_faults(actual,expected)
      row=dict(frame=int(h['frame']),referencePNG=ref['path'],referencePNG_SHA256=ref['wanted'],
           currentRGB_SHA256=digest(actual.tobytes()),referenceRGB_SHA256=digest(expected.tobytes()),
           exactPixels=400*254-differing)
      verified.append(row);log.write('MK2_CURRENT_FRIEND_CHECKED '+' '.join(f'{k}={v}'for k,v in row.items()if k!='referencePNG')+'\n')
      if len(verified)%400==0:print(f'{fighter} P{side}: {len(verified)}/1600 fields, differing fields={len(mismatches)}',flush=True)
     else:
      need(not re.search(b'^[A-F0-9]{1000}',line),'Never log raw pixel/guest transport')
      log.write(line.decode('utf-8',errors='strict'))
    except Exception as error:
     errors.append(dict(error=repr(error),tag=line.split()[0].decode('ascii',errors='replace')if line.strip()else'empty'))
   code=process.wait()
  save(folder/'native_terminal.json',dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=wi,
                                        hostDecodeErrors=errors,naturalTerminal=True))
 save(folder/'visible_frames.json',verified);save(folder/'mismatches.json',mismatches)
 need(wi and wi['ProcessId']==process.pid and wi['Name']=='mkport_candidate.exe'and
      Path(wi['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(LUA)in wi['CommandLine'],
      'Actual native Windows creation/executable/full command identity')
 need(code==0 and not errors,'Actual natural native terminal and full host transport')
 with gzip.open(folder/'run.log.gz','rt')as log:text=log.read()
 need(not re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|access violation',text+(folder/'stderr.log').read_text(),re.I),
      'No native/observer failure')
 need(guests==1 and len(verified)==1600 and len(faults)==3 and not mismatches,
      'Entire current guest and1600complete source-qualified visible fields, no masks/offsets')
 # Existing whole parsers take a path: execute their exact line parser over the
 # gzip text in RAM, not by adding an uncompressed copy of this trace.
 import inspect
 parser=original.audio.audio.scene.previous.parse
 source=inspect.getsource(parser)
 before="Path(path).read_text(encoding='utf-8-sig')"
 need(source.count(before)==1,'One exact original parser RAM input adaptation')
 source=source.replace(before,'text',1)
 scope=dict(parser.__globals__,text=text)
 exec(compile(source,__file__+'::whole_original_event_parser','exec'),scope)
 rows=scope['parse']('RAM')
 old_rows=[(tag,row)for tag,row in parser(reference/'run.log')if not tag.startswith('SHADOW_')]
 need(rows==old_rows,'Every original native physical/health/pose/owner/voice/win/cleanup row retained on current5219')
 control=original.audio.audio.scene.check(rows,fighter,side)
 chronology=original.audio.audio.native.runtime(rows,fighter,side,'positive')
 need(all(sha(p)==h for p,h in pins.items()),'Every actual source/reference/native input unchanged after terminal')
 current.expected()
 result=dict(passed=True,candidate=current.NAME,winner=fighter,side=side,actualNativeExitCode=code,
      wholeCurrentGuestAccepted=True,actualVisibleFrames=1600,exactRGBPixels=1600*400*254,
      actualPixelFaults=faults,nativeScene=control,nativeAudioCueChronology=chronology,
      physicalNativeRows=len(rows),inputHashes=pins,newBuilds=0,newSourceCopies=0,rawMediaWritten=0,
      completeFriendshipAudioWaveformAccepted=False,allFriendshipContextsAccepted=False,fullPortAcceptance=False)
 save(folder/'report.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','actualPixelFaults')},indent=2),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  folder=ROOT/f'audit_v6246_current_{args.fighter}_friendship_scene_p{args.side}'
  if folder.exists():save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
