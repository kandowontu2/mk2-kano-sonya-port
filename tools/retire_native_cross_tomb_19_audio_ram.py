"""Retire only a terminal, accepted actual Tomb capture after full RAM binding.

No game writes, process kills, audio files or source copies. Invoke inside the
original capture interpreter so original PCM/DAC/ROM are checked before release.
"""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(value).hexdigest().upper()


def sha(path):
    return digest(Path(path).read_bytes())


def retire(ram):
    folder, headers, pcm, chunks, dac, rom, buffers, expected = ram['captured']
    path = folder / 'current_19_audio_ram_retirement.json'
    need(not path.exists(), 'Never replace a retirement receipt')
    report_path = folder / 'current_19_audio_report.json'
    report = json.loads(report_path.read_text())
    meta_path = folder / 'result.json'
    meta = json.loads(meta_path.read_text())
    identity_path = folder / 'native_identity.json'
    identity = json.loads(identity_path.read_text())
    need(meta['exit_code'] == 0 and not census.census(),
         'Real normal native terminal and no replacement game')
    need(identity['ProcessId'] == json.loads((folder / 'process.json').read_text())['pid'],
         'Actual capture native identity retained')
    need(report == ram['report'] and report['passed'] and
         report['currentCrossTomb19ChannelFiniteAudioAccepted'] and
         not report['fullPortAcceptance'] and not report['fullStageArtAccepted'] and
         not report['allStageFinishersAccepted'], 'Exact original full bounded report')
    pins = dict(meta['input_hashes'])
    pins.update(report['mixedWaveformSourceInputHashes'])
    pins.update({str(p.resolve()): sha(p) for p in
                 (Path(__file__), report_path, meta_path, identity_path,
                  folder / 'run.log.gz', folder / 'stderr.log')})
    need(all(sha(p) == h for p, h in pins.items()), 'Every actual input remains frozen')
    need(digest(ram['guest']) == report['guestSHA256'] == meta['guestSHA256'] and
         len(ram['guest']) == 1048576, 'Original whole actual guest stays bound')
    need(headers == report['pcmHeaders'] and dac == report['dacHeaders'] and
         rom == report['soundROMHeaders'], 'All original native sound headers')
    need(pcm.shape == (len(headers) * 960, 2) and
         digest(pcm.tobytes()) == meta['mixedPCMSHA256'] ==
         report['waveform']['actualSHA256'] == report['waveform']['predictedSHA256'],
         'Original RAM PCM is the entire source-exact native capture')
    need(report['waveform']['passed'] and report['waveform']['differentChannelSamples'] == 0 and
         report['waveform']['actualMixedRawPCMByteFaultSuiteAccepted'] and
         len(report['waveform']['actualRawMixedPCMFaultsRejected']) == 4 and
         len(report['waveform']['actualMixedSourceOperationFaultsRejected']) == 4,
         'Complete source-clock PCM and operation faults were exercised')
    need(len(chunks) == len(dac) == len(headers) and
         all(digest(raw) == h['sha256'] for raw, h in zip(chunks, dac)),
         'Every original DAC callback remains intact')
    need(len(expected) == 12582912 and set(buffers) == {'startup', 'terminal'} and
         all(bytes(value) == expected for value in buffers.values()),
         'Both whole native sound-ROM observations remain source-exact')
    terminal = report['nativeTerminalChannels']
    pool = report['nativeTerminalOwnerPool']
    need(len(terminal) == 19 and {int(r['channel']) for r in terminal} == set(range(19)) and
         all(r['sample'] == '4294967295' for r in terminal) and len(pool) == 1 and
         pool[0]['actor'] == pool[0]['main'] == '00000000' and
         pool[0]['slots'] == '0000,0;0000,0;0000,0;0000,0;0000,0',
         'All channels and five sound-priority owners really retired')
    need(not list(folder.rglob('*.wav')) and not list(folder.rglob('*.png')) and
         not list(folder.rglob('guest*.bin')), 'No raw media or guest copies')
    proof = dict(passed=True, exactNativeTerminal=identity,
                 originalStereoFrames=len(pcm), originalDACCallbacks=len(chunks),
                 wholeSoundROMBytesPerPhase=len(expected), originalRAMBoundBeforeRelease=True,
                 all19ChannelsAndFivePriorityOwnersRetired=True, inputHashes=pins,
                 fullStageArtAccepted=False, allStageFinishersAccepted=False,
                 fullPortAcceptance=False, publicPlayableChanged=False, newRawMedia=0)
    ram.clear()
    need(not ram, 'Original capture dictionary cleared only after full terminal proof')
    proof['originalCaptureRAMDictionaryCleared'] = True
    path.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(dict(passed=True, retirement=str(path), stereoFrames=len(pcm),
                         fullPortAcceptance=False)), flush=True)
    return proof
