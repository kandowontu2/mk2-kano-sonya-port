"""Stock-state restore preflight, explicitly excluded from campaign acceptance."""
import csv
import json
import os
import subprocess
from pathlib import Path
from inspect_normal_runtime import BASE, PORT, sha
from refresh_special_videos import FLAGS


def main():
    earned=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3'
    proof=json.loads((earned/'EARNED_CHECKPOINT_QUALIFICATION.json').read_text())
    for name,digest in proof['pins'].items():assert sha(Path(name))==digest
    run=BASE/'stock_wolf_2219_kano_checkpoint_load_preflight_v2'
    assert not run.exists(),'Never overwrite planning evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    execution=json.loads((earned/'execution.json').read_text())
    emulator=Path(execution['emulator'])
    assert sha(emulator)==execution['emulatorSHA256']
    run.mkdir()
    observer=run/'autoboot.lua'
    observer.write_bytes((PORT/'diagnostics/checkpoint_load_probe.lua').read_bytes())
    environment=os.environ.copy();environment['KS_PLANNING_STATE']=str(earned/'earned_kintaro_intro.sta')
    args=[str(emulator),'mk3','-noreadconfig','-rompath',str(earned/'roms'),'-video','none',
        '-sound','none','-nothrottle','-skip_gameinfo','-autoboot_script',str(observer),
        '-seconds_to_run','0','-cfg_directory',str(run/'cfg'),'-nvram_directory',str(run/'nvram')]
    result=subprocess.run(args,cwd=run,env=environment,capture_output=True,text=True,timeout=30,creationflags=FLAGS)
    log=result.stdout+result.stderr;(run/'mame.log').write_text(log)
    receipt=dict(scope='Loaded-state planning preflight, not continuous campaign evidence',
        exitCode=result.returncode,command=args,emulatorSHA256=sha(emulator),
        observerSHA256=sha(observer),checkpointSHA256=sha(earned/'earned_kintaro_intro.sta'),
        gameMemoryEdits=False,stateLoadUsed=True,campaignAcceptance=False)
    (run/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
    assert result.returncode==0 and 'Fatal error:' not in log and '[LUA ERROR]' not in log,log[-1500:]
    rows=list(csv.DictReader((run/'planning_load.csv').open()))
    combat=[r for r in rows if r['mode']=='2' and r['p1char']=='17' and r['p2char']=='12']
    assert len(combat)>=120 and all(r['map']=='15' for r in combat)
    assert any(r['p1hp']==r['p2hp']=='161' for r in combat),'Native fresh-round initialization not observed'
    report=dict(scope=receipt['scope'],loadedStateVerified=True,nativeHealthInitializationObserved=True,
        firstCombatField=int(combat[0]['field']),nativeCombatFields=len(combat),
        noCombatInputs=True,campaignAcceptance=False,pins={str(p):sha(p) for p in
            (observer,run/'planning_load.csv',run/'execution.json',earned/'earned_kintaro_intro.sta')})
    (run/'PLANNING_LOAD_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified loaded earned intro and native161/161 initialization; planning only')


if __name__=='__main__':main()
