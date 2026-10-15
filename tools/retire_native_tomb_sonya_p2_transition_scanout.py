"""Full original scanout/rejoin retirement for actual SonyaP2 performer.

Retain every original scene, scanout, motion, contact, terminal and fault gate.
Require newly inspecting ALL held original rasters, rather than assuming the
old KanoP1 frame numbers refer to identical images in this different run.
"""
import inspect
import json
import retire_native_tomb_transition_scanout as legacy


def retire(ram,newly_viewed_frames,visual_observations):
    legacy.need(ram['report']['passed'] and ram['report']['fighter']=='sonya' and
                ram['report']['side']==2 and ram['report']['truePhysicalIDs']==[17,18] and
                visual_observations and len(visual_observations)>40,
                'Actual Sonya18 P2 performer/Kano17 P1 victim and individual visual review')
    body=inspect.getsource(legacy.retire)
    before="known={r['frame']:r['rgbSHA256']for r in prior['individuallyReviewedFields']}"
    legacy.need(body.count(before)==1,'Only prior-image reuse changes: all new actual rasters must be reviewed')
    body=body.replace(before,'known={}',1)
    before='for p in (Path(__file__),Path(previous.__file__),prior_path,base_path,'
    legacy.need(body.count(before)==1,'Keep original complete retirement source pinned')
    body=body.replace(before,'for p in (Path(__file__),Path(legacy.__file__),Path(previous.__file__),prior_path,base_path,',1)
    before="actualVisualObservations='Native fatality shutters/continue, own numbered selection portraits and locked poses, correct native Battle3 portraits, clean Wasteland fight entry, actual Kano/Sonya walking/jump/landing/low-kick contact, both floor shadows and black-shadowed native lifebar names.',"
    legacy.need(body.count(before)==1,'Actual new observations replace only old visual description')
    body=body.replace(before,'actualVisualObservations=visual_observations,performer="sonya",physicalSlot=2,',1)
    scope=dict(vars(legacy),__file__=__file__,legacy=legacy,visual_observations=visual_observations)
    exec(compile(body,__file__+'::whole_original_SonyaP2_terminal_scanout_and24_faults','exec'),scope)
    return scope['retire'](ram,newly_viewed_frames)
