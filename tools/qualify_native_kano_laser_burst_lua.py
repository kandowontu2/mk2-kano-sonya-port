"""Actual bundled native Lua parser, full final wrapper expansion only."""
import gzip
import hashlib
import json
import re
import subprocess
import traceback
from pathlib import Path

ROOT=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port')
OUT=ROOT/'audit_native_kano_laser_burst_lua_source'

def need(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def main():
    need(not OUT.exists(),'Fresh immutable actual Lua source qualification');OUT.mkdir()
    try:
        cpp=ROOT/'tools/validate_native_kano_laser_burst_lua.cpp';library=ROOT/'mame-mkp/build/mingw-gcc/bin/x64/Release/liblua.a'
        files=[cpp,ROOT/'mk2ks_native_kano_laser_burst.lua',ROOT/'mk2ks_native_kano_laser_typed_epochs.lua',ROOT/'mk2ks_native_kano_laser_action.lua',Path(__file__)]
        pins={str(p.resolve()):sha(p) for p in files}
        library_sha=sha(library);probe=OUT/'lua_source_probe.exe'
        run=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',str(cpp),
            '-I'+str(ROOT/'mame-mkp/3rdparty/lua/src'),str(library),'-lm','-o',str(probe)],capture_output=True,text=True)
        (OUT/'compiler.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'Actual bundled native Lua parser probe compiles')
        run=subprocess.run([str(probe),str(ROOT/'mk2ks_native_kano_laser_burst.lua')],cwd=ROOT,capture_output=True)
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=run.returncode,stdoutBytes=len(run.stdout),stderr=run.stderr.decode(errors='replace')),indent=2)+'\n')
        need(run.returncode==0 and not run.stderr,'Entire actual nested wrapper expansion parses using actual native Lua library')
        source=run.stdout.decode();original=(ROOT/'mk2ks_native_kano_laser_action.lua').read_text()
        begin='emu.register_frame(function()';end='emu.register_frame_done(function()'
        need(source.count(begin)==source.count(end)==original.count(begin)==original.count(end)==1 and
             source[source.index(begin):source.index(end)]==original[original.index(begin):original.index(end)],
             'Entire actual physical input/selection/round earning/command callback byte-identical to executed original')
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',source),
             'Full final controller contains only physical inputs/passive observers, no guest state/register/HP/AI/RNG writes')
        need(all(sha(p)==h for p,h in pins.items()) and sha(library)==library_sha,'Whole actual source/library conserved through native parser terminal')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualFinalExpandedController=source),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Exact terminal temporary source probe');probe.unlink()
        report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,actualNativeLuaParserAccepted=True,
            actualControllerBytes=len(run.stdout),actualControllerSHA256=hashlib.sha256(run.stdout).hexdigest().upper(),
            wholePhysicalCallbackByteIdentical=True,guestAssistance=False,fullPortAcceptance=False,
            librarySHA256=library_sha,libraryWasExistingBuildOutput=True,inputHashes=pins,
            newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,actualNativeLuaParser=True,wholePhysicalCallbackIdentical=True,controllerBytes=len(run.stdout))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise

if __name__=='__main__':main()
