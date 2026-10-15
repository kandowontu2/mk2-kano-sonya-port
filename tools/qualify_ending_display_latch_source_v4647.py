"""Before boot: whole ending hardware pipeline against actual native schema.

Validate all emitted fields from the actual terminal failed-schema run;
never call metadata replay a whole RGB/VRAM/ending acceptance. All original
control/source/transport/hardware faults remain required and preserved.
"""
import copy,inspect,json,re,subprocess,sys
from pathlib import Path
import qualify_ending_display_latch_source_v4616 as previous
import ending_display_ram_model_v4645 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4648_ending_display_actual_metadata_source_checked'
OBSERVER,LUA,TRANSITIVE_LUA=previous.OBSERVER,previous.LUA,previous.TRANSITIVE_LUA
observer_source=previous.observer_source
scope=dict(previous.scope,model=model)
exec(compile(inspect.getsource(previous.previous.source_boundary),__file__+'::whole_original_physical_source_boundary','exec'),scope)
source_boundary=scope['source_boundary']

hardware_source=inspect.getsource(previous.hardware_control)
before="line='MK2_NAT_CAMPAIGN_FLOOR_SCANOUT epoch=1 '"
after="line='MK2_NAT_CAMPAIGN_FLOOR_SCANOUT human_slot=2 fighter=kano writes=0 assistance=none epoch=1 '"
need(hardware_source.count(before)==1,'One original actual hardware proof log-context binding')
hardware_source=hardware_source.replace(before,after,1)
hardware_scope=dict(vars(previous),model=model)
exec(compile(hardware_source,__file__+'::whole_actual41_hardware_fault_control','exec'),hardware_scope)
hardware_control=hardware_scope['hardware_control']

def renderer_window(text,fighter):
    # Native controllers stop during the next ordinary frame notifier, after
    # the preceding renderer frame_done. Keep all300 actual attract fields;
    # do not demand a render callback after the original process has exited.
    rows=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()
                    if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    begin,attract,terminal,finished=map(rows,('ENDING_START','ENDING_COMPLETED','RESULT','FLOOR_RESULT'))
    need(len(begin)==len(attract)==len(terminal)==len(finished)==1,'One actual native ending/attract/terminal/renderer-stop ledger')
    lo,returned,stop=int(begin[0]['frame']),int(attract[0]['frame']),int(terminal[0]['frame'])
    need(begin[0]['fighter']==fighter and stop==returned+300 and int(finished[0]['frame'])==stop and
         int(finished[0]['origin'])==lo,'Original unchanged native ending and300-field controller terminal scope')
    snaps=rows('FLOOR_SNAP');fields=[int(r['frame'])for r in snaps]
    need(fields==list(range(lo,stop))and int(finished[0]['snapshots'])==len(fields)and
         sum(frame>=returned for frame in fields)==300,
         'Every actual renderer callback through native stop: exactly300 attract fields, no post-exit callback fabricated')
    lines=text.splitlines()
    last=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and f'frame={stop-1} 'in line)
    ending=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_RESULT ')and f'frame={stop} 'in line)
    need(last<ending,'Actual last completed renderer field precedes original next-notifier terminal')
    return lo,stop-1

