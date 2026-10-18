"""Recheck explicit completed nonlethal recordings; never start an emulator."""
import json
import subprocess
import sys
from refresh_nonlethal_regression import plan, profile, PORT, BASE


def run(prefix):
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    fixtures = plan(prefix)
    def check(script, *args):
        result = subprocess.run([sys.executable, str(PORT / script), *args], cwd=PORT,
                                capture_output=True, text=True, creationflags=flags)
        assert result.returncode == 0, result.stderr[-3000:]
    for name, args, negative in fixtures:
        receipt = json.loads((BASE / name / 'execution.json').read_text())
        assert receipt['testArguments'] == args
        assert receipt['exitCode'] == 0 and not receipt['timedOut']
        kind, actor, _, _ = profile(args, negative)
        if not negative:
            check('qualify_finisher_rejoin.py', name)
        if kind == 'baby':
            check('qualify_baby.py', name, str(actor))
        else:
            check('qualify_kano_friend.py' if actor == 17 else 'qualify_sonya_friend.py', name)
        if kind == 'friend' and actor == 18 and not negative:
            check('qualify_friend_lifecycle.py', name)
        print('REQUALIFIED', name, flush=True)
    for negative, script in ((False, 'qualify_nonlethal_matrix.py'), (True, 'qualify_negative_nonlethal_matrix.py')):
        check(script, *[name for name, _, mode in fixtures if mode == negative])
    print('16 recorded nonlethal cases requalified; no emulator rerun; full port not certified.', flush=True)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Supply the explicit completed fixture prefix'
    run(sys.argv[1])
