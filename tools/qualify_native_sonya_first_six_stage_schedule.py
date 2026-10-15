"""Entire native six-fight/health/paid-control suite plus cold stage pointer.

The actual fault diagnosed a missing check on STAGE0's schedule field. Keep
every original positive/negative contract, add that check for every stage,
and bind the already executed original-reset initializer; no new game/probe.
"""
import inspect
import json
from pathlib import Path
import inspect_native_six_fight_fault_case as diagnostic

checked=diagnostic.checked
prior=checked.paid.prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_sonya_first_six_stage_schedule_checked'


def run():
    failure=checked.OUT/'failure.json'
    need(failure.exists() and not json.loads(failure.read_text())['passed'], 'Original semantic-fault admission failure retained')
    kernel_path=checked.INIT/'native_reset_kernel_report.json'
    kernel=json.loads(kernel_path.read_text())
    need(kernel['passed'] and kernel['sourceOnlyAccepted'] and kernel['proof']['wholeNativeResetAndDamageKernelsUnchanged'] and
         all(sha(p)==h for p,h in kernel['inputHashes'].items()), 'Already executed full-current-guest original reset/damage proof unchanged')
    scope=diagnostic.model()
    original_fields=scope['fields']
    def fields(rows):
        need(all(q['schedule']=='FFFA3000' for q in rows['STAGE']), 'Every actual stage, including the cold first stage, preserves native schedule')
        return original_fields(rows)
    extra=[Path(diagnostic.__file__).resolve(),Path(checked.__file__).resolve(),failure,Path(checked.paid.__file__).resolve(),checked.paid.OUT/'failure.json',
        Path(prior.__file__).resolve(),prior.OUT/'failure.json',kernel_path,checked.INIT/'report.json',Path(checked.original_initializer.__file__).resolve()]
    scope.update(__file__=__file__,OUT=OUT,fields=fields,extraPins=extra)
    source=inspect.getsource(prior.run)
    before="    trials += [('HEALTH',0,'pc','FF838860'),('SELECT_ID',0,'roster','1'),('SELECT_ID',147,'state','1')]"
    after=before+"\n    first_loss=int(rows['LOSS'][0]['frame'])\n    for button,age in (('Coin',20),('Coin',270),('Start',310)):\n        index=next(i for i,q in enumerate(rows['INPUT']) if q['button']==button and int(q['frame'])==first_loss+age)\n        trials.append(('INPUT',index,'button','High_Punch'))"
    need(source.count(before)==1, 'All original semantic faults and all actual paid-pulse faults retained')
    source=source.replace(before,after)
    before="for p in (preserved.OUT/'report.json',preserved.RETIRED/'report.json',source_kernel,Path(__file__).resolve()):"
    after="for p in (*extraPins,preserved.OUT/'report.json',preserved.RETIRED/'report.json',source_kernel,Path(__file__).resolve()):"
    need(source.count(before)==1,'Actual whole corrected contracts, cached source proof and all failed predecessors pinned')
    exec(compile(source.replace(before,after),__file__+'::whole_original_native_progression_and_fault_suite','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual cold-stage-schedule qualification outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
