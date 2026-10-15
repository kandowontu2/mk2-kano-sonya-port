"""276-field kiss inventories bound to independently earned controls per slot."""
import inspect,sys
import qualify_bounded_jax_arms_draw_census as previous

def main(side):
    assert side in (1,2)
    state_source=inspect.getsource(previous.states).replace("'jax'","'kitana'")
    source=inspect.getsource(previous.main)
    source=source.replace('jax_arms','kitana_kiss').replace('147','276').replace('148','277')
    assert source.count('else 11')==1;source=source.replace('else 11','else 4')
    assert source.count('for side in (1,2):')==1;source=source.replace('for side in (1,2):','for side in (requested_side,):')
    source=source.replace("'audit_bounded_kitana_kiss_draw_census_checked'", "f'audit_bounded_kitana_kiss_draw_census_p{requested_side}_checked'")
    namespace=dict(previous.__dict__);namespace.update(__file__=__file__,requested_side=side)
    exec(compile(state_source+'\n'+source,__file__+'::276field_inventory','exec'),namespace);namespace['main']()

if __name__=='__main__':main(int(sys.argv[1]))
