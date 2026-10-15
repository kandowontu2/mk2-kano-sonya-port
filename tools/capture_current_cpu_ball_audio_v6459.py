"""Whole original6293 ball match, source DAC/winner audio; no new build/media."""
import argparse,code,gzip,inspect,json,re,traceback
from pathlib import Path
import capture_current_cpu_ring_audio_v6384 as prior
import capture_current_cpu_ball_render_v6452 as physical
from current_cpu_ball_context_v6451 import phase_gate
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
original,mix,process_tools=prior.original,prior.mix,prior.process_tools
OUT=ROOT/'audit_v6460_current_cpu_ball_audio_ram'
PARENT=ROOT/'audit_v6455_current_cpu_ball_render_checked/report.json'
SCOPE_PARENT=prior.SCOPE_PARENT
LUA='mk2ks_current_cpu_ball_audio_v6458.lua'
CHAIN=(LUA,'mk2ks_current_kano_cpu_extended_ram_v6290.lua',
 'mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v1940.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua','mk2ks_physical_p2_cpu_knife_trace_v1955.lua',
 'mk2ks_physical_p2_cpu_choice_trace_v3303.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')
SCOPE=None
FULL_PHASE=None


def state(text,fighter,side,guest):
 need(fighter=='kano'and side==2,'True Kano17 CPU, physical slot2')
 with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:reference=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 need(rows(text)==rows(reference),'Entire original6293 physical/AI/RNG/HP/state/round chronology unchanged')
 result=FULL_PHASE(text,guest)
 marks=mix.rows(text,'MK2_MAUDIO_BEGIN');ends=mix.rows(text,'MK2_MAUDIO_RESULT')
 need(len(marks)==len(ends)==1 and marks[0]['frame']==marks[0]['origin']=='1813'and marks[0]['id']=='17'and
      ends[0]['frame']=='3615'and ends[0]['origin']=='1813','Exact pre-entry origin and unchanged complete native physical terminal')
 channels=mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==1803*14 and {(int(r['frame']),int(r['channel']))for r in channels}==
      {(f,c)for f in range(1813,3616)for c in range(14)},'All14 channels every complete physical field')
 for r in channels:
  need(r['writes']==r['loop']==r['paused']=='0','Passive unpaused nonlooping channels')
  if r['channel']!='0':need(r['length']=='0'and float(r['pos'])==0,'No unmodeled imported source')
 need(all(r['sample']=='4294967295'and float(r['pos'])>=int(r['length'])for r in channels if r['frame']=='3615'),
      'Every imported source retired at genuine physical terminal')
 pcm=mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(pcm and all(r['bytes']=='3840'and 1813<=int(r['frame'])<=3615 for r in pcm)and
      int(pcm[0]['frame'])<=1814 and int(pcm[-1]['frame'])>=3614 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Whole consecutive50Hz window, no callback or tail trimming')
 bindings=mix.rows(text,'MK2_MAUDIO_BINDING')
 need(len(bindings)==1803*2 and {(int(r['frame']),int(r['slot']))for r in bindings}==
      {(f,s)for f in range(1813,3616)for s in(1,2)},'Complete independent physical role provenance')
 return dict(fullOriginalPhaseContract=result,wholeOriginalTrajectoryRows=len(rows(text)),nativeAudioOrigin=marks[0],
             nativeAudioTerminal=ends[0],channelRows=len(channels),physicalBindingRows=len(bindings),completePCMCallbacks=len(pcm))


def prepare():
 source=inspect.getsource(prior.prepare)
 changes={
  'audit_v6385_current_cpu_ring_audio_ram':'audit_v6460_current_cpu_ball_audio_ram',
  "MK2KS_TEST_BOOT_FRAME='613'":"MK2KS_TEST_BOOT_FRAME='605'",
  "MK2KS_CPU_PAIR_APPROACH='original'":"MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
  'len(raw_proofs)==104':'len(raw_proofs)==42',
  'all104 original native scene callbacks':'all42 original native scene callbacks',
 }
 for a,b in changes.items():
  need(source.count(a)==1,'One original collector context adaptation '+a);source=source.replace(a,b,1)
 scope=dict(prior.__dict__,__file__=__file__,physical=physical,OUT=OUT,PARENT=PARENT,SCOPE_PARENT=SCOPE_PARENT,
            LUA=LUA,CHAIN=CHAIN,state=state,dac_models=original.dac_models)
 exec(compile(source,__file__+'::whole6384_ball_context','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE,FULL_PHASE
 parent=json.loads(PARENT.read_text())
 need(parent['passed']and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Whole current ball art/shadow acceptance unchanged')
 need(not OUT.exists()and not process_tools.census(),'Fresh job; empty authoritative native census')
 FULL_PHASE=phase_gate();SCOPE=prepare()
 if preflight:
  with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
  result=FULL_PHASE(text,original.current.expected())
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True,phase=result)),flush=True);return
 return SCOPE['run']('kano',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same naturally terminal native process; PCM/DAC retained in RAM, no replay.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=mix))
  raise SystemExit(1)
