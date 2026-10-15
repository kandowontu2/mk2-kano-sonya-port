"""Whole original retirement; avoid module/local terminal-name collision.

Preserve the actual failed retirement and its already-passing eight terminal
faults. No sound/native rerun; all original RAM checks remain mandatory.
"""
import inspect
import json
import traceback
from pathlib import Path
import retire_native_current_cross_pit_19_audio as previous

need, sha = previous.need, previous.sha


def retire(ram, error):
    need(isinstance(error,UnboundLocalError) and
         "local variable 'terminal'"in str(error), 'Exact original module/local alias failure')
    folder=ram['folder']
    extra=folder/'current_19_audio_terminal_faults.json'
    terminal_proof=json.loads(extra.read_text())
    need(terminal_proof['passed'] and len(terminal_proof['actualTerminalFaultsRejected'])==8 and
         all(sha(p)==h for p,h in terminal_proof['inputHashes'].items()), 'Entire actual original terminal fault receipt retained')
    report=ram['report']
    need(report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and
         len(report['accepted']['actualAudioSourceWindowFaultsRejected'])==29 and
         len(report['actualEarnedStateFaultsRejected'])==12 and
         not report['cinematicVictimAudioOwnershipAccepted'] and
         not report['allNativePitCuePriorityAndRNGAccepted'], 'Same entire finite current Pit audio proof')
    failure_path=folder/'retirement_source_alias_failure.json'
    need(not failure_path.exists(), 'Preserve fresh actual retirement failure')
    failure_path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=''.join(traceback.format_exception(error)),
        originalTerminalFaultsAlreadyPassed=True,originalCaptureRAMStillRetained=True,newNativeBoots=0,
        inputHashes={str(Path(previous.__file__)):sha(previous.__file__),str(extra):sha(extra)},
        fullPortAcceptance=False),indent=2)+'\n')
    original,actual=previous.original,previous.actual
    body=inspect.getsource(original.retire)
    body=actual.once(body,"report['currentCrossTomb19ChannelFiniteAudioAccepted']",
                     "report['currentCrossPit19ChannelFiniteAudioAccepted']")
    body=actual.once(body,'Path(__file__), report_path, meta_path, identity_path,',
        'Path(__file__), Path(previous.__file__), Path(original.__file__), Path(previous.terminal.__file__), '
        'Path(actual.__file__), actual.SOURCE/"report.json", extra, failure_path, report_path, meta_path, identity_path,')
    body=actual.once(body,"    pins.update(report['mixedWaveformSourceInputHashes'])",
        "    pins.update(report['mixedWaveformSourceInputHashes'])\n"
        "    pins.update(report.get('additionalAnalysisInputHashes',{}))")
    scope=dict(vars(original),__file__=__file__,previous=previous,original=original,actual=actual,extra=extra,failure_path=failure_path)
    exec(compile(body,__file__+'::whole_original_RAM_retirement_with_unambiguous_source_module','exec'),scope)
    return scope['retire'](ram)
