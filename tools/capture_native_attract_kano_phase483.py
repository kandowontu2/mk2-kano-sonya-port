"""Fresh ordinary cold-start timing, current native binary, retained RAM only."""
import code
import capture_native_attract_early_launch as base

if __name__ == '__main__':
    base.LUA = base.ROOT / 'mk2ks_native_attract_kano_phase483.lua'
    base.OUT = base.ROOT / 'audit_native_attract_kano_phase483'
    base.BOOT_FRAME = 483
    base.SECONDS = 780
    capture = base.run()
    code.interact(banner='Original native job terminal; actual audio retained in RAM.', local=dict(capture=capture))
