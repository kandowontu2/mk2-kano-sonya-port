"""Actual CPU Leg Grab startup hit, native hurt reaction and complete cleanup.

Full current cold source, all-mode physical health/state and genuine AI retained.
One actual human pressure run; finite interruption, not all move/arena/render/
audio contexts or physical-port-byte coverage. No synthetic execution events.
"""
import json
import re
import traceback
from pathlib import Path
import capture_native_selector_sonya_cpu_pressure_bound as capture
import qualify_native_selector_existing_sonya_travel_phases as phases

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_interrupt_checked'


def gate(text,guest):
    ledger=capture.base.choices.native_state
    phases.source_gate(text,guest)
    whole=ledger.gate(text,guest)
    choices=capture.base.choices.choices_gate(text,guest,whole['schedule'])
    pair=ledger.original.pair
    fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
    inputs=ledger.rows(text,'MK2_CPU_PAIR_PRESSURE_INPUT')
    need(len(inputs)==len(fields)==1075 and {int(r['frame'])for r in inputs}==set(by),
         'Every original live physical callback has exactly one actual pressure command')
    toward_count=punch_count=0
    for r in inputs:
        f=int(r['frame']);v=by[f];vx=v['vvx'] if v['vvx']<0x80000000 else v['vvx']-0x100000000
        clean=(v['vypos']==v['vfloor'] and v['vvy']==v['vgravity']==v['vtrail']==0 and
               v['vflags']&0x1c==0 and v['vbody']&0xc==0 and
               (vx==0 or v['vaction']==0x303 and abs(vx)<=0x30000))
        eligible=v['vhp']>0 and v['hp']>0 and clean
        gap=abs(v['x']-v['vxpos']);toward=eligible and gap>76;punch=eligible and (f-1818)%24<4
        need(r['policy']=='pressure_hp' and r['writes']=='0' and r['assistance']=='none' and
             tuple(int(r[k])for k in ('eligible','gap','toward','punch'))==(int(eligible),gap,int(toward),int(punch)),
             'Every human command derived from actual controllability/spacing and original physical cadence')
        toward_count+=toward;punch_count+=punch
    need(toward_count>0 and punch_count>0,'Actual distinct walk and punch pressure, not an unexercised case')
    start,hit,ready=1918,1925,1938
    entry=[r for r in pair.rows(text,'ENTRY')if r['frame']==start]
    need(len(entry)==1 and entry[0]['cycle']==1 and entry[0]['action']==0x303,
         'One actual natural Leg Grab entry from ordinary CPU readiness')
    actor,main=entry[0]['actor'],entry[0]['main']
    events=pair.rows(text,'EVENT')
    action=[r for r in events if r['cycle']==1 and r['frame']==start and r['kind']=='action']
    need(len(action)==1 and (action[0]['entry'],action[0]['pc'],action[0]['a8'],action[0]['a13'])==
         (0xfff80800,0xfff80810,actor,main),'Actual executing native Sonya Leg Grab entry and own registers')
    damage=[r for r in ledger.rows(text,'MK2_CPU_ROUND_HEALTH')if r['frame']==str(hit) and r['slot']=='2']
    need(len(damage)==1,'Exactly one actual incoming CPU health store at the interrupted startup')
    d=damage[0];human=by[hit]
    need((d['at'],d['before'],d['after'],d['pc'],d['a8'],d['a13'],d['mode'])==
         ('01060EC0','150','139','FF836700',f"{human['vactor']:08X}",f"{human['vmain']:08X}",'2'),
         'Eleven actual damage from real human Kano owner/Main through original native collision routine')
    flags=[r for r in pair.flag_rows(text)if r['slot']==2 and start<=r['frame']<=ready]
    expected=[(start,'action',0xff877bc0,0x303,0x110),(start,'body',0xff838cf0,0x12,0x16),
        (start,'flags',0xff877d50,0,0x10),(hit,'flags',0xff836030,0x10,0x14),
        (hit+1,'flags',0xff8d4f60,0x14,0x14),(hit+1,'body',0xff8d5060,0x16,0x12),
        (hit+1,'body',0xff837330,0x12,0x1a),
        (ready,'action',0xff83edd0,0x110,0),(ready,'body',0xff83eeb0,0x1a,0x12),
        (ready,'flags',0xff83efc0,0x14,0),(ready,'action',0xff83edd0,0,0),
        (ready,'body',0xff83eeb0,0x12,0x12),(ready,'flags',0xff83efc0,0,0),
        (ready,'action',0xff9065d0,0,0x303)]
    need([(r['frame'],r['kind'],r['pc'],r['before'],r['after'])for r in flags]==expected,
         'Every source-bound startup/hit/body replacement/cleanup/no-op/readiness store in exact original order')
    need(all((r['actor'],r['main'],r['id'],r['state'])==(actor,main,18,0)for r in flags),
         'Every native state store belongs to the same real CPU Sonya, including the human-authored hit flag')
    for f in range(start,ready+3):
        r=by[f]
        need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['state'])==(actor,main,actor,18,18,0) and
             r['y']==r['floor']==81 and r['vy']==r['gravity']==r['trail']==0,
             'All actual interrupted-move/hurt/cleanup callbacks retain own identity and native grounded state')
        if start<f<=hit:
            need((r['action'],r['flags']&0x1c,r['body']&0xc,r['hp'])==(0x110,0x10,4,150),
                 'Live own Leg Grab startup before genuine incoming hit')
        if hit+1<=f<=ready:
            need((r['action'],r['flags']&0x1c,r['hp'])==(0x110,0x14,139),
                 'Full native hurt interval after the actual hit, not relabeled as completed grab')
        if hit+2<=f<=ready:
            need(r['body']&0xc==8 and r['vx']==0,'Own hurt body replaces move body until native cleanup')
        if f>ready:
            need((r['action'],r['flags']&0x1c,r['body']&0xc,r['hp'])==(0x303,0,0,139),
                 'Return to ordinary native movement with no retained move/hurt locks')
    own=[r for r in ledger.original.overlap.rows(text,'EVENT')if
         r['kind']in ('ready','regain')and r['frame']==ready and r['a8']==actor and r['a13']==main]
    need([(r['kind'],r['entry'],r['pc'])for r in own]==
         [('ready',0xff861350,0xff861360),('regain',0xff861500,0xff861510)],
         'Actual original ready and regain execution, not inferred from a later frame')
    need(not any(r['cycle']==1 and start<=r['frame']<=ready and r['kind']in
         ('step','release','damage','fling','victim_regain')for r in events),
         'Interrupted before paired victim handoff; never accepted as a completed Leg Grab')
    kos=whole['wholeNativeHealthLedger']['earnedKOs']
    need([(r['frame'],r['slot'])for r in kos]==[(2324,1),(2942,1)],
         'Both genuine later human KOs accounted by the full original native health ledger')
    return dict(passed=True,wholeNativeStateHealth=whole,allActuallyObservedNativeChoices=choices,
        actualPressureCallbacks=len(inputs),towardCommands=toward_count,punchCommands=punch_count,
        interruptedMove='Sonya Leg Grab startup',start=start,incomingHit=hit,ready=ready,
        damage=11,sourceBoundStateStores=len(flags),nativeReadyRegainActuallyExecuted=True,
        completeFiniteInterruptionCleanupAccepted=True,allMoveInterruptionsAccepted=False,
        wholePhysicalPortBytesAccepted=False,wholeRenderingAudioAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual interruption qualification')
    parent=capture.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed'] and held['process'].poll()==proof['nativeExit']==0 and held['identity']==proof['actualNativeIdentity'] and
         held['identity']['ProcessId']==44780 and all(sha(p)==h for p,h in pins.items()),
         'Same original actual44780 terminal handle and every complete source/evidence input')
    text=capture.RAM_CASES[capture.KEY][1];positive=gate(text,state['guest']);faults=[]
    def change(tag,key,value,**where):
        line=next(l for l in text.splitlines()if l.startswith(tag+' ') and
             all(dict(re.findall(r'(\w+)=([^\s]+)',l)).get(k)==str(v)for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Effective actual incoming-hit/cleanup/input corruption')
        return text.replace(line,bad,1)
    first_input=capture.base.choices.native_state.rows(text,'MK2_CPU_PAIR_PRESSURE_INPUT')[0]
    false_punch='0' if first_input['punch']=='1' else '1'
    trials=[('pressure_false_punch',change('MK2_CPU_PAIR_PRESSURE_INPUT','punch',false_punch,frame=first_input['frame'])),
        ('pressure_false_gap',change('MK2_CPU_PAIR_PRESSURE_INPUT','gap','0',frame=1925)),
        ('hit_damage',change('MK2_CPU_ROUND_HEALTH','after','138',frame=1925,slot=2)),
        ('hit_attacker_proxy',change('MK2_CPU_ROUND_HEALTH','a8','01000000',frame=1925,slot=2)),
        ('hit_instruction',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=1925,slot=2)),
        ('move_source_entry',change('MK2_CPU_PAIR_EVENT','entry','FFF80900',frame=1918,kind='action')),
        ('hurt_source_body',change('MK2_CPU_PAIR_FLAG','after','0016',frame=1926,slot=2,pc='FF837330')),
        ('hurt_owner',change('MK2_CPU_PAIR_FIELD','owner','01000000',frame=1927)),
        ('cleanup_action',change('MK2_CPU_PAIR_FLAG','after','0110',frame=1938,slot=2,pc='FF83EDD0')),
        ('cleanup_flags',change('MK2_CPU_PAIR_FIELD','flags','00000010',frame=1939)),
        ('cleanup_body',change('MK2_CPU_PAIR_FIELD','body','00000016',frame=1939)),
        ('cleanup_floor',change('MK2_CPU_PAIR_FIELD','floor','80',frame=1939)),
        ('native_regain_entry',change('MK2_CPU_OVERLAP_EVENT','entry','FF861520',frame=1938,kind='regain'))]
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except(ValueError,AssertionError,KeyError,IndexError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual interruption counterexample admitted: '+label)
    need(gate(text,state['guest'])==positive,'Whole original positive restored after every effective fault')
    for p in (Path(__file__),parent,Path(capture.__file__),Path(phases.__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed sources/evidence');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every complete source/evidence pin freshly rehashed')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeCurrentPressureInterruption=positive,effectiveInterruptionFaultsRejected=faults,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        finiteCPUInterruptionRecoveryAccepted=True,allMoveArenaInterruptionsAccepted=False,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS genuine CPU Leg Grab interruption, full native cleanup and13 effective faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual interruption qualifier rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
