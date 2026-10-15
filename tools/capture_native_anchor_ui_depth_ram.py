"""Original physical own/stock confirmation cases with passive native list depth."""
import code,inspect,json,traceback
import capture_native_anchor_ui_ram as original

OUT=original.ROOT/'audit_native_anchor_ui_depth_ram'
INIT=original.ROOT/'audit_native_anchor_ui_depth_ram_initializer'
LUA=original.ROOT/'mk2ks_native_anchor_ui_depth_ram.lua'
RAM={}

def run():
    source=inspect.getsource(original.run)
    changes=(
        ("(('kano','sonya',True),('sonya','kano',True),('kano','stock',False),('sonya','stock',False))",
         "(('sonya','kano',True),('sonya','jax',True))"),
        ('transportOnly=True,cases=4,visualReviewRequired=True','transportOnly=True,cases=2,visualReviewRequired=True'),
        ("controllers=[LUA,ROOT/'mk2ks_selector_exit_test.lua'", "controllers=[LUA,ROOT/'mk2ks_native_anchor_ui_ram.lua',ROOT/'mk2ks_selector_exit_test.lua'"))
    for before,after in changes:
        original.need(source.count(before)==1,'Exact unchanged native depth observation boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),OUT=OUT,INIT=INIT,LUA=LUA,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::physical_ui_passive_depth','exec'),scope)
    scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Preserve actual depth observation failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original own/stock UI depth and raster evidence retained.',local=dict(RAM=RAM))
