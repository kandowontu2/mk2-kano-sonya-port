"""Disabled samples intentionally suppress voice ownership, not combat."""
import inspect
import qualify_bounded_voice_hit_pcm_convergence as previous

def gameplay(folder):
    tags=('MK2_BOUNDED_FIELD ','MK2_BOUNDED_PHYSICAL ','MK2_BOUNDED_CUE ',
          'MK2_BOUNDED_HEALTH_WRITE ','MK2_P2CPU_SELECT_RESULT ')
    with (folder/'run.log').open() as stream:
        return [line for line in stream if line.startswith(tags)]

def main():
    source=inspect.getsource(previous.main)
    before="assert trace.scan(onfolder)['digest']==trace.scan(offolder)['digest']"
    assert source.count(before)==1
    source=source.replace(before,"assert gameplay(onfolder)==gameplay(offolder)\n    assert trace.scan(offolder)['active']==set()")
    source=source.replace("'convergence_check.json'","'native_control_convergence_check.json'")
    source=source.replace('unchangedActualGameplayAndOwnerTrace=True','unchangedActualPhysicalGameplay=True,disabledSamplesHaveNoVoiceOwner=True')
    namespace=dict(previous.__dict__);namespace.update(gameplay=gameplay,__file__=__file__)
    exec(compile(source,__file__+'::native_only_control','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
