"""Current compiled guest; new ordinary boot phase, entire native PCM/DAC in RAM."""
import code
import capture_native_attract_early_launch as original
import native_cpu_finisher_spacing_context as current

if __name__=='__main__':
    original.current=current
    original.LUA=current.ROOT/'mk2ks_native_attract_kano_spacing_phase484.lua'
    original.OUT=current.ROOT/'audit_native_attract_kano_spacing_phase484'
    original.BOOT_FRAME=484
    original.SECONDS=780
    capture=original.run()
    code.interact(banner='Exact current native attract job terminal; original PCM/DAC/RGB retained in RAM.',
                 local=dict(capture=capture))
