"""Audit actual loaded Lua controllers, not the Python auditor's regex literal."""
import code,inspect,json,traceback
from pathlib import Path
import capture_native_classic_selector_reference as original

OUT=original.ROOT/'audit_native_classic_selector_reference_loaded'
RAM={}

def run():
    source=inspect.getsource(original.run)
    changes=(('for p in paths[:4]:','for p in paths[1:4]:'),
             ('paths=[Path(__file__),LUA,', 'paths=[Path(__file__),LUA,'))
    before,after=changes[0]
    original.need(source.count(before)==1,'Exact actual loaded-controller audit boundary')
    source=source.replace(before,after,1)
    before="ROOT/'roms/mk2.zip']"
    original.need(source.count(before)==1,'Original failed host source provenance')
    source=source.replace(before,"ROOT/'roms/mk2.zip',Path(original.__file__)]",1)
    scope=dict(vars(original),original=original,OUT=OUT,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::audit_actual_loaded_Lua_only','exec'),scope)
    scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Preserve actual stock reference outcome')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same original stock reference native bytes/handle retained.',local=dict(RAM=RAM))
