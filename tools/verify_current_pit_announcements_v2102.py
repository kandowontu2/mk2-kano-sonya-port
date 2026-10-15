"""Current natural Pit winner announcements and whole-mix non-regression.

The actual owned native winner issues Kano/Sonya's own marker, and the complete
source donor announcement is audible at that marker with the original route
gain. Complete PCM matches prior earned fixtures byte-for-byte. This is not
correctness certification of all DCS effects, victim voices or stage audio.
"""
import json,re,struct
from pathlib import Path
import verify_current_interrupt_v1870 as launch
import inspect_current_move_audio_v1408 as media
ROOT=launch.ROOT
OUT=ROOT/'audit_v2102_current_pit_announcements_checked'
SPECS=(
 ('kano',1,17,'audit_v2094_current_kano_p1_pit_nextscreen_fullscene','audit_v2100_current_kano_p1_pit_movie_checked','audit_v1714_kano_pit_p1',0xfffe),
 ('sonya',2,18,'audit_v2094_current_sonya_p2_pit_nextscreen_fullscene','audit_v2100_current_sonya_p2_pit_movie_checked','audit_v1714_sonya_pit_p2',0xfffd))

def verify():
 pins=launch.source_pins();cases=[]
 source=ROOT/launch.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 config=ROOT/launch.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 text=source.read_text()
 assert 'set_volume(0, 0.30f)'in text and '"mk2ksvoice", 0.70'in config.read_text()
 assert 'unsigned const sample = (data == 0xfffc) ? 0 : (data == 0xfffb) ? 1 : (data == 0xfffe) ? 2 : 3;'in text
 assert 'm_mk2ks_voices->start(0, sample);'in text
 assert 'extend_parameters(0xff8224a0, { 0xff8209e0 }, 0xfe, 0xfd);'in text
 pins[str(source)]=launch.sha(source);pins[str(config)]=launch.sha(config)
 for fighter,side,identity,leaf,checked,oldleaf,word in SPECS:
  case=ROOT/leaf;path=ROOT/checked/'report.json';proof=json.loads(path.read_text())
  assert proof['passed']and not proof['fullPortAcceptance']
  for file,wanted in proof['inputHashes'].items():
   assert launch.sha(file)==wanted;pins[file]=wanted
  pins[str(path)]=launch.sha(path)
  meta=json.loads((case/'result.json').read_text(encoding='utf-8-sig'))
  assert(meta['winner'],meta['side'],meta['candidate'])==(fighter,side,launch.NAME)
  log=(case/'run.log').read_text(encoding='utf-8-sig')
  rows=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',r))for r in log.splitlines()if r.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
  marks=[r for r in rows('FLOOR_SOUND')if int(r['value'],16)in(0xfffd,0xfffe)]
  assert len(marks)==1
  mark=marks[0];frame=int(mark['frame'])
  assert int(mark['value'],16)==word and mark['mask']=='FFFF'and mark['at']=='01D01030'and mark['pc']=='FFFB7140'and mark['mode']=='5'
  states=[r for r in rows('FLOOR_STATE')if int(r['frame'])==frame];assert len(states)==1
  state=states[0]
  assert int(state['winner'])==side and int(state[f'roster{side}'])==identity and int(state[f'state{side}'])==1
  # Original Pit announces after retiring BOTH normal fighter pointers.
  # Bind ownership to the actual earned performer before this native clear,
  # never manufacture a live actor at an announcement-only native phase.
  assert int(state['p1'],16)==int(state['p2'],16)==0 and frame>proof['movie']['physicalPointerRetirement']
  assert int(state[f'main{side}'],16)>0 and int(state[f'health{side}'])==161 and int(state[f'health{3-side}'])==0
  assert proof['nativeState']['earned_matches']==7 and proof['nativeState']['native_action']=='FF8BDDE0'
  first=rows('FLOOR_STATE')[0]
  assert int(first[f'p{side}'],16)>0 and int(first[f'roster{side}'])==identity and int(first[f'health{side}'])==161
  assert state[f'main{side}']==first[f'main{side}']
  mixpath=case/'native_mix.wav';oldpath=ROOT/oldleaf/'native_mix.wav'
  assert launch.sha(mixpath)==meta['mix_sha256']==launch.sha(oldpath),'Entire natural input-only native PCM remains byte-exact'
  pins[str(oldpath)]=launch.sha(oldpath)
  asset=ROOT/'samples/mk2ks'/f'{fighter}_wins.wav'
  assert any(Path(file).resolve()==asset.resolve()and wanted==launch.sha(asset)for file,wanted in meta['input_hashes'].items())
  rate,channels,mix=media.pcm(mixpath);assert(rate,channels)==(48000,2)
  fit=media.voice(mix,rate,asset,float(mark['seconds']))
  # No relaxed gain/correlation/chronology threshold: use the existing full
  # source-announcement fit contract unchanged.
  cases.append(dict(fighter=fighter,side=side,id=identity,ownedWinnerFrame=frame,nativeMarker=f'{word:04X}',
   completePriorNaturalPCMByteExact=True,sourceAsset=str(asset),completeSourceAnnouncementFit=fit,
   fullStageAudioAcceptance=False))
 launch.module_pins(pins)
 return dict(passed=True,candidate=launch.NAME,cases=cases,currentPitOwnedWinnerAnnouncementsAccepted=True,
  allStageAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 assert not OUT.exists(),'Preserve executed evidence'
 try:report=verify()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
