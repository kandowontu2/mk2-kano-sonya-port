"""Preserve actual palette-exclusion counterexample; bind complete stock family.

The already source-validated28 descriptors and17 real pool lifetimes define
the finite native stock-blood family. Do not allow an altered allocator pointer
to remove one of those publications from classification. Independently bind
every family publication to the companion's captured full native palette.
"""
import inspect
import json
import struct
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_pressure_blood_bound as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_palette_checked'
FAILURE=original.OUT/'failure.json'
SCOPE=None


def palette_gate(groups,guest):
    family_path=original.previous.OUT/'report.json'
    accepted=json.loads(family_path.read_text())
    need(accepted['passed'],'Whole prior actual pool/Main/descriptor family accepted')
    descriptors={d for e in accepted['stockBlood']['actualBloodAllocationEpochs']for d in e['descriptors']}
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    at=(0xffaf2a40-0xff800000)//8
    count=struct.unpack_from('<H',stock,at)[0]
    need(count==15 and guest[at:at+2+count*2]==stock[at:at+2+count*2],
         'Entire original fifteen-color stock blood record unchanged')
    colors=struct.unpack_from('<15H',stock,at+2)
    expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest
        for s,dest in ((10,16),(5,8),(0,0)))for c in colors],dtype=np.uint32)
    context=original.companion.scope['CONTEXT']
    capture=original.companion.serialized.body.original.previous.capture
    need(capture.NATIVE_HANDLES[capture.KEY]['process'].poll()==0,
         'Original47004 companion full native palette handle remains terminal')
    checked=0;palettes={}
    for q in groups['QUEUE']:
        if q['cache']not in descriptors:continue
        need(q['palette_source']==0xffaf2a40 and q['refs']>0,
             'Every source-validated stock blood descriptor retains actual allocator palette, never silently excluded')
        frame=q['frame']+1
        need(frame in context['displays'],'Actual next displayed companion field has complete captured palette')
        if frame not in palettes:
            file=context['displays'][frame]['palette_file']
            palettes[frame]=np.frombuffer(capture.DISPLAY['buffers'][file],dtype='<u4')
        need(np.array_equal(palettes[frame][q['bank']:q['bank']+15],expected),
             'Every declared stock blood bank matches all15 source colors in actual companion palette')
        checked+=1
    need(checked==accepted['stockBlood']['nativeBloodPublications'],
         'Entire independently source-validated stock blood family still classified')
    return dict(validatedStockDescriptors=len(descriptors),wholeFifteenColorPaletteComparisons=checked,
        wholeActualCompanionPaletteFields=len(palettes),companionNative=47004,
        currentNewPaletteBuffersIndependentlyCaptured=False)


def gate(groups,guest):
    palette=palette_gate(groups,guest)
    result=original.gate(groups,guest)
    result['completeStockFamilyPaletteBinding']=palette
    return result


def safe_execute(state):
    global SCOPE
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and failed['error']==
         "ValueError('Effective actual blood counterexample accepted: actual_blood_publication_palette_source')",
         'Keep actual palette-exclusion fault-suite failure, no source edit or smaller suite')
    source=inspect.getsource(original.execute)
    before='for p in (Path(__file__),Path(previous.__file__),parent_path,'
    need(source.count(before)==1,'Keep whole actual22-fault/positive/binding source; add all rejected predecessors')
    source=source.replace(before,
        'for p in (Path(__file__),Path(original.__file__),FAILURE,Path(previous.__file__),parent_path,',1)
    SCOPE=dict(original.__dict__,OUT=OUT,__file__=__file__,gate=gate,original=original,FAILURE=FAILURE)
    exec(compile(source,__file__+'::whole_original22_faults_complete_source_blood_palette_family','exec'),SCOPE)
    wrapper=inspect.getsource(original.safe_execute)
    exec(compile(wrapper,__file__+'::original_full_failure_preservation','exec'),SCOPE)
    return SCOPE['safe_execute'](state)
