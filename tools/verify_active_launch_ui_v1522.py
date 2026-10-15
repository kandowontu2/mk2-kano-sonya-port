"""Fresh current both-slot CSS -> native ladder -> actual first match.

Reuse the independent original UI pixel/control contract without reusing its
historical candidate declaration. Match every current launch/source/hash and
the actual observed guest tables to the independently reconstructed payload.
"""
import json,re,struct
from pathlib import Path
import verify_ring_native_lookup_v1342 as current
import verify_active_launch_timer_v1520 as grab
import verify_native_ui_flow_v814 as model
ROOT=current.ROOT;NAME=grab.NAME;OUT=ROOT/'audit_v1522_active_launch_ui_checked'

def verify():
    proof=json.loads((grab.OUT/'report.json').read_text());assert proof['passed']and proof['candidate']==NAME and proof['wholeGuestIndependentlyReconstructed']
    pins=dict(proof['inputHashes'])
    for file,wanted in pins.items():assert current.digest(file)==wanted,'Changed current source proof'
    guest,_,_=grab.expected_guest()
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'));cases={}
    for fighter in ('kano','sonya'):
        for side in (1,2):
            key=f'{fighter}_p{side}';folder=ROOT/f'audit_v1519_ui_{key}'
            launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            assert (launch['exit_code'],launch['candidate'],launch['fighter'],launch['side'],launch['assistance'])==(0,NAME,fighter,side,'none')
            assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
            assert launch['input_hashes']==before and all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
            for file,wanted in before.items():
                assert current.digest(file)==wanted,'Changed current launch input '+file;pins[file]=wanted
                if Path(file).suffix in ('.ps1','.lua','.json'):
                    assert current.digest(folder/'input_sources'/Path(file).name)==wanted,'Changed frozen UI input'
            observer=(folder/'input_sources/mk2ks_native_ui_flow_v2_probe.lua').read_text()
            assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Read-only native UI observer'
            assert '-nocheat' in (folder/'input_sources/run_native_ui_flow_v813.ps1').read_text()
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation|stack traceback',log,re.I)
            for row in model.records(log,'CODE'):
                first,last=model.h(row,'start'),model.h(row,'stop')
                raw=b''.join(struct.pack('<H',int(word,16))for word in row['words'].split(','))
                assert raw==guest[(first-0xff800000)//8:(last-0xff800000)//8],'Entire observed UI guest tables differ from independent native reconstruction'
            cases[key]={**model.verify_log(log,fighter,side),'rendered':model.render(folder,log,fighter,side)}
            print(key+' current border/blink/number/animation/backdrop/teardown/ladder/identity/name-shadow passed',flush=True)
            for path in folder.rglob('*'):
                if path.is_file():pins[str(path)]=current.digest(path)
    for file in ('verify_active_launch_ui_v1522.py','verify_native_ui_flow_v814.py','verify_cpu_air_gate.py','verify_cpu_air_runtime.py','verify_p2_campaign.py','verify_ring_native_lookup_v1342.py','verify_native_grab_audio_v1415.py'):
        path=ROOT/'tools'/file;pins[str(path)]=current.digest(path)
    for file in ('mk2/mk2-maincpu.bin','roms/mk2ks/mk2ks.ui'):
        path=ROOT/file;pins[str(path)]=current.digest(path)
    assert pins[str(ROOT/'roms/mk2ks/mk2ks.ui')]==model.UI_SHA
    assert pins[str(ROOT/'mk2/mk2-maincpu.bin')]==model.ORIGINAL_SHA
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,
                currentBothSlotSelectionLadderFirstMatchAccepted=True,fullLaddersAccepted=False,
                allCinematicsAccepted=False,audioAccepted=False,fullPortAccepted=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve earlier evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Current UI passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
