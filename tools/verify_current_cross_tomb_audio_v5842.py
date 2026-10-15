"""Complete current opposite-character Tomb window/source/voice qualification.

Reuse whole held5785 and random5810 gates, whole33 real window faults,
whole5774 general cue/queue faults and whole actual269phase/role faults.
The winner sample remains performer's; victim identity is deliberately separate.
No inferred branch coverage, duplicate NOSAMPLES parity or full-port acceptance.
"""
import gzip,hashlib,inspect,json,re,struct,traceback
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import bisect
import run_current_cross_tomb_audio_v5838 as host
import verify_current_tomb_winner_mix_v5785 as held
import verify_current_random_tomb_winner_mix_v5810 as dropped
import verify_current_tomb_cue_sources_v5774 as original_cues
import run_current_random_tomb_winner_mix_v5808 as original_phase_faults
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_v5843_current_cross_tomb_audio_checked'
once=host.once

phase_fault_source=inspect.getsource(original_phase_faults.random_phase_faults)
phase_scope=dict(vars(original_phase_faults),pressed=host.state,random_branch=host.branches.branch)
exec(compile(phase_fault_source,__file__+'::whole5808_actual_cross_phase_faults','exec'),phase_scope)
phase_faults=phase_scope['random_phase_faults']
observed=SimpleNamespace(**{k:getattr(host,k)for k in ('ROOT','need','sha','current','model','collector','voice_models')if hasattr(host,k)})
observed.pressed=host.state
observed.runtime=SimpleNamespace(state=host.state)
observed.random_branch=host.branches.branch
observed.random_phase_faults=phase_faults
observed.voice_models=host.branches.voice_models
observed.source=SimpleNamespace(OUT=host.source.OUT,
 previous=SimpleNamespace(held=SimpleNamespace(previous=host.base.source.previous)))
branches=host.branches
inventory=dropped.inventory
channel_scope=dict(vars(dropped),observed=observed)
channel_source=inspect.getsource(dropped.channel_gate)
exec(compile(channel_source,__file__+'::whole5785_precise_channel_gate','exec'),channel_scope)
channel_gate=channel_scope['channel_gate']

def gate_model(falling):
 original=dropped if falling else held
 code=inspect.getsource(original.gate)
 code=once(code,"identity=17 if fighter=='kano'else 18;other=3-side;records=inventory(text)",
  "identity=17 if fighter=='kano'else 18;victim_identity=18 if fighter=='kano'else 17;other=3-side;records=inventory(text)")
 code=once(code,"first['victim_id']==str(identity)","first['victim_id']==str(victim_identity)")
 first=code.index(" routes=audio('ROUTE');victim,main=first['victim'],first['victim_main']")
 last=code.index(" packets=audio('PACKET');",first)
 victim_block=code[first:last]
 need(victim_block.count('identity')==6,'Exactly six original victim-only identity uses; performer/winner untouched')
 code=code[:first]+victim_block.replace('identity','victim_identity')+code[last:]
 if not falling:
  code=once(code,"need(phase['passed']and not phase['nativeDrop']and phase['actualNativeRandomValue']>=50,",
   "need(phase==live['sourceQualifiedNativeBranch']and phase['passed']and not phase['nativeDrop']and phase['actualNativeRandomValue']>=50,")
 namespace=dict(vars(original),observed=observed,branches=branches,channel_gate=channel_gate)
 exec(compile(code,__file__+'::whole_native_gate_actual_cross_'+str(falling),'exec'),namespace)
 fn=namespace['gate'];fn.source=code;return fn

held_gate=gate_model(False)
drop_gate=gate_model(True)

def gate(text,meta,live,fighter,side,guest,stock,expected_sound):
 falling=live['sourceQualifiedNativeBranch']['nativeDrop']
 result=(drop_gate if falling else held_gate)(text,meta,live,fighter,side,guest,stock,expected_sound)
 waveform=live['waveform']
 need(waveform['actualMixedRawPCMByteFaultSuiteAccepted']and
  len(waveform['actualRawMixedPCMFaultsRejected'])==4 and len(waveform['actualMixedSourceOperationFaultsRejected'])==4 and
  all(r.get('differentChannelSamples',1)>0 for r in waveform['actualRawMixedPCMFaultsRejected'])and
  all(r['differentChannelSamples']>0 for r in waveform['actualMixedSourceOperationFaultsRejected']),
  'Full actual first/last/omission PCM and whole source-clock/gain/addition fault suite for every actual branch')
 result.update(actualMixedRawPCMByteFaultSuiteAccepted=True,victimIdentity=18 if fighter=='kano'else 17,
  actualCurrentOppositeCharacterTombEnabledAudioAccepted=True)
 return result