def actual_metadata_control():
    case=ROOT/'audit_v4622_kano_p2_ending_display_latch_ram'
    failed=ROOT/'audit_v4623_kano_p2_ending_display_latch_checked/report.json'
    need(failed.exists(),'Actual failed-schema run must reach its real terminal, never restart a live job')
    report=json.loads(failed.read_text());meta=json.loads((case/'result.json').read_text())
    need(not report['passed']and meta['exit_code']==0 and meta['exactContinuousEndingFields']==0 and
         len(meta['endingModelErrors'])==1 and 'Complete actual native hardware scanout metadata'in meta['endingModelErrors'][0]['error'],
         'Actual native terminal0 but whole renderer unaccepted at first real context-schema error')
    text=(case/'run.log').read_text()
    lo,hi=renderer_window(text,'kano')
    need((lo,hi)==(56296,59335),'Exact actual native frame_done window, not guessed terminal callback')
    lines=[line for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT ')]
    def contract(actual):
        need(len(actual)==3040,'All3040 actual ending and300 attract hardware/context fields')
        result=[]
        for frame,line in zip(range(lo,hi+1),actual,strict=True):
            tag,scan=model.parse(line);model.validate_context(scan,(13,17))
            display={k:scan[k]for k in ('epoch','frame','start','control','tap')}
            start=model.visible_start(scan,display,frame)
            need(tag=='FLOOR_SCANOUT'and scan['frame']==frame,'Every actual emitted hardware field remains consecutive')
            result.append((frame,start))
        return result
    positive=contract(lines);faults=[]
    first=lines[0]
    for label,changed in [('missing_actual_context',first.replace('assistance=none ','')),
                          ('wrong_physical_slot',first.replace('human_slot=2','human_slot=1')),
                          ('wrong_true_fighter',first.replace('fighter=kano','fighter=sonya')),
                          ('native_write_claim',first.replace('writes=0','writes=1')),
                          ('assisted_context',first.replace('assistance=none','assistance=state')),
                          ('duplicate_actual_key',first+' writes=0'),
                          ('unexpected_actual_key',first+' inferred_start=65532')]:
        need(changed!=first,'Actual non-vacuous hardware/context row fault')
        try:contract([changed]+lines[1:])
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual emitted metadata fault: '+label)
        need(contract(lines)==positive,'All3040 unchanged actual hardware/context positives restored after fault')
    need(model.Model.line.__globals__['parse']is model.parse and model.Model.snapshot.__globals__['validate_context']is model.validate_context,
         'Complete generated model actually uses native-schema and per-field true-context guards')
    phase=ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked/report.json'
    phase_proof=json.loads(phase.read_text())
    need(phase_proof['passed']and all(sha(p)==h for p,h in phase_proof['inputHashes'].items()),
         'Original frame_done before MACHINE_NOTIFY_FRAME source order and all phase proof inputs unchanged')
    driver=(ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua').read_text()
    need('emu.register_frame(function()\n frame=frame+1'in driver and
         'if ending_completed and frame-ending_completed>=300 then manager.machine:exit()end'in driver,
         'Actual unchanged native controller exits in next ordinary notifier, not the previous completed renderer callback')
    return dict(passed=True,actualTerminalNativeFields=3040,actualNativeContextFaultsRejected=faults,
      actualNativeStop=59336,actualLastCompletedRendererField=59335,actualAttractRendererFields=300,
      firstActualEmittedLine=first,delayedRequestedVsLatchedFields=sum(model.parse(line)[1]['start']!=start for line,(_,start)in zip(lines,positive)),
      wholeNativeEndingVideoAccepted=False),case,failed

def main():
    need(not OUT.exists(),'Fresh immutable actual-schema before-boot proof')
    contexts=[source_boundary(f)for f in LUA]
    metadata,case,failed=actual_metadata_control();hardware=hardware_control()
    original_path=previous.OUT/'report.json';original=json.loads(original_path.read_text())
    need(original['passed']and len(original['actualObserverSourceFaultsRejected'])==7 and
         all(sha(p)==h for p,h in original['inputHashes'].items()),
         'Entire original observer/control/actual hardware/source faults and qualified inputs unchanged')
    import run_ending_display_latch_campaign_ram_v4646 as capture
    for fighter in LUA:
        generated=capture.collector(fighter);names=generated.__code__.co_varnames
        need('errors'in names and 'scene_errors'in names,'Separate generated full native stderr and model failure locals')
        need(generated.__globals__['model']is model and
             Path(generated.__globals__['source'].__file__).resolve()==Path(__file__).resolve(),
             'Actual generated whole collector bound to corrected schema and fresh qualified source bytes')
    files={Path(__file__).resolve(),Path(model.__file__),Path(capture.__file__),Path(previous.__file__),original_path,failed}
    files.update(map(Path,original['inputHashes']))
    for p in case.rglob('*'):
        if p.is_file():files.add(p)
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path and Path(path).resolve().is_relative_to(ROOT/'tools'):files.add(Path(path).resolve())
    report=dict(passed=True,contexts=contexts,actualNativeMetadataControl=metadata,
      originalActualHardwareFaultControl=hardware,actualObserverSourceFaultsRetained=original['actualObserverSourceFaultsRejected'],
      originalRAMTransportControl=previous.previous.renderer.protocol_control(),
      generatedNativeStderrAndModelFailureLocalsDistinct=True,
      actualGeneratedFullModelAndCollectorSourceBindingChecked=True,
      nativeEndingVideoAcceptance=False,fullPortAcceptance=False,scope=__doc__,
      inputHashes={str(p.resolve()):sha(p)for p in files})
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
