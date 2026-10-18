"""One bounded mixed-policy trial with wider request-time Knife clearance."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, PORT, FLAGS, command


def main():
    name='stock_wolf_2219_kano_finish13_knife260_bounded'
    assert not (BASE/name).exists(), 'Never overwrite evidence'
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    prior=json.loads((BASE/'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    command(BASE/'test_wolf_baseline.py',name,*trial_arguments(prior['testArguments']),
            '--campaign-knife-clearance=260')
    for script in ('audit_campaign_run.py','inspect_kintaro_variety.py',
                   'inspect_kintaro_damage_distribution.py'):
        command(PORT/script,name)


if __name__=='__main__':main()
