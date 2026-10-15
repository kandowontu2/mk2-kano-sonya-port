"""Only source-exact native snapshot API return binding; keep failed attempt."""
import json,traceback
from pathlib import Path
import current_ui_audio_ram_v5427 as original

OUT=original.ROOT/'audit_v5432_current_ui_audio_progress'
FAILED=original.OUT/'progress.json'
LUA=original.ROOT/'mk2ks_current_ui_audio_ram_v5430.lua'
BASE=original.ROOT/'audit_v5431_current_ui_audio_ram'

def run():
 failure=json.loads(FAILED.read_text())
 original.need(not failure['passed']and failure['error']=="ValueError('Actual current native warning-free terminal0 and complete guest')",'Preserve actual first native recorder assertion failure')
 source=original.ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp';text=source.read_text()
 snapshot=text[text.index('video_type["snapshot_pixels"] ='):text.index('video_type["speed_factor"]')]
 size=text[text.index('video_type["snapshot_size"] ='):text.index('video_type["snapshot_pixels"] =')]
 original.need('return sol::make_reference(s, sol::stack_reference(s, -1));'in snapshot and
  'return std::make_tuple(width, height);'in size,'Actual complete native API returns only pixels; dimensions have separate method')
 original.LUA=LUA;original.BASE=BASE
 report=original.run()
 report.update(preservedActualNativeRecorderFailure=str(FAILED),
  recorderCorrectionOnly='Actual compiled snapshot_pixels returns one buffer; snapshot_size returns dimensions. Original controller/timing, actual native displayed pixels, full guest, audio source/channel/waveform and all original UI gates unchanged.',
  newNativeBoots=11,successfulCurrentCombinedNativeBoots=8,failedNativeRecorderBootsPreserved=3)
 paths=[FAILED,Path(__file__).resolve(),source,original.ROOT/'mk2ks_current_ui_audio_ram_v5427.lua']
 paths.extend(p for p in(original.ROOT/'audit_v5428_current_ui_audio_ram').rglob('*')if p.is_file())
 for p in paths:report['newInputHashes'][str(p.resolve())]=original.sha(p)
 return report

if __name__=='__main__':
 original.need(not OUT.exists(),'Fresh immutable source-correct native UI/audio evidence')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=original.COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();original.save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','qualificationLog')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
