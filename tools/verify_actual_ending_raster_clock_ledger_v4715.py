"""Complete actual native timing/operation ledger and real metadata faults.

This deliberately verifies metadata, not fabricated pixel positives. The full
RAM pixel/VRAM replay and real bit faults are required separately from4714.
Only scanline sampling is removed from the whole timing state machine here;
no dummy VRAM or synthetic native image is used for clock qualification.
"""
import argparse,inspect,json,re,subprocess,textwrap,traceback
from pathlib import Path
import ending_raster_clock_model_v4709 as model
import qualify_ending_raster_clock_source_v4710 as source
ROOT,need,sha=source.ROOT,source.need,source.sha

advance=textwrap.dedent(inspect.getsource(model.Scanline.advance))
first="                columns=np.arange(400)\n"
last="                self.completed=count\n"
a,b=advance.index(first),advance.index(last)
need(advance.count(first)==advance.count(last)==1 and a<b,'Only indexed row sampling removed for pure actual metadata verification')
advance=advance[:a]+advance[b:]
advance=advance.replace('self.surface=np.empty((254,400),dtype=np.uint16)','self.surface=None')
scope=dict(vars(model));exec(compile(advance,__file__+'::whole_actual_clock_timing_without_pixel_sampling','exec'),scope)

class Ledger(model.Scanline):
    advance=scope['advance']

def contract(lines,ids):
    clock=Ledger(ids);records=[];scanout=None;last_event=0;timed_operations=0
    for line in lines:
        if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK '):
            kind,row=model.parse(line);clock.advance(None,row)
            if clock.seed is not None:
                expected=clock.seed['next_vblank']+(clock.seed['frame_period']if row['seconds']>=clock.seed['next_vblank']-1e-9 else 0)
                need(abs(row['next_vblank']-expected)<1e-9,'Every real future274deadline bound to exact actual native cycle, including finish')
            continue
        if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_'):continue
        tag=line.split(' ',1)[0].removeprefix('MK2_NAT_CAMPAIGN_')
        if tag in model.Model.OPERATIONS:
            kind,row=model.parse(line)
            need(row['event']>last_event and row['epoch']==1,'All original actual native operation events remain ordered in single epoch')
            clock.bind(kind,row);last_event=row['event'];timed_operations+=1
        elif tag=='FLOOR_SCANOUT':
            kind,row=model.parse(line);model.previous.validate_context(row,ids)
            need(clock.finished and all(row[k]==clock.clock[k]for k in('frame','epoch','start','dpyadr','control','tap','vcount','vsblnk','veblnk')),
                 'Actual completed operation clock and separate native scanout agree on every register/beam/context')
            display={k:row[k]for k in('frame','epoch','start','control','tap')}
            visible=model.visible_start(row,display,row['frame'])
            need(visible==clock.latched,'Independent end hardware address agrees with original real274latch, not RGB matching')
            scanout=row
        elif tag=='FLOOR_SNAP':
            kind,row=model.parse(line)
            need(clock.finished and scanout is not None and row['frame']==clock.frame==scanout['frame'],
                 'Every actual full-field snapshot has original finish clock and independently bound scanout')
            records.append(dict(frame=row['frame'],clocks=clock.current_count,visibleStart=clock.latched))
    need(records and clock.finished and len(records)==clock.records and
         [r['frame']for r in records]==list(range(records[0]['frame'],records[-1]['frame']+1)),
         'Entire actual ledger contains consecutive fully finished renderer fields, no missing final clock')
    return dict(records=records,actualClocks=clock.sequence,actualTimedOperations=timed_operations)

