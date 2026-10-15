"""Original actual corruption suite, bound to the final real control round.

Never corrupt an earlier jump/punch and call that a test of final controls.
KO-only cases are explicitly inapplicable when that native capture has no KO.
"""
import hashlib
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import qualify_natural_smoke_rearmed as current
import check_natural_smoke_decisions as original

need = current.need


def selected_inventory(text):
    records = original.life.original.inventory(text)
    need(len(records['MK2_STAGE_SECRET_RESULT']) == 1, 'One actual final response record')
    final = records['MK2_STAGE_SECRET_RESULT'][0]
    for tag in ('JUMP','PUNCH','RECOVER'):
        records['MK2_STAGE_SECRET_'+tag] = [r for r in records['MK2_STAGE_SECRET_'+tag]
                                           if r['frame'] == final[tag.lower()]]
        need(len(records['MK2_STAGE_SECRET_'+tag]) == 1, 'One actual selected final '+tag)
    return records


source = inspect.getsource(original.faults)
before = "        i = next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and select(dict(re.findall(r'(\\w+)=([^\\s]+)',line))))"
after = """        candidates = [i for i,line in enumerate(lines) if line.startswith(tag+' ') and select(dict(re.findall(r'(\\w+)=([^\\s]+)',line)))]
        if not candidates and label in ('native lethal collision omitted','native KO reset omitted'):
            _inapplicable.append(label)
            continue
        need(candidates, 'Actual non-vacuous final-control/native record available: '+label)
        i = candidates[0]"""
need(source.count(before)==1, 'Only original fault-record selection adapts for actual KO applicability')
scope = dict(original.faults.__globals__, gate=current.gate,
             life=SimpleNamespace(original=SimpleNamespace(inventory=selected_inventory)),
             _inapplicable=[])
exec(compile(source.replace(before,after,1),__file__+'::whole_original_final_epoch_faults','exec'),scope)


def check(c):
    need(c['terminal']['nativeExit']==0 and c['report']['passed'], 'Same original actual clean terminal')
    result = current.gate(c)
    scope['_inapplicable'].clear()
    faults = scope['faults'](c)
    skipped = list(scope['_inapplicable'])
    need(len(faults)+len(skipped)==14 and len(skipped) in (0,2),
         'Every original fault is actually executed or both absent-KO cases explicitly inapplicable')
    need(current.gate(c)==result, 'Whole native entry/HP/RNG/final-round positive restored')
    path = c['folder']/'native_secret_final_round_faults.json'
    need(not path.exists(), 'Fresh actual final-epoch fault receipt')
    report = dict(passed=True, actualNativeSecret=result, actualFaultsRejected=faults,
                  inapplicableUnobservedKOFaults=skipped,
                  sourceHashes={str(Path(p).resolve()):hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
                                for p in (__file__,current.__file__,original.__file__)},
                  finalControlEpochOnly=True, fullPortAcceptance=False,
                  newBuilds=0,newROMCopies=0,newRawMedia=0,newNativeBoots=0)
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True, actualFaultsRejected=len(faults),
                         inapplicableUnobservedKOFaults=skipped)),flush=True)
    return report
