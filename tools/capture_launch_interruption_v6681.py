"""Cold physical two-cycle interruption attempt, full RAM-only native inventory.

Only real controls; no acceptance if no incoming contact actually happens.
Drains this exact native job to terminal after any host observation failure.
--hold preserves the same PCM/DAC/ROM/guest/GFX/RGB carrier without replay.
"""
import argparse,code,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as identity
import current_ending_audio_model_v5733 as models
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_launch_interrupt_v6680.lua'
LAST_CAPTURE=None


def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')


def run(move,side,delay):
 global LAST_CAPTURE
 folder=ROOT/f'audit_v6682_launch_interrupt_{move}_p{side}_delay{delay}'
 need(not folder.exists()and not identity.census(),'Fresh native attempt, no conflicting process and never replay a prior handle')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 expected,rom_pins=models.expected_region(pins)
 for p in(Path(__file__),Path(current.__file__),Path(identity.__file__),Path(models.__file__),LUA,
          ROOT/'mk2ks_special_repeat_v5099.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',
          build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
 folder.mkdir()
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_ACCEPT_|MK2PORT_INTERRUPT_)',k)}
 env.update(MK2PORT_ACCEPT_MOVE=move,MK2PORT_ACCEPT_SIDE=str(side),MK2PORT_ACCEPT_AIR='0',
            MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay))
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
          '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),
          '-samples','-samplerate','48000','-wavwrite','NUL','-skip_gameinfo','-nocheat','-inipath',str(folder),
          '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-snapsize','400x254','-str','100',
          '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
          '-autoboot_script',str(LUA)]
 carrier=dict(folder=folder,move=move,side=side,delay=delay,pins=pins,expectedROM=expected,guest=guest,gfx=gfx,
              pcm=[],pcmHeaders=[],dac=[],dacHeaders=[],rom={p:bytearray()for p in('startup','terminal')},
              rgb=[],guestCount=0,gfxCount=0,decodeErrors=[])
 LAST_CAPTURE=carrier
 with(folder/'stderr.log').open('w',encoding='utf-8')as stderr:
  started=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',errors='replace')
  observed=None
  try:
   for _ in range(100):
    observed=next((j for j in identity.census()if j['ProcessId']==job.pid),None)
    if observed or job.poll()is not None:break
    time.sleep(.02)
   need(observed and observed['ParentProcessId']==os.getpid()and Path(observed['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and
        observed['createdUnix']>=started-1 and str(folder)in observed['CommandLine'],'Actual live kernel executable/PID/parent/creation/full command')
  except Exception as error:carrier['decodeErrors'].append(dict(stage='identity',error=repr(error)))
  save(folder/'process.json',dict(pid=job.pid,command=command,actualWindowsIdentity=observed))
  print(f'Physical interruption {move} P{side} delay={delay} native PID={job.pid}',flush=True)
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in job.stdout:
    try:
     if ' hex='in line:
      tag=line.split()[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);head=dict(pairs)
      need(len(head)==len(pairs),'Unique native transport metadata keys')
      raw=bytes.fromhex(head.pop('hex'));need(len(raw)==int(head['bytes']),'Entire actual declared raw callback')
      head['sha256']=hashlib.sha256(raw).hexdigest().upper()
      if tag=='MK2_BBAUDIO_PCM':carrier['pcm'].append(raw);carrier['pcmHeaders'].append(head)
      elif tag=='MK2_NATIVE_DAC_RAM':carrier['dac'].append(raw);carrier['dacHeaders'].append(head)
      elif tag=='MK2_NATIVE_DCS_ROM':
       phase=head['phase'];need(phase in carrier['rom']and int(head['offset'])==len(carrier['rom'][phase])and head['bytes']=='65536'and
        head['size']=='12582912'and head['bytewidth']=='2'and head['bitwidth']=='16'and head['writes']=='0'and head['assistance']=='none','Consecutive whole original native DCS region')
       at=int(head['offset']);need(raw==expected[at:at+len(raw)],'Every actual original DCS ROM byte matches independent source');carrier['rom'][phase].extend(raw)
      elif tag in('MK2_HPHASE_GUEST','MK2_MAUDIO_GUEST'):
       need(raw==guest,'Whole independently reconstructed actual current guest');carrier['guestCount']+=1
      elif tag=='MK2_HPHASE_GFX':need(raw==gfx,'Whole original owned actual graphics bytes');carrier['gfxCount']+=1
      elif tag=='MK2_HPHASE_RGB':
       need(head['width']=='400'and head['height']=='254'and len(raw)==406400,'Complete actual native full screen')
       carrier['rgb'].append(head)
      else:raise ValueError('Unexpected raw native transport '+tag)
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in head.items())+'\n')
     else:
      need('hex='not in line,'No raw native buffer persisted');log.write(line)
      if re.search(r'MK2_HSPECIAL_(READY|COMMAND|RECOVERED|FINAL|FAILED|RESULT) |MK2_INTERRUPT_ENTRY ',line):print(line.strip(),flush=True)
    except Exception as error:carrier['decodeErrors'].append(dict(stage='decode',tag=line.split()[0]if line.strip()else'empty',error=repr(error)))
   exitcode=job.wait()
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as log:carrier['text']=log.read()
 terminal=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=observed,hostDecodeErrors=carrier['decodeErrors'])
 carrier['terminal']=terminal;save(folder/'native_terminal.json',terminal)
 need(not identity.census(),'Actual native job terminal, not an expired observation')
 report=dict(passed=False,move=move,side=side,delay=delay,candidate=current.NAME,nativeTerminal=terminal,inputHashes=pins,
             newBuilds=0,newROMCopies=0,newZIPs=0,rawGuestGFXRGBPCMOrWAVFilesWritten=0,
             gameplayInterruptionAccepted=False,sourceWaveformAccepted=False,fullPortAcceptance=False)
 try:
  need(exitcode==0 and observed and not carrier['decodeErrors']and (folder/'stderr.log').read_text()==''and
       not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',carrier['text'],re.I),'Actual native natural terminal without emulator/observer/transport error')
  need(carrier['guestCount']==2 and carrier['gfxCount']==1 and all(len(v)==12582912 for v in carrier['rom'].values())and
       len(carrier['pcm'])==len(carrier['dac'])>200,'Both guest inventories, entire original GFX, both sound ROMs and full native PCM/DAC')
  need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input unchanged')
  report.update(passed=True,transportOnlyAccepted=True,completePCMCallbacks=len(carrier['pcm']),nativeRGBCallbacks=len(carrier['rgb']))
 except Exception as error:report.update(error=repr(error),traceback=traceback.format_exc())
 save(folder/'report.json',report);carrier['report']=report
 print(json.dumps(dict(transportPassed=report['passed'],nativeExit=exitcode,completePCMCallbacks=len(carrier['pcm']),
                       error=report.get('error'),gameplayInterruptionAccepted=False)),flush=True)
 return carrier


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square','bicycle'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=1);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:run(args.move,args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and LAST_CAPTURE:
  code.interact(banner='Same actual terminal interruption attempt; native source buffers remain RAM-only. No replay.',local=dict(capture=LAST_CAPTURE,module=__import__(__name__)))
