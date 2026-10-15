"""Whole original missed Bicycle lifecycle with operand-qualified x/vx writes.

Retain startup, all poses, native flags/actions, vertical gravity/ceiling,
fractional landing, true identity/health and cleanup. Horizontal predictions
use the actual complete source-operand journal, including ordinary edge clamps,
instead of the earlier incorrect assumption of constant unobstructed velocity.
Use actual independent native fall taps, never synthesize an execution event.
"""
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
from types import FunctionType
import qualify_native_selector_sonya_horizontal_operands_gateway as operands
import qualify_native_selector_existing_sonya_travel_phases as phases
import qualify_native_selector_existing_sonya_travel_phases_finish_boundary as boundary

ROOT,need,sha=operands.ROOT,operands.need,operands.sha
capture=operands.capture
OUT=ROOT/'audit_native_selector_sonya_bicycle_complete_journal_checked'


def cached_replay_binding():
    # The original pure parser scanned the entire log separately for each
    # horizontal store. Cache its exact rows only within this invocation;
    # all action ownership/value assertions and every horizontal rule remain.
    replay=operands.replay_binding()
    action=replay.__globals__['action_values']
    parser=action.__globals__['previous'].prior.phase_source.bicycle.state.original.flag_rows
    cache={}
    def flags(text):
        if text not in cache:cache[text]=parser(text)
        return cache[text]
    source=inspect.getsource(action)
    source=phases.replace(source,'previous.prior.phase_source.bicycle.state.original.flag_rows(text)',
                          'cached_flags(text)')
    scope=dict(action.__globals__,cached_flags=flags)
    exec(compile(source,__file__+'::same_action_checks_exact_pure_parser_cache','exec'),scope)
    namespace=dict(replay.__globals__,action_values=scope['action_values'])
    return FunctionType(replay.__code__,namespace,replay.__name__,replay.__defaults__)


operand_gate=FunctionType(operands.gate.__code__,dict(operands.gate.__globals__,
                         replay_binding=cached_replay_binding),operands.gate.__name__)


def journal(text,guest):
    qualified=operand_gate(text,guest)
    rows=[r for r in capture.base.choices.native_state.rows(text,'MK2_SONYA_HORIZONTAL_STORE')
          if r['slot']=='2' and 3191<=int(r['frame'])<=3252]
    values={k:int(rows[0][{'x':'xraw','vx':'vx'}[k]],16)for k in ('x','vx')}
    after={};index=0
    for frame in range(3191,3253):
        while index<len(rows) and int(rows[index]['frame'])==frame:
            r=rows[index];proof=qualified['completeSourceBoundOperandStores'][index]
            kind=r['kind'];bit=int(r['at'],16)-(0x010350a0+(0x80 if kind=='x'else 0x40))
            need(int(r['xraw'],16)==values['x'] and int(r['vx'],16)==values['vx'],
                 'One continuous journal seeded only by first independent native pre-store memory')
            mask=int(r['mask'],16);word=(int(proof['sourceValue'],16)>>proof['actualWordBit'])&mask
            need(word==int(r['data'],16),'Computed native store word independently operand-qualified')
            values[kind]=(values[kind]&~(mask<<bit))|(word<<bit)
            index+=1
        after[frame]=dict(values)
    need(index==310,'Every complete actual source write consumed exactly once')
    return qualified,after


