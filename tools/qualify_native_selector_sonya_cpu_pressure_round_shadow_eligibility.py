"""Whole original round/clip gates with source-native hidden-body eligibility.

After the stock final blow, native body flag20h suppresses the player composite
for69 callbacks. The independently owned player still exists and every shadow
eligibility call is observed; an effect corpse is not the hidden player body.
Preserve both actual earlier checker failures, never invent missing candidates.
"""
import inspect
import json
from functools import lru_cache
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow_clip as clip

clip_source=Path(clip.__file__)
clip_failure=clip.OUT/'failure.json'
need=clip.need
need(json.loads(clip_failure.read_text())['error']==
     "ValueError('Both entire actual native body composites observed at every ready field, including routine entries')",
     'Preserve actual post-clip whole native hidden-body eligibility rejection')


@lru_cache(maxsize=2)
def expected_physical_bodies(text):
    pair=clip.mechanics.capture.base.choices.native_state.original.pair
    fields=pair.rows(text,'FIELD')
    need(len(fields)==1075,'Entire independent physical pre-CPU callback inventory')
    eligible=set();hidden=set()
    for r in fields:
        for s in (1,2):
            flag=r['vbody'if s==1 else'body']
            need(flag&2,'All actual physical fighter bodies are native composites')
            (hidden if flag&32 else eligible).add((r['frame'],s))
    need(hidden=={(f,1)for f in range(3107,3176)} and len(eligible)==2081,
         'Exactly69 independently observed hidden victim composites; no standing/move/reset bodies omitted')
    return eligible


def body_expected(b,frames):
    need(frames=={r['frame']for r in clip.mechanics.capture.base.choices.native_state.original.pair.rows(b['cpuLog'],'FIELD')},
         'Hidden eligibility cannot change complete independent live frame inventory')
    return expected_physical_bodies(b['cpuLog'])


source=clip_source.read_text()
before="body_scope=dict(vars(original.body),native_published=native_published)"
after="""body_source=original.mechanics.phases.replace(body_source,
    'set(compositions)=={(f,s)for f in frames for s in(1,2)}',
    'set(compositions)==body_expected(b,frames)')
body_scope=dict(vars(original.body),native_published=native_published,body_expected=body_expected)"""
need(source.count(before)==1,'Only complete source-defined native body eligibility inventory boundary')
source=source.replace(before,after,1)
for before,after in (
    ("audit_native_selector_sonya_cpu_pressure_round_shadow_clip_checked",
     "audit_native_selector_sonya_cpu_pressure_round_shadow_eligibility_checked"),
    ('Path(__file__),original_source,original_failure,ops,parent,Path(disasm.__file__),',
     'Path(__file__),clip_source,clip_failure,original_source,original_failure,ops,parent,Path(disasm.__file__),'),
    ("0xffa0dfc0:'JA     FF876650h',0xff8042b0:'ADDXY  A9,A2',",
     "0xffa0dfc0:'JA     FF876650h',0xff804170:'BTST   1h,A7',0xff804180:'JREQ   FF8042A0h',"
     "0xff804190:'BTST   5h,A7',0xff8041a0:'JRNE   FF8045A0h',0xff8042b0:'ADDXY  A9,A2',"),
    ('originalStrictClipFailurePreserved=True,sourceNativeXYBoundaryChecks=8,',
     'originalStrictClipFailurePreserved=True,sourceNativeXYBoundaryChecks=8,'
     'originalHiddenEligibilityFailurePreserved=True,independentEligibleBodyFields=2081,'
     'independentHiddenVictimBodyFields=69,effectCorpseRenderingAccepted=False,')):
    need(source.count(before)==1,'Exact full original eligibility/failure provenance boundary')
    source=source.replace(before,after,1)
exec(compile(source,str(clip_source)+'::whole_original_clip_model_exact_independent_native_hidden_body_inventory','exec'))
