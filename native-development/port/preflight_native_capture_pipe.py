"""Synthetic bounded IPC/encoder preflight; no emulator or game data used."""
import hashlib
import json
import shutil
import subprocess
from native_capture_pipe import CapturePipe, FRAME_BYTES
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS


def main():
    out = PORT / 'generated_stream_capture_preflight'
    assert not out.exists(), 'Never overwrite preflight evidence'
    out.mkdir()
    capture = CapturePipe(out / 'eight_frames.mp4', 55, max_frames=8, timeout=20)
    expected = hashlib.sha256()
    try:
        with open(capture.address, 'wb', buffering=0) as writer:
            for index in range(8):
                frame = bytes((index * 25, 40, 90, 255)) * (400 * 254)
                assert len(frame) == FRAME_BYTES
                expected.update(frame)
                remaining = memoryview(frame)
                while remaining:
                    written = writer.write(remaining)
                    assert written and written > 0
                    remaining = remaining[written:]
        report = capture.finish()
    finally:
        if capture.thread.is_alive():
            capture.abort()
    assert report['frames'] == 8 and report['rawStreamSHA256'] == expected.hexdigest().upper()
    probe = subprocess.run([shutil.which('ffprobe'), '-v', 'error', '-count_frames',
        '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames,display_aspect_ratio',
        '-of', 'json', str(capture.output)], check=True, capture_output=True, text=True, creationflags=FLAGS)
    stream = json.loads(probe.stdout)['streams'][0]
    assert stream['nb_read_frames'] == '8' and stream['display_aspect_ratio'] == '4:3'
    report.update(scope='Synthetic eight-frame pipe/encoder preflight only; not native MAME capture',
                  videoSHA256=sha(capture.output), encodedBytes=capture.output.stat().st_size,
                  nativeCaptureVerified=False, fullCampaignVideo=False)
    (out / 'PREFLIGHT.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Eight frames streamed and encoded; raw hash/count and decoded frame count match; no raw video file.')


if __name__ == '__main__':
    main()
