"""Bounded close-ready physical-input experiment, not a native balance edit."""
import json
import subprocess
import sys
from refresh_special_videos import BASE, PORT, FLAGS


def main():
    assert sys.argv[1:] in ([], ['--early104'], ['--early104', '--endurance'])
    early = '--early104' in sys.argv
    endurance = '--endurance' in sys.argv
    name = 'stock_wolf_2219_kano_kintaro_' + ('early_ready104' if early else 'ready84')
    if endurance:
        name += '_endurance'
    assert not (BASE / name).exists(), 'Never overwrite evidence'
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                           'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                          capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    prior = json.loads((BASE / 'stock_wolf_2219_kano_kintaro_ready104/execution.json').read_text())
    args = [a for a in prior['testArguments'] if not a.startswith('--campaign-kano-kintaro-ready-range=')]
    args.append('--campaign-kano-kintaro-ready-range=' + ('104' if early else '84'))
    if early:
        args.append('--campaign-kano-kintaro-early-counter')
    if endurance:
        args = [a for a in args if not a.startswith('--campaign-continues=')]
        args += ['--campaign-boss-endurance', '--campaign-continues=64']
    assert '--campaign-kano-kintaro-ready-counter' in args
    with (BASE / (name + '.stdout.log')).open('w') as out, (BASE / (name + '.stderr.log')).open('w') as err:
        result = subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name, *args],
                                cwd=BASE, stdout=out, stderr=err, creationflags=FLAGS)
    assert result.returncode == 0, 'Inspect preserved runtime/stderr before retrying'
    subprocess.run([sys.executable, str(PORT / 'inspect_kintaro_ready_counter.py'), name],
                   cwd=PORT, check=True, creationflags=FLAGS)


if __name__ == '__main__':
    main()
