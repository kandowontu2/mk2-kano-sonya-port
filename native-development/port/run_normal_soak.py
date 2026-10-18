"""One hidden normal-combat stress trial; original game state remains untouched."""
import subprocess
import sys
from refresh_special_videos import BASE, FLAGS


def main():
    assert sys.argv[1:] in ([], ['--mirror'])
    mirror = sys.argv[1:]
    name = 'stock_wolf_2219_normal_soak_v4' + ('_mirror' if mirror else '')
    assert not (BASE / name).exists(), 'Never overwrite evidence'
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    with (BASE / (name + '.stdout.log')).open('w') as out, (BASE / (name + '.stderr.log')).open('w') as err:
        result = subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name,
            '--game', '--normal-moves', '--normal-soak', '--sound-candidate', *mirror],
            cwd=BASE, stdout=out, stderr=err, creationflags=FLAGS)
    assert result.returncode == 0, 'Inspect preserved runtime before retrying'


if __name__ == '__main__':
    main()
