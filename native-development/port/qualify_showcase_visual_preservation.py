"""Stream all source/output frames through SSIM; no unbounded frame arrays."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS


def main(stream_copy=False):
    out = PORT / ('generated_showcases_2219_streamcopy' if stream_copy else 'generated_showcases_2219')
    index = out / 'SHOWCASES.json'
    catalog = PORT / 'NATIVE_VIDEO_CATALOG_FULL_2219.json'
    shows = json.loads(index.read_text())
    assert shows['catalogSHA256'] == sha(catalog)
    clips = {r['key']: r for r in json.loads(catalog.read_text())['cases']}
    ff = shutil.which('ffmpeg'); assert ff
    results = []
    for show in shows['cases']:
        name = 'KANO' if show['actor'] == 17 else 'SONYA'
        video = Path(show['file']); assert sha(video) == show['SHA256']
        listing = out / (name + '.ffconcat')
        paths = re.findall(r"(?m)^file '([^']+)'$", listing.read_text())
        expected = [clips[c['sourceKey']] for c in show['chapters']]
        assert paths == [Path(c['file']).as_posix() for c in expected]
        assert all(sha(Path(c['file'])) == c['SHA256'] for c in expected)
        count = sum(c['frames'] for c in expected)
        assert count == show['sourceFramesPreserved']
        stats = out / (name + '_ssim.log')
        assert not stats.exists(), 'Never overwrite comparison evidence'
        # Compare frame order, independent of the measured container clock shift.
        # Only one frame per input is retained by the streaming comparison.
        graph = ('[0:v]settb=1/55,setpts=N[ref];[1:v]settb=1/55,setpts=N[actual];'
                 f'[ref][actual]ssim=shortest=1:stats_file={stats.name}')
        subprocess.run([ff, '-v', 'error', '-nostdin', '-threads', '1', '-safe', '0',
            '-f', 'concat', '-i', str(listing), '-threads', '1', '-i', str(video),
            '-filter_complex_threads', '1', '-filter_complex', graph, '-an', '-f', 'null', 'NUL'],
            cwd=out, check=True, capture_output=True, timeout=180, creationflags=FLAGS)
        values = []
        for line in stats.read_text().splitlines():
            match = re.search(r'n:(\d+)\s+.*All:([0-9.]+)', line)
            assert match, line
            assert int(match[1]) == len(values) + 1
            values.append(float(match[2]))
        assert len(values) == count, ('Not all frames compared', len(values), count)
        results.append(dict(actor=show['actor'], framesCompared=count,
            minimumFrameSSIM=min(values), meanFrameSSIM=sum(values)/len(values),
            everyFrameSSIMAbovePoint98=all(v > .98 for v in values),
            outputSHA256=show['SHA256'], sourceConcatSHA256=sha(listing), statsSHA256=sha(stats)))
        print(name, count, 'frames; minimum SSIM', min(values), flush=True)
    report = dict(scope='Full-frame encoded-showcase preservation against source clips in chapter order',
        cases=results, nativeArtworkOrAnimationQualityApproved=False,
        subjectiveEveryFrameVisualReviewPassed=False, fullCampaignVideos=False,
        pins={str(p): sha(p) for p in (index, catalog)})
    (out / 'VISUAL_PRESERVATION.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    assert sys.argv[1:] in ([], ['--stream-copy'])
    main('--stream-copy' in sys.argv)
