"""Correct autoboot/dofile configuration; no guest state or audio mutation."""
import code
import capture_native_attract_early_launch as capture_base

if __name__=='__main__':
    capture_base.LUA=capture_base.ROOT/'mk2ks_native_attract_kano_launch_v2.lua'
    capture_base.OUT=capture_base.ROOT/'audit_native_attract_kano_launch_v2'
    capture_base.BOOT_FRAME=420
    capture_base.SECONDS=1600
    capture=capture_base.run()
    code.interact(banner='Corrected physical timing run terminal; retain actual audio and mute evidence.',local=dict(capture=capture))
