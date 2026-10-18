"""Copy streamed video and encode its native WAV interval with bounded memory."""
import array
import csv
import json
from pathlib import Path
import shutil
import subprocess
import wave
import zipfile
from inspect_normal_runtime import PORT, BASE, sha
from campaign_rounds import require_clean_runtime_log
from refresh_special_videos import FLAGS
from verify_finisher_roms import verify


def timing(rows):
    first = last = None; count = 0
    for row in rows:
        assert (row['width'], row['height'], row['bytes']) == ('400', '254', '406400')
        if last:
            assert int(row['frame']) == int(last['frame']) + 1
            assert float(row['seconds']) > float(last['seconds'])
        else:
            first = row
        last = row; count += 1
        assert count <= 300000
    assert count > 1
    rate = (count - 1) / (float(last['seconds']) - float(first['seconds']))
    assert 50 < rate < 60
    return dict(frames=count, rate=rate, firstGuestFrame=int(first['frame']),
        firstGuestSeconds=float(first['seconds']), lastGuestSeconds=float(last['seconds']), duration=count/rate)


def mux(run, video, capture_csv, output, cleanup=False):
    run = Path(run).resolve(); video = Path(video).resolve(); output = Path(output).resolve()
    capture_csv = Path(capture_csv).resolve()
    assert run.parent == BASE.resolve(), 'Only explicit generated runtime folders are accepted'
    assert capture_csv.parent == run and video.parent == output.parent
    assert output.parent.is_relative_to(PORT.resolve()) and not output.exists()
    receipt = json.loads((run / 'execution.json').read_text())
    assert receipt['exitCode'] == 0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['controllerSHA256'] == sha(run / 'autoboot.lua')
    require_clean_runtime_log((run / 'mame.log').read_text())
    with zipfile.ZipFile(run / 'roms/mk3.zip') as archive:
        verify(archive, receipt)
    with capture_csv.open() as stream:
        clock = timing(csv.DictReader(stream))
    wav = run / 'native_dcs.wav'
    peak = 0
    with wave.open(str(wav), 'rb') as native:
        assert native.getsampwidth() == 2 and native.getnchannels() in (1, 2)
        sample_rate = native.getframerate()
        assert native.getnframes() / sample_rate >= clock['lastGuestSeconds'] - .1
        start = round(clock['firstGuestSeconds'] * sample_rate)
        native.setpos(start)
        remaining = min(round(clock['duration'] * sample_rate), native.getnframes() - start)
        while remaining:
            count = min(16384, remaining)
            data = native.readframes(count)
            assert data
            peak = max(peak, max(map(abs, array.array('h', data)), default=0))
            remaining -= count
    assert peak > 0, 'Captured native audio interval is silent'
    ff = shutil.which('ffmpeg'); fp = shutil.which('ffprobe'); assert ff and fp
    def command(args):
        return subprocess.run(args, check=True, capture_output=True, text=True, timeout=600, creationflags=FLAGS)
    video_hash = sha(video); wav_hash = sha(wav)
    command([ff, '-v', 'error', '-nostdin', '-threads', '1', '-i', str(video),
        '-ss', f"{clock['firstGuestSeconds']:.12f}", '-i', str(wav), '-map', '0:v:0', '-map', '1:a:0',
        '-t', f"{clock['duration']:.12f}", '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-threads', '1', '-movflags', '+faststart', '-n', str(output)])
    probe = json.loads(command([fp, '-v', 'error', '-count_frames', '-show_streams', '-of', 'json', str(output)]).stdout)
    actual = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert int(actual['nb_read_frames']) == clock['frames'] and actual['display_aspect_ratio'] == '4:3'
    assert abs(float(actual['r_frame_rate'].split('/')[0]) / float(actual['r_frame_rate'].split('/')[1]) - clock['rate']) < .00001
    assert any(s['codec_type'] == 'audio' for s in probe['streams'])
    command([ff, '-v', 'error', '-xerror', '-nostdin', '-threads', '1', '-i', str(output), '-f', 'null', 'NUL'])
    report = dict(scope='Native audio interval muxed with streamed video; not campaign-clear or exact A/V approval',
        **clock, file=str(output), SHA256=sha(output), bytes=output.stat().st_size,
        sourceVideoSHA256=video_hash, sourceWAVSHA256=wav_hash, capturedAudioPeakPCM16=peak,
        currentAll26ROMBytesVerified=True, nativeAudio=True, videoCopiedWithoutReencoding=True,
        fullAVDecodePassed=True, exactAudioSyncQualified=False, fullCampaignClearVerified=False,
        verifiedIntermediatesRemoved=False,
        pins={str(p): sha(p) for p in (capture_csv, run / 'execution.json', run / 'autoboot.lua')})
    proof = output.with_suffix('.qualification.json'); assert not proof.exists()
    proof.write_text(json.dumps(report, indent=2) + '\n')
    if cleanup:
        assert video.suffix == '.mp4' and video != output and wav.name == 'native_dcs.wav'
        assert sha(video) == video_hash and sha(wav) == wav_hash
        video.unlink(); wav.unlink()
        assert not video.exists() and not wav.exists()
        report['verifiedIntermediatesRemoved']=True
        proof.write_text(json.dumps(report, indent=2) + '\n')
    return report
