"""Whole current Pit movie model, then actual paid rejoin and native scanout.

All existing live movie/floor/stock-shadow/earned/fault predicates retained.
Separate later scanout never anchors that independent initial model. TOMB
record tags are an inherited transport protocol, not a Tomb-stage claim.
"""
import argparse
import code
import gzip
import inspect
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import run_native_current_cross_pit_render_checked as previous
import run_native_tomb_transition_scanout_checked as later

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
RAM={}
PREFIX='audit_native_pit_transition_rejoin'
once=previous.previous.prepared.original.once
LUA=tuple(ROOT/('mk2ks_native_pit_rejoin_'+name+'.lua')for name in
          ('provenance','display','timing_display','scanout_display'))


def paths(fighter,side):
    need(fighter in('kano','sonya')and side in(1,2),'Actual Pit character and physical slot')
    leaf=f'{PREFIX}_{fighter}_p{side}'
    return ROOT/(leaf+'_ram'),ROOT/(leaf+'_checked')


def clone(function,**changes):
    namespace=dict(function.__globals__,**changes)
    return FunctionType(function.__code__,namespace,function.__name__,function.__defaults__,function.__closure__)


def source_guard():
    need(not previous.previous.census.census(),'Never replace any actual native process')
    pins={}
    for name in('audit_native_current_cross_pit_render_matrix_checked',
                'audit_native_current_pit_19_four_owned_audio_checked',
                'audit_native_tomb_transition_matrix_checked'):
        path=ROOT/name/'report.json';proof=json.loads(path.read_text())
        need(proof['passed']and not proof['fullPortAcceptance'],'Whole finite original evidence, no port promotion')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and(p not in pins or pins[p]==h),'Exact frozen original source and native evidence '+p)
            pins[p]=h
        pins[str(path)]=sha(path)
    scope_path=ROOT/'audit_native_paired_stumble_table_bounded_source/report.json'
    scope=json.loads(scope_path.read_text())
    need(scope['passed']and len(scope['originalNaturalIntegrationRequirements'])==14 and
         len(scope['originalRemainingWorkGroups'])==6,'Full original objective retained')
    RAM['objective']=scope
    for p in(*LUA,Path(__file__).resolve()):
        text=p.read_text()
        if p.suffix=='.lua':need(not re.search(r':write_u\d+|\.value\s*=(?!=)|load_?state|snapshot\(',text),
                                 'Only passive observer targets change, no guest/register/raw-file writes')
        pins[str(p)]=sha(p)
    return pins


