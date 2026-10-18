"""Planning-only one backward punch hop, never consecutive backward punch hops."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, PORT, FLAGS, command


def main():
    name='stock_wolf_2219_kano_checkpoint_retreat_hop'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    state=BASE/'stock_wolf_2219_kano_earned_kintaro_checkpoint_v3/earned_kintaro_intro.sta'
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(prior['testArguments']),
        '--planning-state='+str(state),'--campaign-punch-retreat-hop')
    command(PORT/'qualify_planning_boss_run.py',name)
    print('Retreat-hop planning trial terminal; no continuous campaign claim')


if __name__=='__main__':main()
