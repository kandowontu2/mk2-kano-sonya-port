"""Full original native19 RAM retirement plus current movie/voice/RNG proof."""
import gzip
import inspect
import json
from pathlib import Path
import retire_native_cross_tomb_19_audio_ram as original
import check_native_cross_tomb_19_audio_matrix as terminal_checks
import run_native_current_cross_pit_19_owned_audio as actual

need,sha=original.need,original.sha


def retire(ram):
    folder=ram['folder'];report=ram['report']
    owned_path=folder/'current_19_owned_voice_queue_rng_report.json'
    owned=json.loads(owned_path.read_text())
    need(owned['passed'] and len(owned['actualOwnerFaultsRejected'])==22 and
         len(owned['wholeOriginalQueueRNG']['actualFaultsRejected'])==36 and
         owned['fullCurrent19WaveformAnd29FaultsRetained'] and
         report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and
         len(report['accepted']['actualAudioSourceWindowFaultsRejected'])==29 and
         len(report['actualEarnedStateFaultsRejected'])==12,
         'Entire actual19 waveform, movie/true-voice/direct-owner and whole original RNG/queue/fault contracts')
    need(all(sha(p)==h for p,h in owned['inputHashes'].items()), 'All actual owned-analysis inputs remain frozen')
    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
    positive,faults=terminal_checks.terminal_faults(text)
    need(len(faults)==8, 'All added-channel and five-priority-owner retirement faults reject')
    extra=folder/'current_19_audio_terminal_faults.json'
    need(not extra.exists(), 'Fresh native terminal fault receipt')
    extra.write_text(json.dumps(dict(passed=True,actualNativeTerminalProof=positive,
        actualTerminalFaultsRejected=faults,inputHashes={str(Path(terminal_checks.__file__)):sha(terminal_checks.__file__),
                                                      str(folder/'run.log.gz'):sha(folder/'run.log.gz')},
        fullPortAcceptance=False),indent=2)+'\n')
    body=inspect.getsource(original.retire)
    body=actual.once(body,"report['currentCrossTomb19ChannelFiniteAudioAccepted']",
                     "report['currentCrossPit19ChannelFiniteAudioAccepted']")
    body=actual.once(body,'Path(__file__), report_path, meta_path, identity_path,',
        'Path(__file__), Path(original.__file__), Path(terminal_checks.__file__), Path(actual.__file__), '
        'actual.SOURCE/"report.json", owned_path, extra, report_path, meta_path, identity_path,')
    body=actual.once(body,"    pins.update(report['mixedWaveformSourceInputHashes'])",
        "    pins.update(report['mixedWaveformSourceInputHashes'])\n    pins.update(owned['inputHashes'])")
    scope=dict(vars(original),__file__=__file__,original=original,terminal_checks=terminal_checks,actual=actual,
               owned=owned,owned_path=owned_path,extra=extra)
    exec(compile(body,__file__+'::whole_original_native19_owned_Pit_RAM_retirement','exec'),scope)
    return scope['retire'](ram)