def run(fighter):
    capture=ROOT/f'audit_v4713_{fighter}_p2_ending_raster_clock_ram'
    native_report=ROOT/f'audit_v4714_{fighter}_p2_ending_raster_clock_checked/report.json'
    need(native_report.exists(),'Actual full renderer run must be terminal; never restart or infer failure from timeout')
    proof=json.loads(native_report.read_text());need(proof['passed'],'Actual whole native pixel/VRAM pipeline must pass, not metadata substituted for pixels')
    ids=(13,17 if fighter=='kano'else 18)
    text=(capture/'run.log').read_text();lines=text.splitlines();positive=contract(lines,ids)
    lo,hi=source.renderer_window(text,fighter)
    need([r['frame']for r in positive['records']]==list(range(lo,hi+1))and
         len(positive['records'])==proof['exactConsecutiveNativeVideoFields']and
         positive['actualClocks']==proof['actualRasterClocks'],
         'Every whole ending and all300native attract fields retained in both actual metadata and full pixel proofs')
    faults=[]
    end=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '))
    first=lines[:end+1];actual=contract(first,ids)
    seed=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=begin 'in l)
    finish=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=finish 'in l)
    scanned=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT '))
    def reject(label,bad):
        need(bad!=first,'Non-vacuous actual native timing row fault')
        try:contract(bad,ids)
        except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native clock/scanout counterexample admitted '+label)
        need(contract(first,ids)==actual,'Complete unchanged actual first field restored after each real row fault')
    def change(line,key,value):
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Real actual clock field mutation');return[changed if l==line else l for l in first]
    for key,value in(('sequence','2'),('epoch','2'),('human_slot','1'),('fighter','sonya'if fighter=='kano'else'kano'),
                      ('writes','1'),('assistance','forced'),('reason','field'),('vcount','272'),
                      ('next_vblank','0.0'),('scan_period','nan'),('frame_period','0.0')):
        reject('actual_seed_'+key,change(seed,key,value))
    finish_row=dict(re.findall(r'(\w+)=([^\s]+)',finish))
    for key,value in(('sequence','0'),('next_event','0'),('vcount','272'),('dpyadr',f"{int(finish_row['dpyadr'],16)^16:04X}"),
                      ('control','F020'),('tap',f"{int(finish_row['tap'],16)^1:04X}"),('next_vblank','0.0')):
        reject('actual_finish_'+key,change(finish,key,value))
    scanned_row=dict(re.findall(r'(\w+)=([^\s]+)',scanned))
    for key,value in(('dpyadr',f"{int(scanned_row['dpyadr'],16)^16:04X}"),('vcount','272'),
                      ('control','F020'),('tap',f"{int(scanned_row['tap'],16)^1:04X}")):
        reject('actual_scanout_'+key,change(scanned,key,value))
    reject('missing_actual_finish_clock',[l for l in first if l!=finish])
    reject('duplicate_actual_seed_clock',[seed if l==seed else l for l in first[:first.index(seed)+1]]+[seed]+first[first.index(seed)+1:])
    need(contract(lines,ids)==positive,'Every actual whole renderer metadata field unchanged after all24faults')
    pins=dict(proof['inputHashes']);pins[str(native_report)]=sha(native_report);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'All actual full native source/control/capture inputs unchanged')
    return dict(passed=True,fighter=fighter,physicalSlot=2,identity=ids[1],
      actualConsecutiveNativeFields=len(positive['records']),actualRasterClocks=positive['actualClocks'],
      actualOriginalTimedOperations=positive['actualTimedOperations'],actualMetadataFaultsRejected=faults,
      sourceTimedPixelsAcceptedBySeparateWholeNativeRAMProof=True,metadataNeverSubstitutedForPixels=True,
      actualPixelAndVRAMBitFaultsRetained=proof['actualNativePixelFaultsRejected'],inputHashes=pins,
      fullPortAcceptance=False,independentStockChoreographyAccepted=False,allEndingContextsAccepted=False,
      rawMediaFilesWritten=0,newBuilds=0,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4716_{args.fighter}_ending_raster_clock_ledger_checked'
    need(not out.exists(),'Fresh immutable actual clock ledger proof')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualMetadataFaultsRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
