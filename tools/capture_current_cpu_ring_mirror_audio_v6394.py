"""Whole current native Sonya mirror match sound, including KO/reset/Ring.

Reuse6384's complete terminal-first RAM carrier and original float32 native
DAC/resampler/winner-source prediction. Extend the passive window to all
1800 native match fields; preserve every physical/AI/RNG/health callback.
"""
import argparse,code,gzip,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_ring_audio_v6384 as prior
import capture_current_cpu_ring_mirror_render_v6389 as physical
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6395_current_cpu_ring_mirror_audio_ram'
PARENT=ROOT/'audit_v6392_current_cpu_ring_mirror_render_checked/report.json'
LUA='mk2ks_current_cpu_ring_mirror_audio_v6393.lua'
CHAIN=(LUA,*prior.CHAIN[1:])
SCOPE=None


def state(text,fighter,side,guest):
 need(fighter=='sonya' and side==2,'Actual both-Sonya mirror, native CPU slot2')
 with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:reference=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 need(rows(text)==rows(reference),'Entire original mirror physical/AI/RNG/HP/state/child/guard chronology unchanged')
 result=physical.full_phase(text,guest)
 begin=prior.mix.rows(text,'MK2_MAUDIO_BEGIN');end=prior.mix.rows(text,'MK2_MAUDIO_RESULT')
 cold=next(r for r in result['wholeNativeHealth'].items()if r[0]=='first')[1]
 need(len(begin)==len(end)==1 and begin[0]['frame']==begin[0]['origin']==str(cold)=='1823' and
      begin[0]['id']=='18' and end[0]['origin']=='1823' and end[0]['frame']=='3623',
      'Whole actual first-live-to-terminal mirror window, not post-winner Ring-only sound')
 channels=prior.mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==1801*14 and {(int(r['frame']),int(r['channel']))for r in channels}==
      {(f,c)for f in range(1823,3624)for c in range(14)},'Every video field and all14 original sample channels through native terminal')
 for row in channels:
  need(row['writes']==row['loop']==row['paused']=='0','Passive original unpaused nonlooping channels')
  if row['channel']!='0':need(row['length']=='0' and float(row['pos'])==0,'No unmodeled imported source')
 need(all(r['sample']=='4294967295' and float(r['pos'])>=int(r['length'])for r in channels if r['frame']=='3623'),
      'Every imported source retired normally at unchanged physical terminal')
 pcm=prior.mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(pcm and all(r['bytes']=='3840' and 1823<=int(r['frame'])<=3623 for r in pcm) and
      int(pcm[0]['frame'])<=1824 and int(pcm[-1]['frame'])>=3622 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Entire source50Hz sound window, no cached first sample or final callback omitted')
 return dict(fullOriginalPhaseContract=result,wholeOriginalTrajectoryRows=len(rows(text)),nativeAudioOrigin=begin[0],
             nativeAudioTerminal=end[0],channelRows=len(channels),completePCMCallbacks=len(pcm))


def prepare():
 source=inspect.getsource(prior.prepare)
 changes={
  'audit_v6385_current_cpu_ring_audio_ram':'audit_v6395_current_cpu_ring_mirror_audio_ram',
  "MK2KS_TEST_FIGHTER='kano'":"MK2KS_TEST_FIGHTER='sonya'",
  "len(raw_proofs)==104":"len(raw_proofs)==38",
  'all104 original native scene callbacks':'all38 original mirror native scene callbacks',
  'nativeCPUFullRingHitSequence=end[0]':'nativeCPUMirrorMatchAndBlockedRing=end[0]',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Only actual mirror identity/window/reference adaptation '+before)
  source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,PARENT=PARENT,LUA=LUA,CHAIN=CHAIN,physical=physical,state=state,
            dac_models=prior.original.dac_models)
 exec(compile(source,__file__+'::whole6384_terminal_first_full_mirror_match_audio','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE
 proof=json.loads(PARENT.read_text())
 need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Complete current mirror Ring renderer qualification unchanged')
 need(not OUT.exists() and not prior.process_tools.census(),'Fresh actual job, no live native process')
 SCOPE=prepare()
 if preflight:
  text=gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8').read()
  result=physical.full_phase(text,prior.original.current.expected())
  need(result['ring']['acceptedRings'][0]==proof['phase'],'Whole existing current physical branch qualified on actual source guest')
  print(json.dumps(dict(preflightPassed=True,newNativeBoots=0,wholeCollectorCompiled=True,completeMatchFields=1801)),flush=True);return
 return SCOPE['run']('sonya',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():prior.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same native process terminal; complete actual mirror PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=prior.mix))
  raise SystemExit(1)
