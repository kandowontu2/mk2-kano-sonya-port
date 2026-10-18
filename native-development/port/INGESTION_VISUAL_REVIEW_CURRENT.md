# Ingestion review: observations, not acceptance

## Fresh 2219 review completed

All four `stock_wolf_2219_ingestion_{17,18}_p{1,2}` runs completed normally
and qualified. Coordinator exit 0. The runtime report SHA256 is
`3B99DAEDE4F58A26A16331586E97E4E3BF8E6362AF351198854D91E8DB20B2CE`;
it pins actual current 26-chip ROMs, native sources, frozen observers, traces,
and all 32 pose PNG hashes.

All eight fresh pose captures for each of the four roles were individually
viewed. The own body bends into the mouth, shortens through the torso/legs,
and disappears in both directions without an obvious separated-mouth gap,
wrong palette, proxy body, or reversed ingestion trajectory. The tested
pose-to-mouth alignment is visually accepted. This is a scoped human-style
visual judgment, not a machine-derived pixel-equivalence claim or universal
position/edge/audio acceptance. The qualifier intentionally retains its
conservative machine-only `finalMouthAlignmentAccepted:false`; this review
records the separate visual decision rather than silently changing that gate.

Additional original control `stock_ingestion_control_kitana270/snap/bodysuck_05550.png`
was individually viewed: native late leg poses also rise above the mouth.
The same behavior in the own poses is not an ordinary-floor-grounding defect.
Original control runtime remains historical, not current 2219 control proof.

No ROM/art edit was required. No emulator remains running after this batch.

## Earlier provisional observations

The current 2219 source uses sixteen dedicated editable own ingestion PGMs
and readable KSINART native assembly. No artwork or ROM change was made in
this review. The fresh four-role coordinator is ready but must wait until
the live stage batch finishes; historical 265/266 recordings fail current-ROM
qualification as intended.

Historical screenshots individually inspected:

- `stock_ingestion_sonya266/snap/ingest_phase0_05532.png`: own Sonya is upright
  and raised to the right of Mileena at the first ingestion pose.
- `stock_ingestion_control_kitana270/snap/bodysuck_05532.png`: original Kitana
  is already bent toward Mileena's mouth at the corresponding first pose
  (native first phase begins at 5529 in the control report).
- `stock_ingestion_sonya266/snap/ingest_phase2_05540.png`: Sonya is horizontal,
  head immediately beside Mileena's mouth, body extending to the right.
- `stock_ingestion_sonya266/snap/ingest_phase7_05560.png`: no substantial body
  remains visible; tiny final fragments cannot be judged at this scale.

These observations do not establish a native positioning defect or complete
visual acceptance. In particular, a raised first pose is not ordinary combat
grounding, and the original control also has a raised victim. The initial own
pose differs from the original; inspect all eight fresh poses and both mirrored
sides before changing artwork/origins. Current geometry deliberately preserves
the native reference's mouth-side edge and vertical center, not its pixels.

Remaining: fresh 2219 four-role traces and captures, complete pose-to-mouth
continuity review, and current original-control comparison if needed. Do not
promote `finalMouthAlignmentAccepted` from these historical samples.
