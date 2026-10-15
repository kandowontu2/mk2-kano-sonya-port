"""Unassisted STOCK Jax confirmation-pose reference, same delayed UI input style."""
import code,inspect,json,traceback
import capture_native_anchor_ui_ram as original

OUT=original.ROOT/'audit_native_anchor_ui_stock_jax_ram'
INIT=original.ROOT/'audit_native_anchor_ui_stock_jax_ram_initializer'
RAM={}

def run():
    source=inspect.getsource(original.run)
    before="(('kano','sonya',True),('sonya','kano',True),('kano','stock',False),('sonya','stock',False))"
    original.need(source.count(before)==1,'Exact unchanged native case-list boundary')
    source=source.replace(before,"(('sonya','jax',True),)",1)
    # Do not copy the old final four-case count into this single stock reference.
    before='transportOnly=True,cases=4,visualReviewRequired=True'
    original.need(source.count(before)==1,'Unique original reference summary boundary')
    source=source.replace(before,'transportOnly=True,cases=1,visualReviewRequired=True',1)
    scope=dict(vars(original),OUT=OUT,INIT=INIT,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::physical_original_stock_jax_confirmation_reference','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Preserve actual stock reference failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same exact stock Jax reference native handle/rasters retained.',local=dict(RAM=RAM))
