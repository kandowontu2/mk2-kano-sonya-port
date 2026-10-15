"""Read-only reconciliation of independent historical ending receipts."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
pins={}
def read(n):
 p=R/n; pins[n]=sha(p); return json.loads(p.read_text())
visual=[];audio=[]
for slot,n in [(1,'audit_v5283_sonya_current_p1_original_ending_pages_checked'),(2,'audit_v5724_sonya_current_p2_original_ending_pages_checked')]:
 d=read(n+'/report.json');assert d['passed'] and d['identity']==18 and d['physicalSlot']==slot
 visual.append(dict(slot=slot,report=n,fullRGBPixelsCompared=d['actualFullRGBPixelsCompared'],fourEarlyLatePagesAccepted=True,allTransitionsOrExtraBlackPensAccepted=False))
for slot in (1,2):
 n=f'audit_v5745_sonya_p{slot}_ending_audio_window_checked';d=read(n+'/report.json')
 assert d['passed'] and d['identity']==18 and d['actualEntireNativeSourceClockAudioAccepted']
 audio.append({k:d[k] for k in ['physicalSlot','consecutiveNativeFields','actualChannelStates','exactStereoPCMFrames','actualFullWaveformSHA256','actualCompletePackets','noPostKOVoiceLoopOrStaleCharacterChannels','independentStockEndingChoreographyWaveformAccepted']})
p=read('audit_v5305_current_subzero_shadows_and_complete_sonya_ending_progress/progress.json')
s=next(x for x in p['actualCurrentP1CompleteNativeEndingContexts'] if x['fighter']=='sonya')
assert s['fullCurrentP1NativeRendererWindowAccepted'] and s['exactNativeVRAMRGBFields']==3042
component=read('audit_current_sonya_ending_component_transfer_checked/report.json')
soundpins=read('audit_v5738_current_ending_audio_source_checked/report.json')['inputHashes']
loaded=read('audit_current_loaded_sonya_ending_components_checked/report.json')
old=R/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp';current=R/'mame-mkp'
sound={}
for f in ['src/mame/shared/dcs.cpp','src/devices/sound/dmadac.cpp','src/devices/sound/dmadac.h','src/emu/sound.cpp','src/emu/sound.h','src/emu/attotime.h']:
 a,b=old/f,current/f
 references=sorted(set(h for p,h in soundpins.items() if p.replace('\\','/').endswith('/'+f)))
 sound[f]=dict(historicalAvailable=a.exists(),historicalPinnedSHA256=references,currentSHA256=sha(b),exactEquality=bool(references) and all(h==sha(b) for h in references))
out=R/'audit_current_historical_sonya_ending_scope_v2_checked';assert not out.exists();out.mkdir()
report=dict(historicalIndependentVisualReceiptsRetained=visual,historicalP1CompleteRendererWindow=s,historicalIndependentNativeAudioReceiptsRetained=audio,ownEndingComponentTransfer=component['endingComponentSourceTransferAccepted'],loadedCurrentComponentReport=loaded,soundDependencyComparisons=sound,correction='Campaign-matrix pixel/audio false flags describe those campaign receipts only; they do not negate independent ending pixel/native waveform receipts.',transferLimit='Exact own story/photo generator, native picture decoder, video renderer and CPU plus current loaded ending components support component transfer. Not a new current Sonya earned ending or independent stock choreography waveform acceptance; whole changed gameplay and broader contexts remain unproven.',inputHashes=pins,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(report=str(out/'report.json'),sound=sound,historicalPixelsEachSlot=406400,P1RendererFields=3042,audioStereoFrames=[x['exactStereoPCMFrames'] for x in audio])))
