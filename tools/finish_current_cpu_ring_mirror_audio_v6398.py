"""Finish the already-terminal6395 RAM carrier; preserve6396's boundary error.

The first video field precedes the first retained PCM callback. Its source
position belongs to the preceding native sound update, whose exact clock is
retained in the first DAC header. No native boot, omitted field or PCM fit.
"""
import inspect,json
from pathlib import Path
from decimal import Decimal
import finish_current_cpu_ring_mirror_audio_v6396 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6399_current_cpu_ring_mirror_audio_ram_checked'
BOUNDARY=ROOT/'audit_v6398_preserved_first_video_boundary_failure'


def finish(carrier):
 need(not OUT.exists() and not prior.OUT.exists(),'No previous output overwritten')
 terminal=json.loads((prior.CASE/'native_terminal.json').read_text())
 need(terminal['nativeExit']==0 and not prior.original.prior.process_tools.census(),
      'Same naturally terminal emulator, retained host RAM only')
 first=carrier['pcm_headers'][0];dac=carrier['dac_headers'][0]
 preceding=Decimal(dac['previous_seconds'])
 need(preceding==Decimal(first['seconds'])-Decimal('.02'),
      'Actual preceding DAC clock is the native50Hz sound update')
 rows=[r for r in prior.mix.rows(carrier['text'],'MK2_MAUDIO_CHANNEL')if r['channel']=='12']
 need(preceding<=Decimal(rows[0]['seconds'])<Decimal(first['seconds']),
      'Actual first video belongs to precisely retained preceding DAC interval')
 need(not BOUNDARY.exists(),'Preserve new exact failure evidence once')
 BOUNDARY.mkdir()
 prior.original.prior.original.save(BOUNDARY/'failure.json',dict(passed=False,
  error="ValueError('First actual video state follows a retained source callback')",
  executedChecker=str(Path(prior.__file__).resolve()),checkerSHA256=sha(prior.__file__),
  nativeTerminal=terminal,firstPCM=first,firstDAC=dac,firstVideoChannel12=rows[0],
  originalOutputWasNotCreated=True,noNativeRerun=True))
 source=inspect.getsource(prior.square_context)
 before="  need(index>=0,'First actual video state follows a retained source callback')\n  count=min(45512,max(0,mix.sample_clock(headers[index]['seconds'],True)-start))"
 after="  clock=headers[index]['seconds']if index>=0 else preceding_clock\n  need(index>=0 or Decimal(preceding_clock)<=Decimal(row['seconds'])<clocks[0],'Entire first native video interval uses actual preceding DAC clock')\n  count=min(45512,max(0,mix.sample_clock(clock,True)-start))"
 need(source.count(before)==1,'Change only first-video clock boundary; retain all states')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,preceding_clock=dac['previous_seconds'])
 exec(compile(source,__file__+'::whole_square_source_gate_with_previous_DAC_clock','exec'),scope)
 scope['OUT']=OUT
 finish_source=inspect.getsource(prior.finish)
 before="for p in(CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'failure.json',Path(__file__),Path(original.__file__)):"
 after="for p in(CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'failure.json',Path(__file__),Path(original.__file__),Path(prior_checker),boundary_failure):"
 need(finish_source.count(before)==1,'Pin unchanged executed6396 and actual preserved error')
 finish_source=finish_source.replace(before,after,1)
 scope.update(__file__=__file__,prior_checker=prior.__file__,boundary_failure=BOUNDARY/'failure.json')
 exec(compile(finish_source,__file__+'::whole_retained_terminal_RAM_finish','exec'),scope)
 return scope['finish'](carrier)
