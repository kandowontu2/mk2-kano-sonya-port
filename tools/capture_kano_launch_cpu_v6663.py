"""Whole real CPU-chosen ball/mirror match, new native guest and full RAM audio.

Same original physical inputs/RNG/health/state chronology and full motion gate.
One observed internal store-PC relocates by the source-authored96bits. No
scripted CPU choice, guest writes, saved state, early stop or public promotion.
"""
import argparse,code,gzip,inspect,json,re,traceback
from pathlib import Path
import capture_current_cpu_ball_audio_v6459 as prior
import kano_ball_launch_context_v6642 as candidate
import native_process_census_v6647 as process
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6664_kano_launch_cpu_native_audio'
PARENT=ROOT/'audit_v6660_kano_launch_progress_checked/report.json'
FULL_PHASE=None
SCOPE=None

def state(text,fighter,side,guest):
 need(fighter=='kano'and side==2,'Naturally selected real Kano17 CPU, physical slot2')
 with gzip.open(ROOT/'audit_v6293_current_kano_cpu_extended_ram/run.log.gz','rt')as file:old=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 expected=rows(old)
 selected=[s for s in expected if 'pc=FFFFE3A0 'in s]
 need(len(selected)==1 and selected[0].startswith('MK2_CPU_PAIR_FLAG frame=1827 ')and 'kind=action 'in selected[0]and
      'before=020B after=0602 'in selected[0]and 'op0=B00D op1=01F0 'in selected[0],
      'Exactly the native rebound action store inside the independently source-relocated roll')
 expected=[s.replace('pc=FFFFE3A0 ','pc=FFFFE400 ',1)if s==selected[0]else s for s in expected]
 need(rows(text)==expected,'Every real original physical/RNG/HP/round row retained; only the reviewed96-bit instruction-store PC relocates')
 positive=FULL_PHASE(text,guest)
 begin=prior.mix.rows(text,'MK2_MAUDIO_BEGIN');end=prior.mix.rows(text,'MK2_MAUDIO_RESULT')
 need(len(begin)==len(end)==1 and begin[0]['frame']==begin[0]['origin']=='1813'and begin[0]['id']=='17'and
      end[0]['frame']=='3615'and end[0]['origin']=='1813','Whole exact native pre-entry to original1800-field terminal window')
 binding=prior.mix.rows(text,'MK2_MAUDIO_BINDING')
 need(len(binding)==1803*2 and {(int(r['frame']),int(r['slot']))for r in binding}==
      {(f,s)for f in range(1813,3616)for s in(1,2)},'All native physical owner roles through contact, get-up, KO and round transition')
 return dict(fullOriginalPhysicalPhase=positive,wholeOriginalPhysicalRows=len(expected),onlyReviewedReboundPCRelocated=True,
             nativeAudioOrigin=begin[0],nativeAudioTerminal=end[0],physicalOwnerFields=len(binding),fullPortAcceptance=False)

