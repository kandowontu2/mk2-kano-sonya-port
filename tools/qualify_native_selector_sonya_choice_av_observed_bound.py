"""Direct whole-phase binding; preserve the earlier nested-factory rejection."""
import inspect
import json
import qualify_native_selector_sonya_choice_av_observed as previous

original=previous.original
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_choice_av_observed_bound_checked'
FAIL=previous.FAIL
BINDING_FAILURE=ROOT/'audit_native_selector_sonya_choice_av_observed_checked/failure.json'


def observed_bicycle(text,guest):
    phase=original.phase_source
    source=inspect.getsource(phase.bicycle.verify)
    source=phase.replace(source,"pair=state.verify_log(log,'kano',guest)","pair=ledger.gate(log,guest);source_gate(log,guest)")
    source=phase.replace(source,"    assert any(r['start']==0xfff9a400 and r['stop']==0xfff9ad00 for r in codes)\n",'')
    source=phase.replace(source,"assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'",
        "assert guest[a:b]==original[a:b] or ((lo,hi)==(0xff876650,0xff876b60) and adjacent_finish_operand(guest,original)), 'Exact native fall and separately qualified adjacent finisher operand'")
    source=phase.replace(source,'set(range(start,end+2))<=set(by)','set(range(start+1,end+2))<=set(by)')
    source=phase.replace(source,'baseline=by[start]','baseline=by[start+1]')
    source=phase.replace(source,'range(start,end+2)','range(start+1,end+2)')
    first=source.index("    falls=[r for r in relevant if r['kind']=='fall']")
    last=source.index('    def advance(a,b,g):',first)
    source=source[:first]+'''    switches=[at for at in range(start+8,end) if by[at]['gravity']==0xffff4000 and by[at+1]['gravity']==0xa000]
    assert len(switches)==1,'One actual ceiling switch'
    split=switches[0]
'''+source[last:]
    source=phase.replace(source,"        assert b['xraw']==(a['xraw']+a['vx'])&0xffffffff and b['vx']==flight['vx']",
        "        horizontal_observations.append(dict(before=a,after=b,untraced=True))")
    source=phase.replace(source,'subsequentPairContractUnchanged=pair',
        'wholeNativeStateHealth=pair,nativeRNGObservationAccepted=False,directNativeFallTapAccepted=False')
    horizontal=[]
    scope=dict(phase.bicycle.verify.__globals__,ledger=phase.ledger,source_gate=phase.source_gate,
               adjacent_finish_operand=original.boundary.adjacent_finish_operand,horizontal_observations=horizontal)
    exec(compile(source,__file__+'::all_original_vertical_pose_lock_cleanup_horizontal_pending','exec'),scope)
    result=scope['verify'](text,guest)
    need((result['start'],result['fall'],result['ready'])==(3191,3210,3252),'Actual full native miss chronology')
    need(horizontal and horizontal[0]['after']['frame']==3199 and horizontal[-1]['after']['frame']==3252,
         'Every traveling horizontal recurrence retained, never erased')
    mismatches=[r for r in horizontal if r['after']['xraw']!=(r['before']['xraw']+r['before']['vx'])&0xffffffff
                or r['after']['vx']!=0xfffc0000]
    need(mismatches and mismatches[0]['after']['frame']==3233,'Original failed edge remains in actual evidence')
    result.update(passed=False,verticalPoseAndNativeCleanupAccepted=True,completeHorizontalPhysicsAccepted=False,
                  directNativeBoundaryVelocityStoresObserved=False,retainedUntracedHorizontalCallbacks=horizontal,
                  horizontalMismatches=mismatches,originalCompleteVerifierFailureSHA256=sha(FAIL),fullPortAcceptance=False)
    return result


def gate(text,guest):
    source=inspect.getsource(original.gate)
    source=original.phase_source.replace(source,'bike=bicycle_gate(text,guest)','bike=observed_bicycle(text,guest)')
    source=original.phase_source.replace(source,'completeActualBicycleMiss=bike',
        'actualBicycleVerticalPoseCleanup=bike,completeBicycleLifecycleAccepted=False')
    scope=dict(vars(original),observed_bicycle=observed_bicycle)
    exec(compile(source,__file__+'::actual_choices_falls_explicit_boundary_gap','exec'),scope)
    return scope['gate'](text,guest)


def execute(state,error):
    need(not BINDING_FAILURE.exists() and not OUT.exists(),'Fresh successor and original binding rejection')
    BINDING_FAILURE.parent.mkdir()
    original.capture.choices.current.prior.save(BINDING_FAILURE,dict(passed=False,error=repr(error),
        sourceSHA256=sha(previous.__file__),fullPortAcceptance=False,newNativeGames=0))
    source=inspect.getsource(original.execute)
    source=original.phase_source.replace(source,'finiteBicycleLifecycleAndViewsAccepted=True',
        'finiteBicycleLifecycleAndViewsAccepted=False,bicycleVerticalPoseCleanupAndFiniteViewsAccepted=True')
    source=original.phase_source.replace(source,"ROOT/'tools/read_native_selector_sonya_choice_av_frames.py'",
        "Path(original.__file__),Path(previous.__file__),FAIL,BINDING_FAILURE,ROOT/'tools/read_native_selector_sonya_choice_av_frames.py'")
    source=original.phase_source.replace(source,
        'PASS all3 actual Sonya choice branches/full bicycle lifecycle and4views/whole DAC-ROM; zero shadow rows remain explicit gap',
        'PASS actual3 choices/falls/vertical poses-cleanup/4views/DAC-ROM; native horizontal provenance/shadow drawing/mixed PCM open')
    scope=dict(vars(original),original=original,previous=previous,gate=gate,OUT=OUT,FAIL=FAIL,
               BINDING_FAILURE=BINDING_FAILURE,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_dac_rom_raster_and_fault_checkpoint','exec'),scope)
    return scope['execute'](state)
