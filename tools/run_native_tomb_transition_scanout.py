"""Bind completed native scanout to real DPYADR, not pending DPYSTRT.

Use one deterministic source-defined address, never select among targets.
The full earlier failed captures remain unchanged. Native blanking registers
give the visible line count; native DUDATE gives address progression. This
finite400x254 non-repeated scanout scope is explicit and fails other timings.
"""
import run_native_tomb_transition_timing as previous

source=previous.previous.once(previous.source,
    "PREFIX = 'audit_native_tomb_transition_timing'",
    "PREFIX = 'audit_native_tomb_transition_scanout'")
source=previous.previous.once(source,
    "'mk2ks_native_tomb_rejoin_guarded_provenance.lua','mk2ks_native_tomb_rejoin_timing_display.lua'))",
    "'mk2ks_native_tomb_rejoin_guarded_provenance.lua','mk2ks_native_tomb_rejoin_timing_display.lua','mk2ks_native_tomb_rejoin_scanout_display.lua'))")
source=previous.previous.once(source,"    keep = not proof['passed'] or changed",
    "    keep = proof.get('queuedStartDiffersFromEffective',False) or not proof['passed'] or changed")
begin=source.index('def timing_binding(rgb,vram,palette,state):')
end=source.index("if __name__ == '__main__':",begin)
replacement=r'''
def timing_binding(rgb,vram,palette,state):
    frame=state['frame'];timing=RAM['post_timing'][frame]
    current=RAM['post_raw'].pop(f'display_pre_{frame}.bin')
    digest=previous.previous.model.digest
    need(timing['control']==state['control'] and timing['tap']==state['tap'] and
         timing['vsblnk']-timing['veblnk']==254 and timing['vtotal']>=timing['vsblnk'] and
         0<=timing['vcount']<=timing['vtotal'] and state['control']&0xc000==0xc000 and
         state['control']&0x03fc==16 and timing['dpystart']&3==timing['dpyadr']&3==0,
         'Actual native enabled noninterlaced254-line scanout, sixteen-address DUDATE, no repeated lines')
    # get_display_params uses DPYADR, NOT the newly queued DPYSTRT. The source
    # timer subtracts DUDATE on each of these254 completed visible lines.
    # Undo that source-defined progression to obtain this completed scanout.
    effective=(timing['dpyadr']+(timing['vsblnk']-timing['veblnk'])*(state['control']&0x03fc))&0xffff
    try:
        proof=display.check_latch(rgb,vram,palette,effective,state['control'],state['tap'])
    except ValueError as error:
        need(str(error)=='Every screenshot pixel matches the actual newly displayed VRAM and palette',
             'Real source-defined active-DPYADR mismatch, not malformed native transport')
        actual=dict(state,start=effective)
        matches,rows=pixel_matches(rgb,vram,palette,actual)
        proof=dict(passed=False,pixels=matches,error=repr(error),mismatchedNativeRows=rows)
        if len(RAM['post_failures'])<8:
            RAM['post_failures'].append(dict(frame=frame,state=state.copy(),timing=timing.copy(),
                rgb=rgb.copy(),latch=vram,current=current,palette=palette,comparison=proof.copy()))
    proof.update(timing=timing,effectiveNativeStart=effective,queuedNativeStart=state['start'],
                 queuedStartDiffersFromEffective=effective!=state['start'],
                 nativeDPYADRSourceDefinedAddressOnly=True,
                 currentVRAMDiagnosticSHA256=digest(current),currentVRAMNeverSelectedAsPassingTarget=True)
    return proof

'''
source=source[:begin]+replacement+source[end:]
scope=dict(__name__=__name__,__file__=__file__)
exec(compile(source,__file__+'::whole_original_scene_and_real_completed_native_scanout','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
