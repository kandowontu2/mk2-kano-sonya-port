"""Same full morph/source-sound contract on three distinct remaining routes.

No physical/source/audio equation changes. Rebind only exact captured native
identity, actual move/player slot, output path and fault-record slot labels.
Completed P1 Kano is not replayed or relabelled as a remaining-slot instance.
"""
import inspect
import json
from pathlib import Path
import qualify_native_selector_morph_startup_return as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
REPORTS = {}


def bindings(c):
    move, side = c['move'], c['side']
    need((move,side) in (('square',1),('ball',2),('square',2)), 'Only three distinct uncompleted actual routes')
    process = json.loads((c['folder']/'process.json').read_text())
    identity = process['actualWindowsIdentity']
    need(identity == c['terminal']['actualWindowsIdentity'] and
         identity['ProcessId'] == c['process'].pid and identity['ParentProcessId'] == 38752 and
         Path(identity['ExecutablePath']).resolve() == (ROOT/'diagnostic_native_selector_layers_long/mkport_candidate.exe').resolve() and
         identity['CommandLine'] == previous.capture.original.original.subprocess.list2cmdline(process['command']),
         'Exact first live Win32 identity/full command and original retained Popen, not a guessed PID')
    source = inspect.getsource(previous.execute)
    def replace(before,after):
        nonlocal source
        need(source.count(before) == 1, 'Only declared full-contract context adaptation: '+before)
        source = source.replace(before,after,1)
    replace('(46572, 38752, 1791761737.394802)',
            "(expected_identity['ProcessId'],expected_identity['ParentProcessId'],expected_identity['createdUnix'])")
    replace("c['move'] == 'ball' and c['side'] == 1", "(c['move'],c['side']) == expected_route")
    replace("'Exact original terminal46572/latest initialized windows/retained Popen; no replay'",
            "'Exact original remaining-route terminal/current initialized windows/retained Popen; no replay'")
    need(source.count("r['slot'] == '1'") == 3, 'Exactly three original mutation target slot predicates')
    source = source.replace("r['slot'] == '1'", "r['slot'] == str(actual_side)")
    replace("print('Latest real Shang/Kano form, late Cannonball, native return and ordinary controls PASS', flush=True)",
            "print('Latest real Shang form '+c['move']+' P'+str(c['side'])+' late special/native return/ordinary controls PASS', flush=True)")
    replace('actualLatestP1KanoLateSpecialNativeReturnAccepted=True',
            "actualLatestFormLateSpecialNativeReturnAccepted=True,actualMove=c['move'],actualPlayerSlot=c['side']")
    out = ROOT/f'audit_native_selector_morph_startup_return_{move}_p{side}_checked'
    scope = dict(vars(previous), __file__=__file__, OUT=out, expected_identity=identity,
        expected_route=(move,side), actual_side=side)
    exec(compile(source,__file__+'::whole_original_contract_actual_remaining_route','exec'),scope)
    exec(compile(inspect.getsource(previous.safe_execute),__file__+'::unchanged_failure_preservation','exec'),scope)
    return scope


def execute(c):
    scope = bindings(c)
    report = scope['safe_execute'](c)
    REPORTS[c['move'],c['side']] = dict(report=report,path=scope['OUT']/'report.json')
    return report
