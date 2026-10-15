"""Complete native body suite; explicit omission failure before indexed access.

Preserve the earlier actual missing-postfield KeyError. Do not count it as
a semantic negative. Retain every original body/stream/shadow condition and
all17 faults, rejecting missing real fields explicitly. No gameplay replay.
"""
import inspect
import traceback
import verify_native_kano_laser_post_reset_body_shadow as prior

ROOT,need,once,base=prior.ROOT,prior.need,prior.once,prior.base
OUT=ROOT/'audit_native_kano_laser_post_reset_body_complete_fields_checked'


def binding(proof,entries):
    original=prior.binding(proof,entries)
    first,last=proof['actualControls']['round']['actualNativeResume'],proof['actualControls']['round']['last']
    expected={(f,s)for f in range(first,last)for s in (1,2)}
    def check(b,guest,payload,gfx):
        fields=b['rows']['MK2_HPHASE_POST_FIELD']
        keys={(int(r['frame']),int(r['slot']))for r in fields}
        need(len(keys)==len(fields)and keys==expected,'Every actual next-round post-draw field, no omitted slot/frame')
        return original(b,guest,payload,gfx)
    return check


def execute(actual):
    try:
        source=inspect.getsource(prior.run)
        source=once(source,'for p in (Path(__file__),Path(strict.__file__),',
                    "for p in (Path(__file__),Path(prior.__file__),prior.OUT/'failure.json',Path(strict.__file__),")
        scope=dict(vars(prior),prior=prior,binding=binding,OUT=OUT,__file__=__file__)
        exec(compile(source,__file__+'::whole_original_body_suite_explicit_missing_postfield_rejection','exec'),scope)
        scope['run'](actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve strict actual body successor failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(prior.json.dumps(dict(passed=False,error=repr(error))),flush=True)
