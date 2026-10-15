"""Whole actual walk/jump inputs, native health/state and genuine CPU choices."""
import json
import re
import traceback
from pathlib import Path
import capture_native_selector_sonya_cpu_air_approach_checked as capture
import qualify_native_selector_existing_sonya_travel_phases as source

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_control_checked'


def gate(text,guest):
    ledger=capture.previous.base.choices.native_state
    source.source_gate(text,guest)
    whole=ledger.gate(text,guest)
    choices=capture.previous.base.choices.choices_gate(text,guest,whole['schedule'])
    fields=ledger.original.pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    inputs=ledger.rows(text,'MK2_CPU_PAIR_AIR_INPUT')
    need(len(fields)==len(by)==len(inputs) and
         {int(r['frame']) for r in inputs}==set(by), 'Every actual live callback has one genuine air-approach command')
    toward_count=jump_count=0
    for row in inputs:
        f=int(row['frame']);r=by[f];vx=r['vvx'] if r['vvx']<0x80000000 else r['vvx']-0x100000000
        clean=(r['vypos']==r['vfloor'] and r['vvy']==r['vgravity']==r['vtrail']==0 and
               r['vflags']&0x1c==0 and r['vbody']&12==0 and
               (vx==0 or r['vaction']==0x303 and abs(vx)<=0x30000))
        eligible=r['vhp']>0 and r['hp']>0 and clean
        gap=abs(r['x']-r['vxpos']);toward=eligible and gap>90
        jumping=eligible and (f-1818)%84<8
        need(row['policy']=='air_approach' and row['writes']=='0' and row['assistance']=='none' and
             tuple(int(row[k]) for k in ('eligible','gap','toward','jumping'))==
             (int(eligible),gap,int(toward),int(jumping)),
             'Every human command derives from actual controllability/spacing and source-defined jump cadence')
        toward_count+=toward;jump_count+=jumping
    need(toward_count>0 and jump_count>0 and any(r['vypos']<r['vfloor'] for r in fields),
         'Actual walking and airborne human motion exercised, not an unexecuted input branch')
    bound=ledger.rows(text,'MK2_AIR_APPROACH_BIND')
    need(bound==[dict(count='1',controller='original_physical_P1',inputs='walk_periodic_jump',writes='0',assistance='none')],
         'Exactly one actual original physical movement controller')
    return dict(wholeNativeHealthState=whole,allActuallyObservedCPUChoices=choices,
        actualLiveInputCallbacks=len(inputs),towardCommands=toward_count,jumpCommands=jump_count,
        actualAirborneHumanCallbacks=sum(r['vypos']<r['vfloor'] for r in fields),
        allActualAirApproachCommandsSourceBound=True,wholePhysicalPortBytesAccepted=False,
        allBicycleContactsAccepted=False,allArenaContextsAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(), 'Fresh immutable actual airborne control/state proof')
    parent_path=capture.OUT/'report.json';proof=json.loads(parent_path.read_text())
    handle=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed'] and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
         'Same genuine new native terminal handle, not replayed')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Whole prior source/capture inventory intact')
    text=capture.RAM_CASES[capture.KEY][1];result=gate(text,state['guest']);faults=[]
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+str(value),line,count=1)
        need(n==1 and bad!=line, 'Effective actual command/state field corruption')
        return text.replace(line,bad,1)
    rows=capture.previous.base.choices.native_state.rows
    command=next(r for r in rows(text,'MK2_CPU_PAIR_AIR_INPUT') if r['jumping']=='1')
    dose=rows(text,'MK2_CPU_ROUND_HEALTH')[0]
    for label,bad in (
        ('actual_jump_command',change('MK2_CPU_PAIR_AIR_INPUT','jumping',0,frame=command['frame'])),
        ('actual_spacing_command',change('MK2_CPU_PAIR_AIR_INPUT','gap',-1,frame=command['frame'])),
        ('actual_controllability',change('MK2_CPU_PAIR_AIR_INPUT','eligible',0,frame=command['frame'])),
        ('actual_true_human_identity',change('MK2_CPU_PAIR_FIELD','vid',1,frame=command['frame'])),
        ('actual_true_cpu_identity',change('MK2_CPU_PAIR_FIELD','id',17,frame=command['frame'])),
        ('actual_native_health_instruction',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=dose['frame'],slot=dose['slot'])),
        ('actual_controller_duplicate',text+next(s+'\n' for s in text.splitlines() if s.startswith('MK2_AIR_APPROACH_BIND '))),
        ('actual_missing_live_command',text.replace(next(s+'\n' for s in text.splitlines() if
            s.startswith('MK2_CPU_PAIR_AIR_INPUT ') and 'frame='+command['frame']+' ' in s),'',1))):
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError,IndexError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective air-approach native counterexample accepted: '+label)
    need(len(faults)==8 and gate(text,state['guest'])==result, 'All8 effective control/state faults rejected and entire positive restored')
    for p in (Path(__file__),Path(source.__file__),parent_path):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h, 'No prior source/current evidence rewritten');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Entire source/native inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        actualAirApproach=result,effectiveFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        actualControlStateAndNativeChoicesAccepted=True,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual air-control proof failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
