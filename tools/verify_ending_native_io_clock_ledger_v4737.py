"""Actual complete native clock/IO ledger, original caller code and real faults.

Require the separate actual full RAM pixel/VRAM proof first. This metadata
state machine removes only indexed sampling; no dummy VRAM or fabricated
native pixel positive is supplied. Whole ending/attract scope is retained.
"""
import argparse,inspect,json,re,subprocess,textwrap,traceback
from pathlib import Path
import ending_raster_io_model_v4720 as model
import qualify_ending_raster_io_blackpen_source_v4730 as source
ROOT,need,sha=source.ROOT,source.need,source.sha

advance=textwrap.dedent(inspect.getsource(model.Scanline.advance))
changes=[('self.surface=np.empty((254,400),dtype=np.uint16);self.blank=np.zeros((254,400),dtype=bool)',
          'self.surface=None;self.blank=None'),
         ('                self.surface[y]=words[source_row,(column+columns)&511]&0x7fff\n',''),
         ('                if not self.state[\'control\']&0x8000:self.blank[y]=True\n','')]
for before,after in changes:
    need(advance.count(before)==1,'Only actual indexed sampling removed, not timing/IO/source gates')
    advance=advance.replace(before,after,1)
scope=dict(vars(model));exec(compile(advance,__file__+'::whole4720_actual_metadata_no_pixel_sampling','exec'),scope)

class Ledger(model.Scanline):
    advance=scope['advance']

def contract(lines,ids):
    clock=Ledger(ids);records=[];scanout=None;event=0;operations=0;io=[]
    for line in lines:
        if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_'):continue
        tag=line.split(' ',1)[0].removeprefix('MK2_NAT_CAMPAIGN_')
        if tag=='FLOOR_RASTER_CLOCK':
            _,row=model.parse(line);clock.advance(None,row)
        elif tag in model.Model.OPERATIONS:
            kind,row=model.parse(line)
            need(row['epoch']==1 and row['event']>event,'Actual original operation ordering and single epoch')
            clock.bind(kind,row);event=row['event'];operations+=1
            if kind=='FLOOR_RASTER_IO':io.append(row)
        elif tag=='FLOOR_SCANOUT':
            _,row=model.parse(line);model.previous.previous.validate_context(row,ids)
            need(clock.finished and all(row[k]==clock.clock[k]for k in('frame','epoch','start','dpyadr','control','tap','vcount','vsblnk','veblnk')),
                 'Every separate actual scanout agrees with completed register/beam replay')
            display={k:row[k]for k in('frame','epoch','start','control','tap')}
            visible=model.visible_start(row,display,row['frame'])
            need(visible==(clock.state['dpyadr']+254*16)&0xffff,
                 'Independent actual end-hardware address matches continuous CPU/native register state')
            scanout=row
        elif tag=='FLOOR_SNAP':
            _,row=model.parse(line)
            need(clock.finished and scanout is not None and row['frame']==clock.frame==scanout['frame'],
                 'Every actual snapshot includes completed source-timed rows and independent scanout')
            records.append(dict(frame=row['frame'],clocks=clock.current_count,ioStoresAtSnapshot=clock.io_count))
    need(records and clock.finished and len(records)==clock.records and
         [r['frame']for r in records]==list(range(records[0]['frame'],records[-1]['frame']+1)),
         'All actual native ending/attract fields complete and consecutive, no final clock omitted')
    need(len(io)==clock.io_count,'All actual explicit IO stores admitted once, none replaced by automatic latch')
    return dict(records=records,clocks=clock.sequence,operations=operations,io=io)

def original_io_callers(rows,guest,stock):
    callers={}
    for row in rows:
        pc=row['pc'];need(0xff800080<=pc<0x100000000 and pc%16==0,'Actual original ROM display-store instruction cursor')
        offset=(pc-128-0xff800000)//8
        actual=guest[offset:offset+18];original=stock[offset:offset+18]
        need(len(actual)==18 and actual==original,'Original executed display-store instruction/operands byte-exact at '+hex(pc))
        key=f'{pc:08X}';entry=callers.setdefault(key,dict(pc=key,originalInstructionWindowSHA256=model.digest(actual),
                                                       byteOffset=offset,bytes=18,stores=0,registers=set()))
        entry['stores']+=1;entry['registers'].add(row['register'])
    for entry in callers.values():entry['registers']=sorted(entry['registers'])
    need(callers,'Actual original register stores observed, never zero-store acceptance')
    return callers

