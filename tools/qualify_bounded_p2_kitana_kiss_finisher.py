"""Opposite-slot true-ID earned control gate, native276-field kiss completion."""
import inspect
import qualify_bounded_p2_jax_clap_control as previous

def main():
    source=previous.source
    changes={"a['address']=='FF8C7820'":"a['address']=='FF8CC650'", "int(w['frame'])-int(a['frame'])==188":"int(w['frame'])-int(a['frame'])==276", "x['own'].split(':')[-1]=='11'":"x['own'].split(':')[-1]=='4'"}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    main_source=inspect.getsource(previous.main)
    changes={'audit_bounded_p2_jax_clap_control_checked':'audit_bounded_p2_kitana_kiss_finisher_checked','audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime':'audit_bounded_p2_{fighter}_kitana_kiss_finisher_runtime',"'jax'":"'kitana'"}
    for before,after in changes.items():assert main_source.count(before)==1;main_source=main_source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::original_P2_gate','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
