"""Full native kiss FIFO inventory, including already-present nonphysical actors."""
import inspect,sys
import qualify_bounded_jax_arms_draw_census as previous

def main(side):
    assert side in (1,2)
    state_source=inspect.getsource(previous.states).replace("'jax'","'kitana'")
    source=inspect.getsource(previous.main).replace('jax_arms','kitana_kiss').replace('147','276').replace('148','277')
    assert source.count('else 11')==1;source=source.replace('else 11','else 4')
    assert source.count('for side in (1,2):')==1;source=source.replace('for side in (1,2):','for side in (requested_side,):')
    source=source.replace("'audit_bounded_kitana_kiss_draw_census_checked'", "f'audit_bounded_kitana_kiss_all_actor_census_p{requested_side}_checked'")
    needle=" for actor,a in actors.items() if min(a['ages'])>1}"
    assert source.count(needle)==1;source=source.replace(needle,' for actor,a in actors.items()}')
    source=source.replace('newNonphysicalActors','allNonphysicalActors').replace('newActors','nonphysicalActors')
    namespace=dict(previous.__dict__);namespace.update(__file__=__file__,requested_side=side)
    exec(compile(state_source+'\n'+source,__file__+'::complete_actor_inventory','exec'),namespace);namespace['main']()

if __name__=='__main__':main(int(sys.argv[1]))
