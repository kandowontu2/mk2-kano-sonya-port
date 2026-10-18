"""Planning-only original controller continuation, never campaign acceptance."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, FLAGS, command


def main():
    name='stock_wolf_2219_kano_checkpoint_reference'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    source=BASE/'stock_wolf_2219_kano_boss_guard/execution.json'
    state=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3/earned_kintaro_intro.sta'
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(json.loads(source.read_text())['testArguments']),
            '--planning-state='+str(state))
    receipt=json.loads((BASE/name/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'] and receipt['planningStateLoadUsed']
    print('Planning continuation terminal; no continuous campaign acceptance claimed')


if __name__=='__main__':main()
