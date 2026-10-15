"""Late charged launch has a shorter remaining observer window; EOF gate stays."""
import inspect
import qualify_bounded_kano_ball_guard_cleanup as previous

def main():
    source=inspect.getsource(previous.main)
    before='namespace=dict(previous.__dict__);exec('
    assert source.count(before)==1
    source=source.replace(before,"gate=gate.replace('len(cleared)>200','len(cleared)>100')\n    "+before)
    source=source.replace('audit_bounded_kano_ball_guard_cleanup_checked','audit_bounded_kano_ball_post_charge_cleanup_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::post_charge_window','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
