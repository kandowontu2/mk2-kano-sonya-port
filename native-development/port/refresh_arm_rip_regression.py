"""Fresh sequential own arm-rip victims; bounded observation, not full acceptance."""
from pathlib import Path
import subprocess
import sys
from refresh_ingestion_regression import plan as ingestion_plan

PORT = Path(__file__).resolve().parent
BASE = PORT.parent / 'baseline'


def plan(prefix):
    return [(name, ['--arms-victim' if arg == '--body-suck-victim' else arg for arg in args])
            for name, args in ingestion_plan(prefix)]


def run(prefix):
    fixtures = plan(prefix)
    assert all(not (BASE / name).exists() for name, _ in fixtures), 'Never overwrite evidence'
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    for index, (name, args) in enumerate(fixtures, 1):
        if sys.platform == 'win32':
            idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                                   'if (Get-Process -Name mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
                                  capture_output=True, creationflags=flags)
            assert idle.returncode == 0, 'Existing emulator: do not overlap or terminate it'
        print(f'{index}/4 START {name}', flush=True)
        subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name, *args],
                       cwd=BASE, check=True, creationflags=flags)
        print(f'{index}/4 EXECUTED {name}; matrix qualification pending', flush=True)
    result = subprocess.run([sys.executable, str(PORT / 'qualify_arm_rip_runtime.py'),
                             *[name for name, _ in fixtures]], cwd=PORT,
                            capture_output=True, text=True, creationflags=flags)
    assert result.returncode == 0, result.stderr[-3000:]
    print('Four current arm-rip cases qualify; visual/blood acceptance remains open.', flush=True)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply a fresh prefix'
    run(sys.argv[1])
