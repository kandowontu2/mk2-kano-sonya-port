"""Exact audio-only host delta, unchanged whole guest and actual finite voices.

This proves the active-only timer source and the four real human playback
cases. It does not prove all AI, interruptions, campaign or release fidelity.
"""
import json,re
from pathlib import Path
import verify_sonya_launch_audio_v1489 as sound
ROOT=sound.ROOT;NAME='diagnostic_v1517_active_launch_timer'
OUT=ROOT/'audit_v1520_active_launch_timer_checked'
EXE_SHA='B0142C979C56C3906E8645D47CBE5CBE37D7AB33931A3447E3A6911DEC4911E8'
need=sound.need;sha=sound.sha;expected_guest=sound.expected_guest
human=sound.human;media=sound.media
def expected_source(old):
 changes=[
  ('\t\tm_mk2ks_battle_audio_timer->adjust(attotime::zero, 0, attotime::from_hz(60));',
   '\t\tm_mk2ks_battle_audio_timer->adjust(attotime::never);'),
  ('\tm_mk2ks_battle_health[slot] = 0;\n}',
   '\tm_mk2ks_battle_health[slot] = 0;\n'
   '\t// Silent selection, attract and gameplay need no extra scheduler callbacks.\n'
   "\t// Keep checking when the other physical player's launch is still owned.\n"
   '\tif (m_mk2ks_battle_audio_timer && !m_mk2ks_battle_actor[0] && !m_mk2ks_battle_actor[1])\n'
   '\t\tm_mk2ks_battle_audio_timer->adjust(attotime::never);\n}'),
  ('\t\t\t\t\t\tm_mk2ks_voices->start(channel, sample, false);',
   '\t\t\t\t\t\tm_mk2ks_voices->start(channel, sample, false);\n'
   '\t\t\t\t\t\tif (m_mk2ks_battle_audio_timer->expire() == attotime::never)\n'
   '\t\t\t\t\t\t\tm_mk2ks_battle_audio_timer->adjust(attotime::from_hz(60), 0, attotime::from_hz(60));')]
 for before,after in changes:
  need(old.count(before)==1,'Unique original whole-source timer anchor')
  old=old.replace(before,after)
 return old
def verify():
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  need(wanted is None or pins[key]==wanted,'Changed source/evidence '+key)
  return pins[key]
 priorpath=sound.OUT/'report.json';proof=json.loads(priorpath.read_text());pin(priorpath)
 need(proof['passed']and proof['wholeGuestIndependentlyReconstructed'],'Prior entire guest and original voice proof')
 for p,h in proof['inputHashes'].items():pin(p,h)
 folder=ROOT/NAME;build=json.loads((folder/'build-info.json').read_text(encoding='utf-8-sig'));pin(folder/'build-info.json')
 need(build['name']==NAME and build['prior_candidate']==sound.NAME and not build['game_data_changed'],'Host-only successor of v1473')
 need(build['executable_sha256']==EXE_SHA,'Exact compiled active-only candidate')
 for p,h in build['input_hashes'].items():pin(p,h)
 pin(folder/'mkport_candidate.exe',EXE_SHA);pin(folder/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
 oldbase=ROOT/sound.NAME/'input_sources/mame-mkp'
 newbase=folder/'input_sources/mame-mkp'
 old=(oldbase/'src/mame/midway/midtunit_m.cpp').read_text()
 new=(newbase/'src/mame/midway/midtunit_m.cpp').read_text()
 need(new==expected_source(old),'Entire machine source is exactly the three active-only timer edits')
 need(set(p.relative_to(oldbase)for p in oldbase.rglob('*')if p.is_file())==set(p.relative_to(newbase)for p in newbase.rglob('*')if p.is_file()),'Same complete compiled native source inventory')
 for p in oldbase.rglob('*'):
  if p.is_file():
   pin(p);q=newbase/p.relative_to(oldbase);pin(q)
   if p.name!='midtunit_m.cpp':need(p.read_bytes()==q.read_bytes(),'No driver/header/graphics/video/frontend/CPU change')
 # The actual local timer API leaves enabled=true on adjust(never); expiry is
 # the authoritative armed-state check. Callback self-adjustment suppresses
 # automatic periodic rescheduling in the original scheduler implementation.
 scheduler=ROOT/'mame-mkp/src/emu/schedule.cpp';header=ROOT/'mame-mkp/src/emu/schedule.h'
 pin(scheduler);pin(header);api=scheduler.read_text()
 adjust=api.split('void emu_timer::adjust(',1)[1].split('//  elapsed',1)[0]
 need('m_enabled = true;'in adjust and 'm_expire = m_start + start_delay;'in adjust and 'm_callback_timer_modified = true;'in adjust,'Original scheduler semantics actually checked')
 need('if (!m_callback_timer_modified)'in api and 'attotime expire() const noexcept { return m_expire; }'in header.read_text(),'Expiry query and callback adjustment semantics')
 guest,_,payload=expected_guest();need(payload==(folder/'roms/mk2ks/mk2ks.mdata').read_bytes(),'Entire unchanged payload')
 assets=json.loads((ROOT/'audit_v1469_sonya_launch_audio_assets/verification.json').read_text())
 cases=[]
 for move in ('square','bicycle'):
  for side in (1,2):
   case=ROOT/f'audit_v1519_channels_{move}_p{side}'
   meta=json.loads((case/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((case/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
   need(meta['exit_code']==0 and meta['candidate']==NAME and meta['executable_sha256']==EXE_SHA and meta['assistance']=='none'and not meta['cheats_enabled'],'Genuine matched physical human playback')
   need(before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Whole executed input manifest')
   for p,h in before.items():pin(p,h)
   need((case/'guest_maincpu.bin').read_bytes()==guest,'Every actual guest byte identical to independently reconstructed v1473')
   log=(case/'run.log').read_text(encoding='utf-8-sig');need(not re.search('LUA ERROR|fatal error|access violation',log,re.I),'No runtime failure')
   row=sound.verify_live_channel_log(log,move,side,assets,case.name)
   marks=[q for q in sound.sound_rows(log)if q['word']in ('6B00','6B01','6B02')]
   wanted=['6B00']if move=='square'else['6B01','6B02']
   need([q['word']for q in marks]==wanted,'Exactly the actual own native launch requests')
   cases.append(row)
   for p in case.rglob('*'):
    if p.is_file():pin(p)
 for p,h in [('mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),('mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'),('mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'),('mame-mkp/src/mame/midway/midtunit.h','256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644')]:pin(ROOT/p,h)
 pin(__file__)
 return dict(passed=True,candidate=NAME,wholeGuestIndependentlyReconstructed=True,wholeGuestIdenticalToV1473=True,hostSourceExactlyThreeTimerEdits=True,originalSchedulerSemanticsChecked=True,finiteBothSlotPlaybackCases=cases,inputHashes=pins,interruptionAccepted=False,CPUAccepted=False,fullPortAccepted=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite proof')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),candidate=NAME,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),channels=len(report.get('finiteBothSlotPlaybackCases',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
