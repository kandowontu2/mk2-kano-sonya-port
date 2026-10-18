# Own arm-rip source conversion and typed data (staged)

`generate_arm_rip_sources.py` verifies both draft atlas hashes and converts
20 frames to editable ASCII PGM indices in assets/arm_rip. It reads each
actor's actual primary palette from generated_packed, uses indices0..63
with zero transparent, and records source cells, scale, origins, palette
hash and quantization error. Full bodies use native ground heights131/132;
all five poses share the first body's scale, preserving the shorter
kneeling pose. Arms are independently sized at57/53 pixels for their first
frames, rather than inheriting the differently zoomed atlas scale.

The indexed preview was inspected: black/red Kano, green/black Sonya with
white shoes, stretched/intact first pose and four armless reaction poses.
Body and detached-arm alignment is not yet accepted. The arm descriptor
origins are explicit calibration seeds from the native held-arm coordinate
convention, not another character's images.

`build_arm_rip_assets.py` stages generated_arm_rip/KSARART.ASM and a packed
graphics image. Its typed headers reference each actor's own palette.
Body scripts contain five multipart groups; held-arm scripts instead
contain five single-image descriptors, matching the distinct native
consumers. The previous1,856,309-byte graphics prefix is unchanged, with
81,332 bytes appended. No extra6MiB socket copy was emitted at this stage.

`qualify_arm_rip_sources.py` independently decodes the cross-byte6-bit
pixels, checks all20 PGM hashes and indices, image origins/source addresses,
both script layouts and sentinels, and the complete old graphics prefix.
ARM_RIP_SOURCE_QUALIFICATION.json records the bounded encoding proof.

This is source/data progress, not an in-game fix. No active graphics path,
native link, program ROM or release changed; the arm-rip crashes remain.
Next integrate the six missing victim tables and own palette handling,
assemble/link, then calibrate Jax's grip, shoulders, collapse grounding and
blood emitters in actual stock-MAME tests on both sides. Rebuild and runtime
proofs must be refreshed after that link. Original-character paths must
remain intact.
