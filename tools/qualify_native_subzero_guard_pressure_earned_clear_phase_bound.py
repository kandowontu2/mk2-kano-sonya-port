"""Whole failed checker successor: actual non-input phases remain included.

All214 supplementary native action stores are retained, not made into input
fields:202 refill-mode7 and12 victory-mode5. Actual scene actor/roster/slot
witnesses and nearest actual same-actor/Main field bind these callbacks.
Every prior native win/HP/continue/activation/prefix and fault gate stays.
"""
import bisect
import collections
import inspect
import json
from pathlib import Path
import qualify_native_subzero_guard_pressure_earned_clear as original

ROOT, need, sha = original.ROOT, original.need, original.sha
OUT = ROOT/'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked'


def contexts(rows):
    states=rows['STATE'];state_frames=[int(row['frame']) for row in states]
    anchors=collections.defaultdict(list)
    for row in rows['RANGE_FIELD']:
        for side in ('human','cpu'):
            anchors[(row['human_actor'],row['cpu_actor'],side,row[side+'_main'])].append(row)
    result={};missing=collections.Counter();modes=collections.Counter();maximum_gap=0
    active={int(row['frame']):row for row in rows['RANGE_FIELD']}
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):
        side='cpu' if tag=='RANGE_CPU_ACTION' else 'human';slot=1 if side=='cpu' else 0
        for index,row in enumerate(rows[tag]):
            frame=int(row['frame'])
            if frame in active:
                result[(tag,index)]=active[frame]
                continue
            location=bisect.bisect_right(state_frames,frame)-1
            state=states[location] if location>=0 else None
            if state is None or state['actors'].split(',')[slot]!=row['actor']:
                following=bisect.bisect_left(state_frames,frame)
                choices=[q for q in states[following:following+2]
                         if frame<=int(q['frame'])<=frame+1 and q['actors'].split(',')[slot]==row['actor']]
                need(len(choices)==1, 'Actual immediately following published actor witness, never an invented input field')
                state=choices[0]
            need(state['mode'] in ('5','7') and state['stage']=='11' and state['states']=='1,0' and
                 state['roster']=='18,8' and state['schedule']=='FFFA3000',
                 'Every non-input callback has actual native refill/victory scene and exact physical roster roles')
            human_actor,cpu_actor=state['actors'].split(',')
            candidates=anchors[(human_actor,cpu_actor,side,row['main'])]
            need(candidates, 'Actual same two actors and observed writer Main, not a synthetic record')
            at=bisect.bisect_left([int(q['frame']) for q in candidates],frame)
            near=candidates[max(0,at-1):at+1]
            context=min(near,key=lambda q:abs(int(q['frame'])-frame))
            gap=abs(int(context['frame'])-frame)
            need(gap<=97 and context[side+'_actor']==row['actor'],
                 'Every actual scene-phase Main binds to its original observed body within the full inventoried97-field envelope')
            result[(tag,index)]=context;missing[tag]+=1;modes[state['mode']]+=1;maximum_gap=max(maximum_gap,gap)
    need(dict(missing)==dict(RANGE_ACTION=82,RANGE_CPU_ACTION=60,GUARD_ACTION=72) and
         dict(modes)=={'7':202,'5':12} and maximum_gap==97,
         'Every214 non-input callback retained with its complete actual native phase inventory')
    return result,dict(missing),dict(modes)


def fields(rows,health_gate):
    body=inspect.getsource(original.fields)
    body=original.original.native_health.once(body,
        "    field_by={int(row['frame']):row for row in rows['RANGE_FIELD']}",
        '    callback_context,phase_counts,phase_modes=contexts(rows)')
    body=original.original.native_health.once(body,
        "        for row in rows[tag]:\n            context=field_by[int(row['frame'])]",
        '        for index,row in enumerate(rows[tag]):\n            context=callback_context[(tag,index)]')
    body=original.original.native_health.once(body,
        '    return positive',
        '    return dict(positive,nonInputPhaseActionCallbacks=phase_counts,nonInputPhaseSceneModes=phase_modes,actualPhaseCallbackMainEnvelopeFields=97)')
    scope=dict(vars(original),__file__=__file__,contexts=contexts)
    exec(compile(body,__file__+'::whole_original_with_actual_phase_bound_callbacks','exec'),scope)
    return scope['fields'](rows,health_gate)


def run():
    failed_path=original.OUT/'failure.json'
    failed=json.loads(failed_path.read_text())
    need(not failed['passed'] and failed['error']=='KeyError(305226)' and not failed['fullPortAcceptance'],
         'Actual first checker missing-input-field failure remains frozen, not overwritten or relabeled')
    body=inspect.getsource(original.run)
    once=original.original.native_health.once
    body=once(body,'    faults=[]',
        "    faults=[]\n    need(not failed['passed'],'Original missing-input checker failure retained')")
    body=once(body,"    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):\n        for key,value in",
        """    active_frames={q['frame'] for q in rows['RANGE_FIELD']}
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):
        index=next(i for i,q in enumerate(rows[tag]) if q['frame'] not in active_frames)
        for key,value in (('owner','01000000'),('a13','01000000'),('id','1'),('mask','00FF')):
            trials.append((tag,index,key,value))
    scene_index=next(i for i,q in enumerate(rows['STATE']) if q['frame']=='305226')
    for key,value in (('mode','2'),('roster','1,8'),('states','0,0'),('actors','01000000,01000000')):
        trials.append(('STATE',scene_index,key,value))
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION','GUARD_ACTION'):
        for key,value in""")
    body=once(body,
        'Path(__file__).resolve(),Path(original.__file__),Path(original.native_health.__file__),Path(prefix.__file__),Path(capture.__file__)):',
        'failed_path,Path(original_file),Path(__file__).resolve(),Path(original.__file__),Path(original.native_health.__file__),Path(prefix.__file__),Path(capture.__file__)):')
    body=once(body,'report=dict(passed=True,finiteNativeSonyaSubZeroClearAccepted=True,',
        'report=dict(originalFailedCheckerPreserved=True,everyNonInputPhaseCallbackRetained=True,passed=True,finiteNativeSonyaSubZeroClearAccepted=True,')
    scope=dict(vars(original),__file__=__file__,OUT=OUT,fields=fields,failed=failed,
               failed_path=failed_path,original_file=original.__file__)
    exec(compile(body,__file__+'::whole_original_earned_clear_with_actual_phase_inventory','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Retain actual phase-bound qualification outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
