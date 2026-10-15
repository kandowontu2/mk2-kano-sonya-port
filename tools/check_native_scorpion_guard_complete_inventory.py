"""Preserve the failed guessed STATE count; check all 320 actual records.

The whole original checker remains in force, including every native winner,
HP writer, continue input, preceding chronology and unchanged live identity.
No emulator/controller/guest changes and no new native boot.
"""
import inspect
import json
from pathlib import Path
import check_native_scorpion_guard_earned_clear as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_native_scorpion_guard_complete_inventory_checked'
COUNTS = dict(previous.COUNTS, STATE=320)


def run():
    failed_path = previous.OUT / 'failure.json'
    failed = json.loads(failed_path.read_text())
    need(not failed['passed'] and failed['error'] == "ValueError('Entire actual Scorpion-window inventory retained')",
         'Original complete-inventory failure preserved unchanged')
    scope = dict(vars(previous), __file__=__file__, OUT=OUT, COUNTS=COUNTS)
    exec(compile(inspect.getsource(previous.fields), __file__+'::entire_original_native_fields_gate', 'exec'), scope)
    source = inspect.getsource(previous.run)
    before = 'for p in (nine_path,kernel_path,source_path,proof_path,identity_path,pins_path,Path(__file__).resolve(),'
    after = 'for p in (failed_path,Path(previous.__file__).resolve(),nine_path,kernel_path,source_path,proof_path,identity_path,pins_path,Path(__file__).resolve(),'
    need(source.count(before) == 1, 'One exact original input-pin boundary')
    scope.update(failed_path=failed_path, previous=previous)
    exec(compile(source.replace(before, after), __file__+'::entire_original_native_scorpion_clear_gate', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual successor inventory check outcome')
        OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
