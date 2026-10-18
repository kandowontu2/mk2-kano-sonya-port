"""Construct local baseline chips and test on stock MAME; no custom driver."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SRC=HERE/'mk2-rebuild-main/src/rom'
OUT=HERE/(sys.argv[1] if len(sys.argv)>1 else 'stock_mame_test')
MAME=ROOT.parent/'mame0289/mame.exe'
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def main():
    assert not OUT.exists(), 'Keep test evidence; do not overwrite'
    OUT.mkdir(); (OUT/'roms').mkdir()
    chips={}
    for lane,chip in [(0,'uj12'),(1,'ug12')]:
        data=(SRC/f'U12F8.{lane}').read_bytes()+(SRC/f'U12FC.{lane}').read_bytes()
        assert len(data)==524288
        chips[f'l3.1_mortal_kombat_ii_game_rom_{chip}.{chip}']=data
    with zipfile.ZipFile(ROOT/'roms/mk2.zip') as original,zipfile.ZipFile(OUT/'roms/mk2.zip','x',zipfile.ZIP_DEFLATED) as result:
        for n in original.namelist():
            if '/' not in n: result.writestr(n,chips.get(n,original.read(n)))
    before=sha(MAME.read_bytes())
    cmd=[str(MAME),'mk2','-rompath',str(OUT/'roms'),'-video','none','-sound','none','-nothrottle','-skip_gameinfo','-autoboot_script',str(HERE/'probe.lua'),'-seconds_to_run','225','-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap')]
    with (OUT/'mame.log').open('w') as log:
        try:
            completed=subprocess.run(cmd,cwd=OUT,stdout=log,stderr=subprocess.STDOUT,timeout=60)
            status=dict(exitCode=completed.returncode,timedOut=False)
        except subprocess.TimeoutExpired: status=dict(exitCode=None,timedOut=True)
    assert sha(MAME.read_bytes())==before
    report=dict(emulator=str(MAME),emulatorSHA256=before,customDriver=False,gameMemoryWrites=False,
                programChips={n:sha(b) for n,b in chips.items()},**status)
    (OUT/'execution.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
