"""Native-parser proof of whole physical ground callback; source only."""
import gzip
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
import capture_native_kano_laser_audio as current
import native_process_census_v6647 as identity
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_kano_laser_ground_ram_source'

def main():
    need(not OUT.exists() and not identity.census(),'Fresh native parser, no gameplay job live');OUT.mkdir()
    try:
        candidate=ROOT/current.NAME
        build=json.loads((candidate/'build-info.json').read_text())
        need(sha(candidate/'mkport_candidate.exe')==build['executable_sha256'],'Current unchanged native binary')
        paths=[Path(__file__),ROOT/'mk2ks_native_kano_laser_ground_parse.lua',ROOT/'mk2ks_native_kano_laser_ground_ram.lua',
               ROOT/'mk2ks_ground_shadow_v815_probe.lua',candidate/'mkport_candidate.exe',candidate/'build-info.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        pins={str(p.resolve()):sha(p) for p in paths}
        env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
        command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
                 '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
                 '-nothrottle','-str','4','-autoboot_delay','0','-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_ground_parse.lua'),
                 '-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram')]
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        for _ in range(100):
            actual=next((r for r in identity.census() if r['ProcessId']==job.pid),None)
            if actual or job.poll() is not None:break
            time.sleep(.02)
        identity_error=None
        try:
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Actual parser PID/parent/path/birth')
        except Exception as error:identity_error=repr(error)
        raw,err=job.communicate()
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=job.returncode,actualWindowsIdentity=actual,
            identityError=identity_error,stderr=err.decode(errors='replace')),indent=2)+'\n')
        with gzip.open(OUT/'native_stdout.log.gz','wb')as f:f.write(raw)
        need(job.returncode==0 and not err and not identity_error and not any(r['ProcessId']==job.pid for r in identity.census()),'Same parser handle terminal0, no diagnostic errors')
        records=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in raw.decode().splitlines() if line.startswith('MK2_GR_PARSE_PHYSICAL ')]
        need(len(records)==1 and b'gameplay_callbacks_executed=0 guest_writes=0' in raw,'Exactly one actual final compile and no gameplay callbacks')
        text=bytes.fromhex(records[0]['hex']).decode();need(len(text.encode())==int(records[0]['bytes']),'Entire expanded source')
        original=(ROOT/'mk2ks_ground_shadow_v815_probe.lua').read_text()
        need(original.count('io.open(output..')==3 and original.count('screen:snapshot(file)')==1,'Original exact evidence sink counts')
        adapted=original.replace('io.open(output..','_ground_ram_open(output..').replace('screen:snapshot(file)','_ground_ram_rgb(file,frame)')
        need(text.endswith(adapted),'Entire actual physical controller/DMA/timing/ownership observer byte-identical except four sinks')
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),'No guest/item/register/state writes')
        need(all(sha(p)==h for p,h in pins.items()),'Actual native parser inputs conserved')
        with gzip.open(OUT/'executed_source.lua.gz','wt')as f:f.write(text)
        (OUT/'report.json').write_text(json.dumps(dict(passed=True,actualNativeParserAccepted=True,
            wholePhysicalGroundByteIdentical=True,changedBinarySinks=3,changedPNGSinks=1,
            gameplayAccepted=False,inputHashes=pins,nativeExit=0,actualWindowsIdentity=actual,
            newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
            fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=True,actualNativeParser=True,wholePhysicalGroundUnchanged=True)),flush=True)
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise

if __name__=='__main__':main()
