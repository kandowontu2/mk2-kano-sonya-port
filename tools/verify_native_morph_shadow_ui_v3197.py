"""Fresh native-palette candidate: both-slot CSS -> ladder -> actual match.

Reuse the independent original UI pixel/control contract without reusing its
historical candidate declaration. Match every current launch/source/hash and
the actual observed guest tables to the independently reconstructed payload.
"""
import json,re,struct
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as current
from verify_human_special_phases_v1767 import sha
import sys
import verify_native_ui_flow_v814 as model
import verify_human_shang_v3174 as matched
import verify_native_morph_floor_projection_v3185 as floor
ROOT=current.ROOT;NAME=matched.CANDIDATE;OUT=ROOT/'audit_v3198_native_morph_shadow_ui_checked'

def verify():
    proof_path=ROOT/'audit_v3186_native_morph_floor_projection_checked/report.json'
    proof=json.loads(proof_path.read_text())
    assert proof['passed'] and proof['candidate']==NAME and proof['correctedNativeMorphShadowStreamsAccepted']
    floor.source_contract()
    pins={**proof['inputHashes'],**current.source_check(),str(proof_path):sha(proof_path)}
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed current source proof'
    guest,_,_,_,_=current.expected()
    payload=(ROOT/'audit_v3169_native_morph_shadow_payload/roms/mk2ks/mk2ks.mdata').read_bytes()
    import hashlib
    assert hashlib.sha256(guest).hexdigest().upper()=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7'
    assert sha(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==matched.PAYLOAD
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'));cases={}
    assert (build['name'],build['executable_sha256'],build['payload_sha256'])==(NAME,matched.EXE,matched.PAYLOAD)
    assert payload==(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    for fighter in ('kano','sonya'):
        for side in (1,2):
            key=f'{fighter}_p{side}';folder=ROOT/f'audit_v3196_ui_{key}'
            launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            assert (launch['exit_code'],launch['candidate'],launch['fighter'],launch['side'],launch['assistance'])==(0,NAME,fighter,side,'none')
            assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
            assert launch['input_hashes']==before and all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
            for file,wanted in before.items():
                assert sha(file)==wanted,'Changed current launch input '+file;pins[file]=wanted
                if Path(file).suffix in ('.ps1','.lua','.json'):
                    assert sha(folder/'input_sources'/Path(file).relative_to(ROOT))==wanted,'Changed frozen UI input'
            observer=(folder/'input_sources/mk2ks_native_ui_flow_v2_probe.lua').read_text()
            assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),'Read-only native UI observer'
            assert '-nocheat' in (folder/'input_sources/tools/run_native_morph_shadow_ui_v3193.ps1').read_text()
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation|stack traceback',log,re.I)
            for row in model.records(log,'CODE'):
                first,last=model.h(row,'start'),model.h(row,'stop')
                raw=b''.join(struct.pack('<H',int(word,16))for word in row['words'].split(','))
                assert raw==guest[(first-0xff800000)//8:(last-0xff800000)//8],'Entire observed UI guest tables differ from independent native reconstruction'
            cases[key]={**model.verify_log(log,fighter,side),'rendered':model.render(folder,log,fighter,side)}
            print(key+' current border/blink/number/animation/backdrop/teardown/ladder/identity/name-shadow passed',flush=True)
            for path in folder.rglob('*'):
                if path.is_file():pins[str(path)]=sha(path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).resolve()
            if path.is_relative_to(ROOT/'tools')and path.suffix=='.py':pins[str(path)]=sha(path)
    for file in ('mk2/mk2-maincpu.bin','roms/mk2ks/mk2ks.ui'):
        path=ROOT/file;pins[str(path)]=sha(path)
    assert pins[str(ROOT/'roms/mk2ks/mk2ks.ui')]==model.UI_SHA
    assert pins[str(ROOT/'mk2/mk2-maincpu.bin')]==model.ORIGINAL_SHA
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,
                currentBothSlotSelectionLadderFirstMatchAccepted=True,observedUITablesExactlyIndependentGuest=True,
                wholeActualGuestCapturedByThisUIProbe=False,fullLaddersAccepted=False,
                allCinematicsAccepted=False,audioAccepted=False,fullPortAccepted=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve earlier evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Current UI passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
