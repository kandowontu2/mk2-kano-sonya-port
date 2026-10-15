"""Fresh whole ending replay: hardware-derived view, original native controls.

All4540 native terminal/guest/state/graphics/RGB and bitmap fault gates kept.
No raw media writes, new build, game changes or full-port acceptance.
"""
import argparse,inspect,json,subprocess,traceback
import run_ending_display_campaign_ram_v4540 as previous
import qualify_ending_display_latch_source_v4616 as source
import ending_display_ram_model_v4612 as model
ROOT,need,sha,NAME=previous.ROOT,previous.need,previous.sha,previous.NAME

def collector(fighter):
    text=inspect.getsource(previous.collector)
    before='audit_v4547_{fighter}_p2_ending_display_ram'
    need(text.count(before)==1,'Only fresh unused capture leaf changes')
    text=text.replace(before,'audit_v4622_{fighter}_p2_ending_display_latch_ram')
    scope=dict(vars(previous),source=source,model=model)
    exec(compile(text,__file__+'::entire4540_native_RAM_collector','exec'),scope)
    return scope['collector'](fighter)

text=inspect.getsource(previous.run)
scope=dict(vars(previous),collector=collector,source=source,model=model)
exec(compile(text,__file__+'::entire4540_native_video_contract','exec'),scope)
original_run=scope['run']

def run(fighter):
    report=original_run(fighter)
    records=json.loads((ROOT/f'audit_v4622_{fighter}_p2_ending_display_latch_ram/ending_continuous_records.json').read_text())
    need(all('hardwareDerivedVisibleStart'in r and 'nativeDPYADR'in r for r in records),
         'Every consecutive whole native field hardware-bound before pixel comparison')
    report.update(everyVisibleStartDerivedFromActualHardware=True,
                  requestedStartDiffersFromLatchedFields=[dict(frame=r['frame'],requested=r['requestedStart'],derived=r['hardwareDerivedVisibleStart'])
                     for r in records if r['requestedStart']!=r['hardwareDerivedVisibleStart']],
                  scope=__doc__)
    report['inputHashes'][str(__file__)]=sha(__file__)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4623_{args.fighter}_p2_ending_display_latch_checked'
    need(not out.exists(),'Fresh immutable actual whole ending result')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,fighter=args.fighter,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
