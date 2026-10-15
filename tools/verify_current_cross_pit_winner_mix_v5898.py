"""Full current Pit audio window, source-clock waveform and native cleanup.

Entire5785 window/channel/DAC/ROM/mixer/packet/port/ADSP gates retained.
Tomb-specific RNG/ceiling/cue/voice requirements are not Pit admission gates:
Pit-specific cinematic source ownership/phase/cue checks remain explicitly
pending. Complete wider stage audio, full raster and port acceptance stay false.
"""
import gzip,hashlib,inspect,json,re,struct,traceback,bisect
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import run_current_cross_pit_winner_mix_v5894 as host
import verify_current_tomb_winner_mix_v5785 as original
ROOT,need,sha=host.ROOT,host.need,host.sha
OUT=ROOT/'audit_v5899_current_cross_pit_winner_mix_checked'
once=host.once
observed=SimpleNamespace(**vars(host))
observed.runtime=SimpleNamespace(state=host.state)
observed.source=SimpleNamespace(OUT=host.source.OUT,previous=host.original.base.source.previous)
inventory=original.inventory
channel_source=inspect.getsource(original.channel_gate)
channel_scope=dict(vars(original),observed=observed)
exec(compile(channel_source,__file__+'::entire14channel_precise_native_clock','exec'),channel_scope)
channel_gate=channel_scope['channel_gate']

gate_source=inspect.getsource(original.gate)
for before,after in (
 ('observed.runtime.state.check_log(text,fighter,side,1,guest=guest)',
  'observed.runtime.state.check_log(text,fighter,side,6,guest=guest)'),
 ("native==live['nativeEarnedTombState']", "native==live['nativeEarnedPitState']"),
 ("native['earned_matches']==2", "native['earned_matches']==7"),
 ("first['victim_id']==str(identity)", "first['victim_id']==str(35-identity)"),
 ('actualCurrentHeldTombEnabledWaveformVoiceClockAndCleanupAccepted=True',
  'actualCurrentPitEnabledWaveformClockAndCleanupAccepted=True'),
 ('sourceQualifiedNativeBranch=phase,','nativePitPhysicalState=native,cinematicVictimAudioOwnershipAccepted=False,'),
 ('actualTrueWinnerMarkers=1,sourceSelectedInitialVictimVoice=base,actualVictimRole=role,',
  'actualTrueWinnerMarkers=1,sourceSelectedPitCinematicVoiceAndRoleAccepted=False,'),
 ('actualMixedRawPCMByteFaultSuiteAccepted=False,','actualMixedRawPCMByteFaultSuiteAccepted=True,'),
):gate_source=once(gate_source,before,after)
begin=gate_source.index(' phase=branches.branch(text,guest,fighter,side)')
end=gate_source.index(" fields=get('MK2_STAGE_FIELD');",begin)
gate_source=gate_source[:begin]+gate_source[end:]
begin=gate_source.index(' need(guest[off(0xff8ea000):off(0xff8eb490)]')
end=gate_source.index(' need(guest[off(0xffa13ba0):',begin)
gate_source=gate_source[:begin]+" for first,last in ((0xff85c300,0xff85c330),(0xff85c350,0xff85c4a0),(0xff85c4c0,0xff85c700),(0xff9e1290,0xff9e1480),(0xff82b800,0xff82bca0),(0xff80dcc0,0xff80de00)):\n  need(guest[off(first):off(last)]==stock[off(first):off(last)],'Whole original Pit phase/copy/impact/exit code unchanged')\n"+gate_source[end:]
begin=gate_source.index(" routes=audio('ROUTE');victim,main=first['victim'],first['victim_main']")
end=gate_source.index(" packets=audio('PACKET');",begin)
gate_source=gate_source[:begin]+gate_source[end:]
gate_source=once(gate_source,' winner=channel_gate(records,pcm,live,fighter)',
 " need(waveform['actualMixedRawPCMByteFaultSuiteAccepted']and len(waveform['actualRawMixedPCMFaultsRejected'])==4 and\n  len(waveform['actualMixedSourceOperationFaultsRejected'])==4 and all(r.get('differentChannelSamples',1)>0 for r in waveform['actualRawMixedPCMFaultsRejected'])and\n  all(r['differentChannelSamples']>0 for r in waveform['actualMixedSourceOperationFaultsRejected']),\n  'Entire effective actual first/last/omission PCM and native source-clock/gain/addition fault suites retained')\n winner=channel_gate(records,pcm,live,fighter)")
gate_scope=dict(vars(original),observed=observed,channel_gate=channel_gate,inventory=inventory)
exec(compile(gate_source,__file__+'::entire5785_Pit_window_channel_packet_mixer','exec'),gate_scope)
gate=gate_scope['gate'];gate.source=gate_source

run_source=inspect.getsource(original.run)
run_source=once(run_source,'audit_v5784_current_tomb_winner_mix_','audit_v5897_current_cross_pit_winner_mix_')
begin=run_source.index("   baseline=ROOT/f'audit_v5754_current_tomb_source_audio_")
end=run_source.index('   positive=gate(',begin)
run_source=run_source[:begin]+run_source[end:]
for line in (
 "    ('MK2_MAUDIO_ROUTE','a0','00000000','wrong original victim voice selector','return_pc=FF8EAED0'),\n",
 "    ('MK2_MAUDIO_ROUTE','owner','00000000','wrong native victim voice owner','return_pc=FF8EAED0'),\n",
):run_source=once(run_source,line,'')
run_source=once(run_source,"(0xff8ea000,'original whole Tomb predecessor code'),(0xff8ea9e0,'original Tomb effect caller')",
 "(0xff85c350,'original whole Pit fall code'),(0xff85c4c0,'original Pit impact code')")
run_source=once(run_source,'need(len(faults)==31','need(len(faults)==29')
begin=run_source.index('   cue=cues.gate(')
end=run_source.index('   need(not any(p.suffix',begin)
run_source=run_source[:begin]+"   earned=observed.state.actual_faults(text,fighter,side,guest)\n   need(len(earned)==12 and earned==live['actualEarnedStateFaultsRejected'],'Entire actual12earned/Pit-action/801cleanup fault evidence agrees')\n   positive.update(actualAudioSourceWindowFaultsRejected=faults,actualEarnedStateFaultsRejected=earned,capture=str(folder),pairedNOSAMPLESRunAccepted=False)\n"+run_source[end:]
for before,after in (
 ('actualCurrentBothCharactersBothSidesHeldTombEnabledWinnerMixAccepted=True',
  'actualCurrentBothCharactersBothSidesPitEnabledWinnerMixAccepted=True'),
 ('actualSourceAudioFaultsRejected=124,actualEarnedStateFaultsRejected=48,actualBranchFaultsRejected=16,',
  'actualSourceAudioFaultsRejected=116,actualEarnedStateFaultsRejected=48,actualBranchFaultsRejected=0,'),
 ('actualMixedRawPCMByteFaultSuiteAccepted=False,',
  'actualMixedRawPCMByteFaultSuiteAccepted=True,actualRawMixedPCMFaultsRejected=16,actualMixedSourceOperationFaultsRejected=16,pairedNOSAMPLESRunAccepted=False,cinematicVictimAudioOwnershipAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,'),
):run_source=once(run_source,before,after)
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,observed=observed,OUT=OUT,gate=gate)
exec(compile(run_source,__file__+'::entire5785_Pit_window_and29actual_faults','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current Pit source-waveform matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
