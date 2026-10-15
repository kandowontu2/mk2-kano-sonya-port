"""Complete immutable actual clock/IO ledger before a fresh raw-pixel run.

This diagnoses a real terminal capture whose previous pixel checker failed.
Metadata never proves RGB/VRAM. The complete ending plus300attract remains
required, as do actual source-timed pixels and original bit faults later.
"""
import argparse,inspect,json,re,struct,subprocess,traceback
from pathlib import Path
import qualify_actual_cpu_cycle_raster_boundary_v4742 as diagnostic
import verify_ending_native_io_clock_ledger_v4737 as previous
import ending_raster_cpu_cycle_model_v4740 as model
import run_kintaro_pressure_guard_long_campaign_v4439 as guest_provider
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
# Whole prior ledger, with only the actual unrendered terminal seed added.
# The seed must follow a completed final field, contain no operation/row and
# exactly match the original next-notifier native stop; it is never pixels.
contract_source=inspect.getsource(previous.contract)
before="def contract(lines,ids):"
need(contract_source.count(before)==1,'Complete original ledger signature')
contract_source=contract_source.replace(before,'def contract(lines,ids,terminal_frame=None):',1)
before="records and clock.finished and len(records)==clock.records"
after="""records and len(records)==clock.records and
         (clock.finished if terminal_frame is None else
          not clock.finished and clock.frame==terminal_frame==records[-1]['frame']+1 and
          clock.current_count==1 and clock.completed==0 and clock.phase==-1 and
          clock.clock['reason']=='field'and clock.clock['next_event']==event+1)"""
need(contract_source.count(before)==1,'Complete finished-field accounting retained')
contract_source=contract_source.replace(before,after,1)
before="return dict(records=records,clocks=clock.sequence,operations=operations,io=io)"
after="return dict(records=records,clocks=clock.sequence,operations=operations,io=io,unrenderedTerminalSeed=clock.clock if terminal_frame is not None else None)"
need(contract_source.count(before)==1,'Actual separate terminal seed retained without fabricated render')
contract_source=contract_source.replace(before,after,1)
contract_scope=dict(vars(previous),model=model,Ledger=diagnostic.make_ledger().__globals__['Ledger'])
exec(compile(contract_source,__file__+'::whole4737_completed_fields_and_actual_shutdown_seed','exec'),contract_scope)
contract=contract_scope['contract']

