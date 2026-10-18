# Kano Friendship native bubble pop: first linked candidate

Existing project kano_bubble_pop.wav is staged with a2-second input cap;
actual input30022 samples at48kHz. Native PCM19546 samples at31250Hz is
encoded by original HENRY into KSKP.CMP and linked into SoundP playlists
2030–2032. The native priority table entry104 selects the correct physical
track with sp_effect/duration40. The game emits it only at own bubble pose
ff9d2750. No host samples/custom MAME code are involved.

Hidden sound compile24.23s and game compile19.44s created no window.
Source regeneration includes the new priority-table entry and own ASM caller.
Two bounded staging/source tests pass.

Stock-MAME run363 physically wins two rounds and performs Kano Friendship.
The existing behavior qualifier still passes all193 active fields, own body/
bubble timing, object/process retirement and native completion through9000.
The passive port trace contains exactly one2030 call aligned to the actual
pop pose within the one-field frame_done/tap observation ordering difference.

The waveform diagnostic reads at most2 seconds into floats, never the full
match. Correlation with the staged PCM is0.76659 at28.8ms output latency,
with nonzero recorded native DCS signal. This is supporting playback evidence,
not final mix/complete-tail acceptance or an isolated decoded-clip comparison.
An A/B or decoded-reference check and mirrored/audio regression cases remain.
Reports are in run363/kano_pop_audio_diagnostic.json and qualification.json.

Current program and sound ROMs changed. The previous clean rebuild proof,
development IPS ZIP and runtime reports remain historical snapshots until
refreshed against this new link; no new package/release was promoted.

## Decoded-reference/control follow-up

Run364 is a SoundW control; run365 is mirrored SoundP. Both finish without
faults and mirrored behavior still passes the193-field Friendship qualifier.
Original HENRY decode of KSKP produces a19546-sample reference, matching the
full staged duration. Codec correlation against original PCM is0.77875,
explaining much of the weaker direct PCM comparison.

Subtracting the same-profile SoundW control from run363's two-second capture
gives0.99043 correlation against the entire native decoded clip at28.3ms
latency. The full reference fits inside the analyzed window. This is strong
bounded native-playback evidence for that case, not a call-only assertion.
Mirrored run365 has the correctly timed single cue and mixed-audio decoded
correlation0.76839 at30.5ms; it still needs a matching mirrored control to
isolate the whole clip. The diagnostic checks current SoundP archive bytes
and requires control profile equality, not just matching script text/hash.
Final mix/source-codec fidelity acceptance and broader audio regressions remain
open. Every waveform analysis reads at most two seconds per capture.

## Mirrored isolated capture and independent sound rebuild

Run366 supplies the matching mirrored SoundW control. Run365 minus366
correlates0.99034 with the entire native decoded pop clip at30.4ms latency;
both sides now have full decoded-clip matches in bounded two-second windows.
Final mix/source-codec fidelity review remains separate.

Existing clean sound inputs (all10 prior PCM sources,439 original compressed
inputs, tools and prior ROM hashes) were verified, then the new pop PCM and
playlist were independently regenerated from the original project WAV in the
same clean directory. No working CMP or sound ROM was imported. Hidden clean
sound compilation completed in16.01s without a window. All11 own CMPs and4
ROM outputs have fresh timestamps; all four1MiB sound ROMs match the working
SoundP output byte-for-byte. CLEAN_SOUND_INPUTS/QUALIFICATION contain proof.
The from-scratch clean-sound preparation route now includes all11 clips too.
Seven current pop/IPS tests pass. Program clean rebuild/package refresh for
this cue-enabled link and broader port gates still remain unfinished.
