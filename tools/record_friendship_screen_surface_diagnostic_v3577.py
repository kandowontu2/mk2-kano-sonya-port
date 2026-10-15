"""Preserve rejected raw-bitmap probe; never relabel it as game acceptance."""
import json
import re
import subprocess
from pathlib import Path
import run_current_friendship_ram_audio_v3561 as audio

ROOT, need, sha = audio.ROOT, audio.need, audio.sha
OUT = ROOT / 'audit_v3578_friendship_raw_screen_surface_diagnostic'


def main():
    need(not OUT.exists(), 'Immutable rejected observer record')
    pins, cases = {}, {}
    for side in (1, 2):
        folder = ROOT / f'audit_v3571_current_kano_friendship_visible_p{side}'
        records = []
        for line in (folder / 'run.log').read_text().splitlines():
            if line.startswith('MK2_FSTREAM_CHECKED '):
                records.append(dict(re.findall(r'(\w+)=([^\s]+)', line)))
        need(len(records) == 1600, 'Both raw-surface Kano probes actually finished their observed window')
        mismatches = sum(r['currentRGB_SHA256'] != r['referenceRGB_SHA256'] for r in records)
        previous = sum(records[i]['currentRGB_SHA256'] == records[i - 1]['referenceRGB_SHA256']
                       and records[i]['currentRGB_SHA256'] != records[i]['referenceRGB_SHA256']
                       for i in range(1, len(records)))
        need(mismatches > 400 and previous > 200,
             'Actual raw bitmap evidence often matches prior changing snapshot field, not current reference')
        cases[f'kano_p{side}'] = dict(actualRawFields=1600, sameFieldMismatches=mismatches,
                                     differentSameFieldButExactPreviousReference=previous,
                                     currentVisualAcceptance=False)
    for folder in ROOT.glob('audit_v3571_current_*_friendship_visible_p*'):
        need(folder.is_dir(), 'Exact rejected diagnostic capture leaves')
        before = json.loads((folder / 'input_hashes_before.json').read_text())
        for file, digest in before.items():
            need(sha(file) == digest, 'Rejected probe inputs still unchanged')
            need(file not in pins or pins[file] == digest, 'Consistent rejected capture provenance')
            pins[file] = digest
        for file in folder.rglob('*'):
            if file.is_file():
                pins[str(file)] = sha(file)
    for relative in ('tools/run_current_friendship_stream_pixels_v3570.py',
                     'mk2ks_current_friendship_stream_pixels_v3569.lua',
                     'mame-mkp/src/frontend/mame/luaengine.cpp',
                     'mame-mkp/src/emu/screen.cpp', 'mame-mkp/src/emu/video.cpp'):
        path = ROOT / relative
        pins[str(path)] = sha(path)
    screen = (ROOT / 'mame-mkp/src/emu/screen.cpp').read_text()
    video = (ROOT / 'mame-mkp/src/emu/video.cpp').read_text()
    need('void screen_device::pixels(u32 *buffer)' in screen and
         'screen_bitmap &curbitmap = m_bitmap[m_curbitmap];' in screen and
         'void video_manager::pixels(u32 *buffer)' in video and
         'create_snapshot_bitmap(nullptr);' in video,
         'Source distinguishes alternate raw current bitmap from actual snapshot renderer')
    pins[str(Path(__file__).resolve())] = sha(__file__)
    value = dict(diagnosticRecorded=True, passed=False, currentVisualAcceptance=False,
        candidate=audio.collector.CANDIDATE, cases=cases,
        unifiedControllerSession=72393, controllerTerminalExitCode=1,
        terminatedKnownControllerPID=103304, terminatedVerifiedRemainingDiagnosticChildPIDs=[123836],
        terminationReason='Wrong observation surface independently demonstrated; avoid running remaining wrong-surface captures. Not a timeout restart.',
        correctedRenderer='Use video_manager snapshot_pixels, the same create_snapshot_bitmap path as reference PNGs; fresh3573/3574/3575 evidence only.',
        failedRawSurfaceSourceOrCaptureEdited=False, rawPixelsOrImagesWritten=0,
        gameChanged=False, fullPortAcceptance=False, inputHashes=pins)
    OUT.mkdir()
    path = OUT / 'report.json'
    path.write_text(json.dumps(value, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless rejected-probe record')
    print(json.dumps({k: v for k, v in value.items() if k != 'inputHashes'}, indent=2))


if __name__ == '__main__':
    main()