def terminal_boundary(rows,ids,lo,hi,fields):
    def parsed(line):
        row=model.parse(line)
        if row is not None:return row[1]
        need(line.startswith('MK2_NAT_CAMPAIGN_RESULT '),'Only original native terminal has separate controller schema')
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key in('frame','human_slot','writes'):row[key]=int(row[key])
        model.previous.previous.validate_context(row,ids)
        return row
    tagged=lambda tag:[(index,parsed(line))for index,line in enumerate(rows)if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    clocks=tagged('FLOOR_RASTER_CLOCK');snaps=tagged('FLOOR_SNAP')
    end=[(i,r)for i,r in clocks if r['reason']=='finish']
    seeds=[(i,r)for i,r in clocks if r['reason']=='field']
    native=tagged('RESULT');floor=tagged('FLOOR_RESULT')
    need(len(end)==len(seeds)==len(snaps)==len(native)==len(floor)==1,
         'Actual one final completed field and one unrendered ordinary-notifier seed')
    ei,finish=end[0];si,seed=seeds[0];ri,result=native[0];fi,stop=floor[0];ni,snap=snaps[0]
    model.previous.previous.validate_context(finish,ids);model.previous.previous.validate_context(seed,ids)
    need(ei<ni<si<ri<fi and snap['frame']==finish['frame']==hi and seed['frame']==result['frame']==stop['frame']==hi+1,
         'Actual last frame_done, unrendered seed, physical next-notifier stop and renderer-stop order')
    need(seed['sequence']==finish['sequence']+1 and seed['next_event']==finish['next_event'] and
         all(seed[k]==finish[k]for k in('start','dpyadr','control','tap','vcount','vsblnk','veblnk','vtotal','seconds','next_vblank','scan_period','frame_period')) and
         seed['vcount']==273 and stop['origin']==lo and stop['snapshots']==fields,
         'Source-order terminal seed contains no CPU/store/visible row and exactly retains prior finished hardware/deadline')
    return dict(actualTerminalClock=seed,lastCompletedClock=finish,completedRendererFields=fields)


def original_io_callers(rows,guest,stock):
    callers=previous.original_io_callers(rows,guest,stock)
    for row in rows:
        pc=row['pc'];offset=(pc-48-0xff800000)//8
        opcode,target=struct.unpack_from('<HI',guest,offset)
        need(opcode&0xffe0 in(0x0580,0x0780)and target==row['at'],
             'Actual original MOVE register-to-absolute IO destination at executed PC, not arbitrary unchanged ROM')
        entry=callers[f'{pc:08X}']
        entry.update(originalStoreOpcode=f'{opcode:04X}',originalDestination=f'{target:08X}',
                     originalSourceRegister=('B'if opcode&0x10 else'A')+str(opcode&15))
    return callers

def run(fighter):
    capture=ROOT/f'audit_v4733_{fighter}_p2_ending_raster_io_ram'
    oldreport=ROOT/f'audit_v4734_{fighter}_p2_ending_raster_io_checked/report.json'
    failed=json.loads(oldreport.read_text());meta=json.loads((capture/'result.json').read_text())
    need(not failed['passed']and meta['exit_code']==0 and len(meta['endingModelErrors'])==1,
         'Actual prior native terminal0 and failed checker retained, not restarting live or timeout')
    for p,h in meta['input_hashes'].items():need(sha(p)==h,'All actual executed controls/observer/guest source bytes unchanged')
    ids=(13,17 if fighter=='kano'else 18);path=capture/'run.log';first=[];window=[]
    with path.open()as stream:
        for line in stream:
            need(line.endswith('\n'),'Entire terminal native text has only closed records')
            if not first or not first[-1].startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '):first.append(line.rstrip())
            if line.startswith(tuple('MK2_NAT_CAMPAIGN_'+tag+' 'for tag in
               ('ENDING_START','ENDING_COMPLETED','RESULT','FLOOR_RESULT','FLOOR_SNAP'))):window.append(line.rstrip())
    lo,hi=previous.source.renderer_window('\n'.join(window)+'\n',fighter)
    with path.open()as stream:positive=contract(stream,ids,hi+1)
    need([r['frame']for r in positive['records']]==list(range(lo,hi+1))and
         len(positive['records'])==meta['observedEndingRGBFields'],
         'Every actual ending/attract native field once, all300actualattract fields preserved')
    guest=guest_provider.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes()
    callers=original_io_callers(positive['io'],guest,stock)
    baseline=contract(first,ids);faults=[]
    clock_seed=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=begin 'in l)
    clock_end=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=finish 'in l)
    io_line=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_IO '))
    scan_line=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT '))
    def fault(label,bad,caller=False):
        need(bad!=first,'Real non-vacuous native metadata fault')
        try:
            mutated=contract(bad,ids)
            if caller:original_io_callers(mutated['io'],guest,stock)
        except (ValueError,KeyError,struct.error)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native metadata fault admitted '+label)
        need(contract(first,ids)==baseline,'Same complete actual first native field restored')
    def mutate(line,key,value):
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Actual native record/key mutation')
        return[changed if l==line else l for l in first]
    for key,value in(('sequence','2'),('epoch','2'),('vcount','272'),('human_slot','1'),
                      ('fighter','sonya'if fighter=='kano'else'kano'),('writes','1'),('assistance','forced'),('reason','field')):
        fault('actual_notifier_'+key,mutate(clock_seed,key,value))
    values=dict(re.findall(r'(\w+)=([^\s]+)',io_line))
    for key,value in(('at','C0000090'),('register','not_a_register'),('mask','00FF'),
                      ('before',f"{int(values['before'],16)^1:04X}"),('value',f"{int(values['value'],16)^1:04X}"),
                      ('epoch','2'),('writes','1'),('pc','FFF00001'),('pc','FFF00000')):
        fault('actual_IO_'+key+'_'+value,mutate(io_line,key,value),caller=key=='pc')
    values=dict(re.findall(r'(\w+)=([^\s]+)',clock_end))
    for key,value in(('sequence','0'),('next_event','0'),('vcount','272'),
                      ('dpyadr',f"{int(values['dpyadr'],16)^16:04X}"),('control','F020'),('next_vblank','0.0')):
        fault('actual_finish_'+key,mutate(clock_end,key,value))
    values=dict(re.findall(r'(\w+)=([^\s]+)',scan_line))
    for key,value in(('dpyadr',f"{int(values['dpyadr'],16)^16:04X}"),('tap',f"{int(values['tap'],16)^1:04X}")):
        fault('actual_scanout_'+key,mutate(scan_line,key,value))
    fault('missing_actual_IO',[l for l in first if l!=io_line])
    fault('missing_actual_finish',[l for l in first if l!=clock_end])
    with path.open()as stream:need(contract(stream,ids,hi+1)==positive,'Complete actual terminal ledger restored after all actual metadata faults')
    need(len(faults)==27,'All original26metadata faults plus aligned arbitrary-original-ROM PC fault')
    tail=[]
    with path.open()as stream:
        for line in stream:
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and (
              ('reason=finish 'in line and f'frame={hi} 'in line)or f'frame={hi+1} 'in line):tail.append(line.rstrip())
            elif line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_SNAP ', 'MK2_NAT_CAMPAIGN_RESULT ', 'MK2_NAT_CAMPAIGN_FLOOR_RESULT '))and (
              f'frame={hi} 'in line or f'frame={hi+1} 'in line):tail.append(line.rstrip())
    boundary=terminal_boundary(tail,ids,lo,hi,len(positive['records']));terminal_faults=[]
    seed_line=next(l for l in tail if 'reason=field 'in l)
    for key,value in(('frame',str(hi+2)),('sequence','0'),('next_event','0'),('vcount','272'),
                      ('control','F020'),('writes','1'),('seconds','0.0')):
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,seed_line,count=1)
        need(n==1 and changed!=seed_line,'Actual terminal metadata key fault')
        try:terminal_boundary([changed if l==seed_line else l for l in tail],ids,lo,hi,len(positive['records']))
        except (ValueError,KeyError)as error:terminal_faults.append(dict(kind='terminal_'+key,rejectedBy=str(error)))
        else:raise ValueError('Actual terminal notifier fault admitted '+key)
        need(terminal_boundary(tail,ids,lo,hi,len(positive['records']))==boundary,'Whole actual terminal boundary restored')
    try:terminal_boundary([l for l in tail if l!=seed_line],ids,lo,hi,len(positive['records']))
    except ValueError as error:terminal_faults.append(dict(kind='missing_actual_terminal_seed',rejectedBy=str(error)))
    else:raise ValueError('Missing actual terminal notifier admitted')
    need(len(terminal_faults)==8 and positive['unrenderedTerminalSeed']==boundary['actualTerminalClock'] and
         sum(r['clocks']for r in positive['records'])+1==positive['clocks'],
         'Every actual native clock belongs to completed renderer fields or the one source-bound unrendered stop seed')

    files=[Path(__file__).resolve(),Path(model.__file__).resolve(),Path(diagnostic.__file__).resolve(),
           Path(previous.__file__).resolve(),Path(guest_provider.__file__).resolve(),stockpath,oldreport,
           ROOT/'audit_v4743_actual_cpu_cycle_raster_boundary_checked/report.json',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/34010tbl.hxx',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp',
           ROOT/'tools/verify_complete_cpu_cycle_ending_ledger_v4746.py',
           ROOT/'audit_v4747_kano_complete_cpu_cycle_ending_ledger_checked/report.json']
    pins=dict(meta['input_hashes'])
    for p in files:pins[str(p.resolve())]=sha(p)
    for p in capture.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every immutable actual source/native capture byte unchanged')
    return dict(passed=True,fighter=fighter,physicalSlot=2,identity=ids[1],nativeExit=0,
      completeActualMetadataFields=len(positive['records']),actualNativeClockRecords=positive['clocks'],
      actualOriginalTimedOperations=positive['operations'],actualNativeDisplayIOStores=len(positive['io']),
      actualAttractFields=300,sourceQualifiedOriginalIOInstructions=callers,actualMetadataFaultsRejected=faults,
      actualUnrenderedTerminalSeed=boundary,actualTerminalFaultsRejected=terminal_faults,
      completedRendererClockRecords=positive['clocks']-1,
      originalFailedPixelCheckerPreserved=True,previousPixelCheckerExactFields=meta['exactContinuousEndingFields'],
      metadataNeverSubstitutedForPixels=True,dummyVRAMUsed=False,fullEndingVRAMRGBPixelsAccepted=False,
      independentStockTransitionChoreographyAccepted=False,allEndingContextsAccepted=False,fullPortAcceptance=False,
      rawMediaFilesWritten=0,newBuilds=0,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4749_{args.fighter}_complete_cpu_cycle_ending_terminal_ledger_checked'
    need(not out.exists(),'Fresh actual complete ledger result')
    # Pending native capture is never converted into a failed result.
    need((ROOT/f'audit_v4734_{args.fighter}_p2_ending_raster_io_checked/report.json').exists(),
         'Await actual terminal report before this complete immutable ledger verifier')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualMetadataFaultsRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
