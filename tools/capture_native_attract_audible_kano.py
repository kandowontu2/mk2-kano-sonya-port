"""One genuine native demo run; only ordinary factory-screen button timing."""
import code
import capture_native_attract_early_launch as capture_base

if __name__=='__main__':
    capture_base.LUA=capture_base.ROOT/'mk2ks_native_attract_audible_kano.lua'
    capture_base.OUT=capture_base.ROOT/'audit_native_attract_audible_kano'
    capture_base.BOOT_FRAME=480
    capture_base.SECONDS=780
    capture=capture_base.run()
    code.interact(banner='Original native demo job terminal; actual audio and source clocks retained in RAM.',
        local=dict(capture=capture))
