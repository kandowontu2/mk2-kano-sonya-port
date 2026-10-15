"""Whole original native Tomb rejoin retirement for reversed physical slots.

Keep all initial/later scanout, state, damage, motion and24 actual faults.
Only exact physical IDs change to Sonya18 P1/Kano17 P2. All held native
rasters must be newly reviewed; no reuse by old frame number alone.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import retire_native_tomb_transition_scanout as original


def once(source,before,after):
    original.need(source.count(before)==1,'One exact original reversed-slot adaptation '+before)
    return source.replace(before,after,1)


def retire(ram,newly_viewed_frames,visual_observations):
    report=ram['report'];fighter,side=report['fighter'],report['side']
    original.need(report['passed'] and (fighter,side)in(('sonya',1),('kano',2)) and
                  report['truePhysicalIDs']==(18,17) and visual_observations and
                  len(visual_observations)>40,'Actual reversed slots, selected performer and individual review')
    state=inspect.getsource(original.previous.state_facts)
    for before,after in (("a[0]['ids']=='17,18'","a[0]['ids']=='18,17'"),
                         ('((1,17),(2,18))','((1,18),(2,17))'),
                         ('(17 if s==1 else 18)','(18 if s==1 else 17)'),
                         ('actualTruePhysicalIDs=[17,18]','actualTruePhysicalIDs=[18,17]')):
        state=once(state,before,after)
    namespace=dict(vars(original.previous))
    exec(compile(state,__file__+'::whole_original_state_facts_exact_reversed_IDs','exec'),namespace)
    # Keep the whole original12-fault retirement block. Its namespace now
    # exports the exact reversed-ID state gate, not a simplified substitute.
    parent=SimpleNamespace(**namespace)
    body=inspect.getsource(original.retire)
    body=once(body,"known={r['frame']:r['rgbSHA256']for r in prior['individuallyReviewedFields']}",'known={}')
    body=once(body,'for p in (Path(__file__),Path(previous.__file__),prior_path,base_path,',
        'for p in (Path(__file__),Path(original.__file__),Path(previous.__file__),prior_path,base_path,')
    before="actualVisualObservations='Native fatality shutters/continue, own numbered selection portraits and locked poses, correct native Battle3 portraits, clean Wasteland fight entry, actual Kano/Sonya walking/jump/landing/low-kick contact, both floor shadows and black-shadowed native lifebar names.',"
    body=once(body,before,'actualVisualObservations=visual_observations,performer=fighter,physicalSlot=side,')
    scope=dict(vars(original),__file__=__file__,original=original,previous=parent,
               fighter=fighter,side=side,visual_observations=visual_observations)
    exec(compile(body,__file__+'::entire_original_reversed_slot24_faults_review_and_RAM_retirement','exec'),scope)
    return scope['retire'](ram,newly_viewed_frames)
