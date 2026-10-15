"""Whole native body/packed ROM/shadow geometry on actual opposite roles.

Original current CPU geometry gate, all native kernels and eleven original
faults retained. Change only actual role IDs/floor anchors and independent
physical ledger context, never geometry or clipping equations.
"""
import ast
import copy
import inspect
import json
import re
import traceback
from collections import defaultdict
from pathlib import Path
import capture_native_selector_sonya_human_kano_cpu as capture
import qualify_native_selector_opposite_roles_checkpoint as checkpoint
import qualify_native_selector_cpu_guard_body_shadow_syntax as template

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_opposite_roles_geometry_checked'
PARENT=checkpoint.OUT/'report.json'
body=template.scope['body']
current=template.scope['current']


def bindings(guest):
    node=next(n for n in ast.parse(template.source).body if isinstance(n,ast.FunctionDef) and n.name=='bindings')
    source=ast.get_source_segment(template.source,node)
    for before,after in [
        ('physical_cache[digest]=model.verify(text,guest)','physical_cache[digest]=checkpoint.gate(text,guest)'),
        ("a['id']==c['id']==17","a['id']==18 and c['id']==17"),
        ("int(r['roster'])==17","int(r['roster'])==(18 if s==1 else 17)"),
        ("int(r['floor'])==floors[s]==82","int(r['floor'])==floors[s]==(81 if s==1 else 82)")]:
        source=current.replace(source,before,after)
    need(source.count('ids={1:17,2:17}')==2,'Only actual state and geometry role ID contexts')
    source=source.replace('ids={1:17,2:17}','ids={1:18,2:17}')
    scope=dict(template.scope,checkpoint=checkpoint,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_CPU_geometry_actual_opposite_roles','exec'),scope)
    return scope['bindings'](guest)


def execute(state):
    need(not OUT.exists(),'Fresh immutable opposite-role geometry qualification')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    report=json.loads((folder/'result.json').read_text())
    need(parent['passed'] and report['passed'] and held['process'].poll()==report['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']==report['nativeTerminal']['actualWindowsIdentity'] and
         all(sha(p)==h for p,h in pins.items()),'Same original terminal38692 and whole1253 inputs')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_HPHASE_'):
            pairs=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(pairs)==len(dict(pairs)),'Every actual complete drawing record unambiguous')
            rows[line.split()[0]].append(dict(pairs))
    b=dict(move='knife',side=2,folder=folder,report_path=folder/'result.json',report=report,cpuLog=text,rows=rows,
           streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(state['guest'][a:z]==stock[a:z],'Whole original native body/shadow kernels unchanged')
    check=bindings(state['guest'])
    positive=check(b,state['guest'],state['payload'],state['gfx32'])
    print('Whole original opposite-role geometry positive PASS',flush=True)
    faults=current.prior.shadow_faults(dict(b,report=dict(report,sourceBoundBodyShadowSemantics=positive)),
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
    need(len(faults)==11 and len(extra)==4 and check(b,state['guest'],state['payload'],state['gfx32'])==positive,
         'All original/additive15 faults and whole positive restored')
    for path in (Path(__file__),PARENT,Path(template.__file__),ROOT/'tools/qualify_native_selector_cpu_guard_body_shadow.py',
                 Path(body.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py',ROOT/'tools/capture_native_kano_laser_special_shadow.py'):
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No historical source input replaced');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Whole immutable source/evidence inventory after faults')
    report=dict(passed=True,actualNativeIdentity=held['identity'],wholeNativeBodyROMShadowCase=positive,
        originalGeometryFaultsRejected=faults,additionalOppositeRoleFaultsRejected=extra,inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],goalStatus='active',
        finiteOppositeRoleBodyShadowGeometryAccepted=True,allCPUContextsArenasAccepted=False,
        allKnifeEffectsGeometryAccepted=False,fullArtAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    OUT.mkdir();current.prior.save(OUT/'report.json',report)
    print('PASS whole opposite-role body/packed ROM/shadow geometry with15 faults',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original geometry rejection')
        OUT.mkdir();current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',newNativeGames=0,fullPortAcceptance=False))
        raise
