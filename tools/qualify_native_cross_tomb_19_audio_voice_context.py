"""Keep actual captured sound; supply complete drop-voice/phase model context.

The whole original run remains intact except the missing live-report keys.
An offline entry checks the SAME terminal capture, never reboots a failed test.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
import prepare_native_cross_tomb_19_audio_manifest_checked as prepared
import run_native_cross_tomb_19_audio_remaining as remaining

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
RAM = {}


def functions(ram, offline=False):
    scope = prepared.functions()
    scope.update(RAM=ram, analysis_file=Path(__file__))
    body = inspect.getsource(prepared.original.run)
    body = prepared.original.once(body, 'audit_native_cross_tomb_19_audio_', prepared.PREFIX)
    body = prepared.original.once(body, 'sourceQualifiedNativeBranch=phase,sourceQualifiedNativeRandomBranch=phase,',
        "sourceQualifiedNativeBranch=phase,sourceQualifiedNativeRandomBranch=phase,\n"
        "        sourceQualifiedNativeLateVictimVoice=voice,actualLateVictimVoiceFaultsRejected=voice_faults,\n"
        "        actualRandomPhaseFaultsRejected=verification.phase_faults(text,guest,fighter,side)if phase['nativeDrop']else[],")
    body = prepared.original.once(body, 'RAM[\'report\']=report',
        "report['additionalAnalysisInputHashes']={str(analysis_file):sha(analysis_file)}\n"
        "    RAM['report']=report")
    if offline:
        first = body.index('    need(not census.census()')
        last = body.index('    with gzip.open', first)
        body = body[:first] + (
            "    current=context();captured=RAM['captured']\n"
            "    folder,headers,pcm,dac_chunks,dac_headers,rom_headers,buffers,expected=captured\n"
            "    guest=RAM['guest']\n"
            "    failure=folder/'current_19_audio_failure.json'\n"
            "    need(not(folder/'current_19_audio_report.json').exists()and failure.exists(),"
            "'Same terminal failure retained; never replace prior report')\n"
            "    failed=json.loads(failure.read_text())\n"
            "    need(not failed['passed']and failed['error']==\"KeyError('sourceQualifiedNativeLateVictimVoice')\","
            "'Exact observed missing drop-voice context failure')\n"
            "    meta=json.loads((folder/'result.json').read_text())\n"
            "    need(meta['exit_code']==0 and not census.census()and meta['fighter']==fighter and meta['side']==side and "
            "all(sha(p)==h for p,h in meta['input_hashes'].items()),'Same normal terminal, all actual inputs frozen')\n"
        ) + body[last:]
    exec(compile(body, __file__ + '::whole_current19_analysis_complete_drop_voice_context', 'exec'), scope)
    return scope


def qualify(ram, fighter, side):
    return functions(ram, offline=True)['run'](fighter, side)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fighter', choices=('kano', 'sonya'), required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    scope = functions(RAM)
    remaining.preflight(scope, args.fighter, args.side)
    try:
        scope['run'](args.fighter, args.side)
    except Exception as error:
        folder = RAM.get('folder', ROOT / f'{prepared.PREFIX}{args.fighter}_p{args.side}_samples')
        failure = folder / 'current_19_audio_failure.json'
        if folder.exists() and not failure.exists():
            failure.write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=traceback.format_exc(), fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    code.interact(banner='Same actual Tomb; complete current drop context, raw sound only in RAM.', local=dict(RAM=RAM))
