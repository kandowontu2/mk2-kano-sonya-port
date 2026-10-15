-- Autoboot chunks have a private environment; dofile uses Lua's globals.
-- These host-only values configure button timing and passive observations.
_G.mk2ks_boot_frame=420
_G.mk2ks_capture_winners=true
dofile('mk2ks_native_attract_early_launch.lua')
