"""Current v1836 physical startup interruptions and clean retries.

Keeps the original per-field v824 acceptance contract unchanged. The launch
contract is bound independently to the current compiled/source-proven build.
Not all move families, interrupt points, CPU, pixels, audio or full-port proof.
"""
import json
import re
import sys
from pathlib import Path
import verify_current_interrupt_and_ko_v824 as contract
import verify_ball_register_source_v1837 as current
from verify_human_special_phases_v1767 import sha

ROOT=current.ROOT
NAME=current.NAME
OUT=ROOT/'audit_v1870_current_interrupt_checked'
CAPTURE_VERSION=1869

def matched(folder,pins):
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assert result['observer_passed'] and result['exit_code']==0
    assert result['candidate']==NAME and result['assistance']==result['memory_assistance']=='none'
    assert result['cheats']==result['cheats_enabled']==False
    assert result['executable_sha256']==result['candidate_executable_sha256']==build['executable_sha256']
    assert result['payload_sha256']==build['payload_sha256']
    assert result['input_hashes']==before
    assert all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
    assert {'mk2ks_selector_exit_test.lua','mk2ks_native_shang_morph.lua'}<={Path(file).name for file in before}
    for file,wanted in before.items():
        assert sha(file)==wanted,'Changed current launch input '+file
        pins[file]=wanted
        path=Path(file)
        if path.suffix in ('.lua','.ps1','.json'):
            assert sha(folder/'input_sources'/path.name)==wanted,'Changed frozen launch source '+file
        if path.suffix=='.lua':
            assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',path.read_text()),'Guest state injection'
    assert before[str(ROOT/NAME/'mkport_candidate.exe')]==build['executable_sha256']
    assert before[str(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')]==build['payload_sha256']
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    return result

def source_pins():
    proof=json.loads((current.OUT/'report.json').read_text())
    assert proof['passed'] and proof['candidate']==NAME and proof['wholeActualGuestExactlyCallbackDelta']
    pins=dict(proof['inputHashes'])
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed current independent source proof '+file
    # Reconstruct the entire expected native guest, not just a pass summary.
    guest,previous,payload=current.expected()
    assert len(guest)==len(previous) and payload
    pins[str(current.OUT/'report.json')]=sha(current.OUT/'report.json')
    return pins

def module_pins(pins):
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).resolve()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pins[str(path)]=sha(path)

def verify():
    pins=source_pins();cases=[]
    for move,side,victim in contract.INT_CASES:
        folder=ROOT/f'audit_v{CAPTURE_VERSION}_interrupt_{move}_p{side}_{victim}'
        result=matched(folder,pins)
        assert (result['move'],result['side'],result['victim'])==(move,side,victim)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        cases.append(contract.verify_interrupt(log,move,side,victim))
        print(f'{move} p{side} vs {victim}: actual counter, cleanup, native recovery and retry passed',flush=True)
    module_pins(pins)
    return dict(passed=True,candidate=NAME,cases=cases,pairedFields=sum(case['pairedFields']for case in cases),
                inputHashes=pins,originalPerFieldAcceptanceUnchanged=True,gameBytesChanged=False,
                allInterruptionsAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Current interruption verification passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
