"""Fresh whole ending capture after actual native context-schema correction.

Same read-only4613 hardware observer and complete native controls/pipeline.
Only parser module, source preflight and unused capture/report leaves change.
"""
import argparse,inspect,json,subprocess,traceback
import run_ending_display_latch_campaign_ram_v4617 as previous
import ending_display_ram_model_v4645 as model
import qualify_ending_display_latch_source_v4647 as source
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def collector(fighter):
    text=inspect.getsource(previous.collector)
    before='audit_v4622_{fighter}_p2_ending_display_latch_ram'
    need(text.count(before)==1,'Only fresh unused native capture leaf in complete collector')
    text=text.replace(before,'audit_v4649_{fighter}_p2_ending_display_actual_metadata_ram')
    #4617 dynamically compiles4540; its namespace must use the actual new
    #schema module and preflight rather than silently inherited old globals.
    before='scope=dict(vars(previous),source=source,model=model)'
    need(text.count(before)==1,'Exact generated full native capture source/model binding')
    scope=dict(vars(previous),__file__=__file__,source=source,model=model)
    exec(compile(text,__file__+'::whole4617_actual_native_metadata_collector','exec'),scope)
    return scope['collector'](fighter)

run_scope=dict(vars(previous.previous),collector=collector,source=source,model=model)
run_source=inspect.getsource(previous.previous.run)
before="lo,hi=int(start[0]['frame']),int(end[0]['frame'])+300"
need(run_source.count(before)==1,'One actual renderer versus subsequent terminal-notifier window boundary')
run_source=run_source.replace(before,"lo,hi=source.renderer_window(text,fighter)")
exec(compile(run_source,__file__+'::whole4540_native_ending_contract','exec'),run_scope)
original_run=run_scope['run']

def run(fighter):
    report=original_run(fighter)
    records=json.loads((ROOT/f'audit_v4649_{fighter}_p2_ending_display_actual_metadata_ram/ending_continuous_records.json').read_text())
    need(all('hardwareDerivedVisibleStart'in r and 'nativeDPYADR'in r for r in records),'Every whole native field independently hardware-bound')
    report.update(everyVisibleStartDerivedFromActualHardware=True,
      actualOriginalNativeLoggerContextValidatedEveryField=True,
      endingAttract=report['endingAttract']+1,naturalTerminal=report['naturalTerminal']+1,
      lastCompletedRendererField=report['naturalTerminal'],actualAttractRendererFields=300,
      requestedStartDiffersFromLatchedFields=[dict(frame=r['frame'],requested=r['requestedStart'],derived=r['hardwareDerivedVisibleStart'])
         for r in records if r['requestedStart']!=r['hardwareDerivedVisibleStart']],scope=__doc__)
    report['inputHashes'][str(__file__)]=sha(__file__)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4650_{args.fighter}_p2_ending_display_actual_metadata_checked'
    need(not out.exists(),'Fresh immutable actual native ending result')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