def native_fall(text,start,end,actor,main):
    ledger=capture.base.choices.native_state
    rows=ledger.rows(text,'MK2_SONYA_NATIVE_FALL')
    own=[r for r in rows if r['kind']=='fall' and start<int(r['frame'])<=end]
    need(len(own)==1,'One actual source-native fall execution during this Bicycle')
    r=own[0]
    need(r['actor']==r['owner']==f'{actor:08X}' and r['main']==f'{main:08X}' and
         r['id']=='18' and r['action']=='0611' and r['mask']=='FFFF' and
         r['writes']=='0' and r['assistance']=='none',
         'Independent executing fall tap has true actor/Main ownership and full native read mask')
    need(int(r['opcode'],16)==struct.unpack_from('<H',native_fall.guest,
         (int(r['entry'],16)-0xff800000)//8)[0], 'Actual executing fall opcode source-exact')
    return {k:int(v,10 if k=='frame'else 16)for k,v in r.items()
            if k in ('frame','entry','pc','a0','a1','a2','a3','a6')}


def gate(text,guest):
    qualified,after=journal(text,guest)
    source=inspect.getsource(phases.bicycle.verify)
    replace=phases.replace
    source=replace(source,"pair=state.verify_log(log,'kano',guest)",
                   'pair=ledger.gate(log,guest);source_gate(log,guest)')
    # The current observer has seven genuine shared-code windows, not the
    # legacy Bicycle CODE window. Full independently derived cold guest and
    # all seven actual windows are still checked by source_gate unchanged.
    source=replace(source,"    assert any(r['start']==0xfff9a400 and r['stop']==0xfff9ad00 for r in codes)\n",'')
    source=replace(source,"assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'",
        "assert guest[a:b]==original[a:b] or ((lo,hi)==(0xff876650,0xff876b60) and adjacent_finish_operand(guest,original)), 'Exact native fall and full adjacent finisher operand'")
    source=replace(source,"    falls=[r for r in relevant if r['kind']=='fall'];assert len(falls)==1\n    fall=falls[0];split=fall['frame']",
        "    fall=native_fall(log,start,end,actor,main);split=fall['frame']")
    source=replace(source,"        assert b['xraw']==(a['xraw']+a['vx'])&0xffffffff and b['vx']==flight['vx']",
        "        assert (b['xraw'],b['vx'])==(after[a['frame']]['x'],after[a['frame']]['vx']), 'Complete source-operand horizontal journal, including edge clipping and separation'")
    source=replace(source,"assert regain['xraw']==(last['xraw']+last['vx'])&0xffffffff",
        "assert regain['xraw']==after[end]['x'], 'Source-operand horizontal journal at actual fractional landing'")
    native_fall.guest=guest
    scope=dict(phases.bicycle.verify.__globals__,ledger=capture.base.choices.native_state,
               source_gate=phases.source_gate,adjacent_finish_operand=boundary.adjacent_finish_operand,
               native_fall=native_fall,after=after)
    exec(compile(source,__file__+'::whole_original_Bicycle_lifecycle_source_operand_horizontal_model','exec'),scope)
    result=scope['verify'](text,guest)
    need((result['start'],result['fall'],result['ready'])==(3191,3210,3252),
         'Full original naturally selected Bicycle chronology unchanged')
    result.update(completeActualBicycleLifecycleAccepted=True,actualNativeFallTapAccepted=True,
                  sourceOperandHorizontalJournal=qualified,allContactsArenasAccepted=False)
    return result


def execute(state):
    need(not OUT.exists(),'Fresh complete lifecycle qualification')
    parent=operands.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed'] and held['process'].poll()==0 and held['identity']==proof['actualNativeIdentity'] and
         all(sha(p)==h for p,h in pins.items()),'Same original native42616 and every full evidence/source pin intact')
    text=capture.RAM_CASES[capture.KEY][1];positive=gate(text,state['guest']);faults=[]
    def change(tag,key,value,**where):
        line=next(l for l in text.splitlines()if l.startswith(tag+' ') and
             all(dict(re.findall(r'(\w+)=([^\s]+)',l)).get(k)==str(v)for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Effective real lifecycle corruption, no artificial event')
        return text.replace(line,bad,1)
    trials=[('intro_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=3192)),
            ('seek_y',change('MK2_CPU_PAIR_FIELD','yraw','00000000',frame=3200)),
            ('ceiling_gravity',change('MK2_CPU_PAIR_FIELD','gravity','0000A001',frame=3211)),
            ('fall_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=3233)),
            ('floor_fraction',change('MK2_CPU_PAIR_FIELD','yraw','00510000',frame=3253)),
            ('lock_cleanup',change('MK2_CPU_PAIR_FIELD','flags','00000010',frame=3253)),
            ('action_cleanup',change('MK2_CPU_PAIR_FIELD','action','0204',frame=3253)),
            ('fall_owner',change('MK2_SONYA_NATIVE_FALL','owner','01000000',frame=3210)),
            ('fall_opcode',change('MK2_SONYA_NATIVE_FALL','opcode','FFFF',frame=3210)),
            ('fall_parameters',change('MK2_SONYA_NATIVE_FALL','a2','00008000',frame=3210))]
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual lifecycle corruption admitted: '+label)
    need(gate(text,state['guest'])==positive,'Whole original complete lifecycle positive restored')
    for p in (Path(__file__),parent,Path(operands.__file__),Path(phases.__file__),
              Path(phases.bicycle.__file__),Path(boundary.__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every complete original pin after lifecycle counterexamples')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeCurrentBicycleLifecycle=positive,effectiveLifecycleFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        finiteBicycleLifecycleAccepted=True,wholeSavedDisplayAccepted=False,wholeSourceAudioAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS complete actual Bicycle miss/startup/ceiling/fall/fractional landing/cleanup with10 faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual complete lifecycle rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
