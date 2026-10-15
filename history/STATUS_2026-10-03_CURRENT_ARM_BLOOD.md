# Kano arm-rip blood corrected; detached-arm alternate costume still incomplete

Current experimental candidate: diagnostic_v1061_owned_arm_invariant_blood.
EXE SHA256: FBB09125520F91EFE78F619D221D8399E07E6BF961AEE05B7C171889ED9EE78B.
Payload SHA256: 5D78E543EA1E387461BD7EFF0958F9829565469CD51D5B2EE0A6CF1D90F0D322.
Native driver SHA256 remains29A023356C55A7FA89110FA27FDE2B7A6AB49562967D6BD44C5167B40F7AC2EB.
No native CPU/game-source change. Installed EXE/CMD/ZIP untouched. NOT release-ready.

## Before editing

The preceding goal turn made progress: twenty1048 regressions were independently
verified and checkpoint1057 saved. This turn revalidated ALL9,391 checkpoint
pins with zero mismatches. No prior test emulator remained live. Historical
evidence, original sprites and original normal/alternate palettes are unchanged.

## Implemented blood-only conversion

The imagegen skill routed two precise blood-only guide edits through built-in
image_gen. Original five-body/five-arm1774x887 transparent atlases were viewed
first. Cyan guides are saved in art_native_arm_blood_v1059 with exact prompts,
builtin output identities and SHA256s. Guides classify existing wounds; their
silhouettes/shading are NOT copied into game sprites. Intact costume trim stays
unclassified. Original sprites supply all encoded geometry, alpha and shading.

Encoder1060 remaps only classified Kano blood to original pens48,46,63, which
are invariant red in BOTH native palettes.750 blood pixels are classified;
477 indices change, affecting485 packed payload bytes. Every nonblood costume
index and transparent index is preserved. Descriptors, palettes, streams,
positions, Sonya sprites and all other move assets remain byte-identical.
Independent1064 re-crops/re-scales the immutable source and guide, reconstructs
every native descriptor/stream and packed raster, verifies the old nonblood
indices and alpha, and independently bounds ALL changes to Kano pixel spans.
No palette, costume-selector logic, victim ID, health or timer patch is used.

Candidate1061 links the unchanged native sources with the new matched payload.
Installed EXE restoration was verified against413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891.

## Verified current runtime; deliberately separate scopes

Four audit_v1062 cases genuinely select Kano/Sonya in both physical player
slots, earn322 original collision damage/two KOs, inputBBBB LP, enter original
FF8BE240 and complete at147 fields, reach continue and terminate at5,198.
All six native extended tables read actual17/18 rows. Independent1064 passes
true ownership, native floors/raster grounding, FIFO/DMA dimensions, hardware
palettes and actual clipped pixels for all ten body/arm poses per case:
8,224 owned DMAs and80 actual component/prop snapshots. Normal observers are
read-only; original physical input driver unchanged; no cache overrun accepted.

Two audit_v1063 cases EXPLICITLY assist with one victim flag-6 write to exercise
the native alternate-palette branch. They are CONTROLLED DIAGNOSTICS, NEVER
natural selection/ordinary-play acceptance. Independent1065 verifies the
single declared assist, true IDs, original147-field wrap/continue, whole guest,
actual graphics, hardware palettes and all ten presented poses.4,198 owned
DMAs and42 component/prop snapshots prove that classified blood remains red
in the measured alternate body palette and normal detached-arm palette.

Those diagnostics expose a separate incomplete native costume consumer:
the detached arms still use their embedded NORMAL palette. Body trim switches
blue correctly; arm wrist trim remains red. Actual mismatched costume pens are
54,56,57,58,59,60,61 in both slots. OriginalFF83B250 reads the raw descriptor's
palette at+70bits; originalFF8BEC70 overrides only the Mileena-specific case.
This is NOT accepted as full alternate-costume runtime. Next native correction
must make owned arm props follow the actual victim costume without proxies
or live test assistance being installed as gameplay logic.

Main agent viewed all20 corrected Kano encoded poses and72 actual scenes:
48 normal,24 controlled. Sonya's complete306 actual PNGs are byte-identical to
previously reviewed1050 cases. Actual camera-edge clipping is unchanged and
is not claimed as unoccluded full-body proof. Three1069 in-memory counterexamples
are rejected by independent raster reconstruction: old blue blood restored,
costume trim incorrectly remapped and transparent boundary painted opaque.
No image, game source or evidence file is modified by the fixtures.

## Still required for the full unchanged objective

Fix native detached-arm alternate palette selection; prove natural alternate
costume selection and remaining victim variants. Replay established native
regressions on THIS1061 candidate (1055/1056 remain1048 historical scope).
Kung Lao split/other half and successful native hat kill remain incomplete.
Continue remaining stock fatalities, all arenas/cinematics/audio, full real
towers/Kintaro/Shao/continues/endings, final combined native CSS blink/borders/
P1 numbers and portrait teardown, owned ladder icons, names/name shadows,
floor shadows/standing height, complete moves and human/CPU play. Existing
narrow tests do not waive those gates. Update playable CMD/ZIP only after
appropriate complete verification; safe obsolete build cleanup remains.
No deletion occurred. Full-port goal remains active and acceptance FALSE.
