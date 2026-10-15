"""Strict unchanged observed chronology, plus same native Carry/paid-match gates."""
from pathlib import Path
wrapper=Path(__file__).with_name('qualify_current_sonya_p2_jax_ground_jump_leg.py').read_text()
wrapper=wrapper.replace('audit_current_sonya_p2_jax_ground_jump_leg','audit_current_sonya_p2_jax_deferred_ground_taps')
marker="exec(compile(code,__file__,'exec'))"
assert wrapper.count(marker)==1
adapt='''
code=code.replace("prior=load(root/'audit_current_sonya_p2_kano_short_leg_runtime/run.log')", "prior=load(root/'audit_current_sonya_p2_jax_ground_jump_leg_runtime/run.log')")
code=code.replace('101525','105480')
code=code.replace("t not in ('SONYA_JAX_DAMAGE','JAX_GROUND_NATIVE','JAX_GROUND_CODE_CHECKED')", "t!='JAX_NATIVE_TAPS_INSTALLED'")
needle="last=max(int(r['frame']) for t,r in rows);through=min(last,105480)"
assert code.count(needle)==1
extra="""
    installed=[r for t,r in rows if t=='JAX_NATIVE_TAPS_INSTALLED']
    assert len(installed)==1 and int(installed[0]['frame'])<=101525
    for kind,field in [('ground_entry',101525),('human_jump',101528),('ground_result',101541)]:
        got=[r for t,r in rows if t=='JAX_GROUND_NATIVE' and r['kind']==kind and int(r['frame'])==field]
        old=[r for t,r in prior if t=='JAX_GROUND_NATIVE' and r['kind']==kind and int(r['frame'])==field]
        assert got==old and len(got)==1
"""
code=code.replace(needle,needle+extra)
code=code.replace('strictSamePaidJaxToKitanaClears=proofs,', 'strictSamePaidJaxToKitanaClears=proofs, deferredObserversInstalled=installed, initialNativeGroundJumpCarryRecordsExactlyRetained=True,')
'''
wrapper=wrapper.replace(marker,adapt+'\n'+marker)
exec(compile(wrapper,__file__,'exec'))
