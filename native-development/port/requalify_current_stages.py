"""Recheck completed stage recordings; never start an emulator."""
import json
import subprocess
import sys
from refresh_stage_regression import plan, profile, PORT, BASE


def run(prefix):
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    fixtures = plan(prefix)
    def check(script, *args):
        result = subprocess.run([sys.executable, str(PORT / script), *args], cwd=PORT,
                                capture_output=True, text=True, creationflags=flags)
        assert result.returncode == 0, result.stderr[-3000:]
    for name, args in fixtures:
        receipt = json.loads((BASE / name / 'execution.json').read_text())
        assert receipt['testArguments'] == args
        assert receipt['exitCode'] == 0 and not receipt['timedOut']
        kind, actor, _ = profile(args)
        if kind in ('deadpool', 'negative'):
            check('qualify_deadpool_runtime.py', name)
        elif kind == 'tomb':
            check('qualify_tomb_stage.py', name, str(actor))
        else:
            check('qualify_pit_rejoin.py', name, str(actor))
        print('REQUALIFIED', name, flush=True)
    check('qualify_stage_positive_matrix.py', *[name for name, _ in fixtures])
    print('16 recorded stage cases requalified; no emulator rerun; full port not certified.', flush=True)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply the explicit completed fixture prefix'
    run(sys.argv[1])
