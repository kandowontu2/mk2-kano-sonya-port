"""Entire5842 audio/window/channel/voice gates for missing cross Tomb timings.

Whole33 actual audio/window faults and all original general cue, native branch,
phase, late-voice, ROM/DAC and raw PCM/source-operation evidence retained. The
whole physical input sequence is also compared to the independent cold timing
trial; five actual declared-delay faults must reject with positives restored.
"""
import gzip,hashlib,inspect,json,re,struct,traceback
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import verify_current_cross_tomb_audio_v5842 as original
import run_current_cross_tomb_timing_audio_v5877 as host
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_v5882_current_cross_tomb_timing_audio_checked'
once=host.once
held,dropped,original_cues,original_phase_faults=original.held,original.dropped,original.original_cues,original.original_phase_faults
branches=host.branches
observed=SimpleNamespace(**vars(original.observed))
observed.collector=host.collector
observed.source=SimpleNamespace(OUT=host.source.OUT,previous=original.observed.source.previous)
inventory=original.inventory
phase_faults=original.phase_faults
channel_source=original.channel_source
channel_scope=dict(vars(original),observed=observed)
exec(compile(channel_source,__file__+'::whole_precise14channel_clock','exec'),channel_scope)
channel_gate=channel_scope['channel_gate']
gate_factory_source=inspect.getsource(original.gate_model)
factory_scope=dict(vars(original),observed=observed,branches=branches,channel_gate=channel_gate)
exec(compile(gate_factory_source,__file__+'::whole5842_held_and_random_cross_gate_factory','exec'),factory_scope)
held_gate=factory_scope['gate_model'](False)
drop_gate=factory_scope['gate_model'](True)

def physical_gate(text,guest,fighter,side):
 positive=host.qualify_timing(text,guest,fighter,side)
 profile=host.selected_profile(fighter,side)
 reference=Path(profile['capture'])
 journal=json.loads(host.PROFILE_PATH.read_text())
 need(sha(reference/'run.log.gz')==journal['newInputHashes'][str(reference/'run.log.gz')],
  'Exact independent completed timing capture still source-bound')
 with gzip.open(reference/'run.log.gz','rt')as reader:earlier=reader.read()
 tags=('MK2_STAGE_BOOT ','MK2_STAGE_INPUT ','MK2_STAGE_DAMAGE ','MK2_STAGE_MATCH ',
  'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')
 actual=[l for l in text.splitlines()if l.startswith(tags)]
 expected=[l for l in earlier.splitlines()if l.startswith(tags)]
 need(actual==expected and actual,'Every actual normal selection, full-health earned KO, paid match, finishing button and native terminal matches independent cold input trial')
 return dict(passed=True,physicalCommandDelay=positive['physicalCommandDelay'],
  independentCapture=positive['independentCapture'],exactPhysicalRecords=len(actual),nativeRNGStateUntouched=True)

def timing_faults(text,guest,fighter,side):
 positive=physical_gate(text,guest,fighter,side)
 row=next(l for l in text.splitlines()if l.startswith('MK2_TOMB_TIMING_CONFIGURATION '))
 changes=[('actual timing row omitted',text.replace(row+'\n','',1)),
  ('actual timing row duplicated',text.replace(row,row+'\n'+row,1))]
 for name,key,value in [('actual physical delay corrupted','delay',str(positive['physicalCommandDelay']+1)),
  ('actual timing assistance corrupted','assistance','injected'),('actual timing writes corrupted','writes','1')]:
  bad,n=re.subn(r'\b'+key+r'=[^\s]+',key+'='+value,row,count=1)
  need(n==1 and bad!=row,'Effective actual delay provenance mutation')
  changes.append((name,text.replace(row,bad,1)))
 result=[]
 for name,bad in changes:
  need(bad!=text,'Every actual timing counterexample nonvacuous')
  try:physical_gate(bad,guest,fighter,side)
  except Exception as error:result.append(dict(label=name,rejectedBy=str(error)))
  else:raise ValueError('Corrupt actual input-delay provenance accepted: '+name)
  need(physical_gate(text,guest,fighter,side)==positive,'Entire original actual physical-input positive restored')
 need(len(result)==5,'All five actual declared timing faults rejected')
 return result

gate_source=once(inspect.getsource(original.gate),' result.update(actualMixedRawPCMByteFaultSuiteAccepted=True,',
 ' result.update(actualPhysicalInputTimingProof=physical_gate(text,guest,fighter,side),actualMixedRawPCMByteFaultSuiteAccepted=True,')
gate_scope=dict(vars(original),observed=observed,held_gate=held_gate,drop_gate=drop_gate,physical_gate=physical_gate)
exec(compile(gate_source,__file__+'::whole5842_full_audio_plus_independent_physical_timing','exec'),gate_scope)
gate=gate_scope['gate']
cue_models=original.cue_models
run_source=once(original.run.source,'audit_v5841_current_cross_tomb_winner_mix_','audit_v5880_current_cross_tomb_timing_winner_mix_')
run_source=once(run_source,"positive['actualLateVictimVoiceFaultsRejected']=vf(text,fighter,side,guest)if falling else {}",
 "positive['actualLateVictimVoiceFaultsRejected']=vf(text,fighter,side,guest)if falling else {}\n   positive['actualPhysicalTimingFaultsRejected']=timing_faults(text,guest,fighter,side)\n   positive['actualOriginalPCIONativeBranchFaultsRejected']=branches.faults(text,guest,fighter,side)")
run_source=once(run_source,'actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted=True',
 'actualCurrentBothCharactersBothSidesMissingCrossTombEnabledWinnerMixAccepted=True')
run_source=once(run_source,'actualEarnedStateFaultsRejected=48,',
 'actualPhysicalTimingFaultsRejected=20,actualOriginalPCIONativeBranchFaultsRejected=16,actualEarnedStateFaultsRejected=48,')
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,OUT=OUT,observed=observed,branches=branches,
 gate=gate,phase_faults=phase_faults,cue_models=cue_models,timing_faults=timing_faults)
exec(compile(run_source,__file__+'::whole5842_missing_cross_timing_matrix','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable entire missing-cross audio matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
