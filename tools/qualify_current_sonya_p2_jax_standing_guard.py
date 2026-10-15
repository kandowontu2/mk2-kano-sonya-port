"""Current standing-guard trial; retain ground callbacks and legitimate native positive-HP wins."""
from pathlib import Path
wrapper=Path(__file__).with_name('qualify_current_sonya_p2_jax_ground_jump_leg.py').read_text()
wrapper=wrapper.replace('audit_current_sonya_p2_jax_ground_jump_leg','audit_current_sonya_p2_jax_standing_guard')
marker="exec(compile(code,__file__,'exec'))";assert wrapper.count(marker)==1
ko="assert all(r['id']=='18' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in own)"
rounds="""for r in own:
        assert r['id']=='18' and r['pc']=='FF8296B0'
        enemyhp,ownhp=map(int,r['health'].split(','))
        assert 0<=enemyhp<ownhp<=161
        if enemyhp:
            states=[s for tag,s in window if tag=='STATE' and int(r['frame'])<=int(s['frame'])<=int(r['frame'])+2 and s['mode']=='5' and s['winner']=='2' and s['health']==r['health']]
            assert states, 'Positive-HP native winner needs actual own round-completion state'"""
before="namespace={};exec(compile(ast.get_source_segment(code,node),str(helper)+'::pure_gate','exec'),namespace)"
after="namespace={};pure=ast.get_source_segment(code,node)\n    assert pure.count("+repr(ko)+")==1\n    pure=pure.replace("+repr(ko)+","+repr(rounds)+")\n    exec(compile(pure,str(helper)+'::native_positive_HP_or_KO_gate','exec'),namespace)"
adapt="\ncode=code.replace(\"'JAX_GROUND_CODE_CHECKED')\", \"'JAX_GROUND_CODE_CHECKED','JAX_NATIVE_TAPS_INSTALLED')\")\n"
adapt+="code=code.replace("+repr(before)+","+repr(after)+")\n"
adapt+="code=code.replace('strictSamePaidJaxToKitanaClears=proofs,', 'strictSamePaidJaxToKitanaClears=proofs, nativePositiveHPWinnerGateSupported=True, exactRoundTimerRegisterObserved=False,')\n"
wrapper=wrapper.replace(marker,adapt+'\n'+marker)
exec(compile(wrapper,__file__,'exec'))
