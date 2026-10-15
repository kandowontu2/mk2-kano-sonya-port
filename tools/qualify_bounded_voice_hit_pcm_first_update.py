"""Require convergence at the first post-cleanup sound update, no allowance."""
import inspect
import qualify_bounded_voice_hit_pcm_convergence as original
from qualify_bounded_voice_hit_pcm_native_control import gameplay

def main():
    gate=inspect.getsource(original.gate)
    before="tick+Decimal('.1')";assert gate.count(before)==1
    gate=gate.replace(before,'tick')
    gate=gate.replace("settlingAllowanceSeconds='.1'","settlingAllowanceSeconds='0',firstPostTimerUpdateSeconds=after[0][0]['seconds']")
    marker="    assert Decimal(after[-1][0]['seconds'])>tick+Decimal('.5')"
    assert gate.count(marker)==1
    gate=gate.replace(marker,marker+"\n    assert 0<Decimal(after[0][0]['seconds'])-tick<Decimal('.02')")
    source=inspect.getsource(original.main)
    before="assert trace.scan(onfolder)['digest']==trace.scan(offolder)['digest']"
    assert source.count(before)==1
    source=source.replace(before,"assert gameplay(onfolder)==gameplay(offolder)\n    assert trace.scan(offolder)['active']=={2593}")
    source=source.replace("'convergence_check.json'","'first_update_convergence_check.json'")
    source=source.replace('unchangedActualGameplayAndOwnerTrace=True','unchangedActualPhysicalGameplay=True,disabledOwnerSingleObservedField=2593')
    # Effective counterexample must corrupt the newly tightened first update.
    before="tick+Decimal('.1')";assert source.count(before)==1
    source=source.replace(before,'tick')
    namespace=dict(original.__dict__);namespace.update(gameplay=gameplay,__file__=__file__)
    exec(compile(gate+'\n'+source,__file__+'::first_post_timer_update','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