def functions(fighter,side):
    extension=source_guard()
    # Whole already executed corrected Pit factory, original namespaces intact.
    context=previous.functions()
    context.update(__file__=__file__,__doc__=__doc__,RAM=RAM,paths=paths)
    init=inspect.getsource(context['initialize'])
    init=once(init,"leaf = f'audit_native_current_cross_pit_globals_{fighter}_p{side}_render'",
                   "leaf = f'audit_native_pit_transition_rejoin_{fighter}_p{side}'")
    exec(compile(init,__file__+'::whole_original_initializer_only_fresh_paths','exec'),context)
    factory=inspect.getsource(context['functions'])
    factory=once(factory,'    return namespace',"    namespace['run'].source=body\n    return namespace")
    exec(compile(factory,__file__+'::whole_original_Pit_factory_body_export','exec'),context)
    current=context['initialize'](fighter,side)
    scope=context['functions'](current)
    body=scope['run'].source
    body=once(body,'    files.update(Path(p)for p in graphics_pins)',
        '    files.update(LUA)\n    files.update(Path(p)for p in extensionSourceHashes)\n'
        '    files.update(Path(p)for p in graphics_pins)')
    before="                if binary.startswith((b'MK2_TOMB_RAM_BUFFER ',b'MK2_TOMB_RAM_PIXELS ')):"
    body=once(body,before,
        "                if binary.startswith((b'MK2_TOMB_POST_BUFFER ',b'MK2_TOMB_POST_PIXELS ')):\n"
        "                    try:post_packet(binary,process.stdout,log)\n"
        "                    except Exception as error:\n"
        "                        if not errors:errors.append(dict(header=binary.decode('ascii').strip(),error=repr(error),traceback=traceback.format_exc()))\n"
        "                    continue\n"+before)
    body=once(body,"                    line=binary.decode('utf-8')",
        "                    line=binary.decode('utf-8')\n"
        "                    try:post_line(line)\n"
        "                    except Exception as error:\n"
        "                        if not errors:errors.append(dict(line=line.strip(),error=repr(error),traceback=traceback.format_exc()))")
    body=once(body,"    stderr=(CASE/'stderr.log').read_text()",
        "    stderr=(CASE/'stderr.log').read_text()\n"
        "    (CASE/'post_scene_records.json').write_text(json.dumps(RAM['post_records'],indent=2)+'\\n')\n"
        "    (CASE/'post_buffer_digests.json').write_text(json.dumps(RAM['post_transport'].records,indent=2)+'\\n')\n"
        "    (CASE/'post_state_records.json').write_text(json.dumps(RAM['post_states'],indent=2)+'\\n')")
    # All original scene/native movie and state fault gates, with ONLY the
    # actual terminal allowed later. Original paid controls must stay exact.
    contract=previous.previous.contract.scene_contract
    contract_body=inspect.getsource(contract)
    old=" need([s for s in log.splitlines()if s.startswith(physical)]==\n      [s for s in previous.splitlines()if s.startswith(physical)],\n      'Entire independent enabled-audio physical paid selection/health/KO/action/cleanup trajectory')"
    contract_body=once(contract_body,old,' physical_extension(log,previous,physical)')
    contract_scope=dict(contract.__globals__,physical_extension=later.physical_extension)
    exec(compile(contract_body,__file__+'::whole_movie_floor_shadow_faults_only_later_terminal','exec'),contract_scope)
    wrapper=inspect.getsource(previous.previous.scene_contract)
    wrapper=once(wrapper,'contract.scene_contract(scene, log, guest, payload, fighter, side, reference, ids)',
                        'whole_scene_contract(scene, log, guest, payload, fighter, side, reference, ids)')
    outer=dict(previous.previous.scene_contract.__globals__,whole_scene_contract=contract_scope['scene_contract'])
    exec(compile(wrapper,__file__+'::whole_current_live_scope_wrapper','exec'),outer)
    post_line=clone(later.post_line,RAM=RAM,_original_post_line=clone(later._original_post_line,RAM=RAM))
    binding=clone(later.timing_binding,RAM=RAM)
    post_packet=clone(later.post_packet,RAM=RAM,timing_binding=binding)
    model=scope['model']
    RAM.update(post_states=[],post_records=[],post_images={},post_raw={},post_timing={},post_failures=[],
               post_transport=model.Transport(),extensionSourceHashes=extension)
    # Freeze the whole original preflight's observer namespace. The new
    # passive observer is separately pinned; do not accidentally make the
    # old exact-wrapper guard inspect a different wrapper's source text.
    controls=clone(scope['controls'])
    preflight=clone(scope['preflight'],controls=controls)
    scope.update(OBSERVER=LUA[-1],LUA=LUA,extensionSourceHashes=extension,
                 controls=controls,preflight=preflight,post_line=post_line,
                 post_packet=post_packet,scene_contract=outer['scene_contract'])
    exec(compile(body,__file__+'::entire_original_Pit_pipeline_plus_actual_physical_rejoin','exec'),scope)
    return scope


def run(fighter,side):
    folder,output=paths(fighter,side)
    need(not folder.exists()and not output.exists(),'Fresh immutable full actual Pit continuation')
    try:
        scope=functions(fighter,side)
        base=scope['run'](fighter,side)
        base.update(currentPitAudioWaveformAccepted=False,historicalSoundReferenceIsPhysicalInputOnly=True,
                    originalPhaseGroundAndStockShadowContractSHA256=previous.previous.contract.CONTRACT_SOURCE_SHA256)
        RAM['base_report']=base
        (output.parent/(output.name+'_original_scene_report.json')).write_text(json.dumps(base,indent=2)+'\n')
        with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
        post=later.verify_rejoin(text,RAM['post_records'],RAM['post_states'],base['truePhysicalIDs'])
        post['actualSemanticFaultsRejected']=later.faults(text,RAM['post_records'],RAM['post_states'],base['truePhysicalIDs'])
        objective=RAM['objective']
        report=dict(base,laterNativeTransitionAndPhysicalRejoin=post,extensionSourceHashes=RAM['extensionSourceHashes'],
                    originalNaturalIntegrationRequirements=objective['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=objective['originalRemainingWorkGroups'],
                    inheritedTombProtocolTagsAreTransportOnly=True,goalStatus='active')
        RAM['report']=report
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                    fullPortAcceptance=False,goalStatus='active')
        print(json.dumps(report),flush=True)
    need(not output.exists(),'Never overwrite actual Pit continuation outcome')
    output.mkdir();(output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    if report['passed']:print(json.dumps(report['laterNativeTransitionAndPhysicalRejoin'],indent=2),flush=True)
    if RAM.get('images')or RAM.get('post_images'):
        RAM['review_images']=dict(RAM.get('images',{}));RAM['review_images'].update(RAM.get('post_images',{}))
        RAM['server']=previous.previous.review.start(RAM['review_images'],folder)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    run(args.fighter,args.side)
    code.interact(banner='Same original actual Pit continuation; bounded native RGB held only in RAM.',local=dict(RAM=RAM))
