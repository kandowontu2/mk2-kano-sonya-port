"""Fresh same-native campaign with a Subzero-only physical approach strategy."""
import code
import gzip
import json
import traceback
import capture_native_postending_join as base

if __name__=='__main__':
    base.OUT=base.ROOT/'audit_native_postending_kano_p2_sonya_reactive'
    base.LUA='mk2ks_native_kano_p2_postending_sonya_reactive.lua'
    base.CONTROLLERS=[base.LUA,*base.CONTROLLERS]
    try:
        capture=base.run()
    except Exception as error:
        if base.OUT.exists():
            path=base.OUT/'reactive_capture_failure.json'
            base.need(not path.exists(),'Immutable original failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc()),indent=2)+'\n')
        raise
    code.interact(banner='Same terminal native campaign and post-ending Sonya join, images retained in RAM.',local=dict(capture=capture))
