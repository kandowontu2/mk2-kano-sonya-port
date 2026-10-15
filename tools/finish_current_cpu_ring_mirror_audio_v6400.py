"""Complete retained6395 PCM with native50Hz mixer and60Hz owner updates.

samples_device::playing() updates its stream at the existing owner timer;
video positions therefore need both clocks, not just the last PCM callback.
No emulator replay, omitted states, source-clock search or waveform fitting.
"""
import inspect,json
from pathlib import Path
from decimal import Decimal
import finish_current_cpu_ring_mirror_audio_v6396 as prior
import finish_current_cpu_ring_mirror_audio_v6398 as boundary

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6401_current_cpu_ring_mirror_audio_ram_checked'


def finish(carrier):
 need(not OUT.exists() and not prior.OUT.exists() and not boundary.OUT.exists(),
      'No prior checker output overwritten')
 terminal=json.loads((prior.CASE/'native_terminal.json').read_text())
 need(terminal['nativeExit']==0 and not prior.original.prior.process_tools.census(),
      'Same naturally terminal emulator, retained host RAM only')
 first=carrier['pcm_headers'][0];dac=carrier['dac_headers'][0]
 preceding=Decimal(dac['previous_seconds'])
 need(preceding==Decimal(first['seconds'])-Decimal('.02'),
      'Actual preceding DAC clock is native50Hz')
 failure=boundary.BOUNDARY/'owner_timer_failure.json'
 need(not failure.exists(),'Preserve actual6398 failed video-state check once')
 prior.original.prior.original.save(failure,dict(passed=False,
  error="ValueError('Every original Square video position through finite retained EOF')",
  executedChecker=str(Path(boundary.__file__).resolve()),checkerSHA256=sha(boundary.__file__),
  nativeTerminal=terminal,originalOutputWasNotCreated=True,noNativeRerun=True))
 source=inspect.getsource(prior.square_context)
 before="  need(index>=0,'First actual video state follows a retained source callback')\n  count=min(45512,max(0,mix.sample_clock(headers[index]['seconds'],True)-start))"
 after="""  clock=headers[index]['seconds']if index>=0 else preceding_clock
  need(index>=0 or Decimal(preceding_clock)<=Decimal(row['seconds'])<clocks[0],'Entire first native video interval uses actual preceding DAC clock')
  count=min(45512,max(0,mix.sample_clock(clock,True)-start))
  # Original60Hz owner timer calls playing(), which updates this stream
  # between50Hz mixed-PCM callbacks. Resolve the timer index from the
  # source start's one-sample clock interval; never from target positions.
  sec,fraction=divmod(start,48000);upper=sec*mix.ATTO+fraction*mix.PERIOD
  sec,fraction=divmod(start-1,48000);lower=sec*mix.ATTO+fraction*mix.PERIOD
  now=int(Decimal(row['seconds'])*mix.ATTO);period=mix.ATTO//60
  earliest=max(0,(now-upper)//period);latest=max(0,(now-lower)//period)
  need(min(45512,earliest*800)==min(45512,latest*800),'Source start clock interval gives unambiguous native60Hz timer index at every video field')
  count=max(count,min(45512,earliest*800))"""
 need(source.count(before)==1,'Retain whole original Square gate, correct both native update clocks')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,preceding_clock=dac['previous_seconds'])
 exec(compile(source,__file__+'::whole_square_source_gate_with_native_owner_timer','exec'),scope)
 scope['OUT']=OUT
 finish_source=inspect.getsource(prior.finish)
 before="for p in(CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'failure.json',Path(__file__),Path(original.__file__)):"
 after="for p in(CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'failure.json',Path(__file__),Path(original.__file__),Path(prior_checker),Path(boundary_checker),first_boundary_failure,owner_timer_failure):"
 need(finish_source.count(before)==1,'Pin unchanged executed checkers and both actual failures')
 finish_source=finish_source.replace(before,after,1)
 scope.update(__file__=__file__,prior_checker=prior.__file__,boundary_checker=boundary.__file__,
              first_boundary_failure=boundary.BOUNDARY/'failure.json',owner_timer_failure=failure)
 exec(compile(finish_source,__file__+'::whole_retained_terminal_RAM_finish','exec'),scope)
 return scope['finish'](carrier)
