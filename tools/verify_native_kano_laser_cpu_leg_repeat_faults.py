"""Requalify the same terminal Sonya trial; all original repeated/body-shadow faults.

No emulator boot, raw media or reconstructed ROM is written. Use the actual
capture module's in-memory independently derived guest/GFX and native RGB.
"""
import copy
import inspect
import json
import re
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_cpu_leg_repeat as capture
import test_repeated_cpu_contract_v1465 as repeated_faults
from test_physical_cpu_contract_v1458 import change

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_kano_laser_cpu_leg_repeat_fault_checked'


def run(actual):
    out=actual.OUT.with_name(actual.OUT.name.replace('_checked','_fault_checked'))
    need(not out.exists(),'Fresh immutable same-trial fault proof')
    key=getattr(actual,'KEY','leg_cpu_sonya_p1_human_kano_p2')
    folder,text,images=actual.RAM_CASES[key]
    report=json.loads((folder/'result.json').read_text())
    need(report['passed'] and report['nativeExit']==0 and not capture.base.identity.census(),
         'Exact actual trial terminal, no native replay')
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual capture input conserved')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
            rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    human=report['victim']
    b=dict(move='leg',side=report['side'],folder=folder,report_path=folder/'result.json',report=report,
           rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()),human=human,cpuLog=text)
    case=actual.check(b,actual.guest,actual.payload,actual.gfx32)
    canonical=lambda value:json.loads(json.dumps(value))
    need(canonical(case)==report['sourceBoundBodyShadowSemantics'],'Exact repeated positive control, JSON key normalization only')
    body_faults=capture.base.shadow_faults(b,actual.guest,actual.payload,actual.gfx32,actual.check)
    physical=actual.physical_bindings(actual.guest)

    def verify(log,human):
        try:return physical(log,human,actual.guest)['originalContract']
        except (ValueError,AssertionError)as error:return dict(passed=False,errors=[str(error)])

    pristine=verify(text,human);need(pristine['passed'],'Entire full-health current repeated positive')
    source=inspect.getsource(repeated_faults.run)
    first=source.index(" second=pristine['pairs'][1]")
    last=source.index(' assert source.prior.digest(path)==before',first)
    body='\n'.join(line[1:] if line.startswith(' ')else line for line in source[first:last].splitlines())
    need(body.count("model.verify_log(mutant,'kano')")==1,'Entire original physical counterexample dispatch')
    body=body.replace("model.verify_log(mutant,'kano')","model.verify_log(mutant,human)")
    if report['side']==2:
        need(body.count("'human_slot',1")==1,'Single actual physical-role counterexample adaptation')
        body=body.replace("'human_slot',1","'human_slot',2")
    function='def faults(log,pristine):\n'+'\n'.join('    '+line for line in body.splitlines())+'\n    return results\n'
    scope=dict(vars(repeated_faults),model=SimpleNamespace(rows=capture.repeated.rows,verify_log=verify),human=human)
    exec(compile(function,__file__+'::all_ten_original_repeated_pair_counterexamples','exec'),scope)
    physical_faults=scope['faults'](text,pristine)
    need(len(physical_faults)==10,'All ten original first/second-pair and continuation faults')

    # Additional current-native instruction and post-field provenance failures.
    flags=capture.repeated.flag_rows(text)
    extra=[]
    for slot in (1,2):
        target=next(line for line in text.splitlines()if line.startswith('MK2_CPU_PAIR_FLAG ')and f'slot={slot} 'in line)
        observed=int(re.search(r'op0=([0-9A-Fa-f]+)',target)[1],16)
        changed=re.sub(r'op0=[0-9A-Fa-f]+',f'op0={observed^1:04X}',target)
        extra.append((f'current_physical_slot_{slot}_instruction_word_wrong',text.replace(target,changed,1)))
    first_health=next(line for line in text.splitlines()if line.startswith('MK2_CPU_PAIR_HEALTH '))
    observed=int(re.search(r'before=(\d+)',first_health)[1])
    extra.append(('whole_native_health_store_operand_wrong',text.replace(first_health,re.sub(r'before=\d+',f'before={observed-1}',first_health),1)))
    second_start=pristine['pairs'][1]['start']
    post=next(line for line in text.splitlines()if line.startswith('MK2_HPHASE_POST_FIELD ')and f'frame={second_start+1} 'in line)
    extra.append(('second_pair_actual_draw_field_missing',text.replace(post+'\n','',1)))
    for label,changed in extra:
        need(changed!=text,'Actual non-no-op current provenance fault')
        checked=verify(changed,human);need(not checked['passed'],'Current physical provenance fault must reject: '+label)
        physical_faults.append(dict(counterexample=label,rejected=True,errors=checked['errors']))

    restored=actual.check(b,actual.guest,actual.payload,actual.gfx32)
    need(canonical(restored)==canonical(case),'Full original positive restored after all faults')
    pins=dict(report['inputHashes'])
    for p in (Path(__file__),Path(repeated_faults.__file__),ROOT/'tools/test_physical_cpu_contract_v1458.py',
              folder/'result.json',folder/'run.log.gz',folder/'native_terminal.json',folder/'shadow_stream_memory_proofs.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Immutable actual native and counterexample evidence')
    out.mkdir();capture.base.save(out/'report.json',dict(passed=True,candidate=report['candidate'],case=case,inputHashes=pins,
        actualBodyShadowFaultsRejected=body_faults,actualPhysicalFaultsRejected=physical_faults,
        actualFaultsRejected=len(body_faults)+len(physical_faults),actualCPUFullPairs=len(pristine['pairs']),
        nativeReplay=False,everyReadyOwnedBodyShadowFieldSourceBound=True,wholeNativeHealthHistoryVerified=True,
        fullVisualTimelineAccepted=False,fullAudioAcceptance=False,allCPUContextsAccepted=False,allArenasAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'))
    print(json.dumps(dict(passed=True,actualFullPairs=len(pristine['pairs']),actualFaultsRejected=len(body_faults)+len(physical_faults))),flush=True)
