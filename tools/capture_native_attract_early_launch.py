"""One unassisted cold attract run; full images/audio in RAM, no ROM copies."""
import code
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_native_attract_early_launch.lua'
OUT=ROOT/'audit_native_attract_early_launch'
BOOT_FRAME=360
SECONDS=780

def run():
    need(not OUT.exists() and not native.census(),'One fresh native cold attract run')
    guest=current.expected()
    source=LUA.read_text()
    dependencies=[]
    if "dofile('mk2ks_native_attract_early_launch.lua')" in source:
        config='\n'.join(line for line in source.splitlines() if line and not line.startswith('--'))+'\n'
        need(config==f"_G.mk2ks_boot_frame={BOOT_FRAME}\n_G.mk2ks_capture_winners=true\ndofile('mk2ks_native_attract_early_launch.lua')\n",'Exact explicit host-global physical timing/passive winner observer configuration')
        dependencies=[ROOT/'mk2ks_native_attract_early_launch.lua']
        source=dependencies[0].read_text()
    need(not re.search(r'write_[ui]\d+|:write_|\.value\s*=(?!=)|load_?state|set_analog',source),'Whole observer has no guest-state assistance')
    need(source.count('boot_button:set_value(1)')==1 and source.count(':set_value(')==1 and 'frame>=boot_start and frame<boot_start+4' in source,'Only ordinary four-field alternate cold-start High Punch, no coins/selection/demo/RNG assistance')
    build=ROOT/current.NAME
    pins={str(p.resolve()):sha(p) for p in (Path(__file__),LUA,Path(current.__file__),Path(native.__file__),
        build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata',*dependencies)}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    OUT.mkdir()
    env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples',
      '-skip_gameinfo','-nocheat','-inipath',str(OUT),'-video','none','-sound','none','-noautoframeskip',
      '-frameskip','0','-nothrottle','-snapsize','400x254','-str',str(SECONDS),'-autoboot_delay','0',
      '-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),
      '-autoboot_script',str(LUA)]
    capture=dict(folder=OUT,guest=guest,pins=pins,rgbFrames=[],pcm=[],guestCount=0,battleGfx=[],dac=[],dacHeaders=[],errors=[])
    with (OUT/'stderr.log').open('w',encoding='utf-8') as err:
        started=time.time()
        job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')
        actual=None
        for _ in range(100):
            actual=next((r for r in native.census() if r['ProcessId']==job.pid),None)
            if actual or job.poll() is not None:break
            time.sleep(.02)
        need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=started-1,'Actual live native PID/parent/creation identity')
        (OUT/'process.json').write_text(json.dumps(dict(pid=job.pid,command=command,actualWindowsIdentity=actual),indent=2)+'\n')
        print(json.dumps(dict(nativePID=job.pid,command=command)),flush=True)
        with gzip.open(OUT/'run.log.gz','wt',encoding='utf-8') as log:
            for line in job.stdout:
                try:
                    if ' hex=' in line:
                        tag=line.split()[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);head=dict(pairs)
                        need(len(head)==len(pairs),'Unique entire native raw metadata')
                        raw=bytes.fromhex(head.pop('hex'));need(len(raw)==int(head['bytes']),'Entire actual declared native buffer')
                        head['sha256']=hashlib.sha256(raw).hexdigest().upper()
                        if tag=='MK2_ATTRACT_GUEST':need(raw==guest,'Whole compiled initialized guest equals independent native assembly');capture['guestCount']+=1
                        elif tag=='MK2_ATTRACT_BATTLE_GFX':
                            need(len(raw)==65536,'Whole original own battle-picture region');capture['battleGfx'].append(raw)
                        elif tag=='MK2_ATTRACT_RGB':
                            need(head['width']=='400' and head['height']=='254' and len(raw)==406400,'Entire native raster')
                            capture['rgbFrames'].append(dict(header=head,pixels=raw))
                        elif tag=='MK2_NATIVE_DAC_RAM':
                            capture['dac'].append(raw);capture['dacHeaders'].append(head)
                        elif tag=='MK2_ATTRACT_PCM':capture['pcm'].append(dict(header=head,pixels=raw))
                        else:raise ValueError('Unexpected native raw buffer')
                        log.write(tag+'_DIGEST '+' '.join(k+'='+str(v) for k,v in head.items())+'\n')
                    else:
                        log.write(line)
                        if line.startswith(('MK2_ATTRACT_COUNTER ','MK2_ATTRACT_DEMO_OWNER ','MK2_ATTRACT_RESULT ','MK2_ATTRACT_SOUND ','MK2_ATTRACT_ERROR_ENTRY ','MK2_ATTRACT_DIP ','MK2_ATTRACT_SWITCH_POLICY ','MK2_ATTRACT_WINNER_CALL ')):print(line.strip(),flush=True)
                except Exception as error:capture['errors'].append(dict(error=repr(error),tag=line.split()[0] if line.strip() else 'empty'))
            exitcode=job.wait()
    with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8') as f:capture['text']=f.read()
    need(not native.census(),'Same actual native process terminal, not an observation timeout')
    need(all(sha(k)==v for k,v in pins.items()),'Every actual native input unchanged')
    passed=exitcode==0 and capture['guestCount']==1 and len(capture['battleGfx'])==1 and not capture['errors'] and not (OUT/'stderr.log').read_text() and not re.search(r'LUA ERROR|stack traceback|fatal error',capture['text'],re.I)
    actual_inputs=[(int(f),v) for f,v in re.findall(r'^MK2_ATTRACT_INPUT frame=(\d+) [^\n]*?value=([01]) ',capture['text'],re.M)]
    configured=actual_inputs==[(f,'1') for f in range(BOOT_FRAME,BOOT_FRAME+4)]+[(BOOT_FRAME+4,'0')]
    if dependencies:configured=configured and f'boot_start={BOOT_FRAME} capture_winners=1' in capture['text']
    capture['terminal']=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=actual,hostDecodeErrors=capture['errors'])
    report=dict(passed=passed,transportOnlyAccepted=passed,requestedConfigurationAccepted=configured,actualPhysicalInputs=actual_inputs,attractAccepted=False,fullPortAcceptance=False,
        inputHashes=pins,nativeTerminal=capture['terminal'],nativeRGBFrames=len(capture['rgbFrames']),
        nativePCMCallbacks=len(capture['pcm']),nativeDACCallbacks=len(capture['dac']),physicalInputs=f'4 High Punch fields {BOOT_FRAME}..{BOOT_FRAME+3} at ordinary cold boot only',newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({k:dict(sha256=v,text=Path(k).read_text()) for k,v in pins.items() if k.endswith(('.lua','.py'))},f)
    print(json.dumps(dict(transportPassed=passed,nativeExit=exitcode,rgbFrames=len(capture['rgbFrames']),pcmCallbacks=len(capture['pcm']))),flush=True)
    return capture

if __name__=='__main__':
    capture=run()
    code.interact(banner='Same cold attract native job terminal; original RGB/PCM retained in RAM.',local=dict(capture=capture))




