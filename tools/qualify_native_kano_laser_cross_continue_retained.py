"""Same terminal games: real Kano victim-thread choke ownership and pose fault.

Preserve the source-executed rejection of the previously Sonya-only paired
health predicate. Kano's original choke pulses execute on the held victim
Main, under action273/274 with its real paired CPU actor/Main and caller.
Keep all old ordinary, Sonya-pair and child ownership clauses unchanged.

The old pose fault chose the snapshot AT the native CSS exit, not a locked
selection pose. Test the first real confirmed pre-exit pose instead, while
retaining every original source-raster/erasure/correlation criterion.
No game/controller changes or terminal replays.
"""
import copy
import hashlib
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace,FunctionType
import capture_native_kano_laser_cross_continue as prior
import native_kano_laser_cross_continue_retained_scope as retained
import single_continue_origins_v6592 as origins
import verify_restart_pair as spec

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_cross_continue_retained_binding_checked'


def origin(q,enemy):
    if origins.origin(q,enemy):return True
    return (enemy['state']=='0'and enemy['owner']==enemy['actor']and enemy['id']==enemy['roster']=='17'and
        enemy['mode']=='2'and enemy['action']==str(spec.SPECS['kano']['state'])and
        q['mode']=='2'and q['state']=='1'and q['id']==q['ctxID']and q['owner']==q['actor']and
        q['a8']==q['actor']==q['ctxOwner']and q['a13']==q['main']and q['parent']=='00000000'and
        q['pairActor']==enemy['actor']and q['pairMain']==enemy['main']and
        q['pairAction']==enemy['action']and q['caller']=='FFF93470'and q['pc']=='FF836700'and q['mask']=='FFFF')