def prepare():
 source=inspect.getsource(prior.prepare)
 # Preserve the entire original terminal-first collector, replacing only its
 # identity/context/source-result stage. Full waveform qualification is separate.
 before="source=inspect.getsource(prior.prepare)"
 need(source.count(before)==1,'Whole original collector-builder source retained')
 source=source.replace(before,before+"\n source=source.replace(\"len(full_scope['remaining'])==5\",\"len(full_scope['remaining'])==6\",1)",1)
 before="'audit_v6385_current_cpu_ring_audio_ram':'audit_v6460_current_cpu_ball_audio_ram'"
 need(source.count(before)==1,'Fresh compiled CPU audio evidence leaf only')
 source=source.replace(before,"'audit_v6385_current_cpu_ring_audio_ram':'audit_v6664_kano_launch_cpu_native_audio'",1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,PARENT=PARENT,SCOPE_PARENT=PARENT,state=state)
 exec(compile(source,__file__+'::whole_original6459_collector_builder','exec'),scope)
 prepared=scope['prepare']()
 # The original builder compiles a function. Capture its full generated text
 # by replacing only compile in that builder's namespace, never global builtins.
 captured=[]
 def remember(text,filename,mode):
  captured.append((text,filename));return compile(text,filename,mode)
 builder=inspect.getsource(prior.prior.prepare)
 changes={
  'audit_v6385_current_cpu_ring_audio_ram':'audit_v6664_kano_launch_cpu_native_audio',
  "MK2KS_TEST_BOOT_FRAME='613'":"MK2KS_TEST_BOOT_FRAME='605'",
  "MK2KS_CPU_PAIR_APPROACH='original'":"MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
  'len(raw_proofs)==104':'len(raw_proofs)==42',
  'all104 original native scene callbacks':'all42 original native scene callbacks',
  "len(full_scope['remaining'])==5":"len(full_scope['remaining'])==6",
 }
 for a,b in changes.items():need(builder.count(a)==1,'Whole original CPU duration/control/context adaptation '+a);builder=builder.replace(a,b,1)
 build_scope=dict(prior.prior.__dict__,__file__=__file__,compile=remember,physical=prior.physical,
                  OUT=OUT,PARENT=PARENT,SCOPE_PARENT=PARENT,LUA=prior.LUA,CHAIN=prior.CHAIN,state=state,dac_models=prior.original.dac_models)
 exec(compile(builder,__file__+'::remember_whole_original_native_capture','exec'),build_scope);build_scope['prepare']()
 need(len(captured)==1,'One entire original compiled terminal-first native collector')
 text=captured[0][0]
 edits={
  "'-samplepath',str(ROOT/'samples')":"'-samplepath',str(build/'samples')+';'+str(ROOT/'samples')",
  "'-samplerate','48000'":"'-samplerate','48000','-wavwrite','NUL'",
  "wi_result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n  wi=json.loads(wi_result.stdout)if wi_result.returncode==0 and wi_result.stdout.strip()else None":
  "jobs=process_tools.census();wi=next((dict(j,Name='mkport_candidate.exe')for j in jobs if j['ProcessId']==process.pid),None)",
 }
 for a,b in edits.items():need(text.count(a)==1,'Exact actual new samplepath/48k/native kernel identity adaptation '+a);text=text.replace(a,b,1)
 cut=text.index(' gate,fault,gate_sha=')
 text=text[:cut]+"\n need(all(sha(p)==h for p,h in pins.items()),'All actually executed source/new-candidate inputs intact')\n globals()['LAST_CAPTURE'].update(native=native)\n report=dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,inputHashes=pins,nativeTerminal=json.loads((folder/'native_terminal.json').read_text()),wholePhysicalContract=native,nativeRGBCallbacks=raw_proofs,completePCMCallbacks=len(pcm_chunks),sourceWaveformAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False)\n save(folder/'report.json',report)\n print(json.dumps(dict(passed=True,candidate=current.NAME,wholePhysicalContract=native,completePCMCallbacks=len(pcm_chunks),sourceWaveformAccepted=False)),flush=True)\n return globals()['LAST_CAPTURE']\n"
 final_scope=dict(prepared,current=candidate,__file__=__file__,process_tools=process,state=state,PARENT=PARENT,SCOPE_PARENT=PARENT)
 exec(compile(text,__file__+'::whole_native_CPU_collect_then_retain_RAM','exec'),final_scope)
 return final_scope

def main(preflight=False):
 global SCOPE,FULL_PHASE
 need(not process.census(),'No conflicting live native job')
 candidate.expected();FULL_PHASE=prior.phase_gate();SCOPE=prepare()
 if preflight:
  with gzip.open(ROOT/'audit_v6293_current_kano_cpu_extended_ram/run.log.gz','rt')as file:old=file.read()
  need(FULL_PHASE(old,prior.original.current.expected())['passed'],'Whole original independent CPU motion/state/source gate retained')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,fullOriginalCollectorCompiled=True)),flush=True);return
 need(not OUT.exists(),'Fresh immutable native CPU run, never restart a prior handle')
 return SCOPE['run']('kano',2)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');a=parser.parse_args()
 try:main(a.preflight)
 except Exception as error:
  result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():prior.original.save(OUT/'failure.json',result)
  print(json.dumps(result,indent=2),flush=True)
 if a.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
  code.interact(banner='Same naturally terminal CPU match; complete original PCM/DAC/ROM retained in RAM. No replay.',local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__)))
