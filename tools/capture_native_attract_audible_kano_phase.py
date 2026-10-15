"""Fresh physical cold-start phase; retain original audio in a PTY RAM host."""
import code
import capture_native_attract_early_launch as capture_base

if __name__=='__main__':
    capture_base.LUA=capture_base.ROOT/'mk2ks_native_attract_audible_kano_phase.lua'
    capture_base.OUT=capture_base.ROOT/'audit_native_attract_audible_kano_phase'
    capture_base.BOOT_FRAME=481
    capture_base.SECONDS=780
    capture=capture_base.run()
    code.interact(banner='Same original native demo terminal; original PCM/DAC remain in RAM.',
        local=dict(capture=capture))
