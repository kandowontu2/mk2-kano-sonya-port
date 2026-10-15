"""Source-bound original post-KO throw floor, then whole owned body/shadow.

Preserve the rejected lifetime-constant-floor gate. A captured fling return
address and all launch registers bind the unchanged original eight-pixel
floor-lowering branch. The write itself was not tapped: causal attribution
is source inference, not a claimed observation of the floor-store opcode.
No geometry equation, clipping, sprite row or DMA cadence is weakened.
"""
import ast
import copy
import hashlib
import inspect
import json
import re
import traceback
from collections import defaultdict
from pathlib import Path
import qualify_native_selector_opposite_roles_geometry as rejected

capture,checkpoint,template=rejected.capture,rejected.checkpoint,rejected.template
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
body,current=rejected.body,rejected.current
OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_geometry_checked'
PARENT=checkpoint.OUT/'report.json'
FAILURE=rejected.OUT/'failure.json'
LO,HI=0xffa0dce0,0xffa0de70
BRANCH=bytes.fromhex('A0B50002E00BF7FF0DB00002E0090000FCFFC9093A00E1090000F4FFC2090060A31884701070B6000ECA280C0506687FF18C0')


def floor_gate(b,guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=(LO-0xff800000)//8,(HI-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi]==BRANCH,
         'Whole original read-floor/subtract-eight/store/launch/return branch')
    lo,hi=(0xffa0dc60-0xff800000)//8,(0xffa0dce0-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi]==bytes.fromhex('04B5F000641F01CBA64C460BCFFE19C3'),
         'Original facing test and unsigned distance threshold branch')
    text=b['cpuLog'];model=template.scope['model']
    fields=model.knife.R.rows(text,'FIELD')
    by={(r['frame'],r['slot']):r for r in fields}
    events=checkpoint.rows(text,'MK2_CPU_OVERLAP_EVENT')
    flings=[r for r in events if r['kind']=='fling' and r['a7']=='FFA0DE60']
    need(len(flings)==1,'One actual source-return-bound eight-pixel launch')
    r=flings[0];f=int(r['frame']);before=by[f,1];after=by[f+1,1]
    actual_owner=(int(r['a8'],16),int(r['a13'],16))
    need(f==2961 and actual_owner==(before['actor'],before['main'])==
         (after['actor'],after['main']) and r['main_owner']==r['a8'] and
         r['id']=='18' and before['id']==after['id']==18 and before['hp']==after['hp']==0 and
         r['entry']=='FF876650' and r['pc']=='FF876660' and r['writes']=='0' and
         r['assistance']=='none','Actual true Sonya victim/native fling/unchanged owner after real KO')
    need(int(r['a6'],16)<=0x130 and int(r['a4'],16)&16==0 and r['a5']==r['a6'] and
         all(r[k]==v for k,v in dict(a0='FFFC0000',a1='FFF40000',a2='00006000',
             a3='00000005',a7='FFA0DE60',a9='0000003A').items()) and
         r['action']=='050A' and before['action']==0x400 and after['action']==0x50a and
         int(r['yraw'],16)==before['y']<<16 and
         before['floor']==81 and int(r['floor'])==after['floor']==before['floor']-8,
         'Actual original near-throw branch condition/launch ABI and exact eight-pixel floor transition')
    valid=[q for q in fields if q['valid']==1 and q['owner']==q['actor'] and q['id']==(18 if q['slot']==1 else 17)]
    for q in valid:
        predicted=82 if q['slot']==2 else 81-(8 if q['frame']>f else 0)
        need(q['floor']==predicted,'Every independent owned Main floor follows exact source-bound throw timeline')
    return dict(passed=True,actualFling=r,preField=before,nextPreField=after,
        actualIndependentOwnedFields=len(valid),originalFloorLowering=8,
        unchangedBranchSHA256=hashlib.sha256(BRANCH).hexdigest().upper(),
        actualFloorStoreInstructionObserved=False,causalBranchAttributionIsSourceInference=True,
        restorationObserved=False,wholeCampaignFloorAcceptance=False)


