"""Current physical P2 Sonya leg and ordinary follow-up scene: one-base continuous native erase replay.

The v1843 original CPU/DMA/shift-transfer contract remains unchanged. Every
retained later pre-buffer/flip is a target, never a fresh expected-image anchor.
No all-scene, all-move, art/audio or full-port acceptance.
"""
import json
import inspect_ball_register_erase_v1843 as model
import inspect_current_cpu_knife_raster_v1975 as scaled
import verify_current_interrupt_v1870 as launch

ROOT=launch.ROOT;CASE=ROOT/'audit_v1991_current_sonya_p2_cpu_leg_display_sonya'
OUT=ROOT/'audit_v1993_current_sonya_p2_cpu_mirror_leg_erase_checked'

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:
        pins={};scaled.source(pins)
        proof=model.inspect(CASE)
        proof['inputHashes'].update(pins)
        assert proof['passed'],proof
        launch.module_pins(proof['inputHashes'])
        proof.update(candidate=launch.NAME,originalContinuousReplayContractUnchanged=True,scope=__doc__)
    except Exception as error:
        import traceback
        proof=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({k:proof[k]for k in('passed','error','continuousExactPreBuffers','continuousExactFlips','shiftLoads','shiftFills','nativeShiftTransfers','oneInitialBaseOnly')if k in proof}),flush=True)
    raise SystemExit(0 if proof['passed']else 1)




