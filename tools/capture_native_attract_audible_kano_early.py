"""Fresh physical acknowledgement phase, existing native executable only."""
import code
import capture_native_attract_early_launch as capture_base

if __name__=='__main__':
    capture_base.LUA=capture_base.ROOT/'mk2ks_native_attract_audible_kano_early.lua'
    capture_base.OUT=capture_base.ROOT/'audit_native_attract_audible_kano_early'
    capture_base.BOOT_FRAME=482
    capture_base.SECONDS=780
    capture=capture_base.run()
    code.interact(banner='Original native job terminal; same actual PCM/DAC retained in RAM.',
        local=dict(capture=capture))
