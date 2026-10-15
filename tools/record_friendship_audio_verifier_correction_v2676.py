"""Retain the failed audio harness and exact missing-voice rejection correction.
No PCM threshold, reference, actual capture, gameplay or source build changed.
"""
import json
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
OUT=ROOT/'audit_v2677_friendship_audio_verifier_correction_checked'

def need(ok,label):
 if not ok:raise ValueError(label)

def verify():
 pins={}
 def pin(path,wanted=None):
  actual=launch.sha(path);need(wanted is None or actual==wanted,'Immutable executed audio evidence '+str(path));pins[str(path)]=actual
 bad=ROOT/'tools/verify_current_friendship_audio_v2670.py';good=ROOT/'tools/verify_current_friendship_audio_v2672.py'
 pin(bad,'DF64EBACAF5BDC22E3AEB9D54BD38BF4625C7A7BC945E1E9236C2160E9CD6E97')
 pin(good,'6D4522A306C6100D955042F02ED23DEDADFA76AB45518EDCC2EE2D78009D77EC')
 before=bad.read_text().rstrip()+'\n'
 old="outcomes.append(reject(lambda:native.fit_overlap(y,s,c,o),label,('Source waveform gain or voice missing','Wrong waveforms, lost tails or overlapping voice restarted')))"
 new="outcomes.append(reject(lambda:native.fit_overlap(y,s,c,o),label,('Source waveform gain or voice missing','Wrong waveforms, lost tails or overlapping voice restarted')+(('Friendship samples inaudible',)if label=='missing_audible_voice'else ())))"
 need(before.count(old)==1,'Exact original expected-rejection site')
 expected=before.replace('audit_v2671_current_friendship_audio_checked','audit_v2673_current_friendship_audio_checked').replace(old,new)
 need(expected==good.read_text().rstrip()+'\n','Only output leaf and sole missing-voice expected rejection corrected')
 failed=ROOT/'audit_v2671_current_friendship_audio_checked/report.json';pin(failed,'9F0DDF1D91BCDDF5F1C74913D0DD36E2C4AC01FBC2B7E93E122A80B4B765A65B')
 failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error']=="ValueError('Intended audio invariant rejection for missing_audible_voice: Friendship samples inaudible')"and 'check(energy>0' in failure['traceback'],'Actual native zero-energy rejection, not a game/audio failure')
 path=ROOT/'audit_v2673_current_friendship_audio_checked/report.json';pin(path);current=json.loads(path.read_text())
 need(current['passed']and current['originalPCMAndAudibleOverlapAccepted']and current['audibleCues']==80 and current['audibleGroups']==28 and current['rejectedSpecificAudioCounterexamples']==36 and not current['gameChanged']and not current['fullPortAcceptance'],'Fully repeated current original-PCM and overlap controls')
 for file,wanted in current['inputHashes'].items():pin(file,wanted)
 need(all(case['finalUnmodifiedControlPassed']for case in current['cases'].values()),'All four untouched audio controls repeated after corruptions')
 pin(Path(__file__).resolve());launch.module_pins(pins)
 return dict(passed=True,failedOriginalSource=str(bad),failedOriginalReport=str(failed),failedOriginalAccepted=False,
  actualFailureWasExpectedZeroEnergyRejection=True,onlyMissingVoiceExpectedRejectionAndOutputLeafChanged=True,
  PCMThresholdsUnchanged=True,executedSourcesCapturesAndReferencesNeverEdited=True,repeatedAcceptedProof=str(path),
  repeatedCurrentAudioCues=80,repeatedCurrentAudioGroups=28,repeatedSpecificAudioCounterexamples=36,
  gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable audio-harness correction boundary')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
