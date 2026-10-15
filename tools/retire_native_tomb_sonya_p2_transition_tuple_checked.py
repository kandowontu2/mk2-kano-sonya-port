"""Preserve actual tuple/list retirement guard failure; keep whole native proof."""
import inspect
import json
import traceback
from pathlib import Path
import retire_native_tomb_sonya_p2_transition_scanout as failed_wrapper

legacy=failed_wrapper.legacy


def retire(ram,newly_viewed_frames,visual_observations,error):
    need,sha=legacy.need,legacy.sha
    message='Actual Sonya18 P2 performer/Kano17 P1 victim and individual visual review'
    need(isinstance(error,ValueError) and str(error)==message and
         ram['report']['passed'] and ram['report']['fighter']=='sonya' and
         ram['report']['side']==2 and ram['report']['truePhysicalIDs']==(17,18) and
         isinstance(ram['report']['truePhysicalIDs'],tuple) and
         visual_observations and len(visual_observations)>40,
         'Actual tuple-only mismatch, unchanged true native actors and completed visual review')
    failure_path=ram['output']/'actual_tuple_list_retirement_guard_failure.json'
    need(not failure_path.exists(),'Never overwrite actual original retirement failure')
    pins=dict(ram['report']['inputHashes'])
    for p in(Path(__file__),Path(failed_wrapper.__file__),Path(legacy.__file__),
             ram['output']/'report.json',ram['folder']/'result.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Entire actual failed wrapper/run/proof preserved')
    failure_path.write_text(json.dumps(dict(passed=False,error=repr(error),
        traceback=''.join(traceback.format_exception(error)),actualRAMIDType='tuple',
        actualTruePhysicalIDs=ram['report']['truePhysicalIDs'],
        originalExpectedValueType='list',failureBeforeAnyOriginalRetirementGate=True,
        originalRastersStillHeld=len(ram['review_images']),inputHashes=pins,
        fullPortAcceptance=False),indent=2)+'\n')
    body=inspect.getsource(legacy.retire)
    def once(before,after):
        need(body.count(before)==1,'One exact original retirement adaptation '+before)
        return body.replace(before,after,1)
    body=once("known={r['frame']:r['rgbSHA256']for r in prior['individuallyReviewedFields']}",'known={}')
    body=once('for p in (Path(__file__),Path(previous.__file__),prior_path,base_path,',
        'for p in (Path(__file__),Path(legacy.__file__),Path(failed_wrapper.__file__),failure_path,Path(previous.__file__),prior_path,base_path,')
    before="actualVisualObservations='Native fatality shutters/continue, own numbered selection portraits and locked poses, correct native Battle3 portraits, clean Wasteland fight entry, actual Kano/Sonya walking/jump/landing/low-kick contact, both floor shadows and black-shadowed native lifebar names.',"
    body=once(before,'actualVisualObservations=visual_observations,performer="sonya",physicalSlot=2,')
    scope=dict(vars(legacy),__file__=__file__,legacy=legacy,failed_wrapper=failed_wrapper,
               failure_path=failure_path,visual_observations=visual_observations)
    exec(compile(body,__file__+'::entire_original_scene_scanout_motion24_faults_and_RAM_retirement','exec'),scope)
    return scope['retire'](ram,newly_viewed_frames)
