"""Current native missed Ring audio through complete winner/round reset.

Whole original terminal-first RAM collector and native source waveform/ROM
model. Keep actual full-match chronology, original physical inputs and all
750 observed audio fields; stop before the later independent Bicycle cue.
"""
import argparse,code,gzip,inspect,json,traceback
from pathlib import Path
import capture_current_cpu_ring_audio_v6384 as prior
import capture_current_cpu_ring_miss_render_v6412 as physical

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6424_current_cpu_ring_miss_audio_ram'
PARENT=ROOT/'audit_v6415_current_cpu_ring_miss_render_checked/report.json'
LUA='mk2ks_current_cpu_ring_miss_audio_v6422.lua'
CHAIN=(LUA,'mk2ks_current_cpu_ring_miss_render_ram_v6410.lua','mk2ks_current_cpu_ring_render_ram_v6375.lua',
       'mk2ks_native_tomb_ram_v3624.lua',*physical.CHAIN[:6],
       'mk2ks_current_cpu_ring_audio_v6383.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')
SCOPE=None


def state(text,fighter,side,guest):
 need(fighter=='sonya' and side==2,'Actual true Sonya CPU with human Kano')
 with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:reference=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_','MK2_CPU_CHOICE_','MK2_CPU_SQUARE_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 need(rows(text)==rows(reference),'Entire original current miss physical/AI/RNG/HP/state/guard/choice/compound trace unchanged')
 result=physical.miss.full_phase(text,guest)
 begin=prior.mix.rows(text,'MK2_MAUDIO_BEGIN');end=prior.mix.rows(text,'MK2_MAUDIO_RESULT')
 ring=result['ring']['acceptedRings'][0]
 need(len(begin)==len(end)==1 and begin[0]['frame']==begin[0]['origin']==str(ring['start'])=='1879' and
      begin[0]['id']=='18' and end[0]['origin']=='1879' and end[0]['frame']=='3623','Actual true missed-Ring origin and same full-match terminal')
 channels=prior.mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==750*14 and {(int(r['frame']),int(r['channel']))for r in channels}==
      {(f,c)for f in range(1880,2630)for c in range(14)},'Every native channel at all750 video fields through full KO/winner/reset')
 for row in channels:
  need(row['writes']==row['loop']==row['paused']=='0' and row['assistance']=='none','Original passive unpaused/nonlooping channel inventory')
  if row['channel']!='0':need(row['length']=='0' and float(row['pos'])==0,'No unmodeled imported voice inside actual miss audio window')
 need(all(r['sample']=='4294967295' and float(r['pos'])>=int(r['length'])for r in channels if r['frame']=='2629'),
      'Every imported clip reaches original complete EOF/cleanup before unchanged audio terminal')
 pcm=prior.mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(pcm and all(r['bytes']=='3840' and 1879<=int(r['frame'])<=2629 for r in pcm) and
      int(pcm[0]['frame'])<=1880 and int(pcm[-1]['frame'])>=2628 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Complete native50Hz mixed sound window; no trimmed first/last callback')
 return dict(fullOriginalPhaseContract=result,wholeOriginalTrajectoryRows=len(rows(text)),nativeAudioOrigin=begin[0],
             nativeAudioTerminal=end[0],channelRows=len(channels),completePCMCallbacks=len(pcm),
             completeWinnerEOFAndRoundResetIncluded=True,laterBicycleSourceNotClaimed=True)


def dac_models(callbacks):
 need(650<callbacks<750,'Whole750-field missed-Ring audio duration')
 source=inspect.getsource(prior.original.dac_models)
 need(source.count('1600<callbacks<2100')==1,'Only complete native duration parameter differs')
 source=source.replace('1600<callbacks<2100','650<callbacks<750',1)
 scope=dict(prior.original.dac_models.__globals__)
 exec(compile(source,__file__+'::whole_original_DAC_gate_miss_duration','exec'),scope)
 return scope['dac_models'](callbacks)


def prepare():
 source=inspect.getsource(prior.prepare)
 changes={
  'audit_v6385_current_cpu_ring_audio_ram':'audit_v6424_current_cpu_ring_miss_audio_ram',
  "MK2KS_CPU_PAIR_APPROACH='original'":"MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
  "MK2KS_CPU_CONTINUATION_POLICY='retreat'":"MK2KS_CPU_CONTINUATION_POLICY='jump_on_launch'",
  'len(raw_proofs)==104':'len(raw_proofs)==77',
  'all104 original native scene callbacks':'all76 original physical scene callbacks plus one original choice screenshot now in RAM',
  'nativeCPUFullRingHitSequence=end[0]':'nativeCPUMissedRingSequence=end[0]',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Only actual existing miss policy/window/transport scope differs '+before)
  source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,PARENT=PARENT,LUA=LUA,CHAIN=CHAIN,physical=physical,
            state=state,dac_models=dac_models)
 exec(compile(source,__file__+'::whole_terminal_first_native_missed_Ring_audio','exec'),scope)
 return scope['prepare']()


def main(preflight=False):
 global SCOPE
 proof=json.loads(PARENT.read_text())
 need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Entire completed current miss raster/source/shadow proof unchanged')
 need(not OUT.exists() and not prior.process_tools.census(),'Fresh job, empty actual native census')
 SCOPE=prepare()
 if preflight:
  with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
  positive=physical.miss.full_phase(text,prior.original.current.expected())
  need(positive['ring']['acceptedRings'][0]==proof['phase'],'Full existing actual miss source phase remains admitted')
  print(json.dumps(dict(preflightPassed=True,newNativeBoots=0,completeCollectorCompiled=True,audioVideoFields=750)),flush=True);return
 return SCOPE['run']('sonya',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():prior.original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same actual native process terminal; full miss PCM/DAC still in RAM, do not rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=prior.mix))
  raise SystemExit(1)
