"""Four original standard UI gates plus two delayed confirmation-pose reviews."""
import code,inspect,json,traceback
import capture_native_anchor_ui_ram as original
import verify_native_selector_layers_startup as startup

ROOT,NAME=original.ROOT,startup.NAME
OUT=ROOT/'audit_native_selector_layers_ui_ram'
INIT=ROOT/'audit_native_selector_layers_ui_ram_initializer'
LUA=ROOT/'mk2ks_native_selector_layers_ui_depth_ram.lua'
RAM={}

def run():
    source=inspect.getsource(original.run)
    changes=(
        ("concurrent=json.loads((ROOT/'audit_native_shang_drain_anchors_campaign/native_identity.json').read_text())",
         "terminal_path=ROOT/'audit_native_shang_drain_anchors_campaign/native_terminal.json'\n    concurrent=json.loads(terminal_path.read_text())\n    terminal_sha=sha(terminal_path)"),
        ("need(startup.initial.identity.census()==[concurrent], 'Exact already-running independent campaign, no unknown native games')",
         "need(concurrent['nativeExit']==0 and concurrent['identity']['ProcessId']==32016 and not startup.initial.identity.census(),'Original independent campaign actually terminal; no unknown native games')"),
        ("controllers=[LUA,ROOT/'mk2ks_selector_exit_test.lua'",
         "controllers=[LUA,ROOT/'mk2ks_native_anchor_ui_depth_ram.lua',ROOT/'mk2ks_native_anchor_ui_ram.lua',ROOT/'mk2ks_selector_exit_test.lua'"),
        ("for p1,p2,two in (('kano','sonya',True),('sonya','kano',True),('kano','stock',False),('sonya','stock',False)):",
         "for p1,p2,two,confirmation in (('kano','sonya',True,96),('sonya','kano',True,96),('kano','stock',False,96),('sonya','stock',False,96),('kano','sonya',True,370),('sonya','kano',True,370)):"),
        ("case=f'{p1}_p1_{p2}_p2_'+('two'if two else'ladder')",
         "case=f'{p1}_p1_{p2}_p2_'+('two'if two else'ladder')+f'_confirm{confirmation}'"),
        ("MK2KS_TEST_CONFIRM_AT_AGE='370'","MK2KS_TEST_CONFIRM_AT_AGE=str(confirmation)"),
        ("need(concurrent in startup.initial.identity.census(),'Same original independent full campaign remains live')",
         "need(not startup.initial.identity.census() and sha(terminal_path)==terminal_sha,'All original terminal handles remain terminal; complete campaign evidence unchanged')"),
        ('transportOnly=True,cases=4,visualReviewRequired=True','transportOnly=True,cases=6,visualReviewRequired=True'))
    for before,after in changes:
        original.need(source.count(before)==1,'Exact unchanged physical/UI collection boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),startup=startup,ROOT=ROOT,NAME=NAME,OUT=OUT,INIT=INIT,LUA=LUA,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::same_inputs_on_css_layer_successor','exec'),scope)
    scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';original.need(not path.exists(),'Preserve actual new UI failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original six native UI case handles and rasters retained in RAM.',local=dict(RAM=RAM))
