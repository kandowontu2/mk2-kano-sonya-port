"""Same compiled guest/UI/physical replay; initial full RAM inventory corrected."""
import code,inspect
import capture_native_sonya_cpu_finisher as previous
previous.OUT=previous.ROOT/'audit_native_sonya_cpu_finisher_inventory_checked'
previous.LUA='mk2ks_native_sonya_cpu_finisher_inventory_checked.lua'
previous.CONTROLLERS=[previous.LUA,*previous.CONTROLLERS]
def run():
    source=inspect.getsource(previous.run)
    before='ui=ROOT/CONTROLLERS[1]'
    after="ui=ROOT/'mk2ks_native_ui_flow_v2_probe.lua'"
    previous.need(source.count(before)==1,'Exact unchanged UI provenance source; never a transitive-list position')
    scope=dict(vars(previous),__file__=__file__)
    exec(compile(source.replace(before,after),__file__+'::only_explicit_UI_provenance_path','exec'),scope)
    return scope['run']()
if __name__=='__main__':
    capture=run()
    code.interact(banner='Same actual Sonya CPU finisher with complete initial guest proof; native frames retained in RAM.',
                 local=dict(capture=capture))