def cue_models():
 code=inspect.getsource(original_cues.gate)
 code=once(code,"identity=17 if fighter=='kano'else 18",
  "identity=17 if fighter=='kano'else 18;victim_identity=18 if fighter=='kano'else 17")
 code=once(code,"field['id']==field['victim_id']==str(identity)",
  "field['id']==str(identity)and field['victim_id']==str(victim_identity)")
 code=once(code,"r['id']==str(identity),'Literal cue owns real performer or victim task'",
  "r['id']==str(victim_identity if victim else identity),'Literal cue owns real performer or victim task'")
 # The remaining references after this boundary all belong to the victim.
 first=code.index('  elif caller==0xff8eaed0:')
 last=code.index('  else:raise ValueError',first)
 block=code[first:last]
 need(block.count('identity')==7,'Seven original gender/role/victim references, particle checks retained')
 code=code[:first]+block.replace('identity','victim_identity')+code[last:]
 code=once(code,"branch='pressed'if pressed else'held'","branch='unpressed native RNG drop'if pressed else'held'")
 namespace=dict(vars(original_cues))
 exec(compile(code,__file__+'::whole5774_actual_cross_cues','exec'),namespace)
 fn=namespace['gate'];fn.source=code
 exec(compile(inspect.getsource(original_cues.faults),__file__+'::whole5774_real_cue_faults','exec'),namespace)
 return fn,namespace['faults']

run_source=inspect.getsource(dropped.run)
run_source=once(run_source,"pre['wholeEarnedRandomContractSHA256']==observed.pressed.CONTRACT_SHA256",
 "pre['wholeCrossEarnedContractSHA256']==observed.pressed.CONTRACT_SHA256")
run_source=once(run_source,'audit_v5809_current_random_tomb_winner_mix_','audit_v5841_current_cross_tomb_winner_mix_')
run_source=once(run_source,"live=json.loads((folder/'audio_live_source_model.json').read_text())",
 "live=json.loads((folder/'audio_live_source_model.json').read_text())\n   falling=live['sourceQualifiedNativeBranch']['nativeDrop']\n   live=dict(live,sourceQualifiedNativeRandomBranch=live['sourceQualifiedNativeBranch'],actualRandomPhaseFaultsRejected=phase_faults(gzip.open(folder/'run.log.gz','rt').read(),guest,fighter,side)if falling else [])")
run_source=once(run_source,"cue=cg(text,guest,stock,fighter,side,True)","cue=cg(text,guest,stock,fighter,side,falling)")
run_source=once(run_source,"cue['actualGeneralCalls']==12 and len(cf(text,guest,stock,fighter,side,True))==25",
 "cue['actualGeneralCalls']==(12 if falling else 21)and len(cf(text,guest,stock,fighter,side,falling))==(25 if falling else 20)")
run_source=once(run_source,'actualNativeBranchFaultsRejected=observed.random_phase_faults(text,guest,fighter,side)',
 'actualNativeBranchFaultsRejected=observed.random_phase_faults(text,guest,fighter,side)if falling else []')
run_source=once(run_source,"positive['actualLateVictimVoiceFaultsRejected']=vf(text,fighter,side,guest)",
 "positive['actualLateVictimVoiceFaultsRejected']=vf(text,fighter,side,guest)if falling else {}")
run_source=once(run_source,"len(positive['actualNativeBranchFaultsRejected'])==4 and len(positive['actualLateVictimVoiceFaultsRejected'])==8",
 "len(positive['actualNativeBranchFaultsRejected'])==(4 if falling else 0)and len(positive['actualLateVictimVoiceFaultsRejected'])==(8 if falling else 0)")
run_source=once(run_source,'actualCurrentBothCharactersBothSidesRandomTombEnabledWinnerMixAccepted=True',
 'actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted=True')
run_source=once(run_source,'actualEarnedStateFaultsRejected=48,actualBranchFaultsRejected=16',
 "actualEarnedStateFaultsRejected=48,actualBranchFaultsRejected=sum(len(c['actualNativeBranchFaultsRejected'])for c in cases)")
run_source=once(run_source,'actualLateVictimVoiceFaultsRejected=32',
 "actualLateVictimVoiceFaultsRejected=sum(len(c['actualLateVictimVoiceFaultsRejected'])for c in cases)")
run_source=once(run_source,"for p in (Path(__file__),Path(branches.__file__),prepath,ROOT/'mk2/mk2-maincpu.bin'):",
 "for p in (Path(__file__),Path(branches.__file__),Path(held.__file__),Path(dropped.__file__),Path(original_cues.__file__),Path(original_phase_faults.__file__),prepath,ROOT/'mk2/mk2-maincpu.bin'):")
run_source=once(run_source,'actualSavedGainSnapshotsAvailable=False,actualMixedRawPCMByteFaultSuiteAccepted=True,',
 "actualSavedGainSnapshotsAvailable=False,actualMixedRawPCMByteFaultSuiteAccepted=True,\n  actualNativeHeldContexts=sum(not c['sourceQualifiedNativeBranch']['nativeDrop']for c in cases),\n  actualNativeRandomDropContexts=sum(c['sourceQualifiedNativeBranch']['nativeDrop']for c in cases),\n  pairedNOSAMPLESRunAccepted=False,")
run_scope=dict(vars(dropped),__file__=__file__,observed=observed,branches=branches,
 OUT=OUT,gate=gate,cue_models=cue_models,phase_faults=phase_faults,held=held,dropped=dropped,
 original_cues=original_cues,original_phase_faults=original_phase_faults)
exec(compile(run_source,__file__+'::whole5810_matrix_actual_cross_branches','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete opposite-character matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
