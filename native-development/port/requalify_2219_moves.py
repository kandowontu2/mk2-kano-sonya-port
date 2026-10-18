"""Current recorded move families only; this script never launches MAME."""
import subprocess
import sys
from pathlib import Path

PORT = Path(__file__).resolve().parent


def check(label, arguments):
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform == 'win32' else 0
    result = subprocess.run([sys.executable, *arguments], cwd=PORT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                            text=True, creationflags=flags)
    assert result.returncode == 0, label + ': ' + result.stderr[-3000:]
    print('REQUALIFIED', label, flush=True)


def main():
    check('16 ordinary special/side cells', ['-c', '''
from refresh_special_regression import plan,verify_case,matrix
fixtures=plan('stock_wolf_2219_special')
for name,args in fixtures: verify_case(name,args)
assert matrix([n for n,_ in fixtures])['allSixteenFiniteCasesPassed']
'''])
    check('8 own lethal/recovery cells', ['requalify_current_own_fatalities.py', 'stock_wolf_2219_fatal'])
    check('14 recorded morph cases and art cadence', ['-c', '''
import json,subprocess,sys
import refresh_morph_regression as r
flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
fixtures=r.plan('stock_wolf_2219_morph')+r.plan('stock_wolf_2219_morphall',all_specials=True)
for name,args in fixtures:
    receipt=json.loads((r.BASE/name/'execution.json').read_text())
    assert receipt['testArguments']==args and receipt['exitCode']==0 and not receipt['timedOut']
    subprocess.run([sys.executable,str(r.PORT/'qualify_morph.py'),name],check=True,stdout=subprocess.DEVNULL,creationflags=flags)
subprocess.run([sys.executable,str(r.PORT/'qualify_morph_art_trace.py'),'stock_wolf_2219_morphall_special_p1','stock_wolf_2219_morphall_special_p2'],check=True,stdout=subprocess.DEVNULL,creationflags=flags)
'''])
    check('8 transformed lethal/fresh-Shang cells', ['-c', '''
import refresh_morph_finisher_rejoin as r
prefix='stock_wolf_2219_morphfatal'
assert all((r.BASE/name/'execution.json').is_file() for name,_,_,_ in r.plan(prefix))
r.run(prefix)
'''])
    check('16 nonlethal positive/negative cases', ['requalify_current_nonlethals.py', 'stock_wolf_2219_nonlethal'])
    check('16 stage/chord/Pit/rejoin cases', ['requalify_current_stages.py', 'stock_wolf_2219_stage'])
    print('Recorded current-ROM families requalified; no emulator rerun; full port not certified.', flush=True)


if __name__ == '__main__':
    main()
