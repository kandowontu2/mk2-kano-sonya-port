"""One original-game, physically earned finisher reference; media RAM only."""
import code
import gzip
import hashlib
import inspect
import json
import os
import re
import subprocess
import time
from pathlib import Path
import native_process_census_v6647 as process

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_secondary_kano_reference'
EXE=(ROOT/'../hbmame/hbmame.exe').resolve()
LUA=ROOT/'mk3_native_secondary_kano_reference.lua'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def need(value,message):
    if not value:raise ValueError(message)

def census():
    # Same read-only kernel implementation, exact original-game executable
    # name in place of the narrowly hardcoded port-candidate name.
    source=inspect.getsource(process.census)
    need(source.count("'mkport_candidate.exe'")==1,'Exact process-name specialization')
    scope=dict(vars(process))
    exec(compile(source.replace("'mkport_candidate.exe'","'hbmame.exe'"),__file__+'::census','exec'),scope)
    return scope['census']()

def run():
    need(not OUT.exists() and not census() and not process.census(),'One fresh original reference; no native games live')
    source=LUA.read_text()
    need(not re.search(r'write_[ui]\d+|:write_|\.value\s*=(?!=)|load_?state|set_analog|plugin\.cheat',source),
         'Controller contains only physical inputs/passive reads/taps')
    program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    paths=[Path(__file__),LUA,Path(process.__file__),EXE,ROOT/'mk3.zip',ROOT/'mk3/mk3-maincpu.bin',
           ROOT/'audit_native_secondary_finisher_reference/report.json']
    pins={str(path.resolve()):sha(path)for path in paths}
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK3_|MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    command=[str(EXE),'mk3','-rompath',str(ROOT),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
             '-noautoframeskip','-frameskip','0','-nothrottle','-str','180','-autoboot_delay','0',
             '-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),
             '-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(LUA)]
    capture=dict(rgbFrames=[],errors=[],guestCount=0,folder=OUT)
    OUT.mkdir()
    with (OUT/'stderr.log').open('w',encoding='utf-8')as stderr:
        born=time.time()
        job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,
                             encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        try:
            for _ in range(100):
                actual=next((item for item in census()if item['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.02)
            need(actual and actual['ParentProcessId']==os.getpid()and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==EXE,'Actual original native PID/parent/path/creation identity')
        except Exception as error:
            capture['errors'].append(dict(error=repr(error),stage='identity'))
        (OUT/'process.json').write_text(json.dumps(dict(pid=job.pid,command=command,actualWindowsIdentity=actual),indent=2)+'\n')
        print(json.dumps(dict(nativePID=job.pid,actualWindowsIdentity=actual)),flush=True)
        with gzip.open(OUT/'run.log.gz','wt',encoding='utf-8')as log:
            for line in job.stdout:
                try:
                    if ' hex='in line:
                        tag=line.split()[0];head=dict(re.findall(r'(\w+)=([^\s]+)',line))
                        raw=bytes.fromhex(head.pop('hex'))
                        need(len(raw)==int(head['bytes']),'Entire actual native declared buffer')
                        head['sha256']=hashlib.sha256(raw).hexdigest().upper()
                        if tag=='MK3_SECONDARY_GUEST':
                            need(raw==program,'Entire actual original initialized 1MiB program unchanged')
                            capture['guestCount']+=1
                        elif tag=='MK3_SECONDARY_RGB':
                            need(len(raw)==int(head['width'])*int(head['height'])*4,'Entire native raster')
                            capture['rgbFrames'].append(dict(header=head,pixels=raw))
                        else:raise ValueError('Unexpected raw native block')
                        log.write(tag+'_DIGEST '+' '.join(k+'='+v for k,v in head.items())+'\n')
                    else:
                        log.write(line)
                        if line.startswith(('MK3_SECONDARY_SELECTED ','MK3_SECONDARY_ROUND_COUNT ',
                                             'MK3_SECONDARY_OWN_ENTRY ','MK3_SECONDARY_COMMAND_SPACING ',
                                             'MK3_SECONDARY_RESULT ','MK3_SECONDARY_STOP ','MK3_SECONDARY_WRONG_SELECTION ')):
                            print(line.strip(),flush=True)
                except Exception as error:
                    capture['errors'].append(dict(error=repr(error),tag=line.split()[0]if line.strip()else'empty'))
            exitcode=job.wait()
    with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8')as stream:capture['text']=stream.read()
    need(not any(item['ProcessId']==job.pid for item in census()),'Same native handle terminal normally')
    need(all(sha(path)==digest for path,digest in pins.items()),'Actual executed source/ROM/assets conserved')
    passed=exitcode==0 and capture['guestCount']==1 and not capture['errors'] and not (OUT/'stderr.log').read_text()and not re.search(r'LUA ERROR|stack traceback|fatal error',capture['text'],re.I)
    report=dict(passed=passed,transportOnlyAccepted=passed,finisherAccepted=False,fullPortAcceptance=False,
                nativeExit=exitcode,actualWindowsIdentity=actual,errors=capture['errors'],nativeRGBFrames=len(capture['rgbFrames']),
                originalWholeGuestMatched=capture['guestCount']==1,inputHashes=pins,newBuilds=0,newROMCopies=0,
                newRawMedia=0,newZIPs=0,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(path.resolve()):dict(sha256=pins[str(path.resolve())],text=path.read_text())
                   for path in paths if path.suffix in('.py','.lua')},stream)
    print(json.dumps(dict(transportPassed=passed,nativeExit=exitcode,frames=len(capture['rgbFrames']),errors=capture['errors'])),flush=True)
    return capture

if __name__=='__main__':
    capture=run()
    code.interact(banner='Original native handle terminal; whole actual rasters retained in RAM.',local=dict(capture=capture))
