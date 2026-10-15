"""Separate actual blood allocation epochs from legitimate later art reuse.

Preserve global-descriptor palette rejection: native nonlive scenes reuse
some stock frames under other palettes after the blood objects retire.
Bind family by real object allocation lifetime, never art address alone.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood_palette as palette

ROOT,need,sha=palette.ROOT,palette.need,palette.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_epoch_checked'
FAILURE=palette.OUT/'failure.json'
SCOPE=None


def palette_gate(groups,guest):
    accepted=json.loads((palette.original.previous.OUT/'report.json').read_text())
    need(accepted['passed'],'Whole accepted actual source/Main/pool blood allocation family')
    epochs=accepted['stockBlood']['actualBloodAllocationEpochs']
    def in_actual_epoch(q):
        return any(q['actor']==e['actor'] and e['bornSequence']<q['sequence']<e['retiredSequence']
                   and q['cache']in e['descriptors']for e in epochs)
    source=inspect.getsource(palette.palette_gate)
    before="if q['cache']not in descriptors:continue"
    need(source.count(before)==1,'One exact incorrect artwork-only family assumption')
    source=source.replace(before,'if not in_actual_epoch(q):continue',1)
    scope=dict(palette.palette_gate.__globals__,in_actual_epoch=in_actual_epoch)
    exec(compile(source,__file__+'::whole_source_palette_gate_actual_pool_epochs','exec'),scope)
    result=scope['palette_gate'](groups,guest)
    descriptors={d for e in epochs for d in e['descriptors']}
    aliases=[q for q in groups['QUEUE']if q['cache']in descriptors and not in_actual_epoch(q)]
    result['nativeStockDescriptorReuseOutsideBloodLifetimes']=len(aliases)
    result['firstSuchReuseFrame']=min(q['frame']for q in aliases)if aliases else None
    return result


def gate(groups,guest):
    colors=palette_gate(groups,guest)
    result=palette.original.gate(groups,guest)
    result['completeStockFamilyPaletteBinding']=colors
    return result


def safe_execute(state):
    global SCOPE
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Every source-validated stock blood descriptor retains actual allocator palette, never silently excluded')",
         'Actual artwork-only palette rejection retained, no guest or prior source changes')
    bound=palette.original
    source=inspect.getsource(bound.execute)
    before='for p in (Path(__file__),Path(previous.__file__),parent_path,'
    need(source.count(before)==1,'Keep whole original22-fault/whole-positive/companion-binding source')
    source=source.replace(before,
        'for p in (Path(__file__),Path(palette.__file__),FAILURE,Path(bound.__file__),palette.FAILURE,Path(previous.__file__),parent_path,',1)
    SCOPE=dict(bound.__dict__,OUT=OUT,__file__=__file__,gate=gate,palette=palette,FAILURE=FAILURE,bound=bound)
    exec(compile(source,__file__+'::whole_actual22_faults_and_native_source_epoch_palette_binding','exec'),SCOPE)
    wrapper=inspect.getsource(bound.safe_execute)
    exec(compile(wrapper,__file__+'::whole_original_failure_preservation','exec'),SCOPE)
    return SCOPE['safe_execute'](state)
