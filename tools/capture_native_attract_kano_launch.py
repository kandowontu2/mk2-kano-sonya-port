"""Next ordinary cold-start timing; observe Kano launches and winner mute policy."""
import code
from pathlib import Path
import capture_native_attract_early_launch as capture_base

if __name__=='__main__':
    capture_base.LUA=capture_base.ROOT/'mk2ks_native_attract_kano_launch.lua'
    capture_base.OUT=capture_base.ROOT/'audit_native_attract_kano_launch'
    capture_base.BOOT_FRAME=420
    capture_base.SECONDS=1600
    capture=capture_base.run()
    code.interact(banner='Original native run terminal; retain actual audio and winner policy evidence.',local=dict(capture=capture))
