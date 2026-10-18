"""One real native move through the bounded pipe, not a campaign recording."""
import csv
import json
import shutil
import subprocess
import sys
import zipfile
from native_capture_pipe import CapturePipe
from inspect_normal_runtime import BASE, PORT, sha
from campaign_rounds import require_clean_runtime_log
from refresh_special_videos import FLAGS
from verify_finisher_roms import verify


def main():
    assert sys.argv[1:] in ([], ['--audio'])
    audio = '--audio' in sys.argv
    name = 'stock_wolf_2219_stream_ball_preflight' + ('_audio' if audio else '')
    out = PORT / ('generated_stream_native_preflight_audio' if audio else 'generated_stream_native_preflight')
    assert not out.exists() and not (BASE / name).exists()
    idle = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True, creationflags=FLAGS)
    assert idle.returncode == 0, 'Existing emulator'
    reference = json.loads((BASE / 'stock_wolf_2219_video_ball/FINISHER_VIDEO.json').read_text())
    out.mkdir()
    capture = CapturePipe(out / 'native_ball.mp4', reference['rate'], max_frames=400, timeout=90)
    try:
        with (out / 'runner.stdout.log').open('w') as stdout, (out / 'runner.stderr.log').open('w') as stderr:
            result = subprocess.run([sys.executable, str(BASE / 'test_wolf_baseline.py'), name,
                '--game', '--special', '--sound-candidate', '--capture-move', '--capture-action=0x20b',
                '--capture-side=1', '--capture-min-fields=150', '--capture-pipe=' + capture.address, *(['--audio'] if audio else [])],
                cwd=BASE, stdout=stdout, stderr=stderr, creationflags=FLAGS)
        assert result.returncode == 0, 'Inspect preserved runner stderr'
        stream = capture.finish()
    finally:
        if capture.thread.is_alive():
            capture.abort()
    run = BASE / name
    receipt = json.loads((run / 'execution.json').read_text())
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256'] == sha(run / 'autoboot.lua')
    require_clean_runtime_log((run / 'mame.log').read_text())
    with zipfile.ZipFile(run / 'roms/mk3.zip') as archive:
        verify(archive, receipt)
    with (run / 'finisher_capture.csv').open() as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == stream['frames'] >= 150
    assert [int(r['frame']) for r in rows] == list(range(int(rows[0]['frame']), int(rows[-1]['frame'])+1))
    assert not (run / 'finisher_capture.bgra').exists()
    probe = subprocess.run([shutil.which('ffprobe'), '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_read_frames,display_aspect_ratio', '-of', 'json', str(capture.output)],
        check=True, capture_output=True, text=True, creationflags=FLAGS)
    video = json.loads(probe.stdout)['streams'][0]
    assert int(video['nb_read_frames']) == stream['frames'] and video['display_aspect_ratio'] == '4:3'
    final = capture.output
    if audio:
        from mux_stream_native_audio import mux
        final = out / 'native_ball_with_audio.mp4'
        mux(run, capture.output, run / 'finisher_capture.csv', final, cleanup=True)
    report = dict(scope='Short real native Ball frame-stream/encoder preflight, not campaign or A/V acceptance',
        **stream, all26CurrentROMChipsVerified=True, videoSHA256=sha(final),
        nativeAudioCaptured=audio, fullCampaignVideo=False,
        pins={str(p): sha(p) for p in (run / 'execution.json', run / 'autoboot.lua', run / 'finisher_capture.csv')})
    (out / 'NATIVE_PREFLIGHT.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Native streamed frames', stream['frames'], 'decoded count matches; no raw video file.')


if __name__ == '__main__':
    main()
