"""Bounded chapter audio alignment against source clips, not native A/V approval."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import numpy as np
from scipy.signal import correlate
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS

RATE = 8000


def alignment(reference, observed, expected_lead):
    reference = np.asarray(reference, dtype=np.float64)
    observed = np.asarray(observed, dtype=np.float64)
    assert len(observed) >= len(reference) > 100
    reference -= reference.mean()
    energy = np.dot(reference, reference)
    assert energy > 1e-5, 'Silent source cannot prove alignment'
    numerator = correlate(observed, reference, mode='valid', method='fft')
    count = len(reference)
    total = np.r_[0, np.cumsum(observed)]
    square = np.r_[0, np.cumsum(observed * observed)]
    variance = square[count:] - square[:-count] - (total[count:] - total[:-count]) ** 2 / count
    score = numerator / np.sqrt(np.maximum(variance * energy, 1e-30))
    peak = int(np.argmax(score))
    return dict(correlation=float(score[peak]), offsetSeconds=peak / RATE - expected_lead)


def main(stream_copy=False):
    ff = shutil.which('ffmpeg'); assert ff
    fp = shutil.which('ffprobe'); assert fp
    out = PORT / ('generated_showcases_2219_streamcopy' if stream_copy else 'generated_showcases_2219')
    index = out / 'SHOWCASES.json'
    catalog = PORT / 'NATIVE_VIDEO_CATALOG_FULL_2219.json'
    showcases = json.loads(index.read_text())
    assert showcases['catalogSHA256'] == sha(catalog)
    clips = {r['key']: r for r in json.loads(catalog.read_text())['cases']}

    def decode(path, start, duration):
        result = subprocess.run([ff, '-v', 'error', '-nostdin', '-threads', '1',
            '-ss', f'{start:.9f}', '-i', str(path), '-t', str(duration), '-vn',
            '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'],
            check=True, capture_output=True, timeout=30, creationflags=FLAGS)
        return np.frombuffer(result.stdout, dtype='<f4').copy()

    records = []
    for case in showcases['cases']:
        output = Path(case['file']); assert sha(output) == case['SHA256']
        timing = subprocess.run([fp, '-v', 'error', '-threads', '1', '-select_streams', 'v:0',
            '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(output)],
            check=True, capture_output=True, timeout=60, creationflags=FLAGS)
        frames = json.loads(timing.stdout)['frames']
        assert len(frames) == case['sourceFramesPreserved']
        first_frame = 0
        for chapter in case['chapters']:
            clip = clips[chapter['sourceKey']]
            source = Path(clip['file']); assert sha(source) == clip['SHA256'] == chapter['SHA256']
            source_timing = subprocess.run([fp, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=start_time', '-of', 'json', str(source)],
                check=True, capture_output=True, timeout=30, creationflags=FLAGS)
            source_start = float(json.loads(source_timing.stdout)['streams'][0]['start_time'])
            assert source_start == 0, 'Nonzero source clock needs an explicit decode-seek model'
            # One second away from chapter seams. At most1.4 seconds is decoded
            # at once; AAC delay is measured, never corrected in this inspector.
            reference = decode(source, .5, 1)
            observed = decode(output, chapter['startMilliseconds'] / 1000 + .3, 1.4)
            measured = alignment(reference, observed, .2)
            video_offset = float(frames[first_frame]['best_effort_timestamp_time']) - chapter['startMilliseconds'] / 1000
            measured['videoClockOffsetSeconds'] = video_offset
            measured['audioOffsetRelativeToVideoSeconds'] = measured['offsetSeconds'] - video_offset
            records.append(dict(actor=case['actor'], sourceKey=chapter['sourceKey'],
                                sourceSHA256=clip['SHA256'], **measured))
            first_frame += clip['frames']
        assert first_frame == len(frames)
    report = dict(scope='One one-second audio alignment window per chapter against encoded source clip',
                  cases=records, allWithinOneVideoField=all(abs(r['audioOffsetRelativeToVideoSeconds']) < 1/55 for r in records),
                  allCorrelationsAbovePoint95=all(r['correlation'] > .95 for r in records),
                  nativeAudioVideoSyncVerified=False, allFrameVisualReviewPassed=False,
                  pins={str(p): sha(p) for p in (index, catalog)})
    (out / 'AUDIO_ALIGNMENT_VIDEO_CLOCK.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Windows', len(records), 'max offset', max(abs(r['offsetSeconds']) for r in records),
          'max video-relative offset', max(abs(r['audioOffsetRelativeToVideoSeconds']) for r in records),
          'min correlation', min(r['correlation'] for r in records), flush=True)


if __name__ == '__main__':
    assert sys.argv[1:] in ([], ['--stream-copy'])
    main('--stream-copy' in sys.argv)
