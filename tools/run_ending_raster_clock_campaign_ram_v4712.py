"""Fresh native ending/attract full one-base operation-clock RAM replay.

Whole4646/4540 controls/guest/source/pixels/VRAM/bit faults retained. Generic
native scanline clocks replace the static end-VRAM RGB assumption only.
No public build change or independent stock choreography/all-context claim.
"""
import argparse,inspect,json,subprocess,traceback
from pathlib import Path
import run_ending_display_latch_campaign_ram_v4646 as previous
import ending_raster_clock_model_v4709 as model
import qualify_ending_raster_clock_source_v4710 as source
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def collector(fighter):
    text=inspect.getsource(previous.collector)
    before='audit_v4649_{fighter}_p2_ending_display_actual_metadata_ram'
    need(text.count(before)==1,'Only fresh unused native capture leaf')
    text=text.replace(before,'audit_v4713_{fighter}_p2_ending_raster_clock_ram')
    scope=dict(vars(previous),__file__=__file__,source=source,model=model)
    exec(compile(text,__file__+'::whole4646_actual_raster_clock_collector','exec'),scope)
    return scope['collector'](fighter)

text=inspect.getsource(previous.run)
before='audit_v4649_{fighter}_p2_ending_display_actual_metadata_ram'
need(text.count(before)==1,'Full unchanged native run contract with fresh record leaf')
text=text.replace(before,'audit_v4713_{fighter}_p2_ending_raster_clock_ram')
scope=dict(vars(previous),collector=collector,source=source,model=model,original_run=previous.original_run)
# previous.original_run is already bound to its collector; rebind its whole
# actual source once, retaining the original corrected renderer window.
original=inspect.getsource(previous.previous.previous.run)
before="lo,hi=int(start[0]['frame']),int(end[0]['frame'])+300"
need(original.count(before)==1,'Whole4540 actual frame_done window role')
original=original.replace(before,'lo,hi=source.renderer_window(text,fighter)')
original_scope=dict(vars(previous.previous.previous),collector=collector,source=source,model=model)
exec(compile(original,__file__+'::whole4540_native_terminal_video_contract','exec'),original_scope)
scope['original_run']=original_scope['run']
exec(compile(text,__file__+'::whole4646_native_clock_video_contract','exec'),scope)
whole_run=scope['run']

def run(fighter):
    report=whole_run(fighter)
    records=json.loads((ROOT/f'audit_v4713_{fighter}_p2_ending_raster_clock_ram/ending_continuous_records.json').read_text())
    need(all(r['actualRasterClocks']>=2 and 'sourceTimedIndexedSHA256'in r for r in records),
         'Every full actual ending/attract field includes native notifier/finish clocks and source-timed indexed surface')
    report.update(everyRGBPixelUsesActualNativeOperationScanlineTiming=True,
                  actualRasterClocks=sum(r['actualRasterClocks']for r in records),scope=__doc__)
    report['inputHashes'][str(__file__)]=sha(__file__)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4714_{args.fighter}_p2_ending_raster_clock_checked'
    need(not out.exists(),'Fresh immutable actual raster video result')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
