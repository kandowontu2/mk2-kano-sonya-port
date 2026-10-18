"""Save-only planning checkpoint, never a loaded-state campaign acceptance run."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, FLAGS, command


def main():
    name='stock_wolf_2219_kano_earned_kintaro_checkpoint_v3'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(prior['testArguments']),
            '--campaign-boss-checkpoint')
    execution=json.loads((BASE/name/'execution.json').read_text())
    assert execution['exitCode']==0 and not execution['timedOut']
    log=(BASE/name/'mame.log').read_text()
    assert 'Fatal error:' not in log and '[LUA ERROR]' not in log
    assert (BASE/name/'earned_kintaro_intro.sta').stat().st_size>1024
    print('Save-only earned checkpoint created; no state loaded or campaign clear claimed')


if __name__=='__main__':main()
