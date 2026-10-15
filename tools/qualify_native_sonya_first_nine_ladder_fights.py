"""Full finite nine-fight chronology; final forced-stop loss is NOT a continue.

Reuse the entire first-six contract with explicit new inventory/opponents,
the verified absolute native HP-store interpretation, and source-defined
paid pulses. Do not credit Scorpion, endings, art, sound or whole campaign.
"""
import gzip
import hashlib
import inspect
import json
import re
from pathlib import Path
import retire_native_regular_guard_losing_scorpion as preserved
import qualify_native_sonya_first_six_ladder_fights as original
import qualify_native_sonya_first_six_global_reset as reset

ROOT, need, sha = original.ROOT, original.need, original.sha
FOLDER = preserved.capture.OUT
OUT = ROOT / 'audit_native_sonya_first_nine_ladder_fights_checked'
COUNTS = dict(LIVE=8587, STAGE=10, SELECT_ID=188, WIN=222, LOSS=94, HEALTH=39889,
              ROM=6, STATE=5186, SELECT=94, INPUT=386335, SPECIAL=883, CPU_ID=0)
OPPONENTS = (17,11,7,4,0,18,3,9,2,10)
OBSERVED_FINAL_FIELD = 391843


def once(text, before, after):
    need(text.count(before) == 1, 'Exactly one complete original contract boundary')
    return text.replace(before, after)


def contract(kernel):
    scope = dict(vars(original), __file__=__file__, FOLDER=FOLDER, OUT=OUT,
                 COUNTS=COUNTS, OPPONENTS=OPPONENTS, reset_kernel_proof=kernel,
                 OBSERVED_FINAL_FIELD=OBSERVED_FINAL_FIELD)
    health = inspect.getsource(original.health_history)
    health = once(health, "need(len(starts)==171,", "need(len(starts)==221,")
    health = once(health,
        "            need(all(0x01000000<=int(q[k],16)<0x01100000 for k in ('a8','a13')), 'Actual native health-writer actor/task context in RAM')",
        """            need(0x01000000<=int(q['a13'],16)<0x01100000, 'Actual native health writer task remains valid')
            if q['pc']==reset_pc:
                need(reset_kernel_proof['wholeNativeResetAndDamageKernelsUnchanged'] and index+1<len(chain) and
                     chain[index+1]['pc']==start_pc and int(chain[index+1]['frame'])==int(q['frame'])+1 and q['after']=='161',
                     'Original absolute global round-reset store immediately followed by complete native slot refill')
            else:
                need(0x01000000<=int(q['a8'],16)<0x01100000, 'Every combat/refill writer actual actor context remains in RAM')""")
    health = once(health, 'wholeObservedHPHistoryExplained=True)',
        'wholeObservedHPHistoryExplained=True,globalResetUsesAbsoluteNativeHealthStores=True,unusedGlobalResetA8NotClaimedAsActor=True)')
    exec(compile(health, __file__+'::entire_original_native_HP_history', 'exec'), scope)
    fields = inspect.getsource(original.fields)
    for before, after in (
        ("[:7]==OPPONENTS", "[:10]==OPPONENTS"),
        ("list(range(7)), 'Cold earned sequential ladder progression0..6'", "list(range(10)), 'Cold earned sequential ladder progression0..9'"),
        ("list(range(1,75))", "list(range(1,95))"),
        ("frame+360 for s in selections), 'Every earned loss followed by actual360-field physical continue selection'",
         "frame+314 for s in selections), 'Every continued earned loss followed by actual314-field native selection admission'"),
        ("for button,age in (('Coin_1',116),('1_Player_Start',156)):",
         "for button,age in [*[(\"Coin\",age) for age in (*range(20,25),*range(270,275))],*[(\"Start\",age) for age in range(310,315)]]:"),
        ("any(s['button']==button and int(s['frame'])==frame+age for s in inputs)", "(button,frame+age) in input_edges"),
        ("    need(sum(q['stage']=='6' for q in losses)>=47 and not any(q['stage']=='6' and q['slot']=='1' for q in wins), 'Failed Baraka policy never relabelled as earned seventh victory')",
         "    need(sum(q['stage']=='9' for q in losses)>=44 and not any(q['stage']=='9' and q['slot']=='1' for q in wins), 'Failed Scorpion policy never credited as earned tenth victory')"),
        ("verifiedCompletedOpponentIDs=list(OPPONENTS[:6]),verifiedCompletedOpponentNames=['Kano','Jax','Raiden','Kitana','Kung Lao','Sonya'],",
         "verifiedCompletedOpponentIDs=list(OPPONENTS[:9]),verifiedCompletedOpponentNames=['Kano','Jax','Raiden','Kitana','Kung Lao','Sonya','Baraka','Reptile','Cage'],"),
        ("reachedStage=6,failedOpponent='Baraka'", "reachedStage=9,failedOpponent='Scorpion'"),
        ("physicalInputEdges=len(inputs),physicalPaidLosses=len(losses),nativeHealth=health)",
         "physicalInputEdges=len(inputs),physicalPaidLosses=len(losses),completedPaidContinues=93,explicitStopUncontinuedLosses=1,actualObservedFinalField=OBSERVED_FINAL_FIELD,nativeHealth=health)")):
        fields = once(fields, before, after)
    fields = once(fields, "    selections=rows['SELECT'];confirmed=rows['SELECT_ID'];inputs=rows['INPUT']",
        "    selections=rows['SELECT'];confirmed=rows['SELECT_ID'];inputs=rows['INPUT']\n    input_edges={(q['button'],int(q['frame'])) for q in inputs}")
    fields = once(fields, "        frame=int(q['frame']);number=str(int(q['number'])+1)",
        """        frame=int(q['frame']);number=str(int(q['number'])+1)
        if q is losses[-1]:
            need(q['number']=='94' and q['stage']=='9' and frame==OBSERVED_FINAL_FIELD and
                 int(states[-1]['frame'])==frame and states[-1]['mode']=='3' and states[-1]['health']=='0,107' and
                 states[-1]['winner']=='2' and states[-1]['roster']=='18,10' and
                 states[-1]['actors']=='00000000,00000000' and
                 not any(s['number']==number for s in selections) and
                 not any(int(s['frame'])>=frame for s in inputs),
                 'Exact observed terminal loss preserved, no unobserved continuation or expected future fields credited')
            continue""")
    fields = once(fields, "    rom=rows['ROM'];need(len({q['order'] for q in rom})==6,'All six actual native schedule rows')",
        "    need(all(q['schedule']=='FFFA3000' for q in rows['STAGE']), 'Every stage including cold start binds exact native schedule')\n"+
        "    rom=rows['ROM'];need(len({q['order'] for q in rom})==6,'All six actual native schedule rows')")
    exec(compile(fields, __file__+'::entire_original_progression_contract_with_exact_nine_fight_inventory', 'exec'), scope)
    return scope['fields']


