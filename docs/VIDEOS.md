# Video demonstration coverage

Two separate complete-movelist showcases were assembled on 2026-10-15:

- Kano: 189.01 seconds; SHA-256
  `F2A2CD3531C1F57BEAD0AE8F7980CD9EFCAB6179A0C7781911E200A6154E9D55`.
- Sonya: 186.85 seconds; SHA-256
  `8FB0135247DAF3E691563884205810624191683CF9389242FBF44C62F5C6207D`.

Each has 18 labelled chapters: six shared controls, four specials, two
fatalities, Friendship, Babality, three stage finishes and Shang's morph to
that character. F/B are relative to the opponent. The game picture is 4:3;
the command footer is outside it. Audio is native gameplay audio.

The recorder requires actual native move/contact/recovery or earned
finisher/scene evidence, verifies the encoded frame/audio duration, and only
then removes intermediate media. Morph clips include natural restoration.
Chaptered showcases are edited demonstrations, not uninterrupted campaigns.

The two final MP4s passed full video/audio decoding and sampled visual review.
The footage is not uploaded to this code-only repository. No ROM/media download
is embedded here.

Recording implementation:

- `tools/record_move_showcase_20261015.py`
- `tools/review_showcase_frames_20261015.py`
- `tools/assemble_move_showcases_20261015.py`
- `tools/seal_showcase_delivery_20261015.py`

These source tools retain historical local path assumptions described in
`BUILD.md`; do not mistake source publication for a portable capture installer.

## Full campaigns are separate

Both full current-build campaign recordings are now complete through both
bosses and both own ending pages:

- Kano:22m58.55s,6 paid losses/continues. Current MP4 SHA-256
  `A9B1F5D1AAA59D4506B5AA576796E32063A2097D0E87A863E08364E2E9EF6D75`.
- Sonya:53m51.57s,30 paid losses/continues. Current MP4 SHA-256
  `A43AA9F057AA08E18A2F3F9F49E123ECACEF994E1267BD53C77DA6DFF21F8B7A`.

They are automated native-control runs, not represented as human play or
lossless/no-continue clears. All failed rounds and paid continues remain in
the full recordings. No health/AI/difficulty/RNG/state edits were used.
All four actual MP4 files passed full video/audio decoding and have non-silent
native audio. Final Sonya victory, both own ending pages and presentation
samples were visually reviewed. Native full-game aspect metadata is exactly
4:3; the SAR correction was stream-copy metadata only, with no gameplay cut
or re-encoding. Temporary WAV/video-only files were removed after verification.

## Development history of the recording controller

Earlier failed attempts were not presented as clears; their large temporary
video/audio files were deleted. The following is development history, not a
statement that the final videos are still pending.
A bounded scalar-only Kitana controller test passed: Sonya earned KOs at native
fields 105535 and 107216, then entered Mileena at 107749 without a paid continue
between those rounds. Four negative evidence mutations were rejected. This
proves that encounter, not the whole ladder. The same controller is now being
tested through the rest of the ladder before another large recording.
It uses physical inputs, not health/AI/difficulty changes.

The successor also cleared Mileena (native KO fields 121324 and 123128, same
paid selection25) and Scorpion (143616 and 145291, same paid selection28;
Scorpion won one preceding round). Actual next-match admissions were at123637
and145799. That finite test stopped at its200000-field bound while facing
Raiden, without an ending. The next controller changes only Raiden12/Shang14
to the same guarded close-leg policy; it does not reset or rewrite game state.
No unsuccessful scalar test is represented as a completed video.

The subsequent test cleared Raiden, Shang and Kintaro. A final-stage-only
successor replaced the weak Ring policy with the charge-recovery uppercut
controls used in Kano's successful video. It then earned Sonya's native Shao
KO at170656, entered her ending at173747, completed both own pages at176489,
and stopped at176789. It included30 actual paid losses/continues. Six missing
completion/identity/boss/page mutations were rejected. This proves a complete
current-build automated campaign. The separate fresh AV recording subsequently
passed independently:176789 actual encoded native frames, matching the
benchmark's entire canonical native event log exactly (SHA-256
`AB7F7992F49371DA2D97CD2B01FFC1B7C9CBC2EDEB97A25AD71F2F756113B4A4`).
The completion-audit and sampled visual-review code is published alongside
the controller; the media itself remains outside this source-only repository.
