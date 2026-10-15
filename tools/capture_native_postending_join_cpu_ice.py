"""Fresh earned campaign, real native CPU projectile drives ordinary Block."""
import code,json,traceback
import capture_native_postending_join as base

if __name__=='__main__':
    base.OUT=base.ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice'
    base.LUA='mk2ks_native_kano_p2_postending_sonya_cpu_ice.lua'
    base.CONTROLLERS=[base.LUA,'mk2ks_native_kano_p2_postending_sonya_defensive.lua',*base.CONTROLLERS]
    try:capture=base.run()
    except Exception as error:
        if base.OUT.exists():
            path=base.OUT/'cpu_ice_capture_failure.json';base.need(not path.exists(),'Immutable actual capture failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc()),indent=2)+'\n')
        raise
    code.interact(banner='Same actual terminal CPU-ice-aware earned campaign; no tower-clear claim until independently qualified.',local=dict(capture=capture))
