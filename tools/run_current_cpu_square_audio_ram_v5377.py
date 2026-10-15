"""Entire CPU Square audio gate with source-exact first-load/timer bookkeeping."""
import inspect,json,traceback
from pathlib import Path
import run_current_cpu_square_audio_ram_v5374 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v5379_current_cpu_square_audio_ram_checked'

def capture(enabled,guest):
 source=inspect.getsource(original.capture)
 before='audit_v5375_current_cpu_square_audio_ram_'
 need(source.count(before)==1,'Only fresh evidence leaf changes')
 source=source.replace(before,'audit_v5378_current_cpu_square_audio_ram_',1)
 namespace=dict(original.capture.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_actual_native_RAM_capture','exec'),namespace)
 return namespace['capture'](enabled,guest)

def owner_contract(log,typed,enabled):
 source=inspect.getsource(original.owner_contract)
 before="all(int(r['length'])==45512 and int(r['sample'])==13 for r in active)"
 need(source.count(before)==1,'Qualify actual first-load source_num against unmodified native device')
 source=source.replace(before,"all(int(r['length'])==45512 and int(r['sample'])==0xffffffff for r in active)",1)
 before="need(all(r['actor']==r['main']=='00000000'and r['health']=='0'and r['writes']=='0'for r in owners),'Disabled imported cue has no stale owners')"
 after="""for f in frames:
   seconds=float(cb[f,12]['seconds']);pending=float(marks[0]['seconds'])<seconds<float(marks[0]['seconds'])+1/60
   for slot in(1,2):
    r=ob[f,slot];need(r['writes']=='0','Read-only disabled owner callbacks')
    if slot==2 and pending:
     need((r['actor'],r['main'],int(r['health']))==(f\"{own['actor']:08X}\",f\"{own['main']:08X}\",own['hp']),'Actual disabled cue ownership exists only before first native60Hz cleanup tick')
    else:need(r['actor']==r['main']=='00000000'and r['health']=='0','Disabled sample owner cleared by exact first native cleanup tick')"""
 need(source.count(before)==1,'Model actual native disabled-sample first timer, not immediate inferred cleanup')
 source=source.replace(before,after,1)
 namespace=dict(original.owner_contract.__globals__)
 exec(compile(source,__file__+'::whole_source_exact_native_channel_owner_contract','exec'),namespace)
 return namespace['owner_contract'](log,typed,enabled)

def run():
 failure=ROOT/'audit_v5376_current_cpu_square_audio_ram_checked/report.json'
 need(not json.loads(failure.read_text())['passed']and json.loads(failure.read_text())['error']=="ValueError('Complete Square asset on actual CPU channel12/sample13')",'Retain actual unsupported source_num assumption counterexample')
 device=ROOT/'mame-mkp/src/devices/sound/samples.cpp';text=device.read_text()
 old=ROOT/'audit_v3402_current_cpu_bicycle_hit_audio_checked/report.json'
 need(sha(device)==json.loads(old.read_text())['inputHashes'][str(device)],'Whole actually qualified original sample device unchanged')
 start=text[text.index('void samples_device::start('):text.index('void samples_device::start_raw(')]
 need(start.index('chan.source_num = (chan.source_len > 0) ? samplenum : -1;')<start.index('chan.source_len = sample.data.size();')and
  'chan.pos = 0;'in start and 'if (m_sample.empty())'in start,'Source-exact first loaded cue index uses preceding zero length; disabled start leaves sample channels untouched')
 compiled=ROOT/original.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 driver=ROOT/original.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 need('unsigned const sample = 13 + data - 0x6b00;'in compiled.read_text()and
  'm_mk2ks_battle_audio_timer->adjust(attotime::from_hz(60), 0, attotime::from_hz(60));'in compiled.read_text()and
  'm_mk2ks_voices->add_route(ALL_OUTPUTS, "mk2ksvoice", 0.70);'in driver.read_text(),'Actual compiled sample13/channel12/60Hz finite owner timer/.70 output route')
 paths=[failure,Path(original.__file__),device,old,compiled,driver,Path(__file__)]
 pins={str(p):sha(p)for p in paths}
 source=inspect.getsource(original.run)
 before="'wrong_sample':log.replace('sample=13 length=45512','sample=14 length=45512')"
 after="'wrong_first_load_bookkeeping':log.replace('sample=4294967295 length=45512','sample=13 length=45512')"
 need(source.count(before)==1,'Fault test mutates actual observed device bookkeeping, not an absent hypothetical value')
 source=source.replace(before,after,1)
 namespace=dict(original.run.__globals__,OUT=OUT,capture=capture,owner_contract=owner_contract,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_CPU_Square_audio_contract_native_first_load_and_timer','exec'),namespace)
 report=namespace['run']()
 for p,h in pins.items():need(sha(p)==h,'Whole original implementation and failure unchanged');report['inputHashes'][p]=h
 report.update(originalWholeAudioGateRetainedWithSourceExactFirstLoadAndTimer=True,originalSampleNumber13IdentityProvenByCompiledRouteAndFullWaveform=True,
  firstLoadSourceNumUsesPrecedingZeroLength=0xffffffff,disabledOwnerLifetimeBoundToFirstNative60HzTimer=True,preservedExecutedBookkeepingFailure=str(failure))
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable source-exact audio proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','wholeNativeHealth','wholeNativeState','phase')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
