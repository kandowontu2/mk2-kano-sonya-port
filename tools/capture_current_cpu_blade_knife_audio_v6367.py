"""Source-exact frame admission/EOS bookkeeping; preserve original failures.

The audio entry happens after that field's video callback. The first full
channel snapshot is therefore1872, not1871. samples.cpp retains source_len
and completed pos after EOF; source_num=-1 means inactive. No callback,
physical trajectory, native output or audio tail is dropped.
"""
import argparse,code,gzip,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_blade_knife_audio_v6365 as prior
original=prior.original
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6368_current_cpu_blade_knife_audio_ram'
SCOPE=None


def state(text,fighter,side,guest):
 source=inspect.getsource(original.state)
 changes={
  '640*14':'639*14',
  'range(1871,2511)':'range(1872,2511)',
  "all(r['length']=='0'for r in channels if r['frame']=='2510')":
  "all(r['sample']=='4294967295' and float(r['pos'])>=int(r['length'])for r in channels if r['frame']=='2510')",
 }
 for before,after in changes.items():
  need(source.count(before)==(2 if before=='640*14'else 1),'Only original admission/EOS bookkeeping changes')
  source=source.replace(before,after)
 scope=dict(original.state.__globals__)
 exec(compile(source,__file__+'::whole_original_state_correct_video_admission_and_native_EOS','exec'),scope)
 result=scope['state'](text,fighter,side,guest)
 pcm=original.mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(len(pcm)==584 and pcm[0]['frame']=='1872'and pcm[-1]['frame']=='2509'and
      all(r['bytes']=='3840'for r in pcm), 'Entire actual source50Hz audio window, no dropped callbacks')
 need(all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Every actual20ms PCM callback retained')
 return dict(result,completePCMCallbacks=len(pcm),nativeEOSEvidence='source_num=-1, retained source_len and completed pos')


def prepare():
 source=inspect.getsource(prior.prepare)
 need(source.count('audit_v6366_current_cpu_blade_knife_audio_ram')==1,'Only fresh evidence path changes')
 source=source.replace('audit_v6366_current_cpu_blade_knife_audio_ram','audit_v6368_current_cpu_blade_knife_audio_ram',1)
 scope=dict(prior.__dict__,__file__=__file__)
 exec(compile(source,__file__+'::whole6365_current_audio_EOS_context','exec'),scope)
 prepared=scope['prepare']();prepared['state']=state
 run=prepared['run']
 def retained_run(fighter,side):
  try:return run(fighter,side)
  except Exception as error:
   # Keep the actual native buffers even when a host state gate fails before
   # waveform prediction. Native terminal is already persisted by6213.
   trace=error.__traceback__
   while trace:
    values=trace.tb_frame.f_locals
    if all(k in values for k in('dac_chunks','dac_headers','pcm_chunks','pcm_headers','text')):
     terminal=json.loads((OUT/'native_terminal.json').read_text())
     need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],'Same native process terminal before retained-RAM host repair')
     prepared['LAST_CAPTURE']=dict(values)
    trace=trace.tb_next
   raise
 prepared['run']=retained_run
 return prepared


def main(preflight=False):
 global SCOPE
 failed=ROOT/'audit_v6366_current_cpu_blade_knife_audio_ram/failure.json'
 terminal=json.loads((failed.parent/'native_terminal.json').read_text())
 failure=json.loads(failed.read_text())
 need(not failure['passed'] and 'Every actual channel at every consecutive observed field'in failure['error'] and
      terminal['nativeExit']==0 and not terminal['hostDecodeErrors'], 'Preserve actual observer frame-assumption rejection and natural native terminal')
 parent=json.loads(original.PARENT.read_text())
 need(parent['passed'] and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Full current original renderer qualification intact')
 need(not OUT.exists() and not original.process_tools.census(),'Fresh actual job and empty native process census')
 # Source-only EOF premise, not an inference from absence of sound.
 sample=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 source=sample.read_text();section=source[source.index('void samples_device::sound_stream_update'):source.index('void samples_device::start(')]
 need('chan.source_num = -1;'in section and 'chan.source_len = 0;'not in section,
      'Original sample device marks EOF without clearing retained clip length')
 SCOPE=prepare()
 if preflight:
  with gzip.open(failed.parent/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
  result=state(text,'kano',2,original.original.current.expected())
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,existingActualChannelRows=result['channelRows'],completePCMCallbacks=result['completePCMCallbacks'])),flush=True);return
 return SCOPE['run']('kano',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Native terminal; actual PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=original.mix))
  raise SystemExit(1)
