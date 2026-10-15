"""Bounded scalar-only fresh campaign test; never import historical capture chains."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parent.parent
sp=importlib.util.spec_from_file_location('helpers',ROOT/'video_sonya_subzero_hk_20261015_preparation/run.py')
h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
OUT=ROOT/'video_sonya_kitana_leg_bench_20261015'
LUA=ROOT/'video_sonya_kitana_leg_bench_20261015_preparation/campaign.lua'

def main():
    h.need(not OUT.exists() and h.sha(h.EXE)==h.EXPECTED_EXE,'Fresh unchanged native executable')
    prep=json.loads((LUA.parent/'preparation.json').read_text());h.need(h.sha(LUA)==prep['sourceSHA256'],'Prepared source pin')
    OUT.mkdir()
    for d in ('cfg','nvram','snap'):(OUT/d).mkdir()
    env={k:v for k,v in os.environ.items() if not k.startswith(('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_','MK2PORT_'))}
    env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_TEST_BOOT_FRAME='600')
    build=h.EXE.parent
    args=[str(h.EXE),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(OUT),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','2800','-wavwrite','NUL','-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(LUA)]
    peak=0;limits=[];start=time.monotonic()
    with (OUT/'run.log').open('wb') as log,(OUT/'stderr.log').open('wb') as err:
        p=subprocess.Popen(args,cwd=ROOT,env=env,stdout=log,stderr=err,creationflags=h.HIDDEN)
        (OUT/'launch.json').write_text(json.dumps(dict(pid=p.pid,command=args,luaSHA256=h.sha(LUA),executableSHA256=h.sha(h.EXE)),indent=2))
        while p.poll() is None:
            peak=max(peak,h.memory(p.pid))
            if peak>320*1024**2:limits.append('memory320MiB')
            if time.monotonic()-start>300:limits.append('wall300')
            if log.tell()+err.tell()>20*1024**2:limits.append('text20MiB')
            if limits:p.kill();break
            time.sleep(.2)
        p.wait(timeout=5)
    (OUT/'terminal.json').write_text(json.dumps(dict(exitCode=p.returncode,limits=limits,peakWorkingSetBytes=peak,elapsedSeconds=time.monotonic()-start,mediaWritten=False,guestWrites=False,completedCampaign=False),indent=2))
    h.need(p.returncode==0 and not limits and not (OUT/'stderr.log').read_text().strip(),'Bounded successful process, not outcome acceptance')
    print(OUT)

if __name__=='__main__':main()
