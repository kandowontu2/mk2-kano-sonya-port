"""Preserve the actual ineffective Lua-wrapper run, not a gameplay pass."""
import json
import subprocess
from pathlib import Path
import qualify_native_attract_early_square as mix
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

def archive(c):
    out=c['folder'];path=out/'configuration_failure.json'
    mix.need(not path.exists() and c['terminal']['nativeExit']==0 and not native.census(),'Same actual failed-configuration run fully terminal')
    inputs=mix.names.runtime.rows(c['text'],'INPUT')
    mix.need([int(r['frame']) for r in inputs]==[360,361,362,363,364],'Actual observed timing differs from intended420')
    before=json.loads((out/'report.json').read_text())
    mix.need(before['passed'] and '420..423' in before['physicalInputs'],'Preserve inaccurate transport-only input description; never reinterpret it as scenario success')
    result=dict(passed=False,transportOnlyAccepted=True,requestedConfigurationAccepted=False,fullPortAcceptance=False,
        nativeTerminal=c['terminal'],intendedBootFrames=[420,421,422,423],actualInputs=inputs,
        winnerObserverActuallyEnabled=False,actualWinnerCallRows=mix.names.runtime.rows(c['text'],'WINNER_CALL'),
        actualSoundMarkers=mix.names.runtime.rows(c['text'],'SOUND'),
        wholeNativePCMHeaders=[r['header'] for r in c['pcm']],wholeNativeDACHeaders=c['dacHeaders'],
        cause='MAME applies make_environment() to autoboot chunks. Bare wrapper assignments stay in the private environment, while dofile and rawget(_G,...) use Lua globals. Common observer therefore kept default360/false.',
        sourceProof=['mame-mkp/src/frontend/mame/mame.cpp sol::set_environment(lua()->make_environment(), func)',
                     'mame-mkp/src/frontend/mame/luaengine.cpp make_environment: sol::environment(sol(), sol::create, sol().globals())'],
        actualCompiledGuestUnchanged=c['guest']==mix.current.expected(),goalStatus='active',newBuilds=0,newROMCopies=0,newZIPs=0,
        newRawAudioCopies=0,nextAction='Explicitly configure host Lua _G values; require actual observed420..423/release424 and live native winner opcode evidence before scenario qualification.')
    path.write_text(json.dumps(result,indent=2)+'\n')
    storage=[]
    for file in [p for p in out.rglob('*') if p.is_file()]:
        digest=mix.sha(file)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(file)],check=True,capture_output=True)
        mix.need(mix.sha(file)==digest,'Actual failed-run evidence unchanged')
        storage.append(dict(path=str(file),allocatedBytes=allocated(file),sha256=digest))
    (out/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(configurationAccepted=False,nativeExit=0,actualBootFrame=360,retainedAllocatedBytes=sum(r['allocatedBytes'] for r in storage))),flush=True)
    return result