def prepare(scope):
    need(not OUT.exists()and not prior.native_base.identity.census(),'All four exact current native captures terminal; no replay')
    old=scope['contract'];guest=scope['guest']
    rows=old.rows;folder,text,images,report=scope['RAM_CASES']['sonya_p2_to_kano']
    need(report['passed']is False and report['nativeExit']==0 and
         report['error']=="ValueError('Actual native damage delivered by original CPU actor/Main, not another human or forced HP')"and
         all(sha(p)==h for p,h in report['inputHashes'].items()),'Exact immutable actual missing Kano paired-origin rejection')
    native_fields={(r['frame'],r['slot']):r for r in rows(text,'FIELD')}
    added=[]
    for q in rows(text,'HEALTH'):
        if q['pc']!='FF836700'or q['slot']!='2'or int(q['before'])<=int(q['after']):continue
        enemy=native_fields[q['frame'],'1'];victim=native_fields[q['frame'],'2']
        if not origins.origin(q,enemy):
            need(origin(q,enemy)and victim['action']==str(spec.SPECS['kano']['victim_state'])and
                 (q['actor'],q['main'],q['id'])==(victim['actor'],victim['main'],victim['id'])and
                 int(q['before'])-int(q['after'])==8 and q['after']==victim['hp'] and q['writes']=='0'and q['assistance']=='none',
                 'Each actual added origin is an eight-point native Kano pulse on the actual held owned victim; not unrelated damage')
            added.append(q)
    need(len(added)==12,'Exactly twelve genuinely observed missing paired Kano health records, not a permissive unknown-owner waiver')
    # Verify the original health writer against the actual current guest.
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();at=(0xff836700-48-0xff800000)//8
    need(guest[at:at+6]==original[at:at+6]and hashlib.sha256(guest).hexdigest().upper()==report['guestSHA256'],
         'Whole actual current guest proof and complete unchanged original native health-store instruction')
    base=FunctionType(old.base_gate.__code__,dict(old.base_gate.__globals__,origin=origin),'gate')
    flow=FunctionType(old._gate.__code__,dict(old._gate.__globals__,base_gate=base),'gate')
    gate=FunctionType(old.gate.__code__,dict(old.gate.__globals__,_gate=flow),'gate')
    dependencies=[*old.DEPENDENCIES,Path(__file__),Path(origins.__file__),Path(spec.__file__),
        ROOT/'audit_native_kano_laser_cross_continue_retained_scope_failure_sonya_p1/failure.json',
        ROOT/'audit_native_kano_laser_cross_continue_retained_scope_failure_sonya_p2/failure.json']
    new=SimpleNamespace(**(dict(vars(old))|dict(gate=gate,base_gate=base,_gate=flow,DEPENDENCIES=dependencies)))
    # The extra pixel fault must copy a real locked pose BEFORE native teardown.
    source=prior.pixels.source
    source=prior.replace(source,'audit_cross_continue_adaptive_checked_',prior.PREFIX+'_checked_')
    source=prior.replace(source,'audit_cross_continue_adaptive_pixels_',prior.PREFIX+'_pixels_')
    source=prior.replace(source,"locked=next(q for q in reversed(snaps)if q['scene']=='select'and int(q['age'])>=260)",
        "locked=next(q for q in snaps if q['scene']=='select'and int(q['age'])>=260 and int(q['frame'])<exit_at)")
    source=prior.replace(source,'except(ValueError,AssertionError,KeyError)as e:',
                        'except(ValueError,AssertionError)as e:')
    pixel_scope=dict(prior.pixels.scope,__file__=__file__,contract=new)
    exec(compile(source,__file__+'::whole_original_extra_pixel_suite_genuine_pre_exit_locked_pose','exec'),pixel_scope)
    scope['contract']=new
    qualify,_,control_check=prior.qualification(new)
    scope['qualify'],scope['pixel_check'],scope['control_check']=qualify,pixel_scope['check'],control_check
    positive=gate(text,'sonya',2,'kano');faults=[]
    actual=added[0];enemy=native_fields[actual['frame'],'1']
    for key,value in [('ctxOwner','00000000'),('parent',enemy['actor']),('ctxID','17'),('pairActor',actual['actor']),
                      ('pairMain',actual['main']),('pairAction','272'),('caller','FF835D70')]:
        line=next(s for s in text.splitlines()if s.startswith('MK2_SC_HEALTH ')and dict(re.findall(r'(\w+)=([^\s]+)',s))==actual)
        changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(changed!=line,'Every actual paired-origin semantic fault genuinely changes evidence')
        try:gate(text.replace(line,changed,1),'sonya',2,'kano')
        except(ValueError,AssertionError)as error:faults.append(dict(fault=key,rejectedBy=str(error)))
        else:raise ValueError('Actual false paired Kano ownership admitted: '+key)
    for key,value in [('action','0'),('id','18'),('owner','00000000')]:
        line=next(s for s in text.splitlines()if s.startswith('MK2_SC_FIELD ')and
                  dict(re.findall(r'(\w+)=([^\s]+)',s))==enemy)
        changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        try:gate(text.replace(line,changed,1),'sonya',2,'kano')
        except(ValueError,AssertionError)as error:faults.append(dict(fault='paired_CPU_'+key,rejectedBy=str(error)))
        else:raise ValueError('Actual false paired CPU field admitted: '+key)
    need(gate(text,'sonya',2,'kano')==positive,'Whole original positive restores after ten real origin/CPU semantic faults')
    for fighter,side,target in (('kano',1,'sonya'),('kano',2,'sonya'),('sonya',1,'kano')):
        prior_text=scope['RAM_CASES'][f'{fighter}_p{side}_to_{target}'][1]
        need(gate(prior_text,fighter,side,target)==old.gate(prior_text,fighter,side,target),
             'All three previously accepted actual routes retain exactly their entire original positive')
    pose_text=scope['RAM_CASES']['sonya_p1_to_kano'][1];snaps=new.model.records(pose_text,'SNAP')
    exit_at=int(new.model.records(pose_text,'EXIT')[0]['frame'])
    last=next(q for q in reversed(snaps)if q['scene']=='select'and int(q['age'])>=260)
    locked=next(q for q in snaps if q['scene']=='select'and int(q['age'])>=260 and int(q['frame'])<exit_at)
    need(int(last['frame'])==exit_at and int(locked['frame'])<exit_at,'Original false-negative copied CSS-exit image, corrected fault uses genuine confirmed pre-exit pose')
    pins=dict(report['inputHashes'])
    for p in (*dependencies,folder/'report.json',ROOT/'mk2/mk2-maincpu.bin'):
        pins[str(p.resolve())]=sha(p)
    OUT.mkdir();prior.native_base.save(OUT/'report.json',dict(passed=True,wholeOriginalControllerAndOtherOriginClausesConserved=True,
        actualAddedPairedKanoHealthStores=added,actualAdditionalOriginFaultsRejected=faults,
        correctedPoseFaultSource=locked,originalWrongPoseFaultSource=last,inputHashes=pins,
        originalRejectionsPreserved=True,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,goalStatus='active'))
    new.DEPENDENCIES.append(OUT/'report.json')
    print(json.dumps(dict(passed=True,actualNativeKanoPairedStores=12,originFaults=10,
                         correctedPoseFaultFrame=locked['frame'],nativeExit=exit_at,newNativeBoots=0)),flush=True)


def finish(scope):
    # Sonya P1 had passed full state/UI/control-positive capture, but pixel
    # qualification stopped on the erroneous negative before the control suite.
    for fighter,side in (('sonya',1),('sonya',2)):
        target='kano';key=f'{fighter}_p{side}_to_{target}';folder,text,images,report=scope['RAM_CASES'][key]
        if side==2:scope['qualify'](folder,text,images,report,fighter,side,target)
        scope['pixel_check'](folder,text,images,fighter,side,target)
        scope['control_check'](folder,text,fighter,side,target)
        scope['COMPLETED'].append(key)
    print(json.dumps(dict(passed=True,completedActualRoutes=scope['COMPLETED'],newNativeBoots=0)),flush=True)


def execute(scope):
    try:prepare(scope);finish(scope)
    except Exception as error:
        failure=ROOT/'audit_native_kano_laser_cross_continue_retained_qualification_failure'
        need(not failure.exists(),'Preserve exact retained-game successor failure');failure.mkdir()
        prior.native_base.save(failure/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
