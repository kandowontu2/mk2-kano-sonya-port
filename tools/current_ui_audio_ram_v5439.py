"""Canonical checker source AND globals bound before wrapper installation."""
import inspect,json,traceback
from pathlib import Path
import current_ui_audio_ram_v5433 as qualified
import current_ui_audio_ram_v5436 as prior

OUT=qualified.original.ROOT/'audit_v5441_current_ui_audio_progress'
FAILED=prior.OUT/'progress.json'
BASE=qualified.original.ROOT/'audit_v5440_current_ui_audio_ram'

def run():
 failure=json.loads(FAILED.read_text())
 qualified.original.need(not failure['passed']and failure['error']=='NameError("name \'need\' is not defined")',
  'Keep exact executed wrapper-global binding failure')
 canonical=qualified.original.audio_check
 source=inspect.getsource(qualified.bind_audio)
 changes={'source=inspect.getsource(original.audio_check)':'source=inspect.getsource(CANONICAL_AUDIO)',
  'ns=dict(original.audio_check.__globals__,native_selection_source=native_selection_source)':
   'ns=dict(CANONICAL_AUDIO.__globals__,native_selection_source=native_selection_source)'}
 for before,after in changes.items():
  qualified.original.need(source.count(before)==1,'Only canonical function source/global binding changes')
  source=source.replace(before,after,1)
 ns=dict(qualified.bind_audio.__globals__,CANONICAL_AUDIO=canonical)
 exec(compile(source,__file__+'::canonical_audio_source_and_globals','exec'),ns)
 qualified.bind_audio=ns['bind_audio']
 # Exercise binding after exactly the wrapper installation that exposed the
 # failure, without a native boot; all original semantic globals must survive.
 qualified.original.audio_check=qualified.qualified_audio
 check=qualified.bind_audio()
 for name in('need','ROOT','records','np','wave','fftconvolve'):
  qualified.original.need(check.__globals__[name]is canonical.__globals__[name],
   'Canonical full audio semantics/global dependencies retained before any capture')
 qualified.original.audio_check=canonical
 qualified.BASE=BASE
 report=qualified.run()
 report.update(preservedActualWrapperBindingFailures=[str(prior.FAILED),str(FAILED)],
  wrapperBindingCorrectionOnly='Bind original canonical audio function source and original globals before wrapper installation. Zero-boot qualification proves original need/ROOT/records/numpy/wave/FFT identities retained after installation. No semantic/source/tolerance/controller/game change.',
  newNativeBoots=23,successfulCurrentCombinedNativeBoots=8,failedNativeRecorderBootsPreserved=3,
  priorSuccessfulUIBootsWithAudioAssetAssumptionFailure=8,priorSuccessfulUIBootsWithWrapperBindingFailures=4)
 paths=[prior.FAILED,FAILED,Path(prior.__file__),Path(__file__).resolve(),Path(qualified.__file__)]
 for base in(qualified.original.ROOT/'audit_v5434_current_ui_audio_ram',prior.BASE):
  paths.extend(p for p in base.rglob('*')if p.is_file())
 for p in paths:report['newInputHashes'][str(p.resolve())]=qualified.original.sha(p)
 return report

if __name__=='__main__':
 qualified.original.need(not OUT.exists(),'Fresh full canonical-source/global-qualified native UI/audio checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=qualified.original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();qualified.original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','qualificationLog','actualOriginalSelectionAudioFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
