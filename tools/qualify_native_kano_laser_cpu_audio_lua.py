"""Real installed native parser diagnostic; no game callbacks or guest writes."""
import gzip
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_audio as source
import native_process_census_v6647 as identity

ROOT,need,sha=source.ROOT,source.need,source.sha
OUT=ROOT/'audit_native_kano_laser_cpu_audio_lua_source'


def main():
    need(not OUT.exists() and not identity.census(),'Fresh actual parser diagnostic; no native game live');OUT.mkdir()
    try:
        candidate=ROOT/source.original.NAME
        build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
        need(sha(candidate/'mkport_candidate.exe')==build['executable_sha256'],'Exact existing private executable')
        paths=[Path(__file__),Path(source.__file__),*source.CONTROLLERS,ROOT/'mk2ks_native_kano_laser_cpu_parse.lua',
               candidate/'build-info.json',candidate/'mkport_candidate.exe',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        pins={str(p.resolve()):sha(p) for p in paths}
        env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
        env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1',MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900')
        command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
                 '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
                 '-nothrottle','-str','4','-autoboot_delay','0','-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_cpu_parse.lua'),
                 '-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram')]
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        for _ in range(100):
            actual=next((r for r in identity.census() if r['ProcessId']==job.pid),None)
            if actual or job.poll()is not None:break
            time.sleep(.02)
        need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
             Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Actual parser native PID/parent/path/birth')
        raw,err=job.communicate()
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=job.returncode,actualWindowsIdentity=actual,stderr=err.decode(errors='replace')),indent=2)+'\n')
        with gzip.open(OUT/'native_stdout.log.gz','wb')as f:f.write(raw)
        need(job.returncode==0 and not err and not any(r['ProcessId']==job.pid for r in identity.census()),'Same actual parser terminal without error')
        parts={}
        for line in raw.decode().splitlines():
            if line.startswith(('MK2_CPU_PARSE_CAMPAIGN ','MK2_CPU_PARSE_AUDIO ')):
                tag=line.split()[0];fields=dict(re.findall(r'(\w+)=([^\s]+)',line));data=bytes.fromhex(fields['hex'])
                need(len(data)==int(fields['bytes']) and tag not in parts,'Entire exactly-once native compiled source');parts[tag]=data.decode()
        need(set(parts)=={'MK2_CPU_PARSE_CAMPAIGN','MK2_CPU_PARSE_AUDIO'} and b'gameplay_callbacks_executed=0 guest_writes=0' in raw,
             'Actual complete final campaign/audio parse; no gameplay diagnostic callbacks executed')
        need('_cpu_laser_followup(frame);return end' in parts['MK2_CPU_PARSE_CAMPAIGN'] and
             'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO'],'Actual post-join boundary/full sound window expanded')
        for text in parts.values():need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),'Full actual expanded controllers passive/physical only')
        need(all(sha(p)==h for p,h in pins.items()),'All actual sources/executable conserved through terminal')
        with gzip.open(OUT/'executed_sources.json.gz','wt')as f:json.dump(parts,f)
        (OUT/'report.json').write_text(json.dumps(dict(passed=True,actualNativeParserAccepted=True,gameplayAccepted=False,
            inputHashes=pins,actualWindowsIdentity=actual,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            latestPlayableChanged=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=True,actualNativeParser=True,gameplayAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
