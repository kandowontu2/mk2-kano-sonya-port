"""Finite combined-input experiment; no game or emulator modifications."""
import json
import subprocess
from run_kano_finishing_uppercut13 import trial_arguments
from refresh_special_videos import BASE, PORT, FLAGS, command


def combined_arguments(prior):
    return trial_arguments(prior) + ['--campaign-kano-kintaro-stomp-refresh']


def main():
    name = 'stock_wolf_2219_kano_finish13_stomp_refresh'
    assert not (BASE / name).exists(), 'Never overwrite evidence'
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    prior = json.loads((BASE / 'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    command(BASE / 'test_wolf_baseline.py', name, *combined_arguments(prior['testArguments']))
    for script in ('audit_campaign_run.py', 'inspect_kintaro_variety.py',
                   'inspect_kintaro_ready_counter.py', 'inspect_stomp_refresh.py',
                   'inspect_kintaro_damage_distribution.py'):
        command(PORT / script, name)


if __name__ == '__main__':
    main()