def bindings(guest):
    node=next(n for n in ast.parse(template.source).body if isinstance(n,ast.FunctionDef) and n.name=='bindings')
    source=ast.get_source_segment(template.source,node)
    for before,after in [
        ('physical_cache[digest]=model.verify(text,guest)','physical_cache[digest]=checkpoint.gate(text,guest)'),
        ("a['id']==c['id']==17","a['id']==18 and c['id']==17"),
        ("int(r['roster'])==17","int(r['roster'])==(18 if s==1 else 17)"),
        ("owners={};floors={}","owners={};floors={};floor_proof=floor_gate(b,guest);floor_by_field={}"),
        ("int(r['floor'])==floors[s]==82",
         "int(r['floor'])==(82 if s==2 else 81-(floor_proof['originalFloorLowering'] if f>=int(floor_proof['actualFling']['frame']) else 0))"),
        ("            native=pair.get(f+1)","            floor_by_field[f,s]=int(r['floor'])\n            native=pair.get(f+1)"),
        ("owners=owners,floors=floors,ids={1:17,2:17}",
         "owners=owners,floors=floors,floorByDrawingField=floor_by_field,originalThrowFloor=floor_proof,ids={1:17,2:17}"),
        ("    namespace=dict(vars(body),state_gate=state_gate)",
         "    source=current.replace(source,\"num(t,'floor')==floors[s]\",\"num(t,'floor')==state['floorByDrawingField'][f,s]\")\n    namespace=dict(vars(body),state_gate=state_gate)")]:
        source=current.replace(source,before,after)
    need(source.count('ids={1:17,2:17}')==2,'Only actual state and body ID contexts')
    source=source.replace('ids={1:17,2:17}','ids={1:18,2:17}')
    scope=dict(template.scope,checkpoint=checkpoint,floor_gate=floor_gate,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_geometry_source_bound_throw_floor','exec'),scope)
    return scope['bindings'](guest)


def execute(state):
    need(not OUT.exists(),'Fresh immutable source-bound throw-floor geometry successor')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    failed=json.loads(FAILURE.read_text())
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    need(parent['passed'] and not failed['passed'] and meta['passed'] and
         held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         all(sha(p)==h for p,h in pins.items()),'Same original terminal38692/entire immutable parent and rejection')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_HPHASE_'):
            pairs=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(pairs)==len(dict(pairs)),'Every actual complete drawing record unambiguous')
            rows[line.split()[0]].append(dict(pairs))
    b=dict(move='knife',side=2,folder=folder,report_path=folder/'result.json',report=meta,cpuLog=text,rows=rows,
        streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(state['guest'][a:z]==stock[a:z],'Whole original native body/shadow kernels unchanged')
    check=bindings(state['guest']);positive=check(b,state['guest'],state['payload'],state['gfx32'])
    print('Whole original opposite-role geometry/source-bound throw floor positive PASS',flush=True)
    faults=current.prior.shadow_faults(dict(b,report=dict(meta,sourceBoundBodyShadowSemantics=positive)),
        state['guest'],state['payload'],state['gfx32'],check)
    extra=[]
    for label,tag,key,value in [
        ('Sonya_post_proxy','MK2_HPHASE_POST_FIELD','id','1'),
        ('post_pose','MK2_HPHASE_POST_FIELD','pose','00000000'),
        ('Sonya_floor_raised','MK2_HPHASE_POST_FIELD','floor','82'),
        ('Kano_CPU_entry_opcode','MK2_HPHASE_CPU_NATIVE_ENTRY','opcode','FFFF')]:
        changed=dict(b,rows=copy.copy(rows));changed['rows'][tag]=copy.deepcopy(rows[tag])
        need(changed['rows'][tag][0][key]!=value,'Effective actual post/entry corruption')
        changed['rows'][tag][0][key]=value
        try:check(changed,state['guest'],state['payload'],state['gfx32'])
        except (ValueError,AssertionError) as error:extra.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual opposite-role geometry corruption admitted '+label)
    floor_faults=[]
    event=positive['state']['originalThrowFloor']['actualFling']
    line=next(s for s in text.splitlines() if s.startswith('MK2_CPU_OVERLAP_EVENT ') and
        'frame=2961 ' in s and 'kind=fling ' in s)
    for key,value in [('a7','FFA0DFF0'),('a6','00000131'),('a0','00020000'),('floor','81'),('id','17')]:
        changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and changed!=line,'Effective actual original throw corruption')
        bad=dict(b,cpuLog=text.replace(line,changed,1))
        try:floor_gate(bad,state['guest'])
        except (ValueError,AssertionError) as error:floor_faults.append(dict(fault='actual_throw_'+key,rejectedBy=str(error)))
        else:raise ValueError('Actual throw-floor corruption admitted '+key)
    for pc in (0xffa0dcb0,0xffa0dd00,0xffa0dd20):
        bad=bytearray(state['guest']);index=(pc-0xff800000)//8;bad[index]^=1
        try:floor_gate(b,bytes(bad))
        except (ValueError,AssertionError) as error:floor_faults.append(dict(fault=f'original_throw_opcode_{pc:08X}',rejectedBy=str(error)))
        else:raise ValueError('Original throw opcode corruption admitted')
    need(len(faults)==11 and len(extra)==4 and len(floor_faults)==8 and
         check(b,state['guest'],state['payload'],state['gfx32'])==positive,
         'All original/additive23 faults rejected and whole exact positive restored')
    for path in (Path(__file__),PARENT,FAILURE,Path(rejected.__file__),Path(template.__file__),
        ROOT/'tools/qualify_native_selector_cpu_guard_body_shadow.py',Path(body.__file__),
        ROOT/'tools/verify_move_phase_shadow_v5089.py',ROOT/'tools/capture_native_kano_laser_special_shadow.py',
        ROOT/'mk2/mk2-maincpu.bin'):
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No historical source/evidence replaced');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Whole immutable source/evidence inventory after faults')
    value=dict(passed=True,actualNativeIdentity=held['identity'],wholeNativeBodyROMShadowCase=positive,
        originalGeometryFaultsRejected=faults,additionalOppositeRoleFaultsRejected=extra,
        originalThrowFloorFaultsRejected=floor_faults,inputHashes=pins,requirements=parent['requirements'],
        remainingGroups=parent['remainingGroups'],goalStatus='active',
        finiteOppositeRoleBodyShadowGeometryAccepted=True,actualFloorStoreInstructionObserved=False,
        causalBranchAttributionIsSourceInference=True,allCPUContextsArenasAccepted=False,
        allKnifeEffectsGeometryAccepted=False,fullArtAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    OUT.mkdir();current.prior.save(OUT/'report.json',value)
    print('PASS whole opposite-role body/ROM/shadow plus original throw-floor source with23 faults',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original successor rejection')
        OUT.mkdir();current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',newNativeGames=0,fullPortAcceptance=False))
        raise
