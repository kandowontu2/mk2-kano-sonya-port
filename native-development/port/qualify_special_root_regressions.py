"""Run existing behavior assertions only after pinning the current entire ROM set."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
results=[]
for name in sys.argv[1:]:
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    args=receipt['testArguments']
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
            assert archive.read(chip)==b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC'))
        verify_archive_sockets(archive)
    mirror='--mirror' in args
    side=2 if mirror else 1
    if '--special' in args:
        square='--square' in args
        move_side=(1 if mirror else 2) if square else (2 if mirror else 1)
        result=importlib.import_module('qualify_initial_specials').qualify(name,move_side,0x207 if square else 0x20b)
    elif '--blade' in args or '--bike' in args:
        module='qualify_blade' if '--blade' in args else 'qualify_bike'
        result=importlib.import_module(module).qualify(name,mirror)
    elif '--choke' in args or '--leg' in args:
        choke='--choke' in args
        module='qualify_choke' if choke else 'qualify_leg'
        victim=1 if '--stock-victim' in args else (18 if choke else 17)
        move_side=side if choke else (1 if mirror else 2)
        result=importlib.import_module(module).qualify(name,move_side,victim)
    elif '--friend' in args:
        module='qualify_kano_friend' if '--kano' in args else 'qualify_sonya_friend'
        checked=subprocess.run([sys.executable,str(PORT/f'{module}.py'),name],capture_output=True,text=True,
            timeout=30,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        assert checked.returncode==0,checked.stdout+checked.stderr
        result=json.loads(checked.stdout)
    else:
        kind=next(flag for flag in ('extract','kiss','laser','bubble') if '--'+flag in args)
        victim=1 if '--stock-victim' in args else (18 if kind in ('extract','laser') else 17)
        call=importlib.import_module('qualify_'+kind).qualify
        result=call(name,side,victim,False) if kind in ('laser','bubble') else call(name,side,victim)
    result=dict(test=name,currentFullROMVerified=True,behavior=result,fullPortVerified=False)
    (folder/'SPECIAL_ROOT_REGRESSION.json').write_text(json.dumps(result,indent=2)+'\n')
    results.append(result)
print(json.dumps(results,indent=2))
