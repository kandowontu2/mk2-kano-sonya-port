"""Actual bundled Lua parser: full physical wrapper and passive audio expansion.

Source-only; all emulator callbacks parsed but never executed. No guest.
"""
import gzip
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path
import qualify_native_kano_laser_audio as source

ROOT=source.ROOT
OUT=ROOT/'audit_native_kano_laser_audio_lua_source'
need,sha=source.need,source.sha


def main():
    need(not OUT.exists(),'Fresh immutable audio Lua qualification');OUT.mkdir()
    try:
        cpp=ROOT/'tools/validate_native_kano_laser_audio_lua.cpp'
        lua=ROOT/'mk2ks_native_kano_laser_audio.lua'
        files=[Path(__file__),cpp,lua,ROOT/'mk2ks_native_kano_laser_burst.lua',ROOT/'mk2ks_native_kano_laser_typed_epochs.lua',
               ROOT/'mk2ks_native_kano_laser_action.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',
               ROOT/'audit_native_kano_laser_burst_lua_env_source/report.json']
        pins={str(p.resolve()):sha(p) for p in files}
        library=ROOT/'mame-mkp/build/mingw-gcc/bin/x64/Release/liblua.a';library_hash=sha(library)
        probe=OUT/'lua_audio_probe.exe'
        run=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',str(cpp),
                            '-I'+str(ROOT/'mame-mkp/3rdparty/lua/src'),str(library),'-lm','-o',str(probe)],capture_output=True,text=True)
        (OUT/'compiler.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'Actual native Lua parser probe compiles warning-free')
        run=subprocess.run([str(probe),str(lua)],cwd=ROOT,capture_output=True)
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=run.returncode,stdoutBytes=len(run.stdout),stderr=run.stderr.decode(errors='replace')),indent=2)+'\n')
        need(run.returncode==0 and not run.stderr,'Entire physical/audio nested source parsed by actual Lua')
        at=0;chunks=[]
        for _ in range(2):
            size=struct.unpack_from('<I',run.stdout,at)[0];at+=4;raw=run.stdout[at:at+size];at+=size
            need(len(raw)==size,'Whole native parser output');chunks.append(raw.decode())
        need(at==len(run.stdout),'No unparsed native output')
        physical,audio=chunks;original=(ROOT/'mk2ks_native_kano_laser_action.lua').read_text()
        first,last='emu.register_frame(function()','emu.register_frame_done(function()'
        need(physical[physical.index(first):physical.index(last)]==original[original.index(first):original.index(last)],
             'Whole selection/physical combat/round earning/laser command callback unchanged')
        for text in (physical,audio,lua.read_text()):
            need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),'No guest or register assistance')
        need(audio.count('for n=0,18 do')==audio.count('for channel=0,18 do')==2 and
             'MK2_MAUDIO_GUEST' not in audio and 'frame==origin+751' in audio,
             'All19 channels at video and sound callbacks; no duplicate guest or narrower audio window')
        need(all(sha(p)==h for p,h in pins.items()) and sha(library)==library_hash,'Executed source/library immutable through terminal')
        with gzip.open(OUT/'executed_sources.json.gz','wt')as f:json.dump(dict(actualExpandedPhysicalController=physical,actualExpandedAudioObserver=audio,outerObserver=lua.read_text()),f)
        probe.unlink()
        report=dict(passed=True,sourceOnlyAccepted=True,nativeGameplayAccepted=False,fullPortAcceptance=False,
                    actualNativeLuaParserAccepted=True,wholePhysicalCallbackByteIdentical=True,totalSampleChannels=19,
                    librarySHA256=library_hash,inputHashes=pins,latestPlayableChanged=False,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,sourceOnly=True,wholePhysicalCallbackUnchanged=True,channels=19)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
