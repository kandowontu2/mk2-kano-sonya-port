# Updated native development IPS package

development_patches/MK2KS_NATIVE_DEVELOPMENT_IPS.zip was replaced in place,
not archived/duplicated. It is5578388 bytes, SHA256:
CDCE665AD30E8538373D8B7427D8D64F077ADC420D0CF18157B227396EFA884C

Latest refresh adds the verified post-blocking Knife input tip and current
runtime status, including earned Kano/Sub-Zero2–0 progression to Mileena.
Patch/source audit passes again; ROM patcher output bytes/hash remain unchanged.

The program is221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A.
The26-chip patcher output archive SHA256 is:
454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38

Fourteen IPS patches/twelve unchanged original-graphics copies roundtrip through
two independent decoders. Every packaged file hash is verified; the original
source diff applies and matches current compiled source; all59 own ASM modules
match the actual build. The new grounding integrator, tests and explanation are
included alongside the native MKDEATH ASM diff. No complete ROM, emulator binary,
custom driver or host samples are included.

Four current torso-rip runtime archives have matching26 chip bytes. A fifth
stock_wolf_2219_patched_torso run uses the exact patcher-produced archive as a
hardlinked input, completes normally and passes earned-fatality/grounding/
600-field fresh-combat/palette checks. PACKAGE_QUALIFICATION.json records
exactPatchedArchiveContainer=true for that run. The other test containers retain
unselected retail clone entries, so their container hashes correctly differ.

The checked local CMD's ROM pin is updated and its no-launch check passes the
exact unmodified MAME executable and new patched archive. All323 local tests
pass. No compiler/emulator remains running. Earlier6AE0 source/campaign/audio
observations are clearly labelled historical in the packaged guide; full new-
build gameplay/visual/audio/earned-Kano-campaign acceptance remains open.
This is a development snapshot, not a new final GitHub release.
