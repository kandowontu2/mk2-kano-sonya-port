"""Original earned-state gate for secondary Jax arm-rip, exact147-field wrap."""
import inspect
import qualify_bounded_jax_clap_finisher as previous

def main():
    gate=inspect.getsource(previous.gate)
    needle="a['address']=='FF8C7820' and a['variant']=='1'"
    assert gate.count(needle)==1;gate=gate.replace(needle,"a['address']=='FF8BE240' and a['variant']=='2'")
    gate=gate.replace("    assert t['reason']", "    assert int(w['frame'])-int(a['frame'])==147\n    assert t['reason']",1)
    source=inspect.getsource(previous.main).replace('jax_clap_finisher','jax_arms_finisher')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::original_earned_gate','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
