"""All original CPU body/shadow/physical faults on the accepted Kano mirror only.

The cross trial naturally selected CPU Sonya and remains rejected. Never
attribute its incomplete/unsupported observations to CPU Kano acceptance.
"""
import inspect
import json
from pathlib import Path
import capture_native_kano_laser_cpu_choke_shadow as live
import capture_native_kano_laser_cpu_choke_approach as actual

ROOT,need,sha=live.ROOT,live.need,live.sha
OUT=ROOT/'audit_native_kano_laser_cpu_choke_approach_fault_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_choke_fault_initializer_source'


def verify(cases):
    need(not OUT.exists() and not live.base.identity.census(),'Fresh full checker-fault qualification; actual trials terminal')
    source_path=actual.BASE/'choke_cpu_kano_human_kano/result.json'
    positive=json.loads(source_path.read_text())
    rejected_path=actual.BASE/'choke_cpu_kano_human_sonya/result.json'
    rejected=json.loads(rejected_path.read_text())
    need(positive['passed'] and positive['nativeExit']==0 and not rejected['passed'] and rejected['nativeExit']==0,
         'Actual accepted mirror and preserved rejected cross terminal are distinct')
    report=dict(inputHashes=positive['inputHashes'],outputHashes={str(p.resolve()):sha(p)for p in source_path.parent.rglob('*')if p.is_file()},
                cases=[positive],candidate=positive['candidate'])
    for group in('inputHashes','outputHashes'):
        need(all(sha(p)==h for p,h in report[group].items()), 'Actual executed input/output evidence conserved')
    scope=dict(vars(live.base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(live.base.ui.expectation),__file__+'::whole_independent_guest_for_fault_checks','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,_,_,_=live.base.bindings(guest,build)
    pins=dict(report['inputHashes'])
    gfx32=live.base.reconstruct(native,pins)
    payload=(ROOT/live.base.audio.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    original_source=inspect.getsource(live.cpu_body.run)
    first=original_source.index(' faults=[]');last=original_source.index(' for p,h in b',first)
    block='\n'.join(line[1:]if line.startswith(' ')else line for line in original_source[first:last].splitlines())
    whole_faults='def original_faults(b,guest,payload,gfx,case,human):\n'+ \
                '\n'.join('    '+line for line in block.splitlines())+'\n    return faults,physical_faults\n'
    results=[]
    need(set(cases)=={'choke_cpu_kano_human_kano','choke_cpu_kano_human_sonya'},'Both original actual native captures')
    for human,positive in zip(('kano',),report['cases']):
        folder,text,images=cases[f'choke_cpu_kano_human_{human}']
        rows=live.base.defaultdict(list)
        for line in text.splitlines():
            if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
                rows[line.split()[0]].append(dict(live.base.re.findall(r'(\w+)=([^\s]+)',line)))
        b=dict(move='choke',side=2,human=human,cpuLog=text,folder=folder,report_path=folder/'result.json',
               report=positive,rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
        check=live.bindings(human)
        closure=dict(zip(check.__code__.co_freevars,(cell.cell_contents for cell in check.__closure__)))
        cpu=closure['original_check'].__globals__['cpu']
        case=check(b,guest,payload,gfx32)
        need(case==positive['sourceBoundBodyShadowSemantics'],'Exact original positive restored before actual faults')
        scope=dict(vars(live.cpu_body),check=check,cpu=cpu)
        exec(compile(whole_faults,__file__+'::entire_original_eleven_body_shadow_four_physical_faults','exec'),scope)
        shadow,physical=scope['original_faults'](b,guest,payload,gfx32,case,human)
        need(len(shadow)==11 and len(physical)==4,'All original fault mutations retained, none selected out')
        need(check(b,guest,payload,gfx32)==case,'Entire actual positive restored after all mutations')
        results.append(dict(human=human,case=case,actualBodyShadowFaultsRejected=shadow,actualPhysicalFaultsRejected=physical))
        print(f'CPU Kano versus {human}: all eleven body/shadow and four physical faults rejected',flush=True)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Executed sources still immutable')
    for p in(Path(__file__),source_path,rejected_path,actual.OUT/'failure.json',INIT/'report.json',Path(actual.__file__),Path(live.__file__)):
        pins[str(p.resolve())]=sha(p)
    value=dict(passed=True,candidate=report['candidate'],sourceReportSHA256=sha(source_path),cases=results,inputHashes=pins,
               actualFaultsRejected=15,actualPhysicalCPUChokeCases=1,wholeNativeHealthHistoryVerified=True,
               actualCPUKanoMirrorOnly=True,crossCPUSonyaTrialStillRejected=True,
               everyReadyOwnedBodyShadowFieldSourceBound=True,allCPUContextsAccepted=False,allArenasAccepted=False,
               fullVisualTimelineAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
               publicPlayableChanged=False,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();live.base.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,actualFaultsRejected=15,fullPortAcceptance=False)),flush=True)
    return value
