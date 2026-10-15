"""Preserve failed6529 recorder; use existing source-qualified5430 pixel API.

snapshot_pixels() returns the buffer only; snapshot_size() supplies dimensions.
Entire physical UI policy, full pixel/state/negative gates remain unchanged.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
import check_repaired_selection_pixels_v6528 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_v6532_repaired_selection_transport_ram'
OUT=ROOT/'audit_v6533_repaired_selection_transport_checked'
LUA=ROOT/'mk2ks_current_ui_audio_ram_v5430.lua'
FAILURE=ROOT/'audit_v6530_repaired_selection_pixels_checked/report.json'

def bindings():
 source=inspect.getsource(prior.bindings)
 a='scope=dict(original.__dict__,__file__=__file__,current=candidate,BASE=BASE,host=host,time=time)'
 b='scope=dict(original.__dict__,__file__=__file__,current=candidate,BASE=BASE,host=host,time=time,LUA=LUA)'
 need(source.count(a)==1,'Only already qualified native API observer binding')
 scope=dict(prior.__dict__,__file__=__file__,BASE=BASE,LUA=LUA)
 exec(compile(source.replace(a,b,1),__file__+'::entire_original_capture_correct_native_API','exec'),scope)
 return scope['bindings']()

def main():
 failure=json.loads(FAILURE.read_text());need(not failure['passed'] and
      failure['error']=="ValueError('Actual current native warning-free terminal0 and complete guest')",'Keep actual unsupported multi-return pixel API recorder failure')
 native=ROOT/'audit_v6529_repaired_selection_pixels_ram/kano_p1_samples'
 terminal=json.loads((native/'native_terminal.json').read_text())
 need(terminal['exitCode']==0 and not terminal['observationErrors'] and '[LUA ERROR]' in (native/'stderr.log').read_text(),
      'Original game terminal successful, native observer assertion remains an actual failed qualification')
 source=(ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp').read_text()
 body=source[source.index('video_type["snapshot_pixels"] ='):source.index('video_type["speed_factor"]')]
 size=source[source.index('video_type["snapshot_size"] ='):source.index('video_type["snapshot_pixels"] =')]
 need('return sol::make_reference(s, sol::stack_reference(s, -1));' in body and 'return std::make_tuple(width, height);' in size,
      'Actual native snapshot API returns one buffer with separate dimensions')
 lua=LUA.read_text();need('local raw=manager.machine.video:snapshot_pixels()' in lua and
      'local width,height=manager.machine.video:snapshot_size()' in lua,'Existing corrected observer uses actual source-defined API')
 factory=inspect.getsource(prior.main)
 a="pins=dict(meta['input_hashes']);prior=ROOT/'audit_v3736_guarded_native_ui_qualified_ram_checked/report.json'"
 b="pins=dict(meta['input_hashes']);pins.update({str(p.resolve()):sha(p) for p in (LUA,Path(previous.__file__),FAILURE,ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp')});prior=ROOT/'audit_v3736_guarded_native_ui_qualified_ram_checked/report.json'"
 need(factory.count(a)==1,'Pin corrected native observer and preserved actually executed failed collector/report')
 scope=dict(prior.__dict__,__file__=__file__,BASE=BASE,OUT=OUT,bindings=bindings,LUA=LUA,FAILURE=FAILURE,previous=prior)
 exec(compile(factory.replace(a,b,1),__file__+'::whole_original_UI_pixel_state_fault_gate','exec'),scope)
 report=scope['main']();report.update(preservedNativeRecorderFailure=str(FAILURE),
      nativeObserverCorrectionOnly='Use existing source-qualified5430 observer; snapshot_pixels returns one buffer, snapshot_size returns dimensions. No physical input/game/source/pixel gate change.')
 for p in native.rglob('*'):
  if p.is_file():
   h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Compress original failed recorder evidence unchanged')
   report['inputHashes'][str(p.resolve())]=sha(p)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable corrected native UI recorder result')
 try:report=main()
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),completedCases=prior.COMPLETED,fullPortAcceptance=False)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving exact UI result compression')
 print(json.dumps({k:v for k,v in report.items()if k not in ('cases','completedCases','inputHashes','qualificationLog','actualWholeFrameBackings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
