"""Exact existing physical-body pixel gate adapted to independently earned P2."""
import inspect
import qualify_bounded_jax_clap_body_pixels as previous
from qualify_bounded_p2_jax_voice_priority import read
from qualify_bounded_p2_jax_clap_control import gate

def state_at(folder,fighter):return read(folder,fighter)[0]
def control_gate(rows,ident):
    value=gate(rows,[],ident)
    return dict(nativeActionFrame=value['actionFrame'])

def main():
    source=inspect.getsource(previous.main)
    replacements={
        "audit_bounded_jax_clap_body_pixels_checked":"audit_bounded_p2_jax_body_pixels_checked",
        "audit_bounded_jax_clap_draw_census_checked":"audit_bounded_p2_jax_draw_census_checked",
        "audit_bounded_{fighter}_jax_clap_body_pixels_runtime":"audit_bounded_p2_{fighter}_jax_body_pixels_runtime",
        "audit_bounded_{fighter}_jax_clap_draw_census_runtime":"audit_bounded_p2_{fighter}_jax_draw_census_runtime",
    }
    for before,after in replacements.items():
        assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__)
    namespace.update(state_at=state_at,control_gate=control_gate,__file__=__file__)
    exec(compile(source,__file__+'::unchanged_pixel_gate','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