def run(fighter):
    capture=ROOT/f'audit_v4733_{fighter}_p2_ending_raster_io_ram'
    report_path=ROOT/f'audit_v4734_{fighter}_p2_ending_raster_io_checked/report.json'
    need(report_path.exists(),'Actual renderer run must reach real terminal first; no timeout-based restart')
    proof=json.loads(report_path.read_text());need(proof['passed'],'Separate actual whole raw pixel/VRAM replay required; metadata is not a substitute')
    # The existing immutable full guest provider, not native data fabricated
    # or sourced from later comparison snapshots.
    import run_kintaro_pressure_guard_long_campaign_v4439 as guest_provider
    guest=guest_provider.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    ids=(13,17 if fighter=='kano'else 18);text=(capture/'run.log').read_text();lines=text.splitlines()
    positive=contract(lines,ids);callers=original_io_callers(positive['io'],guest,stock)
    lo,hi=source.renderer_window(text,fighter)
    need([r['frame']for r in positive['records']]==list(range(lo,hi+1))and
         len(positive['records'])==proof['exactConsecutiveNativeVideoFields']and positive['clocks']==proof['actualRasterClocks']and
         len(positive['io'])==proof['actualOriginalDisplayIOStores']and len(proof['actualNativePixelFaultsRejected'])==2,
         'Every native full ending/all300attract fields, original IO stores, actual whole VRAM/RGB and bit faults retained')
    stop=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '))
    first=lines[:stop+1];baseline=contract(first,ids);faults=[]
    clock_seed=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=begin 'in l)
    clock_end=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'reason=finish 'in l)
    io_line=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_IO '))
    scan_line=next(l for l in first if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT '))
    def fault(label,bad,caller=False):
        need(bad!=first,'Non-vacuous actual native row fault')
        try:
            mutated=contract(bad,ids)
            if caller:original_io_callers(mutated['io'],guest,stock)
        except (ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native IO/clock fault admitted '+label)
        need(contract(first,ids)==baseline,'Whole unchanged actual first-field metadata restored after real fault')
    def mutate(line,key,value):
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Actual real source-timed row/key mutation')
        return[changed if l==line else l for l in first]
    for key,value in(('sequence','2'),('epoch','2'),('vcount','272'),('human_slot','1'),
                      ('fighter','sonya'if fighter=='kano'else'kano'),('writes','1'),('assistance','forced'),('reason','field')):
        fault('actual_notifier_'+key,mutate(clock_seed,key,value))
    values=dict(re.findall(r'(\w+)=([^\s]+)',io_line))
    for key,value in(('at','C0000090'),('register','not_a_register'),('mask','00FF'),
                      ('before',f"{int(values['before'],16)^1:04X}"),('value',f"{int(values['value'],16)^1:04X}"),
                      ('epoch','2'),('writes','1'),('pc','FFF00001')):
        fault('actual_IO_'+key,mutate(io_line,key,value),caller=key=='pc')
    values=dict(re.findall(r'(\w+)=([^\s]+)',clock_end))
    for key,value in(('sequence','0'),('next_event','0'),('vcount','272'),
                      ('dpyadr',f"{int(values['dpyadr'],16)^16:04X}"),('control','F020'),('next_vblank','0.0')):
        fault('actual_finish_'+key,mutate(clock_end,key,value))
    values=dict(re.findall(r'(\w+)=([^\s]+)',scan_line))
    for key,value in(('dpyadr',f"{int(values['dpyadr'],16)^16:04X}"),('tap',f"{int(values['tap'],16)^1:04X}")):
        fault('actual_scanout_'+key,mutate(scan_line,key,value))
    fault('missing_actual_IO',[l for l in first if l!=io_line]);fault('missing_actual_finish',[l for l in first if l!=clock_end])
    need(contract(lines,ids)==positive,'Entire actual native hardware ledger unchanged after all real metadata counterexamples')
    pins=dict(proof['inputHashes'])
    for p in(report_path,Path(__file__).resolve(),Path(model.__file__).resolve(),Path(guest_provider.__file__).resolve(),ROOT/'mk2/mk2-maincpu.bin'):pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual current source/control/native guest/pixel input unchanged')
    return dict(passed=True,fighter=fighter,physicalSlot=2,identity=ids[1],
      completeActualRendererFields=len(positive['records']),actualNativeClockRecords=positive['clocks'],
      actualOriginalTimedOperations=positive['operations'],actualNativeDisplayIOStores=len(positive['io']),
      sourceQualifiedOriginalIOCallers=callers,actualMetadataFaultsRejected=faults,
      separateActualWholeVRAMRGBAndBitFaultProofRequired=True,metadataNeverSubstitutedForPixels=True,
      originalColdNativeCampaignAndQualifiedEndingPagesRetained=True,fullPortAcceptance=False,
      independentStockTransitionChoreographyAccepted=False,allEndingContextsAccepted=False,
      rawMediaFilesWritten=0,newBuilds=0,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4738_{args.fighter}_ending_native_io_clock_ledger_checked'
    need(not out.exists(),'Fresh immutable native IO/timing/caller qualification')
    try:report=run(args.fighter)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualMetadataFaultsRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
