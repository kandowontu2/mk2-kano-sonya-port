"""Original Kitana kiss activation, earned true-ID rounds and276-field completion."""
import inspect
import qualify_bounded_jax_clap_finisher as previous

def main():
    gate_source=inspect.getsource(previous.gate)
    changes={"a['address']=='FF8C7820'":"a['address']=='FF8CC650'", "x['own'].split(':')[-1]=='11'":"x['own'].split(':')[-1]=='4'"}
    for before,after in changes.items():assert gate_source.count(before)==1;gate_source=gate_source.replace(before,after)
    gate_source=gate_source.replace("    assert t['reason']", "    assert int(w['frame'])-int(a['frame'])==276\n    assert t['reason']",1)
    main_source=inspect.getsource(previous.main).replace('jax_clap_finisher','kitana_kiss_finisher')
    assert main_source.count("'jax'")==1;main_source=main_source.replace("'jax'","'kitana'")
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate_source+'\n'+main_source,__file__+'::original_control_gate','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
