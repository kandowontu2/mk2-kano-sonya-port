"""One hidden, bounded campaign trial; never overwrite a prior runtime."""
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS


def main():
    assert sys.argv[1:] in ([], ['--short-kick'], ['--retreat-ball'], ['--retreat-ball-finish-knife'], ['--varied'], ['--varied-spacing'], ['--varied-spacing-bounded'], ['--varied-counter'], ['--varied-adaptive'])
    variant = sys.argv[1][2:].replace('-', '_') if len(sys.argv)>1 else 'evade_counter'
    name = 'stock_wolf_2219_kano_kintaro_' + variant
    assert not (BASE / name).exists(), 'Never overwrite evidence'
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                           'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                          capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    prior = json.loads((BASE / 'stock_wolf_2219_kano_boss_guard/execution.json').read_text())
    policy = 'varied' if variant.startswith('varied_spacing') or variant in ('varied_counter','varied_adaptive') else variant.replace('_', '-')
    args = prior['testArguments'] + ['--campaign-kano-kintaro-' + policy]
    if variant=='varied_counter':args.append('--campaign-kano-kintaro-varied-counter')
    if variant=='varied_adaptive':args.append('--campaign-kano-kintaro-varied-adaptive')
    if variant == 'retreat_ball_finish_knife':
        args.append('--campaign-kano-kintaro-retreat-ball')
    with (BASE / (name + '.stdout.log')).open('w') as out, (BASE / (name + '.stderr.log')).open('w') as err:
        result = subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name, *args],
                                cwd=BASE, stdout=out, stderr=err, creationflags=FLAGS)
    assert result.returncode == 0, 'Inspect preserved stderr/runtime before retrying'
    subprocess.run([sys.executable, str(PORT / 'audit_campaign_run.py'), name],
                   cwd=PORT, check=True, creationflags=FLAGS)


if __name__ == '__main__':
    main()
