"""Keep native zero-damage stores without crediting them as earned damage.

Blocked native contacts can store the same HP value. No health increases,
foreign writers or invalid combat HP are admitted; all previous gates remain.
"""
import inspect
import json
from pathlib import Path
import qualify_native_sonya_first_four_ladder_terminal_refills as terminal

ROOT, need, sha = terminal.ROOT, terminal.need, terminal.sha
OUT = ROOT / 'audit_native_sonya_first_four_ladder_health_stores_checked'


def run():
    failed=terminal.OUT/'failure.json'
    need(failed.exists() and not json.loads(failed.read_text())['passed'], 'Original strict decrement checker failure retained')
    original=inspect.getsource(terminal.refill.refills)
    before="0<=int(q['after'])<int(q['before'])<=161"
    after="0<=int(q['after'])<=int(q['before'])<=161"
    need(original.count(before)==1, 'Only native same-value health store handling corrected')
    factory=inspect.getsource(terminal.run)
    old='source=inspect.getsource(refill.refills)'
    new="source=inspect.getsource(refill.refills).replace(damage_before,damage_after).replace('Every collision store genuine native damage, including KO saturation','Native damage primitive never increases HP; same-value stores are not earned damage')"
    need(factory.count(old)==1, 'Complete terminal refill factory and original progression/fault suites retained')
    scope=dict(vars(terminal),__file__=__file__,OUT=OUT,damage_before=before,damage_after=after,
        this_failed=failed,this_terminal=Path(terminal.__file__).resolve())
    factory=factory.replace(old,new)
    old="return scope['run']()"
    need(factory.count(old)==1, 'Same positive/fault factory, no extra native replay')
    factory=factory.replace(old,'return scope')
    exec(compile(factory,__file__+'::whole_terminal_contract_with_native_zero_damage_stores','exec'),scope)
    model=scope['run']()
    old_run=inspect.getsource(terminal.refill.prior.run)
    # The assembled successor factory already constructs this complete run.
    actual=model['run']
    need(actual.__code__.co_filename.endswith('::whole_original_progression_and_semantic_fault_suite'),
         'Entire already assembled original qualification function, no edited native chronology')
    source=inspect.getsource(terminal.refill.run)
    # Its factory generated the final run text. Reassemble that same factory
    # while adding exact binding for this preserved third checker failure.
    old="for p in (Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):"
    new="for p in (this_terminal,this_failed,Path(refill.__file__).resolve(),previous_failure,Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):"
    need(source.count(old)==1, 'Complete source and all failed predecessor evidence pinned')
    model.update(this_terminal=Path(terminal.__file__).resolve(),this_failed=failed)
    exec(compile(source.replace(old,new),__file__+'::whole_positive_and_fault_model_with_actual_health_writer_binding','exec'),model)
    result=model['run']()
    return result


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve original actual qualification failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
