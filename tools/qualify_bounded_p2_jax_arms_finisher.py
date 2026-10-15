"""Unchanged opposite-slot earned-state gate with native secondary147-field action."""
import inspect
import qualify_bounded_p2_jax_clap_control as previous

def main():
    source=previous.source
    changes={"a['address']=='FF8C7820' and a['variant']=='1'":"a['address']=='FF8BE240' and a['variant']=='2'", "int(w['frame'])-int(a['frame'])==188":"int(w['frame'])-int(a['frame'])==147"}
    for before,after in changes.items():
        assert source.count(before)==1;source=source.replace(before,after)
    main_source=inspect.getsource(previous.main)
    for before,after in [('audit_bounded_p2_jax_clap_control_checked','audit_bounded_p2_jax_arms_finisher_checked'),('audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime','audit_bounded_p2_{fighter}_jax_arms_finisher_runtime')]:
        assert main_source.count(before)==1;main_source=main_source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::unchanged_P2_control','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
