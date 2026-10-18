"""One hidden, bounded stock-state input search; never campaign acceptance."""
import json
import os
from pathlib import Path
import subprocess
from inspect_normal_runtime import BASE,PORT,sha
from refresh_special_videos import FLAGS


def main():
    earned=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3'
    proof=json.loads((earned/'EARNED_CHECKPOINT_QUALIFICATION.json').read_text())
    state=earned/'earned_kintaro_intro.sta';assert sha(state)==proof['pins'][str(state)]
    run=BASE/'stock_wolf_2219_kano_short_search'
    assert not run.exists(),'Preserve old search evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((earned/'execution.json').read_text());emulator=Path(prior['emulator'])
    assert sha(emulator)==prior['emulatorSHA256']
    run.mkdir();states=run/'states';states.mkdir()
    frozen=run/'autoboot.lua';frozen.write_bytes((PORT/'diagnostics/kintaro_short_search.lua').read_bytes())
    environment=os.environ.copy();environment.update(KS_SEARCH_ROOT=str(state),KS_SEARCH_OUT=states.as_posix())
    args=[str(emulator),'mk3','-noreadconfig','-rompath',str(earned/'roms'),'-video','none',
        '-sound','none','-nothrottle','-skip_gameinfo','-seconds_to_run','0',
        '-autoboot_script',str(frozen),'-cfg_directory',str(run/'cfg'),'-nvram_directory',str(run/'nvram')]
    with (run/'mame.log').open('x') as log:
        try:
            result=subprocess.run(args,cwd=run,env=environment,stdout=log,stderr=subprocess.STDOUT,
                timeout=180,creationflags=FLAGS)
            status=dict(exitCode=result.returncode,timedOut=False)
        except subprocess.TimeoutExpired:status=dict(exitCode=None,timedOut=True)
    report=dict(scope='Loaded-state short-input planning ONLY',planningStateLoadUsed=True,
        campaignAcceptance=False,gameMemoryEdits=False,emulatorSHA256=sha(emulator),
        observerSHA256=sha(frozen),checkpointSHA256=sha(state),command=args,**status)
    (run/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
    log=(run/'mame.log').read_text()
    assert status['exitCode']==0 and not status['timedOut']
    assert all(error not in log for error in ('SEARCH_ERROR:','Fatal error:','[LUA ERROR]')),log[-2000:]
    assert (run/'search_end.txt').exists(),'No terminal search receipt'
    print((run/'search_end.txt').read_text().strip(),'; retained input/results, not campaign acceptance')


if __name__=='__main__':main()
