"""Whole native body/packed-stream/quarter-height shadow model on actual44988.

Real human Kano17 / CPU Sonya18, all independently expected live drawing
fields through KO/reset. Original geometry equations, projection cadence,
palette/pen/source row/clip/FIFO assertions are retained. No universal arena,
victim, artistic, audio, or finished-port claim.
"""
import hashlib
import inspect
import json
import re
import traceback
from collections import defaultdict
from pathlib import Path
import capture_native_selector_sonya_choice_shadow_bound_loader as capture
import qualify_native_selector_sonya_shadow_bound_faults_words as coverage
import qualify_native_selector_cpu_guard_body_shadow_syntax as template
import verify_special_shadow_v5141 as body

ROOT,need,sha=coverage.ROOT,coverage.need,coverage.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_geometry_checked'
PARENT=coverage.OUT/'report.json'


def coverage_bindings():
    prior=coverage.original.previous
    source=inspect.getsource(prior.execute)
    source=coverage.original.phases.original.phase_source.replace(source,"return scope['execute'](state)",'return scope')
    scope=dict(vars(prior))
    exec(compile(source,__file__+'::whole_current_draw_coverage_without_reexecuting_saved_report','exec'),scope)
    return scope['execute'](None)


def bindings(guest):
    observed=coverage_bindings()
    def state_gate(b,current_guest,payload):
        need(current_guest==guest,'Same full initialized current guest')
        coverage.original.phases.original.phase_source.source_gate(b['cpuLog'],guest)
        # Keep physical ledgers independent of the body rows under test. Rebind
        # ALL actual phase records to the unchanged coverage gate, not just the
        # subset the geometry collector happened to emit or a constant success.
        text='\n'.join(s for s in b['cpuLog'].splitlines() if not s.startswith('MK2_HPHASE_'))
        text+='\n'+'\n'.join(tag+' '+' '.join(k+'='+str(v) for k,v in r.items())
                              for tag,rows in b['rows'].items() for r in rows)
        result=observed['gate'](text,guest)
        return dict(actualDrawingCoverage=result,ids={1:17,2:18},floors={1:82,2:81},
                    physicalDrawCompleteFields=result['actualDrawingFields'],fullPortAcceptance=False)
    source=inspect.getsource(body.check)
    first=source.index(' # The older physical/ownership/health checker')
    last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
    source=coverage.original.phases.original.phase_source.replace(source,source[first:last],
        " state=state_gate(b,guest,payload)\n entry_frames={int(r['frame'])for r in rows['MK2_HPHASE_CPU_NATIVE_ENTRY']}\n")
    source=coverage.original.phases.original.phase_source.replace(source,'ids={side:identity,3-side:4}','ids={1:17,2:18}')
    namespace=dict(vars(body),state_gate=state_gate)
    exec(compile(source,__file__+'::whole_original_body_ROM_and_native_shadow_geometry_actual17_18','exec'),namespace)
    return namespace['check']


def execute(state):
    need(not OUT.exists(),'Fresh immutable whole native geometry qualification')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p)==h for p,h in pins.items()),'Entire previous1223 source/build/evidence inputs unchanged')
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    report=json.loads((folder/'result.json').read_text())
    need(held['process'].poll()==report['nativeExit']==0 and report['passed'] and held['identity']==parent['actualNativeIdentity']==report['nativeTerminal']['actualWindowsIdentity'],
         'Same original terminal44988 exact handle, no new game or state injection')
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_HPHASE_'):
            pairs=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(pairs)==len(dict(pairs)),'Every actual drawing record unambiguous')
            rows[line.split()[0]].append(dict(pairs))
    b=dict(move='bicycle',side=2,folder=folder,report_path=folder/'result.json',report=report,cpuLog=text,rows=rows,
           streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    # Keep the complete original source kernels unchanged; never reinterpret
    # altered geometry instructions as a compatible stock path.
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        a,z=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(state['guest'][a:z]==stock[a:z],'Whole original native shadow/body clipping kernel unchanged')
    OUT.mkdir()
    try:
        check=bindings(state['guest'])
        positive=check(b,state['guest'],state['payload'],state['gfx32'])
        print('Whole actual Kano/Sonya CPU body/shadow geometry positive PASS',flush=True)
        fault_runner=template.scope['current'].prior.shadow_faults
        faults=fault_runner(dict(b,report=dict(report,sourceBoundBodyShadowSemantics=positive)),state['guest'],state['payload'],state['gfx32'],check)
        need(len(faults)==11 and check(b,state['guest'],state['payload'],state['gfx32'])==positive,'Every original geometry/packed-stream fault and full positive restored')
        paths=(Path(__file__),PARENT,Path(coverage.__file__),Path(template.__file__),Path(body.__file__),
               ROOT/'tools/verify_move_phase_shadow_v5089.py',ROOT/'tools/capture_native_kano_laser_special_shadow.py',
               *(p for p in folder.rglob('*') if p.is_file()))
        for p in paths:
            key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No historical pin replacement');pins[key]=h
        need(all(sha(p)==h for p,h in pins.items()),'Fresh full source/build/native evidence census')
        value=dict(passed=True,actualNativeIdentity=held['identity'],wholeNativeBodyROMShadowCase=positive,
                   originalGeometryFaultsRejected=faults,inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
                   goalStatus='active',finiteCurrentPairBodyShadowGeometryAccepted=True,allCPUContextsArenasAccepted=False,
                   fullArtAudioAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
                   newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
        coverage.original.phases.original.capture.choices.current.prior.save(OUT/'report.json',value)
        print('PASS whole actual17/18 native body/packed ROM/shadow projection with11 original geometry faults',flush=True)
        return value
    except Exception as error:
        coverage.original.phases.original.capture.choices.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),actualNativeIdentity=held['identity'],inputHashes=pins,
            fullPortAcceptance=False,newNativeGames=0))
        raise
