"""Finite inspected retained P2 sheets; bind exact current body poses/sources."""
import inspect
import bind_bounded_jax_clap_retained_review as previous

def main():
    source=inspect.getsource(previous.main)
    changes={
        'audit_bounded_jax_clap_retained_review_bound':'audit_bounded_p2_jax_retained_review_bound',
        'audit_bounded_jax_clap_draw_census_checked':'audit_bounded_p2_jax_draw_census_checked',
        'audit_bounded_{fighter}_jax_clap_draw_census_runtime':'audit_bounded_p2_{fighter}_jax_draw_census_runtime',
        'audit_v6135_current_jax_clap_{fighter}_p1_native_scene_ram':'audit_v6135_current_jax_clap_{fighter}_p2_native_scene_ram',
        '{fighter}-p1-native-clap-review.png':'{fighter}-p2-native-clap-review.png',
        '3127<=frame<=3314':'3138<=frame<=3325',
        'range(3127,3315)':'range(3138,3326)',
    }
    for before,after in changes.items():
        assert source.count(before)==1;source=source.replace(before,after)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::retained_P2_bridge','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
