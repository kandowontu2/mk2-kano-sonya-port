"""Recheck explicit completed recordings; never launch or rerun the emulator."""
import importlib
import json
import subprocess
import sys
from refresh_fatality_regression import plan, profile, PORT, BASE, matrix


def run(prefix):
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    fixtures = plan(prefix)
    for name, args in fixtures:
        receipt = json.loads((BASE / name / 'execution.json').read_text())
        assert receipt['testArguments'] == args
        assert receipt['exitCode'] == 0 and not receipt['timedOut']
        recovery = subprocess.run([sys.executable, str(PORT / 'qualify_finisher_rejoin.py'), name],
                                  cwd=PORT, capture_output=True, text=True, creationflags=flags)
        assert recovery.returncode == 0, recovery.stderr[-3000:]
        kind, side, victim = profile(args)
        importlib.import_module('qualify_' + kind).qualify(name, side, victim)
        print('REQUALIFIED', name, flush=True)
    result = matrix([name for name, _ in fixtures])
    print(json.dumps(dict(cases=len(result['cases']), allEightCasesPassed=result['allEightCasesPassed'],
                          emulatorRerun=False, fullPortVerified=False)), flush=True)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply the explicit completed fixture prefix'
    run(sys.argv[1])
