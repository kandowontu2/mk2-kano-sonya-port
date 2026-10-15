"""Actual pair/stream corruptions on four fresh source-bound CPU matches.

No capture rewritten. Each mutation must change a real row and be rejected by
the relevant native phase or independent full state/health invariant.
"""
import json
import traceback
from pathlib import Path
import verify_native_extended_cpu_v2942 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT=model.ROOT
OUT=ROOT/'audit_v2945_native_extended_cpu_units'
need=model.need

def verify():
    path=model.OUT/'report.json';proof=json.loads(path.read_text())
    need(proof['passed'] and proof['threeActualSonyaMirrorPairsAccepted'] and not proof['fullPortAcceptance'],'Actual scoped accepted extended CPU evidence')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.assembly.sha(path)
    guest,old,_,_,_=model.assembly.expected()
    results=[]
    actual_logs={(ROOT/c['case']/'run.log').read_text(encoding='utf-8-sig')for c in proof['cases'].values()}
    def rejected(label,changed,callback,expected):
        need(changed not in actual_logs,'Nonvacuous actual mutation '+label)
        try:callback(changed)
        except ValueError as error:
            need(any(e in str(error)for e in expected),'Intended invariant rejection for '+label+': '+str(error))
            results.append(dict(name=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted corrupted actual evidence '+label)
    mirror=proof['cases']['new_sonya'];log=(ROOT/mirror['case']/'run.log').read_text(encoding='utf-8-sig')
    for base in mirror['selectedPairContracts']:
        cycle,start,release,own,victim=(base[k]for k in ('cycle','start','release','own_handoff','victim_handoff'))
        P='MK2_CPU_PAIR_'
        step=next(r for r in model.pair.rows(log,'EVENT')if r['cycle']==cycle and r['kind']=='step')
        dose=next(r for r in model.pair.rows(log,'EVENT')if r['cycle']==cycle and r['kind']=='damage')
        tests=[
            ('CPU proxy',P+'FIELD',{'frame':str(start+20)},'id','1','Stable published actual CPU/human roles'),
            ('wrong physical roles',P+'FIELD',{'frame':str(start+20)},'cpu_slot','1','Read-only observations and input-only natural scope'),
            ('wrong victim Main',P+'FIELD',{'frame':str(start+20)},'vowner','010350A0','Stable published actual CPU/human roles'),
            ('wrong held body',P+'FIELD',{'frame':str(start+20)},'pose','FE82AAA0','Every original leg paired pose'),
            ('wrong held victim',P+'FIELD',{'frame':str(start+20)},'vpose','FE82AAA0','Every original leg paired pose'),
            ('missing callback',P+'FIELD',{'frame':str(start+20)},None,None,'Every real paired callback field'),
            ('wrong own composite',P+'EVENT',{'frame':str(step['frame']),'kind':'step','cycle':str(cycle)},'group','FE82AAA0','Original five-phase/46-field leg choreography'),
            ('wrong leg dose',P+'EVENT',{'frame':str(dose['frame']),'kind':'damage','cycle':str(cycle)},'a10','00000022','Native 35-point leg damage'),
            ('wrong victim launch',P+'FIELD',{'frame':str(release+1)},'vvy','00000000','Actual original victim airborne continuation'),
            ('stale own lock',P+'OWN_REGAIN',{'frame':str(own)},'flags','00000010','Actual original ready handoff'),
            ('stale victim child',P+'VICTIM_REGAIN',{'frame':str(victim)},'vtrail','010350A0','Actual original ready handoff'),
            ('state assistance',P+'FIELD',{'frame':str(start+20)},'writes','1','Read-only observations and input-only natural scope'),
        ]
        def phase(changed):
            value=model.pair.verify_pair(changed,'sonya',cycle,guest)
            need(value['passed'],' | '.join(value['errors']))
        for label,tag,criteria,key,value,expected in tests:
            changed=mutate(log,tag,criteria,key,value)
            rejected(f'mirror cycle{cycle}: {label}',changed,phase,(expected,))
        need(model.pair.verify_pair(log,'sonya',cycle,guest)==base,'Final untouched actual mirror pair')
    for key,case in proof['cases'].items():
        log=(ROOT/case['case']/'run.log').read_text(encoding='utf-8-sig')
        image=guest if key.startswith('new')else old
        player=case['player']
        h,round_by=model.health_ledger(log,image,player)
        state=model.state_ledgers(log,image,player,round_by)
        first=h['first'];stores=model.rounds.rows(log,'HEALTH')
        store=next(r for r in stores if r['mode']==2 and r['before']>r['after'])
        flags=model.pair.flag_rows(log)
        flag=next(r for r in flags if r['frame']>=first and r['before']!=r['after'])
        def full(changed):
            _,round_rows=model.health_ledger(changed,image,player)
            model.state_ledgers(changed,image,player,round_rows)
        tests=[
            ('missing all-mode field','MK2_CPU_ROUND_FIELD',{'frame':str(first+10),'slot':'1'},None,None,'Every all-mode physical callback'),
            ('proxy all-mode ID','MK2_CPU_ROUND_FIELD',{'frame':str(first+10),'slot':'2'},'id','1','All live physical slots retain actual native owner/identity'),
            ('invalid live HP','MK2_CPU_ROUND_HEALTH',{'frame':str(store['frame']),'slot':str(store['slot']),'before':str(store['before'])},'after','65535','Only original mode7 fill sentinel'),
            ('wrong health opcode','MK2_CPU_ROUND_HEALTH',{'frame':str(store['frame']),'slot':str(store['slot']),'before':str(store['before'])},'op0','0000','Every actual health store instruction'),
            ('wrong physical health address','MK2_CPU_ROUND_HEALTH',{'frame':str(store['frame']),'slot':str(store['slot']),'before':str(store['before'])},'at','01060220','Physical original health writer'),
            ('unlogged health change','MK2_CPU_ROUND_FIELD',{'frame':str(first+10),'slot':'1'},'hp','160','Every all-mode callback agrees'),
            ('wrong state opcode','MK2_CPU_PAIR_FLAG',{'frame':str(flag['frame']),'slot':str(flag['slot']),'kind':flag['kind'],'before':f"{flag['before']:04X}"},'op0','0000','Every native state store matches'),
            ('wrong state target','MK2_CPU_PAIR_FLAG',{'frame':str(flag['frame']),'slot':str(flag['slot']),'kind':flag['kind'],'before':f"{flag['before']:04X}"},'at','01060220','Actual store targets'),
            ('wrong independent live action','MK2_CPU_PAIR_FIELD',{'frame':str(first+10)},'action','0','Independent all-mode and live'),
            ('missing live native field','MK2_CPU_PAIR_FIELD',{'frame':str(first+10)},None,None,'Every raw live'),
        ]
        # Missing live rows must be rejected by explicit cross-stream coverage,
        # not accidentally accepted by replaying only the surviving adjacent rows.
        for label,tag,criteria,column,value,expected in tests:
            changed=mutate(log,tag,criteria,column,value)
            if label=='missing live native field':
                # The current source-bound ledger does not yet demand every
                # mode2 row from the independent stream. Keep this as a strict
                # diagnostic: acceptance is a real verifier gap, not a pass.
                pass
            rejected(key+': '+label,changed,full,(expected,))
        need(model.health_ledger(log,image,player)[0]==h and model.state_ledgers(log,image,player,round_by)==state,'Final untouched full native streams')
    for file,wanted in pins.items():need(model.assembly.sha(file)==wanted,'Immutable actual unit-test dependency '+file)
    pins[str(Path(__file__).resolve())]=model.assembly.sha(__file__)
    return dict(passed=True,actualPhysicalFixtures=4,actualMirrorPairs=3,actualCounterexamplesRejected=len(results),counterexamples=results,
        originalPairPhaseInvariantsRetained=True,actualCapturesUnmodified=True,gameChanged=False,
        allCPUOrMorphsAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual CPU corruption evidence')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','counterexamples')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
