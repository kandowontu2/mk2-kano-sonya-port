"""Unchanged complete effect pixel/clip/DMA gate in separately earned P2 context."""
import inspect
import qualify_bounded_jax_clap_effect_pixels as previous
from qualify_bounded_p2_jax_body_pixels import state_at,control_gate

def main():
    source=inspect.getsource(previous.main)
    changes={
        'audit_bounded_jax_clap_effect_pixels_checked':'audit_bounded_p2_jax_effect_pixels_checked',
        'audit_bounded_jax_clap_draw_census_checked':'audit_bounded_p2_jax_draw_census_checked',
        'audit_bounded_{fighter}_jax_clap_effect_pixels_runtime':'audit_bounded_p2_{fighter}_jax_effect_pixels_runtime',
        'audit_bounded_{fighter}_jax_clap_draw_census_runtime':'audit_bounded_p2_{fighter}_jax_draw_census_runtime',
        'p2ContextAccepted=False':'p2ContextAccepted=True',
    }
    for before,after in changes.items():
        assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__)
    namespace.update(state_at=state_at,control_gate=control_gate,__file__=__file__)
    exec(compile(source,__file__+'::unchanged_effect_gate','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
