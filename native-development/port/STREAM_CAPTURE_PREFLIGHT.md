# Bounded native video-stream preflight

`native_capture_pipe.py` sends raw BGRA frames through a local Windows named
pipe to one hidden, BelowNormal, single-thread video encoder. The Python
bridge reads64KiB at a time, hashes the stream incrementally and enforces a
frame/timeout limit. It does not retain a frame array or write raw video to disk.
These are buffer bounds, not a claim that the entire emulator/encoder consumes
only64KiB of RAM.

The synthetic eight-frame preflight checks the input stream hash and decoded
frame count/4:3 aspect. Unit tests reject incomplete frames and prove cancellation
before writer connection terminates the encoder.

The real `stock_wolf_2219_stream_ball_preflight` completed normally on stock
MAME with all26 current ROM chips verified. It streamed150 native frames
(60,960,000 BGRA bytes), with150 decoded output frames and no `.bgra` file.
The capture CSV hash is C630996645BB9C42E09F8F7C5F10A1C36E03271D3D79BF24C15F444916AFE6D1,
identical to the earlier current native Ball capture's timing CSV.

Evidence: `generated_stream_native_preflight/NATIVE_PREFLIGHT.json`, its
encoded MP4, and the frozen controller/runtime receipt in the named run.
The first preflight has **no audio** and is not a full campaign video,
audiovisual acceptance or a substitute for the existing move demonstrations.
No game logic or driver code was modified.

## Native audio mux preflight

`stock_wolf_2219_stream_ball_preflight_audio` also completed normally and
streamed150 frames without a raw video file. The actual contiguous guest-time
CSV determines the WAV trim and video duration. `mux_stream_native_audio.py`
reads at most16384 audio frames per analysis block, copies the video stream
without a second video encode, and encodes the native DCS interval to AAC.
It requires a non-silent captured interval, all26 current ROM bytes, terminal
success, matching observer hash, matching decoded frame count,4:3 ratio and
full audio/video decode before cleanup.

The encoded result and qualification are in
`generated_stream_native_preflight_audio/`. Its verified video-only intermediate
and native WAV were removed; input hashes remain in the qualification. This
proves the short capture/mux path, not subjective A/V timing, every sound or
an earned full-campaign video. Full-duration recording remains pending.

## Campaign observer preflight and current recording

`campaign_stream_capture.lua` has a separate function scope so it does not
exceed the existing controller's Lua200-local limit. The first campaign
preflight failed at script loading for that reason; it is retained as failed
setup evidence, not gameplay or a recording success. The runner now checks
the native exit receipt before waiting for a recording pipe.

The corrected `stock_wolf_2219_campaign_stream_preflight_v2` completed with
4075 contiguous captured fields, including the controller's final field. Its
native audio/video mux and full decode passed, and verified intermediates were
removed. It is a partial first-attempt preflight, not an earned campaign clear.

`record_native_campaign.py` subsequently started the full Sonya replay at
`stock_wolf_2219_sonya_campaign_stream`, using the verified clear's original
physical-input policy. It streams frames, retains a temporary native WAV, and
requires current-ROM campaign/clear qualification before labeling a full
campaign video. The full recording is pending while the process is live;
no completion follows from starting it or from an in-progress MP4.

The full attempt subsequently completed and passed native clear, contiguous
capture, audio mux and full-decode qualification:157503 frames with an earned
Sonya clear. The final MP4 is418,957,924bytes. Its native game trace is
byte-identical to the earlier verified clear, and verified WAV/video-only
intermediates were removed. See `SONYA_CAMPAIGN_VIDEO_2219.md` for exact scope,
hashes, visual samples and remaining work. No process remains from this job.
