"""Full unchanged round geometry; exact truth for pre-live entry observation.

Five real special entries include two pre-live opening callbacks1817/2610,
without body collection on those fields. Three entries are observed at draw;
the openings' following first-live draws are observed. Correct inherited
always-true entry metadata, not an acceptance predicate or native observation.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow_bound as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_scope_checked'
whole_parent=previous.OUT/'report.json'
whole_prior=json.loads(whole_parent.read_text())
need(whole_prior['passed']and all(sha(p)==h for p,h in whole_prior['inputHashes'].items()),
     'Entire original whole-round result, source and every retained failure intact')


def bindings(guest):
    old=previous.bindings(guest)
    source=inspect.getsource(previous.body.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=previous.mechanics.phases.replace(source,source[first:last],
        " state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_HPHASE_CPU_NATIVE_ENTRY']}\n")
    for before,after in (
        ('ids={side:identity,3-side:4}','ids={1:17,2:18}'),
        ("num(t,'floor')==floors[s]","num(t,'floor')==context(b['cpuLog'])['post'][f,s]['floor']"),
        ('entryBodyPublicationProven=True,',
         'entryBodyPublicationProven=entry_frames<=frames,'
         'actualRoutineEntryDrawFrames=sorted(entry_frames&frames),'
         'preliveRoutineEntriesWithoutBodyObservation=sorted(entry_frames-frames),'
         'actualFirstDrawFollowingOpeningEntries=sorted({f+1 for f in entry_frames-frames if f+1 in frames}),')):
        source=previous.mechanics.phases.replace(source,before,after)
    scope=dict(old.__globals__)
    exec(compile(source,__file__+'::entire_original_geometry_exact_pre_live_entry_metadata','exec'),scope)
    return scope['check']


source=inspect.getsource(previous.original.execute)
source=previous.mechanics.phases.replace(source,'pins=dict(proof[\'inputHashes\'])',
    "pins=dict(whole_prior['inputHashes']);need(all(pins.get(k)==h for k,h in proof['inputHashes'].items()),'Whole prior input inventory is a strict unchanged superset')")
source=previous.mechanics.phases.replace(source,
    'Path(__file__),parent,Path(disasm.__file__),',
    'Path(__file__),Path(previous.__file__),whole_parent,parent,Path(disasm.__file__),')
scope=dict(previous.execute.__globals__,__file__=__file__,OUT=OUT,bindings=bindings,
           previous=previous,whole_prior=whole_prior,whole_parent=whole_parent)
exec(compile(source,__file__+'::whole_original_execute_faults_exact_entry_scope','exec'),scope)
original_execute=scope['execute']


def execute(state):
    value=original_execute(state)
    case=value['wholePressureBodyShadowGeometry']
    need(not case['entryBodyPublicationProven']and case['actualRoutineEntryDrawFrames']==[1918,2847,2921]and
         case['preliveRoutineEntriesWithoutBodyObservation']==[1817,2610]and
         case['actualFirstDrawFollowingOpeningEntries']==[1818,2611],
         'Only three actual entry-frame bodies accepted; two pre-live openings remain explicitly unobserved')
    # Corrected metadata does not change a single source/physical/body/shadow
    # positive result from the original whole-round acceptance.
    comparable=dict(case)
    for key in ('actualRoutineEntryDrawFrames','preliveRoutineEntriesWithoutBodyObservation',
                'actualFirstDrawFollowingOpeningEntries'):comparable.pop(key)
    comparable['entryBodyPublicationProven']=True
    need(comparable==whole_prior['wholePressureBodyShadowGeometry'],
         'Every original whole body/shadow positive result unchanged except exact entry coverage metadata')
    return value
