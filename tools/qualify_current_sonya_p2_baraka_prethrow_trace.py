"""Loaded original handoff words and actual pre/post actor-owned throw pairing."""
from pathlib import Path
import check_campaign_stage_chronology as chronology
original_load=chronology.load
def comparable_load(path):
    result=original_load(path)
    # Cold loaded-word receipt has no counterpart in historical control logs.
    result.pop('THROW_HANDOFF_WORD',None)
    return result
chronology.load=comparable_load
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_throw_onset.py').read_text().replace('audit_current_sonya_p2_baraka_hk_throw_onset','audit_current_sonya_p2_baraka_prethrow_trace')
# Added passive rows are intentionally absent in reference.
source=source.replace("'BARAKA_THROW_START','HOST_BOUND'","'BARAKA_THROW_START','BARAKA_PRETHROW','THROW_HANDOFF_WORD','HOST_BOUND'")
exec(compile(source,__file__+'::native_context','exec'))
chronology.load=original_load
rows['THROW_HANDOFF_WORD']=original_load(case/'run.log')['THROW_HANDOFF_WORD']
expected=json.loads((sync.ROOT/'audit_current_sonya_p2_baraka_prethrow_trace_preparation/original-words.json').read_text())
assert expected['originalROM_SHA256']==sync.sha(sync.ROOT/'mk2/mk2-maincpu.bin')
observed={r['address']:int(r['value'],16) for r in rows.get('THROW_HANDOFF_WORD',[])}
assert observed=={r['address']:r['value'] for r in expected['words']}
pre=rows.get('BARAKA_PRETHROW',[]);assert pre
assert all(r['pc']=='FF8B6C70' and r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main'] and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in pre)
pairs=[]
for r in pre:
    post=[q for q in onsets if q['frame']==r['frame'] and q['cpu_main']==r['cpu_main'] and q['human_main']==r['human_main']]
    assert len(post)==1
    pairs.append(dict(frame=int(r['frame']),preAction=int(r['action']),preFlags=r['flags'],preHeight=int(r['height']),postAction=int(post[0]['action']),preGap=int(r['gap']),hardware=r['hardware'],kickAge=int(r['kick_age'])))
detail=dict(passedFiniteChecks=True,loadedOriginalInstructionWords=len(observed),actualSameFramePrePostPairs=pairs,postHandoffIdleInferenceRejected=True,fullPortAccepted=False)
(out/'prethrow-context.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
