# Phase-specific detached-arm origins

The initial single origin per actor left all five arm images at the same
location, despite Jax's changing held/throw movement. `arm_rip_origins.py`
now uses the native MKMK3.TBL phase center/bottom trajectories as geometry
references. It adjusts each origin for the dimensions of the OWN component:
x=oldX+round((ownWidth-oldWidth)/2), y=oldY+ownHeight-oldHeight. No reference
character's pixels, palette, ID or executable code are substituted.

`build_arm_rip_assets.py --refresh-header-origins` first verifies the old
generated ASM, packed image and unchanged source manifest. It regenerates
typed headers while asserting packed pixels are identical, then retains
the existing sockets only after rechecking every hash. Thus no extra gfx
socket copies or artwork variants were added. Packed SHA remains
1126CCAF9ED1CA5859C95AC4D26E504D10B6F3532DC49BAE817013A6CDDE6CE8.

The hidden native build passed23.56 seconds with no window. Stock MAME
runs221–224 each completed9,000 fields, covering both own fighters and both
physical player sides after two natural round wins. Native fatality state2
lasted147 fields and reachedffff completion. All five own body poses and
five own arm frames were observed, with two detached-arm objects and no
missing-art, illegal recovery, Lua error or timeout. Current runtime
qualification additionally reads all20 compiled image headers and verifies
dimensions, origins, palette pointers, controls and pixel-source addresses.

`test_arm_rip_origins.py` checks all10 native reference rows against source,
all10 own headers' center/bottom preservation and distinct per-phase origins.
`qualify_arm_rip_sources.py` again verifies the pixel/PGM/ASM contracts.
Current preparation audit:243 generated files, zero structural differences.
The current link is not yet independently clean-rebuilt.

Viewed final-arm captures221/222 now place the discarded components beside
Jax, rather than suspended beneath him. This does NOT accept the entire
animation. Earlier phase-zero captures show a T-pose while Jax bends and
reaches forward, so the victim's initial grip pose needs an artwork revision:
both hands must extend toward Jax, angled down from the shoulders, instead
of one arm extending away. Moving the entire body lower would sink its feet
and would not correct the pose. Keep later armless poses intact when fixing
that first frame. Blood emitters and mirrored visuals still need review.
No release was promoted; alignment acceptance stays false.
