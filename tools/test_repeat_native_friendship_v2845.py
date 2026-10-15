"""Reject specific corruptions of actual repeated native Friendship evidence."""
import json, traceback
from pathlib import Path
import verify_repeat_native_friendship_v2841 as model

ROOT=model.ROOT
OUT=ROOT/'audit_v2846_repeat_native_friendship_units'

def run():
    pins={};outcomes=[]
    for side in (1,2):
        folder=ROOT/f'audit_v2840_repeat_native_friendship_p{side}'
        accepted=model.verify(folder)
        checked=ROOT/f'audit_v2842_repeat_native_friendship_p{side}_checked/report.json'
        saved=json.loads(checked.read_text())
        model.need(saved==accepted,'Actual independently reverified untouched positive control')
        pins.update(accepted['inputHashes']);pins[str(checked)]=model.assembly.sha(checked)
        rows=model.parse(folder/'run.log');control=model.replay(rows,side,3)
        def locate(tag,predicate):
            return next(i for i,(kind,r) in enumerate(rows) if kind==tag and predicate(r))
        def reject(name,index,changes,expected):
            corrupted=list(rows)
            if changes is None:corrupted.pop(index)
            else:corrupted[index]=(corrupted[index][0],dict(corrupted[index][1],**changes))
            model.need(corrupted!=rows,'Non-vacuous actual mutation '+name)
            try:model.replay(corrupted,side,3)
            except ValueError as error:
                model.need(expected in str(error),'Specific corruption rejected for intended invariant '+name+': '+str(error))
                outcomes.append(dict(side=side,name=name,rejectedBy=str(error)))
            else:raise ValueError('Actual corruption accepted '+name)
        for match in control['matches']:
            cycle=match['cycle'];belongs=lambda r:int(r.get('context',r['cycle']))==cycle
            ctor=locate('CONSTRUCT',belongs)
            release=locate('RELEASE_ENTRY',lambda r:model.frame(r)==match['nativePaletteRelease'] and model.ptr(r,'a8')==match['object'])
            decrement=locate('TABLE_STORE',lambda r:model.frame(r)==match['nativePaletteRelease'] and model.ptr(r,'a8')==match['object'] and model.ptr(r,'pc')==0xff80d710)
            selectid=locate('SELECT_ID',lambda r:belongs(r) and model.num(r,'slot')==side)
            damage=locate('DAMAGE',belongs)
            task=locate('ALLOC_TASK',belongs)
            phase=locate('PHASE',lambda r:belongs(r) and model.frame(r)==match['construction'])
            freed=locate('PHASE',lambda r:belongs(r) and model.frame(r)==match['taskReturn'])
            reused=locate('PHASE',lambda r:belongs(r) and model.frame(r)==match['spriteReuse'])
            firsttable=locate('CONSTRUCT_TABLE',belongs)
            table=rows[firsttable][1]['table'].split(',');components=table[match['paletteIndex']].split(':')
            components[0]='FFADBBD0';table[match['paletteIndex']]=':'.join(components)
            faults=(
                ('missing_native_release',release,None,'Actual original palette release'),
                ('missing_reference_decrement',decrement,None,'Every complete palette snapshot'),
                ('stock_proxy_palette',firsttable,{'table':','.join(table)},'Every complete palette snapshot'),
                ('wrong_child_cache',ctor,{'cache':'01060000'},'Original allocator supplies independent'),
                ('wrong_child_task_pid',task,{'taskID':'0'},'Original allocator supplies independent'),
                ('selected_wrong_fighter',selectid,{'actual':'1'},'Both actual native selections'),
                ('unearned_damage',damage,{'before':str(model.num(rows[damage][1],'before')-1)},'Native damage stores actually earn'),
                ('missing_child_field',phase,None,'Every actual child lifecycle field'),
                ('task_not_freed',freed,{'taskFree':'0'},'Actual child task reclaimed'),
                ('early_sprite_free',phase,{'objectFree':'1'},'Actual independent child sprite/cache'),
                ('lingering_reused_bubble',reused,{'objectCache':f'{match["task"]+0x100:08X}','objectPose':'FE9D2610'},'Actual native reuse replaces'),
                ('wrong_original_free_pool_terminator',phase,{'freeObjectsStop':'00000000'},'Continuous actual native child identity/list'),
            )
            for name,index,changes,expected in faults:
                reject(f'cycle{cycle}_{name}',index,changes,expected)
                if len(outcomes)%10==0:print('Actual corruption checks completed:',len(outcomes),flush=True)
        missingstate=locate('STATE',lambda r:model.frame(r)==100)
        reselect=locate('RESELECT',lambda r:model.num(r,'cycle')==2)
        terminal=locate('RESULT',lambda r:True)
        command=model.one(rows,'COMMAND',1);action=model.one(rows,'ACTION',1)
        button=locate('INPUT',lambda r:model.frame(r)==model.frame(action) and r['button']=='High_Kick' and model.num(r,'slot')==side)
        for name,index,changes,expected in (
            ('missing_consecutive_native_field',missingstate,None,'Every consecutive native field'),
            ('missing_natural_reselection',reselect,None,'Natural reselection'),
            ('wrong_terminal_completed_count',terminal,{'completed':'2'},'Actual uninterrupted terminal completed'),
            ('missing_actual_activation_button',button,None,'Actual physical Friendship command')):
            reject(name,index,changes,expected)
        model.need(model.replay(rows,side,3)==control,'Untouched final genuine repeated-match control')
    pins[str(Path(__file__).resolve())]=model.assembly.sha(__file__)
    for file,wanted in pins.items():model.need(model.assembly.sha(file)==wanted,'Actual source/capture files never changed '+file)
    model.need(len(outcomes)==80,'All eighty intended actual corruptions rejected')
    return dict(passed=True,candidate=model.assembly.NAME,actualOriginalCounterexamplesRejected=len(outcomes),
                actualCaptureFilesUnmodified=True,corruptions=outcomes,inputHashes=pins,fullPortAcceptance=False,
                scope='Only actual three-match palette/task/sprite/identity/input/damage/reselection evidence, both slots')

if __name__=='__main__':
    model.need(not OUT.exists(),'Immutable counterexample report')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','corruptions')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
