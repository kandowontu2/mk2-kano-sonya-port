"""Exact original physical UI, full19channel passive observer: native parser."""
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
OUT=ROOT/'audit_native_kano_laser_ui_lua_source'


def main():
    need(not OUT.exists() and not identity.census(),'Fresh actual UI parser; no native game live');OUT.mkdir()
    try:
        candidate=ROOT/current.NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
        need(sha(candidate/'mkport_candidate.exe')==build['executable_sha256'],'Exact existing private candidate')
        paths=[Path(__file__),ROOT/'mk2ks_native_kano_laser_ui_parse.lua',ROOT/'mk2ks_native_kano_laser_ui.lua',ROOT/'mk2ks_native_kano_laser_ui_channels.lua',
               ROOT/'mk2ks_launch_candidate_ui.lua',ROOT/'mk2ks_current_ui_audio_ram_v5430.lua',ROOT/'mk2ks_current_ui_audio_ram_v5427.lua',
               ROOT/'mk2ks_native_ui_flow_v2_probe.lua',candidate/'mkport_candidate.exe',candidate/'build-info.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        pins={str(p.resolve()):sha(p) for p in paths}
        env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
        env.update(MK2KS_UI_SIDE='1',MK2KS_UI_FIGHTER='kano')
        command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
                 '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
                 '-nothrottle','-str','4','-autoboot_delay','0','-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_ui_parse.lua'),
                 '-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram')]
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        for _ in range(100):
            actual=next((r for r in identity.census() if r['ProcessId']==job.pid),None)
            if actual or job.poll()is not None:break
            time.sleep(.02)
        need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
             Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Actual parser PID/parent/path/birth')
        raw,err=job.communicate()
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=job.returncode,actualWindowsIdentity=actual,stderr=err.decode(errors='replace')),indent=2)+'\n')
        with gzip.open(OUT/'native_stdout.log.gz','wb')as f:f.write(raw)
        need(job.returncode==0 and not err and not any(r['ProcessId']==job.pid for r in identity.census()),'Same parser native handle actually terminal')
        parts={}
        for line in raw.decode().splitlines():
            if line.startswith(('MK2_UI_PARSE_PHYSICAL ','MK2_UI_PARSE_AUDIO ')):
                tag=line.split()[0];head=dict(re.findall(r'(\w+)=([^\s]+)',line));data=bytes.fromhex(head['hex'])
                need(len(data)==int(head['bytes']) and tag not in parts,'Whole exactly-once compiled UI source');parts[tag]=data.decode()
        need(set(parts)=={'MK2_UI_PARSE_PHYSICAL','MK2_UI_PARSE_AUDIO'} and b'gameplay_callbacks_executed=0 guest_writes=0' in raw,'Both actual final Lua expansions; no gameplay callback execution')
        base=(ROOT/'mk2ks_native_ui_flow_v2_probe.lua').read_text();physical=parts['MK2_UI_PARSE_PHYSICAL']
        adapted=base.replace('screen:snapshot(name)','_ui_emit(name,frame)')
        need(base.count('screen:snapshot(name)')==1 and physical.endswith(adapted),'Entire actual original physical UI callback unchanged, only its PNG sink replaced')
        audio=parts['MK2_UI_PARSE_AUDIO']
        need(audio.count('for channel=0,18 do')==2 and 'for channel=0,13 do' not in audio,'Both complete passive native source-channel loops expanded to19')
        for text in parts.values():need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),'Physical input/passive observation only')
        need(all(sha(p)==h for p,h in pins.items()),'All actual parser/controller/candidate inputs conserved')
        with gzip.open(OUT/'executed_sources.json.gz','wt')as f:json.dump(parts,f)
        (OUT/'report.json').write_text(json.dumps(dict(passed=True,actualNativeParserAccepted=True,wholePhysicalUIByteIdentical=True,totalSampleChannels=19,
            gameplayAccepted=False,inputHashes=pins,nativeExit=0,actualWindowsIdentity=actual,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            latestPlayableChanged=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=True,actualNativeParser=True,wholePhysicalUIUnchanged=True,channels=19)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
