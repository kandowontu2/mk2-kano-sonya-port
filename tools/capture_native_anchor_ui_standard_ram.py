"""Original96-frame confirmation, separate from the deliberately delayed review."""
import code
import inspect
import json
import traceback
import capture_native_anchor_ui_ram as original

OUT=original.ROOT/'audit_native_anchor_ui_standard_ram'
INIT=original.ROOT/'audit_native_anchor_ui_standard_ram_initializer'
RAM={}

def run():
    source=inspect.getsource(original.run)
    before="MK2KS_TEST_CONFIRM_AT_AGE='370'"
    original.need(source.count(before)==1,'Unique deliberate-delay input boundary; restore original96-frame confirmation')
    source=source.replace(before,"MK2KS_TEST_CONFIRM_AT_AGE='96'",1)
    scope=dict(vars(original),OUT=OUT,INIT=INIT,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::original_physical_confirmation_timing','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Frozen original UI failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original96-frame UI controls and exact native cases retained in RAM.',local=dict(RAM=RAM))