def run():
    need(not OUT.exists(), 'Fresh finite nine-fight qualification')
    saved_path = preserved.OUT / 'report.json'
    retired_path = preserved.RETIRED / 'report.json'
    six_path = ROOT / 'audit_native_sonya_first_six_stage_schedule_checked/report.json'
    kernel_path = reset.INIT / 'native_reset_kernel_report.json'
    saved, retired, six, kernel = [json.loads(p.read_text()) for p in (saved_path, retired_path, six_path, kernel_path)]
    proof = json.loads((FOLDER/'guest_memory_proof.json').read_text())
    result = json.loads((FOLDER/'result.json').read_text())
    terminal = json.loads((FOLDER/'native_terminal.json').read_text())
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and six['passed'] and
         six['finiteFirstSixLadderProgressionAccepted'] and kernel['passed'] and kernel['sourceOnlyAccepted'] and
         all(sha(p)==h for report in (saved,retired,six,kernel) for p,h in report['inputHashes'].items()) and
         proof['everyActualByteComparedInRAM'] and proof['bytes']==1048576 and
         proof['sha256']==kernel['proof']['wholeGuestSHA256']==result['guestSHA256'] and
         not result['passed'] and not result['nativeCacheOverrunObserved'] and terminal['nativeExit']==0xffffffff and
         not (FOLDER/'stderr.log').read_text().strip(),
         'Entire actual source/runtime guest, original native kernels and exact retired failed transport preserved')
    controller = ROOT / 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    source = controller.read_text()
    need("if age>=20 and age<25 or age>=270 and age<275 then press('Coin')end" in source and
         "if age>=310 and age<315 then press('Start')end" in source,
         'Full original paid-control pulse boundaries unchanged')
    text = gzip.open(FOLDER/'run.log.gz', 'rt', encoding='utf-8').read()
    need(not re.search(r'MK2_CURRENT_CAMPAIGN_CACHE_FAILURE |MK2_MILEENA_CAMPAIGN_OVERRUN |MK2_NAT_CAMPAIGN_ENDING_COMPLETED |MK2_POSTENDING_COMPLETE |LUA ERROR|stack traceback',text),
         'No observed corruption; ending/join absent and unaccepted')
    rows = {tag:[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
        if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')] for tag in COUNTS}
    fields = contract(kernel['proof'])
    positive = fields(rows)
    trials = []
    for stage in range(10):
        indices = [i for i,q in enumerate(rows['LIVE']) if q['stage']==str(stage)]
        for index in (indices[0],indices[len(indices)//2],indices[-1]):
            for key,value in (('human','1:1'),('cpu','18:1'),('human_main','00000000')):
                trials.append(('LIVE',index,key,value))
        trials.append(('STAGE',stage,'schedule','00000000'))
    trials += [('WIN',i,'slot','2') for i,q in enumerate(rows['WIN']) if q['slot']=='1']
    for pc in ('FF9DECE0','FF9DED10','FF9DEF40','FF9DEF70','FF825930','FF825960'):
        index = next(i for i,q in enumerate(rows['HEALTH']) if q['pc']==pc)
        trials.append(('HEALTH',index,'after','65534' if pc in ('FF9DECE0','FF9DED10') else '5'))
    trials += [('HEALTH',0,'pc','FF838860'),('SELECT_ID',0,'roster','1'),('SELECT_ID',187,'state','1'),
               ('LOSS',93,'frame',str(OBSERVED_FINAL_FIELD+1)),('STATE',5185,'health','161,107'),
               ('SELECT',93,'number','95')]
    first_loss = int(rows['LOSS'][0]['frame'])
    for button,age in (('Coin',20),('Coin',270),('Start',310)):
        index = next(i for i,q in enumerate(rows['INPUT']) if q['button']==button and int(q['frame'])==first_loss+age)
        trials.append(('INPUT',index,'button','High_Punch'))
    faults = []
    for tag,index,key,value in trials:
        bad = dict(rows); bad[tag] = list(rows[tag]); bad[tag][index] = dict(bad[tag][index], **{key:value})
        try: fields(bad)
        except (ValueError,IndexError,StopIteration) as error:
            faults.append(dict(tag=tag,row=index,field=key,rejectedBy=str(error)))
        else: raise ValueError('False native nine-fight evidence admitted')
    for tag,index in (('LIVE',0),('STAGE',3),('WIN',0),('HEALTH',0),('SELECT_ID',0),('INPUT',0),('LOSS',93)):
        bad = dict(rows); bad[tag] = rows[tag][:index]+rows[tag][index+1:]
        try: fields(bad)
        except ValueError as error: faults.append(dict(tag=tag,row=index,field='missing',rejectedBy=str(error)))
        else: raise ValueError('Omitted original nine-fight evidence admitted')
    need(fields(rows)==positive, 'Entire original chronology still passes after fault suite')
    pins = dict(saved['inputHashes'])
    for p in (saved_path,retired_path,six_path,kernel_path,controller,Path(__file__).resolve(),
              Path(original.__file__).resolve(),Path(reset.__file__).resolve()): pins[str(p)] = sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Every bound executed source and actual report still frozen after qualification')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(dict(passed=True,finiteFirstNineLadderProgressionAccepted=True,
        actualNativeGame=preserved.GAME,actualRAMParent=preserved.PARENT,accepted=positive,
        semanticFaultsRejected=faults,currentWholeGuestSHA256=proof['sha256'],
        completeChronologySHA256=hashlib.sha256(text.encode()).hexdigest().upper(),completeOriginalInventory=COUNTS,
        originalFailedCampaignTransportPreserved=True,fullTowerAccepted=False,endingAccepted=False,
        freshJoinAccepted=False,KanoCampaignAccepted=False,artAccepted=False,audioAccepted=False,
        allFinishersAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=saved['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=saved['originalRemainingWorkGroups'],inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteFirstNineLadderProgressionAccepted=True,accepted=positive,
                         semanticFaultsRejected=len(faults),fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(), 'Preserve original actual nine-fight checker outcome')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
