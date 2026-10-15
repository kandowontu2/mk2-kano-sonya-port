"""Preserve actual post-gate NameError; bind only its missing capture folder.

Qualify the SAME terminal RAM capture without new native boot or source edits.
The entire source-clock waveform/29 faults remain mandatory and are rerun.
"""
import hashlib
import inspect
import json
from pathlib import Path
import run_native_current_cross_pit_19_audio as original

ROOT, need, sha = original.ROOT, original.need, original.sha


def functions():
    body = inspect.getsource(original.functions)
    before = "faults_body = 'def check_faults(text,meta,live,fighter,side,guest,stock,expected):\\n'"
    after = "faults_body = 'def check_faults(text,meta,live,fighter,side,guest,stock,expected,folder):\\n'"
    body = original.once(body,before,after)
    namespace = dict(vars(original),__file__=__file__)
    exec(compile(body,__file__+'::whole_factory_only_missing_folder_argument','exec'),namespace)
    return namespace['functions']()


def qualify(ram):
    folder = ram['folder']
    failure_path = folder/'current_19_audio_failure.json'
    failed = json.loads(failure_path.read_text())
    need(not failed['passed'] and failed['error']=="NameError(\"name 'folder' is not defined\")",
         'Exact actual original post-gate reporting failure preserved')
    need(not(folder/'current_19_audio_report.json').exists(), 'Never overwrite an accepted audio report')
    meta = json.loads((folder/'result.json').read_text())
    need(meta['exit_code']==0 and not original.census.census() and
         hashlib.sha256(ram['guest']).hexdigest().upper()==meta['guestSHA256'] and
         all(sha(p)==h for p,h in meta['input_hashes'].items()),
         'Exact same normally terminal native/RAM/input context, not a replacement capture')
    scope = functions()
    body = inspect.getsource(original.run)
    start = body.index('    folder,headers,pcm,chunks,dac,rom,buffers,expected=captured')
    body = 'def qualify_same_capture(scope,ram):\n    captured=ram[\'captured\']\n    guest=ram[\'guest\']\n' + body[start:]
    before = "accepted=scope['check_faults'](text,meta,live,fighter,side,guest,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),expected)"
    body = original.once(body,before,before[:-1]+',folder)')
    body = original.once(body,"    RAM['report']=report",
        "    additional={str(p.resolve()):sha(p)for p in (Path(__file__),Path(original.__file__),failure_path,original.SOURCE/'report.json')}\n"
        "    need(all(sha(p)==h for p,h in additional.items()),'Original failure and exact successor context preserved')\n"
        "    report.update(additionalAnalysisInputHashes=additional,originalPostGateFailurePreserved=str(failure_path),newNativeBoots=0)\n"
        "    RAM['report']=report")
    namespace = dict(vars(original),__file__=__file__,RAM=ram,original=original,
                     failure_path=failure_path,fighter=meta['fighter'],side=meta['side'])
    exec(compile(body,__file__+'::entire_original_current19_audio_same_actual_RAM','exec'),namespace)
    return namespace['qualify_same_capture'](scope,ram)
