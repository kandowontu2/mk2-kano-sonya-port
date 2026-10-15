"""Closed native timing counterexample and source-defined CPU-cycle boundary.

Metadata only: no dummy VRAM, fabricated pixels or whole-ending acceptance.
The actual native capture continues naturally; no growing-log hash is pinned.
"""
import inspect,json,subprocess,textwrap,traceback
from pathlib import Path
import verify_ending_native_io_clock_ledger_v4737 as ledger
import ending_raster_cpu_cycle_model_v4740 as model
ROOT,need,sha=ledger.ROOT,ledger.need,ledger.sha
OUT=ROOT/'audit_v4743_actual_cpu_cycle_raster_boundary_checked'

def make_ledger():
    # Same entire metadata-only adapter, with the new complete source model.
    advance=textwrap.dedent(inspect.getsource(model.Scanline.advance))
    for before,after in ledger.changes:
        need(advance.count(before)==1,'Whole metadata-only adapter; only indexed sampling removed')
        advance=advance.replace(before,after,1)
    scope=dict(vars(model));exec(compile(advance,__file__+'::whole4740_no_dummy_pixels','exec'),scope)
    class Ledger(model.Scanline):
        advance=scope['advance']
    scope=dict(vars(ledger),model=model,Ledger=Ledger)
    exec(compile(inspect.getsource(ledger.contract),__file__+'::whole4737_actual_register_ledger','exec'),scope)
    return scope['contract']

def main():
    need(not OUT.exists(),'Fresh actual native timing/source diagnostic')
    old=(ROOT/'tools/ending_raster_io_model_v4720.py').read_text()
    new=Path(model.__file__).read_text()
    before="phase>=self.phase and first-1e-9<=row['seconds']<first+row['scan_period']+1e-9"
    after="phase>=self.phase and first-CPU_CYCLE_SECONDS-1e-9<=row['seconds']<first+row['scan_period']+1e-9"
    need(old.count(before)==1 and new.count(after)==1 and model.CPU_CYCLE_SECONDS==8/50000000,
         'One actual TMS34010 native cycle, not a chosen image tolerance')
    # Ignore only explanatory module docstrings when comparing exact sources.
    body=lambda s:s.split('"""',2)[2]
    expected=body(old).replace('IO_KEYS=','CPU_CYCLE_SECONDS=8/50000000\nIO_KEYS=',1).replace(before,after,1)
    need(body(new)==expected,'All complete one-base VRAM/RGB/IO source unchanged except source-bound early-time gate')
    files=[ROOT/'mame-mkp/src/emu/schedule.cpp',ROOT/'mame-mkp/src/emu/diexec.cpp',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.h',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp',ROOT/'mame-mkp/src/mame/midway/midtunit.cpp']
    schedule,execute,cpu,cpu_body,driver=[p.read_text()for p in files]
    need('m_executing_device->local_time() : m_basetime;'in schedule and
         'if (m_callback_timer != nullptr)'in schedule and 'return m_callback_timer_expire_time;'in schedule and
         'delta >= exec->m_attoseconds_per_cycle'in schedule and
         'divu_64x32(u64(delta) >> exec->m_divshift, exec->m_divisor)'in schedule and
         'return m_localtime + cycles_to_attotime(cycles);'in execute and
         'return (cycles * 8);'in cpu and '#define CPU_CLOCK       (50000000)'in driver and
         'SMART_IOREG(VCOUNT) = vcount;'in cpu_body and 'm_scantimer->adjust(screen().time_until_pos(vcount)'in cpu_body,
         'Timer callback global time and floor-cycle CPU-local timestamps are distinct actual source domains')
    path=ROOT/'audit_v4733_kano_p2_ending_raster_io_ram/run.log';lines=[];started=False
    # A complete, fixed prefix ending at a real SNAP, not a timeout or stop.
    with path.open()as stream:
        for line in stream:
            need(line.endswith('\n'),'Only closed actual native rows')
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK frame=56296 '):started=True
            if started and line.startswith('MK2_NAT_CAMPAIGN_FLOOR_'):lines.append(line.rstrip())
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP frame=56309 '):break
    need(lines and lines[-1].startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP frame=56309 '),
         'Actual complete14field prefix, never partial or fabricated native positive')
    try:ledger.contract(lines,(13,17))
    except ValueError as error:
        need(str(error)=='Actual CPU beam follows source-scheduled native scanline; no field skipped or chosen by image',
             'Exact retained original timing counterexample, not another failing gate')
        prior_error=str(error)
    else:raise ValueError('Old actual boundary counterexample not reproduced')
    real=next(l for l in lines if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK ')and 'sequence=475 'in l)
    _,row=model.parse(real)
    seed=next(model.parse(l)[1]for l in lines if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK frame=56309 ')and 'reason=field 'in l)
    nominal=seed['next_vblank']-seed['frame_period']+((row['vcount']-274)%289)*row['scan_period']
    early=nominal-row['seconds'];need(1e-9<early<model.CPU_CYCLE_SECONDS,'Actual30ns boundary lag is below one source-defined160ns CPU cycle')
    contract=make_ledger();positive=contract(lines,(13,17));faults=[]
    need(len(positive['records'])==14 and positive['records'][-1]['frame']==56309,
         'Entire actual first14field register/IO ledger; not pixel acceptance')
    import re
    for label,seconds in(('more_than_one_native_cycle',nominal-model.CPU_CYCLE_SECONDS*2),
                          ('different_native_scanline',nominal-row['scan_period'])):
        bad=real.replace('seconds='+re.search(r'\bseconds=(\S+)',real)[1],f'seconds={seconds:.15f}',1)
        need(bad!=real,'Real non-vacuous timing row mutation')
        try:contract([bad if l==real else l for l in lines],(13,17))
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Out-of-source CPU clock counterexample admitted')
        need(contract(lines,(13,17))==positive,'Same actual complete metadata prefix restored')
    files+=[Path(__file__).resolve(),Path(model.__file__).resolve(),Path(ledger.__file__).resolve(),ROOT/'tools/ending_raster_io_model_v4720.py']
    report=dict(passed=True,actualClosedMetadataPrefix=lines,actualFailedClock=real,
      reproducedOriginalTimingFailure=prior_error,actualBoundaryEarlySeconds=early,
      originalSourceDefinedCPUCycleSeconds=model.CPU_CYCLE_SECONDS,actualFieldsMetadataAccepted=14,
      actualClockRecords=positive['clocks'],actualIOStores=len(positive['io']),actualTimingFaultsRejected=faults,
      wholeOneBaseVRAMRGBSourceRetained=True,pixelToleranceAdded=False,dummyVRAMUsed=False,
      nativeWholeEndingPixelsAccepted=False,nativeRunStoppedOrRestarted=False,fullPortAcceptance=False,
      inputHashes={str(p.resolve()):sha(p)for p in files},scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualClosedMetadataPrefix')},indent=2),flush=True)

if __name__=='__main__':main()
