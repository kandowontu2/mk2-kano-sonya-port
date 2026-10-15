"""Same live Sonya campaign: complete actual Mileena clear and HP prefix.

Preserve the whole independently qualified native Scorpion contract, changing
only observed opponent/window/inventory and successful-round expectations.
All earlier native/physical chronology must match the qualified predecessor.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import check_native_scorpion_guard_earned_clear as original
import prepare_native_mileena_guard_campaign as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_mileena_guard_earned_clear_checked'
START,NEXT=268421,304271
COUNTS=dict(LIVE=737,WIN=22,LOSS=9,HEALTH=4054,SPECIAL=74,GUARD_FIELD=20719,
    GUARD_DECISION=20719,SELECT=9,SELECT_ID=18,INPUT=35619,STATE=487)


def run():
    prior_path=ROOT/'audit_native_scorpion_guard_complete_inventory_checked/report.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed']and prior['finiteNativeSonyaScorpionClearAccepted']and
         prior['actualObservedNextStage']['frame']==str(START)and
         all(sha(p)==h for p,h in prior['inputHashes'].items()),
         'Entire earlier independently qualified nine fights and actual native Scorpion clear retained')
    prefix=SimpleNamespace(**vars(original.prefix_model))
    prefix.OLD=original.current.OUT
    prefix.TAGS=(*original.prefix_model.TAGS,'GUARD_FIELD','GUARD_DECISION')
    scope=dict(vars(original),__file__=__file__,OUT=OUT,START=START,NEXT=NEXT,
        COUNTS=COUNTS,current=current,prefix_model=prefix,prior_path=prior_path)
    fields=inspect.getsource(original.fields)
    fields=fields.replace("'9'","'10'")
    fields=original.native_health.once(fields,"q['cpu']=='10:10'","q['cpu']=='5:5'")
    fields=original.native_health.once(fields,"q['cpu_id']==q['cpu_roster']=='10'","q['cpu_id']==q['cpu_roster']=='5'")
    fields=original.native_health.once(fields,'identity=18 if side==1 else 10','identity=18 if side==1 else 5')
    fields=original.native_health.once(fields,'len(guard_by)==13127','len(guard_by)==20719')
    before="""    need([int(q['frame']) for q in own]==[266291,267912] and
         [q['health'] for q in own]==['48,0','46,0'] and
         all(int(q['frame'])>int(rows['LOSS'][-1]['frame']) for q in own),"""
    after="""    need([int(q['frame']) for q in own]==[282162,302375,303762] and
         [q['health'] for q in own]==['141,0','20,0','74,0'] and
         [int(q['frame']) for q in own if int(q['frame'])>int(rows['LOSS'][-1]['frame'])]==[302375,303762],"""
    fields=original.native_health.once(fields,before,after)
    fields=original.native_health.once(fields,
        "return dict(actualOwnedLegEntries=35,actualScorpionRoundWinnerCalls=14,ownSuccessfulRoundFrames=[266291,267912],\n        ownSuccessfulRoundHP=['48,0','46,0'],actualPaidScorpionContinues=6,completeGuardFields=13127,\n        completePhysicalDecisionFields=13127,completeScorpionInputEdges=21545,wholeNativeHealthPrefix=health)",
        "return dict(actualOwnedLegEntries=74,actualMileenaRoundWinnerCalls=22,ownSuccessfulRoundFrames=[302375,303762],\n        ownSuccessfulRoundHP=['20,0','74,0'],allOwnRoundFrames=[282162,302375,303762],allOwnRoundHP=['141,0','20,0','74,0'],\n        earlierOwnRoundInFailedAttemptNotCreditedAsSuccessfulMatch=True,actualPaidMileenaContinues=9,completeGuardFields=20719,\n        completePhysicalDecisionFields=20719,completeMileenaInputEdges=35619,wholeNativeHealthPrefix=health)")
    exec(compile(fields,__file__+'::whole_native_fields_contract_actual_Mileena','exec'),scope)
    body=inspect.getsource(original.run)
    for before,after in (
        ("next_stage=[q for q in stages if q['stage']=='10']","next_stage=[q for q in stages if q['stage']=='11']"),
        ("q['stage']=='10' and q['human']=='18:18' and q['cpu']=='5:5'",
         "q['stage']=='11' and q['human']=='18:18' and q['cpu']=='8:8'"),
        ('len(whole_hp)==26851','len(whole_hp)==30905'),
        ("'need(len(starts)==146,'","'need(len(starts)==168,'"),
        ("for p in (nine_path,kernel_path,source_path,proof_path,identity_path,pins_path,Path(__file__).resolve(),",
         "for p in (prior_path,Path(original_file),Path(current.__file__),nine_path,kernel_path,source_path,proof_path,identity_path,pins_path,Path(__file__).resolve(),"),
        ('finiteNativeSonyaScorpionClearAccepted=True','finiteNativeSonyaMileenaClearAccepted=True'),
    ):
        # The result and console use the same acceptance key, both changed.
        if before=='finiteNativeSonyaScorpionClearAccepted=True':
            need(body.count(before)==2,'Both finite result labels, not broader acceptance')
            body=body.replace(before,after)
        else:body=original.native_health.once(body,before,after)
    first=body.index("    trials=[('LIVE'")
    last=body.index('    faults=[]',first)
    body=body[:first]+"""    trials=[('LIVE',0,'human','1:1'),('LIVE',736,'cpu','5:1'),('GUARD_FIELD',0,'cpu_roster','18'),
        ('GUARD_FIELD',20718,'human_owner','01000000'),('SPECIAL',0,'pc','FFF00000'),('SPECIAL',73,'a8','01000000'),
        ('SPECIAL',0,'roster','1'),('WIN',20,'slot','2'),('WIN',21,'health','0,0'),('WIN',20,'frame','280000'),
        ('SELECT',0,'target','1'),('SELECT_ID',17,'state','1'),('GUARD_DECISION',0,'scope','forced_activation')]
"""+body[last:]
    scope['original_file']=original.__file__
    exec(compile(body,__file__+'::whole_native_clear_HP_and_fault_contract_actual_Mileena','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual finite native Mileena qualification failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        raise
