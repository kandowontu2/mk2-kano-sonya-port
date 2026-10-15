"""Same complete-window retirement predicates for both Kano slots."""
import inspect
import qualify_bounded_twohuman_square_hit_pcm as previous

def main():
    gate=inspect.getsource(previous.gate)
    assert gate.count('len(on)==len(off)==148')==1
    gate=gate.replace('len(on)==len(off)==148','len(on)==len(off)>200').replace('updates=148','updates=len(on)')
    source=inspect.getsource(previous.main)
    for before,after in {
        'audit_bounded_twohuman_square_hit_pcm_checked':'audit_bounded_kano_ball_hit_pcm_checked',
        'audit_bounded_twohuman_square_slot_positions_checked':'audit_bounded_kano_ball_post_charge_cleanup_checked',
        'audit_bounded_twohuman_square_p{side}_rise_counter_runtime':'audit_bounded_kano_ball_p{side}_guard_counter_runtime',
        'audit_bounded_twohuman_square_p{side}_pcm_{label}_runtime':'audit_bounded_kano_ball_p{side}_pcm_{label}_runtime',
    }.items():
        assert before in source;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::kano_mix','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
