"""Entire original24-fault later retirement plus whole current native Pit proof.

All held original raster buffers require fresh individual inspection. No
visual clearing is inferred from physical or cinematic pointer retirement.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import retire_native_tomb_transition_scanout as original


def once(source,before,after):
    original.need(source.count(before)==1,'Exact entire original Pit retirement adaptation '+before)
    return source.replace(before,after,1)


def retire(ram,newly_viewed_frames,visual_observations):
    report=ram['report'];scene=report['nativeScene']
    root=ram['folder'].parent
    matrix_path=root/'audit_native_current_cross_pit_render_matrix_checked/report.json'
    matrix=json.loads(matrix_path.read_text())
    original.need(matrix['passed']and all(original.sha(p)==h for p,h in matrix['inputHashes'].items()),
                  'Whole original current Pit one-base scene and actual fault/review source stays frozen')
    physical=scene['nativeState'];movie=scene['movie'];policy=scene['actualNativePitShadowPolicy']
    original.need(report['passed']and report['actualCurrentCrossNativePitWholeRenderPaletteShadowEraseAccepted']and
                  scene['currentLiveContinuousPipelineAccepted']and scene['wholeNativePitShadowPolicyAccepted']and
                  policy['passed']and policy['currentPitShadowSchedulingMatchesOriginal']and
                  physical['earned_matches']==7 and physical['consecutive_fields']==801 and
                  physical['native_action']=='FF8BDDE0'and movie['nextScreen']==scene['retired']and
                  movie['actualMovieAddressRepurposed']==scene['retired']+8 and
                  scene['visibleMoviePoses']==scene['actualMoviePoses']and len(scene['visibleMoviePoses'])==6 and
                  len(scene['actualMovieFaultsRejected'])==31 and len(scene['actualEarnedFaultsRejected'])==12 and
                  len(scene['actualNativePhaseGroundFaultsRejected'])==6 and
                  len(policy['actualShadowPolicyFaultsRejected'])==5 and
                  len(report['actualPixelFaultsRejected'])==2 and len(report['sourcePreflight']['rejectedProxyTuples'])==5 and
                  scene['nativeShadowCopies']==0 and scene['actualNativePhaseGround']['originalVictimFloorDisplacement']==1024 and
                  not report['currentPitAudioWaveformAccepted']and visual_observations and len(visual_observations)>40,
                  'Whole original earned movie/floor/stock-shadow/pixel/proxy faults, actual fresh visual observations')
    expectedSceneFields=scene['retired']+30-scene['origin']
    original.need(report['sampledFrames']==expectedSceneFields and expectedSceneFields in(676,677),
                  'Exact original full current same-performer Pit scene interval')
    ids=report['truePhysicalIDs'];fighter,side=report['fighter'],report['side']
    own=17 if fighter=='kano'else 18
    original.need(tuple(ids)==tuple(own if n==side else 35-own for n in(1,2)),
                  'True opposite characters in requested native slots')
    state=inspect.getsource(original.previous.state_facts)
    if tuple(ids)==(18,17):
        for before,after in(("a[0]['ids']=='17,18'","a[0]['ids']=='18,17'"),
                           ('((1,17),(2,18))','((1,18),(2,17))'),
                           ('(17 if s==1 else 18)','(18 if s==1 else 17)'),
                           ('actualTruePhysicalIDs=[17,18]','actualTruePhysicalIDs=[18,17]')):
            state=once(state,before,after)
    namespace=dict(vars(original.previous))
    exec(compile(state,__file__+'::whole_original_native_state_only_exact_physical_IDs','exec'),namespace)
    parent=SimpleNamespace(**namespace)
    body=inspect.getsource(original.retire)
    body=once(body,'len(scene.records)==537','len(scene.records)==expectedSceneFields')
    body=once(body,'Original complete537-field independent model retained, separate later scope explicit',
                   'Entire original current Pit independent model retained, separate later scope explicit')
    body=once(body,"known={r['frame']:r['rgbSHA256']for r in prior['individuallyReviewedFields']}",'known={}')
    body=once(body,'for p in (Path(__file__),Path(previous.__file__),prior_path,base_path,',
                   'for p in (Path(__file__),Path(original.__file__),Path(previous.__file__),matrix_path,prior_path,base_path,')
    body=once(body,'finiteNativeTombTransitionAndPaidRejoinAccepted=True',
                   'finiteNativePitTransitionAndPaidRejoinAccepted=True,performer=fighter,physicalSlot=side')
    old="actualVisualObservations='Native fatality shutters/continue, own numbered selection portraits and locked poses, correct native Battle3 portraits, clean Wasteland fight entry, actual Kano/Sonya walking/jump/landing/low-kick contact, both floor shadows and black-shadowed native lifebar names.',"
    body=once(body,old,'actualVisualObservations=visual_observations,')
    scope=dict(vars(original),__file__=__file__,original=original,previous=parent,
               expectedSceneFields=expectedSceneFields,matrix_path=matrix_path,fighter=fighter,side=side,
               visual_observations=visual_observations)
    exec(compile(body,__file__+'::entire_original_scanout24_faults_visual_review_and_RAM_retirement_Pit','exec'),scope)
    return scope['retire'](ram,newly_viewed_frames)
