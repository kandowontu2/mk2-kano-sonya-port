"""Entire six-fight proof; actual source-defined paid-continue pulse timing.

Preserve the initial wrong360/116/156-field checker assumptions. Original
controller uses Coin20..24/270..274, Start310..314; selection arrives314.
"""
import inspect
import json
from pathlib import Path
import qualify_native_sonya_first_six_ladder_fights as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_sonya_first_six_ladder_paid_controls_checked'


def run():
    failure=prior.OUT/'failure.json'
    need(failure.exists() and not json.loads(failure.read_text())['passed'], 'Original incorrect paid-control timing checker failure preserved')
    controller=ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    text=controller.read_text()
    need("if age>=20 and age<25 or age>=270 and age<275 then press('Coin')end" in text and
         "if age>=310 and age<315 then press('Start')end" in text,
         'Exact original whole physical controller defines genuine paid coin/start pulses')
    scope=dict(vars(prior),__file__=__file__,OUT=OUT)
    source=inspect.getsource(prior.fields)
    before="    selections=rows['SELECT'];confirmed=rows['SELECT_ID'];inputs=rows['INPUT']"
    need(source.count(before)==1,'Only source-defined physical pulse indexing added')
    source=source.replace(before,before+"\n    input_edges={(q['button'],int(q['frame'])) for q in inputs}")
    for before,after in (
        ("frame+360 for s in selections), 'Every earned loss followed by actual360-field physical continue selection'",
         "frame+314 for s in selections), 'Every earned loss followed by actual314-field native selection admission'"),
        ("for button,age in (('Coin_1',116),('1_Player_Start',156)):",
         "for button,age in [*[(\"Coin\",age) for age in (*range(20,25),*range(270,275))],*[(\"Start\",age) for age in range(310,315)]]:"),
        ("any(s['button']==button and int(s['frame'])==frame+age for s in inputs)","(button,frame+age) in input_edges")):
        need(source.count(before)==1,'Entire existing earned progress/state/health gate retained')
        source=source.replace(before,after)
    exec(compile(source,__file__+'::whole_six_fight_contract_with_actual_paid_controls','exec'),scope)
    source=inspect.getsource(prior.run)
    before="    trials += [('HEALTH',0,'pc','FF838860'),('SELECT_ID',0,'roster','1'),('SELECT_ID',147,'state','1')]"
    after=before+"\n    first_loss=int(rows['LOSS'][0]['frame'])\n    for button,age in (('Coin',20),('Coin',270),('Start',310)):\n        index=next(i for i,q in enumerate(rows['INPUT']) if q['button']==button and int(q['frame'])==first_loss+age)\n        trials.append(('INPUT',index,'button','High_Punch'))"
    need(source.count(before)==1,'All original semantic faults plus actual paid pulse omission faults')
    source=source.replace(before,after)
    before="for p in (preserved.OUT/'report.json',preserved.RETIRED/'report.json',source_kernel,Path(__file__).resolve()):"
    after="for p in (Path(prior.__file__).resolve(),failure,controller,preserved.OUT/'report.json',preserved.RETIRED/'report.json',source_kernel,Path(__file__).resolve()):"
    need(source.count(before)==1,'Original failed checker and exact source controls also frozen in final receipt')
    scope.update(prior=prior,failure=failure,controller=controller)
    exec(compile(source.replace(before,after),__file__+'::whole_original_positive_and_fault_suite','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual successor qualification failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
