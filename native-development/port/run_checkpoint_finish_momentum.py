"""Planning original-spacing finish13 with existing refresh+momentum escape."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, PORT, FLAGS, command


def main():
    name='stock_wolf_2219_kano_checkpoint_finish_momentum'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    state=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3/earned_kintaro_intro.sta'
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(prior['testArguments']),
        '--planning-state='+str(state),'--campaign-kano-kintaro-stomp-refresh',
        '--campaign-kano-kintaro-stomp-momentum')
    command(PORT/'qualify_planning_boss_run.py',name)
    print('Finish/momentum planning terminal; no continuous campaign acceptance')


if __name__=='__main__':main()
