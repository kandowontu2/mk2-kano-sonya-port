"""Require positive output while owned, not before an early hit's timestamp."""
import inspect
import qualify_bounded_kano_ball_hit_pcm as previous

def main():
    source=inspect.getsource(previous.main)
    marker='namespace=dict(previous.__dict__);'
    assert source.count(marker)==1
    source=source.replace(marker,"gate=gate.replace(\"if Decimal(a['seconds'])<hit]\",\"if Decimal(a['seconds'])<clear]\")\n    source=source.replace('audit_bounded_kano_ball_hit_pcm_checked','audit_bounded_kano_ball_owned_pcm_checked')\n    "+marker)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::owned_positive_control','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
