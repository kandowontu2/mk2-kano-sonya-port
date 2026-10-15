"""Exact target-absence gate for physical reapproach attempts."""
import inspect
import inspect_bounded_twohuman_kano_ball_counter as previous

def main():
    source=inspect.getsource(previous.main)
    source=source.replace('audit_bounded_twohuman_kano_ball_counter_observed','audit_bounded_kano_ball_approach_observed')
    source=source.replace('ball_p{side}_counter_runtime','ball_p{side}_approach_runtime')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::reapproach','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
