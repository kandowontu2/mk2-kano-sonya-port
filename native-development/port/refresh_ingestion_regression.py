"""Fresh, sequential own-victim ingestion observations; no guest writes."""
from pathlib import Path
import subprocess
import sys

PORT = Path(__file__).resolve().parent
BASE = PORT.parent / 'baseline'


def plan(prefix):
    assert prefix and all(c.isalnum() or c in '_-' for c in prefix)
    return [(f'{prefix}_{actor}_p{side}',
             ['--game', '--body-suck-victim', '--sound-candidate',
              *(['--sonya'] if actor == 18 else []),
              *(['--mirror'] if side == 1 else [])])
            for side in (2, 1) for actor in (17, 18)]


def run(prefix, *, fixture_plan=plan, qualifier='qualify_ingestion_runtime.py', label='ingestion'):
    fixtures = fixture_plan(prefix)
    assert all(not (BASE / name).exists() for name, _ in fixtures), 'Never overwrite evidence'
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    for index, (name, args) in enumerate(fixtures, 1):
        if sys.platform == 'win32':
            idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                                   'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                                  capture_output=True, creationflags=flags)
            assert idle.returncode == 0, 'Existing emulator: do not overlap or terminate it'
        print(f'{index}/{len(fixtures)} START {name}', flush=True)
        subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name, *args],
                       cwd=BASE, check=True, creationflags=flags)
        print(f'{index}/{len(fixtures)} EXECUTED {name}; qualification pending complete matrix', flush=True)
    checked = subprocess.run([sys.executable, str(PORT / qualifier),
                              *[name for name, _ in fixtures]],
                             cwd=PORT, capture_output=True, text=True, creationflags=flags)
    assert checked.returncode == 0, checked.stderr[-3000:]
    print(f'{len(fixtures)} current {label} cases qualify; final visual/art acceptance remains open.', flush=True)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply a fresh evidence prefix'
    run(sys.argv[1])
