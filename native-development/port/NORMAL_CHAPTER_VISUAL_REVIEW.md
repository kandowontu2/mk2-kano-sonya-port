# Sparse current-showcase normal review

2026-10-18: prepared and actually viewed six labeled contact sheets covering
17 normal/proximity chapters for each actor, three decoded samples per chapter
(102 samples total). Source video SHA256 values are checked before extraction;
generated_showcases_2219_streamcopy/normal_chapter_review/SAMPLES.json pins
the six sheet hashes, video hashes, chapter titles and sample timestamps.
Extraction uses one hidden BelowNormal single-thread FFmpeg at a time, no
emulator and no raw video dump. The initial script invocation failed on a
string/Path mismatch before producing any sheet; the corrected run succeeded.

Visible samples show true Kano/Sonya artwork, floor shadows, hit reactions,
airborne and ground poses, throw victim rotation, and subsequent stance
recovery. No selection portraits or obvious palette corruption appear in
these samples. Existing overview sheets for both actors were also viewed,
including special/finisher and Shang-morph samples; these are sparse evidence.

This is not full animation approval. In particular, the three fixed chapter
fractions often miss the brief punch strike and extended vertical-kick pose.
Their title alone does not prove a visible attack. Denser action-local review
is needed for those chapters and complete motion/seams cannot be judged from
three stills. Nor do these samples approve every floor offset, lifebar glyph
pixel, finisher interaction or audio timing. Numeric action/contact evidence
is separate and must not be substituted for this missing temporal review.

Follow-up: actually viewed six additional sheets sampling each actor's High
Punch, Low Punch and Vertical Jump Kick every50ms from chapter start through
1.15s (144 decoded samples). The short_attack_review/SAMPLES.json beside the
showcases pins the videos, sheets and timestamps. Both punch sequences show
windup, extended fist, opponent recoil and retraction rather than only idle
poses. Both vertical kicks show takeoff, extended kicking leg, victim recoil,
landing compression and return to stance; no stuck pose or missing body part
appears in those samples. High/low punches visibly differ in strike height.
This closes the specific missing-strike-pose sampling gap noted above, not
continuous every-frame animation, subjective real-time motion or audio review.
No ASM, ROM, timing or gameplay change was warranted by this inspection.
