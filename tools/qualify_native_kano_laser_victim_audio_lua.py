"""Actual installed candidate Lua parser; typed opponent constants only.

Native process is a hardware/parser diagnostic, not earned gameplay proof.
No compiler cache, raw media, ROM copy or build is created.
"""
import gzip
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
import capture_native_kano_laser_audio as original
import native_process_census_v6647 as identity

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_kano_laser_victim_audio_lua_source'


def main():
    need(not OUT.exists() and not identity.census(),'Fresh source qualification; no native game live');OUT.mkdir()
    try:
        prior_path=ROOT/'audit_native_kano_laser_audio_lua_headers_source/report.json'
        prior=json.loads(prior_path.read_text());need(prior['passed'] and all(sha(p)==h for p,h in prior['inputHashes'].items()),'Original actual full physical/audio source qualification conserved')
        prior_sources=json.loads(gzip.open(prior_path.parent/'executed_sources.json.gz','rt').read())
        candidate=ROOT/original.NAME;build_path=candidate/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'))
        need(sha(candidate/'mkport_candidate.exe')==build['executable_sha256'] and not build['public_build_promoted'],'Exact private playable candidate')
        paths=[Path(__file__),ROOT/'mk2ks_native_kano_laser_victim_audio.lua',ROOT/'mk2ks_native_kano_laser_victim_parse.lua',
               ROOT/'mk2ks_native_kano_laser_audio.lua',ROOT/'mk2ks_native_kano_laser_burst.lua',ROOT/'mk2ks_native_kano_laser_typed_epochs.lua',
               ROOT/'mk2ks_native_kano_laser_action.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',Path(identity.__file__),
               prior_path,prior_path.parent/'executed_sources.json.gz',build_path,candidate/'mkport_candidate.exe',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        pins={str(p.resolve()):sha(p) for p in paths};cases=[];expanded={}
        for victim in (4,17):
            need(not identity.census(),'Prior exact parser process actually terminal')
            folder=OUT/f'victim{victim}';folder.mkdir()
            env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
            env['MK2KS_LASER_VICTIM']=str(victim)
            command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
                     '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
                     '-nothrottle','-str','4','-autoboot_delay','0','-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_victim_parse.lua'),
                     '-inipath',str(folder),'-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram')]
            born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
            actual=None
            for _ in range(100):
                actual=next((r for r in identity.census() if r['ProcessId']==job.pid),None)
                if actual or job.poll() is not None:break
                time.sleep(.02)
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Actual parser PID/parent/path/birth')
            raw,err=job.communicate()
            (folder/'native_exit.json').write_text(json.dumps(dict(nativeExit=job.returncode,actualWindowsIdentity=actual,stderr=err.decode(errors='replace')),indent=2)+'\n')
            need(job.returncode==0 and not err and not any(r['ProcessId']==job.pid for r in identity.census()),'Same native parser handle terminal without error')
            text=raw.decode();parts={}
            for line in text.splitlines():
                if line.startswith(('MK2_VARIANT_PHYSICAL ','MK2_VARIANT_AUDIO ')):
                    tag=line.split()[0];fields=dict(re.findall(r'(\w+)=([^\s]+)',line));data=bytes.fromhex(fields['hex'])
                    need(len(data)==int(fields['bytes']) and tag not in parts,'Entire exactly-once native source output');parts[tag]=data.decode()
            need(set(parts)=={'MK2_VARIANT_PHYSICAL','MK2_VARIANT_AUDIO'} and 'gameplay_callbacks_executed=0 guest_writes=0' in text,
                 'Both real native Lua compilations, no physical diagnostic callback execution')
            expected=prior_sources['actualExpandedPhysicalController']
            edits=[('victim.id==18',f'victim.id=={victim}',1),('n==side and 17 or 18',f'n==side and 17 or {victim}',2),
                   ('victim.id~=18',f'victim.id~={victim}',1),('victim.roster~=18',f'victim.roster~={victim}',1)]
            for old,new,count in edits:
                need(expected.count(old)==count,'Only known literal identity constant boundaries');expected=expected.replace(old,new)
            need(parts['MK2_VARIANT_PHYSICAL']==expected and parts['MK2_VARIANT_AUDIO']==prior_sources['actualExpandedAudioObserver'],
                 'Every physical button/timing/earning/command/body observer byte identical except requested opponent predicates; full audio observer unchanged')
            need(all(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',s) for s in parts.values()),'All expanded observations passive; physical inputs only')
            cases.append(dict(victimID=victim,actualNativeParserAccepted=True,physicalChangedIdentityConstantsOnly=True,audioByteIdentical=True,actualWindowsIdentity=actual,nativeExit=0))
            expanded[str(victim)]=parts
        need(all(sha(p)==h for p,h in pins.items()),'All actual executed parser/controller/candidate inputs immutable')
        with gzip.open(OUT/'executed_sources.json.gz','wt')as f:json.dump(expanded,f)
        report=dict(passed=True,sourceOnlyAccepted=True,actualNativeLuaParserAccepted=True,nativeGameplayAccepted=False,cases=cases,
                    inputHashes=pins,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active',fullPortAcceptance=False)
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,nativeLuaParser=True,victims=[4,17],gameplayAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
