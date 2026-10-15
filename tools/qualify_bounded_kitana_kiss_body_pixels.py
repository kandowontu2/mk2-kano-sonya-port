"""Exact physical FIFO/opaque/clip/presentation coverage for276 native fields."""
import inspect,sys
import qualify_bounded_jax_arms_body_pixels as previous

def main(side):
    assert side in (1,2)
    gate_source=inspect.getsource(previous.previous.coverage_gate).replace('188','276').replace('189','277')
    state_source=inspect.getsource(previous.states).replace("'jax'","'kitana'")
    source=inspect.getsource(previous.main).replace('jax_arms','kitana_kiss')
    assert source.count('for side in (1,2):')==1;source=source.replace('for side in (1,2):','for side in (requested_side,):')
    source=source.replace("'audit_bounded_kitana_kiss_body_pixels_checked'", "f'audit_bounded_kitana_kiss_body_pixels_p{requested_side}_checked'")
    source=source.replace("'audit_bounded_kitana_kiss_draw_census_checked/report.json'", "f'audit_bounded_kitana_kiss_all_actor_census_p{requested_side}_checked/report.json'")
    namespace=dict(previous.__dict__);namespace.update(__file__=__file__,requested_side=side)
    exec(compile(gate_source+'\n'+state_source+'\n'+source,__file__+'::276field_pixel_gate','exec'),namespace);namespace['main']()

if __name__=='__main__':main(int(sys.argv[1]))
