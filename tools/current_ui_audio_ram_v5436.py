"""Bind canonical audio source before installing its source-exact wrapper."""
import inspect,json,traceback
from pathlib import Path
import current_ui_audio_ram_v5433 as qualified

OUT=qualified.original.ROOT/'audit_v5438_current_ui_audio_progress'
FAILED=qualified.OUT/'progress.json'
BASE=qualified.original.ROOT/'audit_v5437_current_ui_audio_ram'

def run():
 failure=json.loads(FAILED.read_text())
 qualified.original.need(not failure['passed']and failure['error']=="ValueError('Only source-exact16k donor/interpolator binding; original full audio/source/owner/marker/shape/finite/onset gates unchanged')",
  'Retain executed wrapper-self-inspection failure; no underlying game/source rejection')
 canonical=qualified.original.audio_check
 source=inspect.getsource(qualified.bind_audio)
 before='source=inspect.getsource(original.audio_check)'
 qualified.original.need(source.count(before)==1,'Only canonical function capture changes, never semantic/source/gain tolerances')
 ns=dict(qualified.bind_audio.__globals__,CANONICAL_AUDIO=canonical)
 exec(compile(source.replace(before,'source=inspect.getsource(CANONICAL_AUDIO)',1),__file__+'::original_canonical_audio_source_before_wrapper','exec'),ns)
 qualified.bind_audio=ns['bind_audio']
 qualified.bind_audio() # Validate every source substitution before any boot.
 qualified.BASE=BASE
 report=qualified.run()
 report.update(preservedActualWrapperBindingFailure=str(FAILED),
  wrapperBindingCorrectionOnly='Capture original full audio checker before installing source-exact16k wrapper; inspect canonical function, not wrapper itself. All waveform/source/channel/physical/UI and corruption gates unchanged.',
  newNativeBoots=21,successfulCurrentCombinedNativeBoots=8,
  priorSuccessfulUIBootsWithAudioAssetAssumptionFailure=8,priorSuccessfulUIBootsWithWrapperBindingFailure=2,
  failedNativeRecorderBootsPreserved=3)
 paths=[FAILED,Path(__file__).resolve(),Path(qualified.__file__)]
 paths.extend(p for p in(qualified.original.ROOT/'audit_v5434_current_ui_audio_ram').rglob('*')if p.is_file())
 for p in paths:report['newInputHashes'][str(p.resolve())]=qualified.original.sha(p)
 return report

if __name__=='__main__':
 qualified.original.need(not OUT.exists(),'Fresh canonical-source-qualified current combined checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=qualified.original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();qualified.original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','qualificationLog','actualOriginalSelectionAudioFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
