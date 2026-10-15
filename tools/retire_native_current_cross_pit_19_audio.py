"""Original full DAC/ROM/PCM RAM retirement, current Pit19 and terminal faults.

No whole-port, in-scene voice/priority or broader victim acceptance inferred.
Invoke in the actual terminal interpreter; never replace or rerun its native.
"""
import gzip
import inspect
import json
from pathlib import Path
import retire_native_cross_tomb_19_audio_ram as original
import check_native_cross_tomb_19_audio_matrix as terminal
import run_native_current_cross_pit_19_audio as actual

need, sha = original.need, original.sha


def retire(ram):
    report = ram['report']
    need(report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and
         len(report['accepted']['actualAudioSourceWindowFaultsRejected']) == 29 and
         len(report['actualEarnedStateFaultsRejected']) == 12 and
         not report['cinematicVictimAudioOwnershipAccepted'] and
         not report['allNativePitCuePriorityAndRNGAccepted'],
         'Entire original current Pit window and faults, no unobserved voice/priority claim')
    folder = ram['folder']
    extra = folder / 'current_19_audio_terminal_faults.json'
    need(not extra.exists(), 'Fresh actual terminal fault receipt')
    with gzip.open(folder/'run.log.gz','rt') as reader:
        text = reader.read()
    positive, faults = terminal.terminal_faults(text)
    need(len(faults) == 8, 'All added-channel and five-priority-owner retirement faults reject')
    pins = {str(p.resolve()):sha(p) for p in
            (Path(__file__),Path(original.__file__),Path(terminal.__file__),Path(actual.__file__),
             actual.SOURCE/'report.json',folder/'current_19_audio_report.json',folder/'result.json',folder/'run.log.gz')}
    extra.write_text(json.dumps(dict(passed=True,actualNativeTerminalProof=positive,
                                    actualTerminalFaultsRejected=faults,inputHashes=pins,
                                    inSceneVoicePriorityAccepted=False,fullPortAcceptance=False),indent=2)+'\n')
    body = inspect.getsource(original.retire)
    body = actual.once(body,"report['currentCrossTomb19ChannelFiniteAudioAccepted']",
                       "report['currentCrossPit19ChannelFiniteAudioAccepted']")
    body = actual.once(body, 'Path(__file__), report_path, meta_path, identity_path,',
                       'Path(__file__), Path(original.__file__), Path(terminal.__file__), Path(actual.__file__), '
                       'actual.SOURCE/"report.json", extra, report_path, meta_path, identity_path,')
    body = actual.once(body, "    pins.update(report['mixedWaveformSourceInputHashes'])",
                       "    pins.update(report['mixedWaveformSourceInputHashes'])\n"
                       "    pins.update(report.get('additionalAnalysisInputHashes',{}))")
    scope = dict(vars(original),__file__=__file__,original=original,terminal=terminal,actual=actual,extra=extra)
    exec(compile(body,__file__+'::whole_original_current_Pit_19_sound_RAM_retirement','exec'),scope)
    return scope['retire'](ram)
