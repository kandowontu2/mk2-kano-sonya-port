"""Continuous power-on physical replay: no state load/save and no guest edits."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, PORT, FLAGS, command


def main():
    name='stock_wolf_2219_kano_continuous_short_route'
    assert not (BASE/name).exists(),'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(prior['testArguments']),'--campaign-short-route')
    command(PORT/'audit_campaign_run.py',name)
    print('Continuous route replay terminal; inspect native result and route fidelity before acceptance')


if __name__=='__main__':main()
