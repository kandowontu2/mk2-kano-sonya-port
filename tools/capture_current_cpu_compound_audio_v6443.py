"""Original5324 complete match audio; terminal-first RAM carrier, no playable edits."""
import argparse,code,gzip,inspect,json,sys,traceback
from pathlib import Path
import capture_current_cpu_ring_audio_v6384 as prior
import capture_current_cpu_compound_render_v6433 as physical
import current_cpu_compound_audio_model_v6444 as mix
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6445_current_cpu_compound_audio_ram'
PARENT=ROOT/'audit_v6436_current_cpu_compound_render_checked/report.json'
LUA='mk2ks_current_cpu_compound_audio_v6442.lua'
CHAIN=(LUA,'mk2ks_current_cpu_ring_miss_audio_v6422.lua','mk2ks_current_cpu_ring_miss_render_ram_v6410.lua',
 'mk2ks_current_cpu_ring_render_ram_v6375.lua','mk2ks_native_tomb_ram_v3624.lua',
 'mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v3302.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
 'mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_physical_p2_cpu_ring_trace_v2013.lua',
 'mk2ks_current_cpu_ring_mirror_audio_v6393.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')
SCOPE=None


def state(text,fighter,side,guest):
 need(fighter=='sonya'and side==2,'True human Kano17/physical CPU Sonya18')
 with gzip.open(ROOT/'audit_v6439_current_cpu_compound_render_ram/run.log.gz','rt',encoding='utf-8')as f:reference=f.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_','MK2_CPU_CHOICE_','MK2_CPU_SQUARE_')
 sequence=lambda v:[s for s in v.splitlines()if s.startswith(prefixes)]
 need(sequence(text)==sequence(reference),'Entire qualified5324 physical/AI/RNG/HP/state/choice trajectory unchanged')
 phase=physical.full_phase(text,guest)
 begin=mix.rows(text,'MK2_MAUDIO_BEGIN');end=mix.rows(text,'MK2_MAUDIO_RESULT')
 need(len(begin)==len(end)==1 and begin[0]['frame']==begin[0]['origin']=='1823'and begin[0]['id']=='18'and
      end[0]['frame']=='3623'and end[0]['origin']=='1823','Whole first-live-to-terminal audio, no trimming')
 channels=mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==1801*14 and {(int(r['frame']),int(r['channel']))for r in channels}==
      {(f,c)for f in range(1823,3624)for c in range(14)},'All14 channels at every video field')
 for r in channels:
  need(r['writes']==r['loop']==r['paused']=='0','Passive unpaused nonlooping channel')
  if r['channel']not in('0','12','13'):need(r['length']=='0'and float(r['pos'])==0,'No unmodeled imported source')
 need(all(r['sample']=='4294967295'for r in channels if r['frame']=='3623'),'No imported source still playing at natural match terminal')
 callbacks=mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(callbacks and all(r['bytes']=='3840'and 1823<=int(r['frame'])<=3623 for r in callbacks)and
      int(callbacks[0]['frame'])<=1824 and int(callbacks[-1]['frame'])>=3622 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(callbacks,callbacks[1:])),
      'Entire original50Hz PCM window')
 return dict(fullOriginalPhaseContract=phase,wholeOriginalTrajectoryRows=len(sequence(text)),nativeAudioOrigin=begin[0],
             nativeAudioTerminal=end[0],channelRows=len(channels),completePCMCallbacks=len(callbacks))


def prepare():
 source=inspect.getsource(prior.prepare)
 changes={'audit_v6385_current_cpu_ring_audio_ram':'audit_v6445_current_cpu_compound_audio_ram',
  "MK2KS_CPU_PAIR_APPROACH='original'":"MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
  "MK2KS_CPU_CONTINUATION_POLICY='retreat'":"MK2KS_CPU_CONTINUATION_POLICY='jump_on_launch'",
  'len(raw_proofs)==104':'len(raw_proofs)==77','all104 original native scene callbacks':'all77 original native scene callbacks',
  'nativeCPUFullRingHitSequence=end[0]':'nativeCPUFullCompoundMatch=end[0]'}
 for before,after in changes.items():
  need(source.count(before)==1,'Whole terminal-first collector adaptation '+before);source=source.replace(before,after,1)
 # The reference folder has the full continuous renderer trace, not the older Ring trace.
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,PARENT=PARENT,LUA=LUA,CHAIN=CHAIN,
            physical=physical,mix=mix,state=state,dac_models=prior.original.dac_models)
 exec(compile(source,__file__+'::whole6213_complete_compound_audio','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE
 proof=json.loads(PARENT.read_text())
 need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Current complete compound renderer proof unchanged')
 need(not OUT.exists()and not prior.process_tools.census(),'Fresh actual job; no live emulator')
 SCOPE=prepare()
 if preflight:
  need(SCOPE['run'].__globals__['mix']is mix,'Whole collector binds complete multi-source model')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,completeMatchFields=1801)),flush=True);return
 return SCOPE['run']('sonya',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():prior.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same naturally terminal process: complete PCM/DAC remains in RAM; do not rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=sys.modules[__name__],mix=mix))
  raise SystemExit(1)
