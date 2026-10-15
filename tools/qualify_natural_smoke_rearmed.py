"""Whole secret/native-RNG/lifecycle proof with one final control epoch.

Earlier actual round responses are retained, not reused to pass a later
round. Every selected final response must belong to the surviving round.
"""
import gzip
import hashlib
import inspect
import json
import re
from pathlib import Path
import qualify_natural_smoke_lifecycle as previous
import check_natural_smoke_decisions as decisions

ROOT, need = previous.ROOT, previous.need


def responses(records, by, first, last, side, own, life):
    result = records['MK2_STAGE_SECRET_RESULT'][0]
    ready = max(f for f in life['originalNativeRoundStarts'] if f <= int(result['recover']))
    selected = dict(records)
    for tag in ('JUMP','PUNCH','RECOVER'):
        selected['MK2_STAGE_SECRET_'+tag] = [r for r in records['MK2_STAGE_SECRET_'+tag]
                                           if int(r['frame']) == int(result[tag.lower()]) and int(r['frame']) >= ready]
    need(int(result['walk']) >= ready, 'Final walking marker belongs to the actual final round, not an earlier KO epoch')
    actual = previous.responses(selected, by, ready, last, side, own, life)
    need(all(by[f,1]['mode'] == by[f,2]['mode'] == '2' for f in range(ready,last+1)), 'One real final round contains all controls and survival')
    actual.update(singleUninterruptedRoundControlSequenceAccepted=True, finalActualRoundStart=ready,
                  earlierRoundResponsesNeverSubstitute=True)
    return actual


scope = dict(previous.scope, responses=responses)
exec(compile(previous.source, __file__+'::whole_native_secret_lifecycle_final_epoch', 'exec'),scope)
phase_gate = scope['gate']
source = inspect.getsource(decisions.gate)
need(source.count('result = life.gate(c)') == 1, 'Only control epoch binding changes in complete native RNG gate')
scope = dict(vars(decisions),phase_gate=phase_gate)
exec(compile(source.replace('result = life.gate(c)','result = phase_gate(c)',1),__file__+'::whole_native_RNG_final_control_epoch','exec'),scope)
gate = scope['gate']


def qualify(c):
    need(c['report']['passed'] and c['terminal']['nativeExit'] == 0 and not previous.original.capture_host.native.census(), 'Same actual native terminal')
    actual = gate(c)
    path = c['folder']/'native_secret_rearmed_contract.json'
    need(not path.exists(), 'Fresh complete epoch proof')
    sources = {}
    for name,wanted in c['pins'].items():
        raw = Path(name).read_bytes()
        need(hashlib.sha256(raw).hexdigest().upper() == wanted, 'Whole executed input unchanged before archival')
        if Path(name).suffix in ('.py','.lua'):
            sources[name] = dict(sha256=wanted,text=raw.decode())
    with gzip.open(c['folder']/'executed_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump(sources,f)
    actual.update(nativeTerminal=c['terminal'],candidate=previous.original.capture_host.current.NAME,
                  inputHashes=dict(c['pins']), sourceHashes={str(Path(p).resolve()):hashlib.sha256(Path(p).read_bytes()).hexdigest().upper() for p in (__file__,previous.__file__,decisions.__file__,previous.original.__file__)},
                  allSecretBranchesAccepted=False, fullSecretAudioAccepted=False, fullPortAcceptance=False,
                  newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    path.write_text(json.dumps(actual,indent=2)+'\n')
    print(json.dumps(dict(passed=True,fighter=c['fighter'],physicalSlot=c['side'],actualSecretEntry=True,
                         completeSameRoundControlsAndSurvival=True,secretFieldsPerSlot=actual['secretFightFieldsPerSlot'])),flush=True)
    return actual
