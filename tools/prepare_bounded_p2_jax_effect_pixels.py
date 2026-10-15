"""Opposite-slot effects use their own independent census and exact pixel observer."""
import inspect
import prepare_bounded_jax_clap_effect_pixels as previous

def main():
    source=inspect.getsource(previous.main)
    changes={
        'audit_bounded_jax_clap_body_pixels_preparation':'audit_bounded_p2_jax_body_pixels_preparation',
        'audit_bounded_jax_clap_effect_pixels_preparation':'audit_bounded_p2_jax_effect_pixels_preparation',
        'audit_bounded_jax_clap_draw_census_checked':'audit_bounded_p2_jax_draw_census_checked',
        'audit_bounded_{fighter}_jax_clap_body_pixels_runtime':'audit_bounded_p2_{fighter}_jax_body_pixels_runtime',
        'audit_bounded_{fighter}_jax_clap_effect_pixels_runtime':'audit_bounded_p2_{fighter}_jax_effect_pixels_runtime',
    }
    for before,after in changes.items():
        assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::native_effect_observer','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
