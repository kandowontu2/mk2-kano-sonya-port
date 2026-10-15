"""Independent whole guest, original-cue assets, real-input state and channel proof.

No all-move/AI/interruption/campaign/release acceptance is implied. Normal mixed
PCM proves the actual early launch audio; read-only live channel positions prove
finite full-length playback independently of variable native DCS contact voices.
"""
import hashlib,json,re,struct,sys,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import verify_native_grab_audio_v1415 as prior
import verify_human_special_matrix as human
import inspect_current_move_audio_v1408 as media
ROOT=prior.ROOT;NAME='diagnostic_v1473_sonya_launch_audio';OUT=ROOT/'audit_v1488_sonya_launch_audio_checked'
need=prior.need
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def inserted_routine(old,start,limit,insertions):
 """Relocate only declared original absolute branch operands around additions."""
 blob=old[start:limit];end=(len(blob.rstrip(b'\xff'))+1)//2*2
 if start==0xff940:
  # The final JA operand ends in FFFFh, which is instruction data, not
  # allocation padding. Original square code is exactly 0x11c bytes.
  end=0x11c
  need(blob[end:]==b'\xff'*(len(blob)-end) and blob[end-6:end-4]==struct.pack('<H',0xc080),'Original final square recovery JA and untouched padding')
 blob=bytearray(blob[:end]);points=[]
 for marker,addition in insertions:
  at=bytes(blob).find(marker);need(at>=0 and bytes(blob).count(marker)==1,'Unique original native instruction anchor')
  points.append((at+len(marker),addition))
 points.sort();low=0xff800000+start*8;high=low+len(blob)*8;branches=[]
 for at in range(0,len(blob)-3,2):
  target=struct.unpack_from('<I',blob,at)[0]
  if low<=target<high:
   opcode=struct.unpack_from('<H',blob,at-2)[0] if at>=2 else None
   need(opcode in (0xc080,0xca80,0xcb80,0xc880,0xc980) or (opcode==0xc380 and low+(at-2)*8==0xfff9b260),'Only identified original branches, including the source/disassembly-backed bicycle ceiling JAHI, may relocate')
   destination=(target-low)//8
   need(all(destination!=point for point,extra in points),'Insertion must not ambiguously replace a native branch label')
   translated=target+sum(len(extra)*8 for point,extra in points if point<destination)
   struct.pack_into('<I',blob,at,translated);branches.append(dict(original=f'{target:08X}',relocated=f'{translated:08X}'))
 rebuilt=b'';cursor=0
 for point,extra in points:rebuilt+=bytes(blob[cursor:point])+extra;cursor=point
 rebuilt+=bytes(blob[cursor:]);need(len(rebuilt)<=limit-start,'Existing owned native code allocation')
 return rebuilt+b'\xff'*(limit-start-len(rebuilt)),branches

def expected_guest():
 old,_,payload=prior.expected_guest();new=bytearray(old)
 def marker(command):return prior.movi(0,command)+struct.pack('<3H',0x0580,0x1030,0x01d0)
 branches={}
 for name,start,end,action,extra in [('square',0xff940,0xffb40,0x207,marker(0x6b00)),('bicycle',0xf3480,0xf3a00,0x204,marker(0x6b01)+marker(0x6b02))]:
  rebuilt,branches[name]=inserted_routine(old,start,end,[(prior.movi(1,action)+prior.call(0xff877ba0),extra)])
  new[start:end]=rebuilt
 return bytes(new),branches,payload
def events(log):return [re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',q)for q in log.splitlines()if q.startswith('MK2_HSPECIAL_')]
def sound_rows(log):return media.records(log,'MK2_HAUDIO_SOUND')
def mixed_launch(folder,baseline,move):
 rate,ch,a=media.pcm(folder/'game_mix.wav');oldrate,oldch,b=media.pcm(baseline/'game_mix.wav')
 need((rate,ch)==(oldrate,oldch)==(48000,2),'Same actual mixed PCM format')
 count=min(len(a),len(b));delta=(a[:count]-b[:count]).mean(axis=1)
 log=(folder/'run.log').read_text(encoding='utf-8-sig');markers=[q for q in sound_rows(log)if q['word'].startswith('6B')]
 names=['sonya_square_launch']if move=='square'else['sonya_bicycle_launch','sonya_bicycle_cry']
 voices=[media.pcm(ROOT/'samples/mk2ks'/(n+'.wav'))[2][:,0]for n in names]
 # Bicycle's independent native DCS contact variants are not time-aligned
 # waveform oracles. Check the complete uncontaminated launch before contact.
 length=len(voices[0])if move=='square'else 8000
 voice=np.zeros(length)
 for v in voices:voice[:min(length,len(v))]+=v[:length]
 at=round(float(markers[0]['seconds'])*rate);start=at-480
 need(not np.any(delta[:start]),'No mixed PCM change before actual launch')
 region=delta[start:at+480+length];product=fftconvolve(region,voice[::-1],mode='valid')
 index=int(np.argmax(product));actual=region[index:index+length]
 gain=float(np.dot(actual,voice)/np.dot(voice,voice));corr=float(np.dot(actual,voice)/(np.linalg.norm(actual)*np.linalg.norm(voice)))
 need(corr>.995 and .69<gain<.71 and abs(start+index-at)<=3,'Own original cues audible at the real marker and native route level')
 return dict(correlation=corr,gain=gain,offsetSamples=start+index-at,verifiedSeconds=length/rate,fullCuePCMMatched=move=='square',scope='Actual normal mixed PCM; bicycle only before variable native contact sounds')
def verify():
 pins={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path.resolve());actual=pins.setdefault(key,sha(path));need(wanted is None or actual==wanted,'Input hash changed: '+key)
 folder=ROOT/NAME;compiled=json.loads((folder/'build-info.json').read_text(encoding='utf-8-sig'));pin(folder/'build-info.json')
 need(compiled['name']==NAME and compiled['prior_candidate']==prior.NAME and compiled['executable_sha256']=='42151DB8134D8D68A2DD68DB5E1B81EA5B3CB0298DCDB5DAA8748421C6CA0209','Exact new candidate')
 for p,h in compiled['input_hashes'].items():pin(p,h)
 pin(folder/'mkport_candidate.exe',compiled['executable_sha256']);pin(folder/'roms/mk2ks/mk2ks.mdata',compiled['payload_sha256'])
 proofpath=ROOT/'audit_v1415_native_grab_audio_checked/report.json';proof=json.loads(proofpath.read_text());pin(proofpath)
 need(proof['passed']and proof['wholeGuestIndependentlyReconstructed'],'Prior independent native guest proof')
 for p,h in proof['inputHashes'].items():pin(p,h)
 assetpath=ROOT/'audit_v1469_sonya_launch_audio_assets/verification.json';assets=json.loads(assetpath.read_text());pin(assetpath)
 need(assets['all_15_launch_channel_commands_pcm_identical_within_cue']and len(assets['assets'])==3,'Original five-channel oracle per cue')
 for p,h in assets['checked_inputs'].items():pin(p,h)
 for name,item in assets['assets'].items():pin(item['file'],item['sha256'])
 # Original own Sonya table/group bindings, not another fighter's voices.
 original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();pin(ROOT/'mk3/mk3-maincpu.bin')
 need(struct.unpack_from('<I',original,(0xffaa8f90-0xff800000)//8)[0]==0xffaa92f0,'Actual Sonya original voice table')
 originalcases={}
 for move,command in [('square','0212'),('bicycle','02D0')]:
  ref=ROOT/('audit_v1470_original_audio_square'if move=='square'else'audit_v1407_original_audio_bicycle')
  meta=json.loads((ref/'result.json').read_text(encoding='utf-8-sig'));pin(ref/'result.json')
  need(meta['exit_code']==0 and meta['assistance']=='none'and meta['writes']==0,'Actual original-game reference')
  for p,h in meta['input_hashes'].items():pin(p,h)
  text=(ref/'run.log').read_text(encoding='utf-8-sig');pin(ref/'run.log')
  requests=media.records(text,'MK3_SPECIAL_AUDIO_SOUND');commands=[]
  for high,low in zip(requests[::2],requests[1::2]):
   need(high['pc']=='FFAA88B0'and low['pc']=='FFAA8920'and high['frame']==low['frame']and high['a8']==low['a8'],'Whole actual native original command pairs')
   commands.append(high['byte']+low['byte'])
  need(command in commands and (move!='bicycle'or'0899'in commands),'Original launch cue really occurs')
  originalcases[move]=dict(commands=commands,guestWrites=0)
 guest,branches,payload=expected_guest();need(payload==(folder/'roms/mk2ks/mk2ks.mdata').read_bytes(),'Exact unchanged payload')
 # Compile changes outside the two native routines are audio-only.
 newbase=folder/'input_sources/mame-mkp/src/mame/midway';oldbase=ROOT/prior.NAME/'input_sources/mame-mkp/src/mame/midway'
 new=(newbase/'midtunit_m.cpp').read_text();old=(oldbase/'midtunit_m.cpp').read_text()
 remove=["\tm_mk2ks_battle_audio_timer = timer_alloc(FUNC(midtunit_state::mk2ks_battle_audio_tick), this);\n\tsave_item(NAME(m_mk2ks_battle_actor));\n\tsave_item(NAME(m_mk2ks_battle_main));\n\tsave_item(NAME(m_mk2ks_battle_health));\n", "\t// Original Sonya voice group 4 (0212h): own square-wave launch.\n\tsquare_movi(0, 0x6b00); square_code({0x0580, 0x1030, 0x01d0});\n", "\t// Original Sonya voice groups 3 and 5: short launch plus bicycle cry.\n\tleg_movi(0,0x6b01); leg_code({0x0580,0x1030,0x01d0});\n\tleg_movi(0,0x6b02); leg_code({0x0580,0x1030,0x01d0});\n"]
 # Whole function-boundary deltas are source-pinned and separately inspected.
 for begin,end in [('void midtunit_state::mk2ks_battle_audio_stop','uint16_t midtunit_state::midtunit_sound_state_r'),('\t\t\t\tif (m_mk2ks_voices && data >= 0x6b00','\t\t\t\tif (m_mk2ks_voices && data >= 0x6aa0'),('\tif (m_mk2ks_battle_audio_timer)','\n\t/* reset sound */')]:
  start=new.index(begin);stop=new.index(end,start);block=new[start:stop]
  need('write_word'not in block and 'write_dword'not in block and 'write_u'not in block,'Audio handler/timer cannot change guest state')
  if begin.startswith('\tif '):block=block.rstrip('\n')+'\n'
  remove.append(block)
 for block in remove:need(new.count(block)==1,'One declared source block');new=new.replace(block,'')
 need(new==old,'Whole machine source differs only by declared native cues/audio lifecycle')
 driver=(newbase/'midtunit.cpp').read_text()
 driver=driver.replace('\t"sonya_chicken_af", "sonya_chicken_96",\n\t"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", nullptr','\t"sonya_chicken_af", "sonya_chicken_96", nullptr')
 driver=driver.replace('\t// Two additional channels per physical player keep both simultaneous\n\t// bicycle launch cues independent from the opponent and announcements.\n\tm_mk2ks_voices->set_channels(14);','\tm_mk2ks_voices->set_channels(10);')
 need(driver==(oldbase/'midtunit.cpp').read_text(),'Whole driver only three own assets and four independent channels')
 header=(newbase/'midtunit.h').read_text()
 start=header.index('\t// Independent, finite original Sonya launch voices.')
 stop=header.index('\n',header.index('\tvoid mk2ks_battle_audio_stop(',start))+1
 need(header[:start]+header[stop:]==(oldbase/'midtunit.h').read_text(),'Whole header only audio ownership/timer declarations')
 for name in ('midtunit_v.cpp','midtunit_v.h','mk2ks_native_picture.h'):need((newbase/name).read_bytes()==(oldbase/name).read_bytes(),'Unchanged native visual implementation')
 cases=[]
 for move,side,air in [(m,s,False)for m in('square','bicycle','leg','choke')for s in(1,2)]+[('square',s,True)for s in(1,2)]:
  case=ROOT/(f'audit_v1475_human_launch_{move}'+('_air'if air else'')+f'_p{side}')
  meta=json.loads((case/'result.json').read_text(encoding='utf-8-sig'));pin(case/'result.json');before=json.loads((case/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  need(meta['exit_code']==0 and meta['candidate']==NAME and meta['executable_sha256']==compiled['executable_sha256']and meta['assistance']=='none'and not meta['cheats_enabled'],'Unassisted real candidate capture')
  need(before==meta['input_hashes']and all(before.get(p)==h for p,h in compiled['input_hashes'].items()),'Whole matched runtime manifest')
  for p,h in before.items():pin(p,h)
  need((case/'guest_maincpu.bin').read_bytes()==guest,'Every byte of the independently reconstructed actual guest')
  log=(case/'run.log').read_text(encoding='utf-8-sig');state=human.verify_log(log,move,side,air)
  baseline=ROOT/(f'audit_v1478_baseline_square_air_p{side}'if air else f'audit_v1398_human_audio_square_p{side}'if move=='square'else f'audit_v1414_human_audio_{move}_p{side}')
  oldlog=(baseline/'run.log').read_text(encoding='utf-8-sig');need(events(log)==events(oldlog),'Every prior actual input/identity/action/pose/contact/recovery event unchanged')
  for name in ('special_before.png','special_recovered.png','special_final.png'):
   need((case/'snap'/name).read_bytes()==(baseline/'snap'/name).read_bytes(),'Entire actual prior screen byte-exact');pin(baseline/'snap'/name)
  marks=[q for q in sound_rows(log)if q['word']in('6B00','6B01','6B02')]
  wanted=['6B00']if move=='square'else['6B01','6B02']if move=='bicycle'else[]
  need([q['word']for q in marks]==wanted and all(int(q['frame'])==state['entry']for q in marks),'Exactly own native startup cue markers')
  row=dict(case=case.name,move=move,side=side,air=air,state=state,wholeGuestExact=True,priorFullScreensByteMatched=3,priorNativeEventsExact=True)
  if move in('square','bicycle'):row['mixedAudio']=mixed_launch(case,baseline,move)
  else:need((case/'game_mix.wav').read_bytes()==(baseline/'game_mix.wav').read_bytes(),'Unchanged actual grab PCM')
  for p in case.rglob('*'):
   if p.is_file():pin(p)
  pin(baseline/'run.log');pin(baseline/'game_mix.wav');cases.append(row)
 channels=[]
 for move in('square','bicycle'):
  for side in(1,2):
   case=ROOT/('audit_v1483_live_bicycle_channels_p1'if(move,side)==('bicycle',1)else f'audit_v1484_live_{move}_channels_p{side}')
   meta=json.loads((case/'result.json').read_text(encoding='utf-8-sig'));need(meta['exit_code']==0 and meta['candidate']==NAME,'Live channel runtime')
   for p,h in meta['input_hashes'].items():pin(p,h)
   log=(case/'run.log').read_text(encoding='utf-8-sig');state=human.verify_log(log,move,side)
   need(events(log)==events((ROOT/f'audit_v1475_human_launch_{move}_p{side}/run.log').read_text(encoding='utf-8-sig')),'Live read-only ledger does not alter game')
   need((case/'guest_maincpu.bin').read_bytes()==guest,'Live channel guest exact')
   rows=media.records(log,'MK2_LAUNCH_CHANNEL');owners=media.records(log,'MK2_LAUNCH_OWNER');by={(int(q['frame']),int(q['channel'])):q for q in rows};ob={(int(q['frame']),int(q['slot'])):q for q in owners}
   frames=range(1450,int(human.rows(log,'RESULT')[0]['frame'])+1)
   need(len(by)==len(rows)==len(frames)*4 and len(ob)==len(owners)==len(frames)*2,'Every physical sample and owner callback retained')
   fields=human.rows(log,'FIELD');owner=next(q for q in fields if q['slot']==side)
   base=10+(side-1)*2;names=['sonya_square_launch']if move=='square'else['sonya_bicycle_launch','sonya_bicycle_cry'];active=[]
   for channel in range(10,14):
    stream=[by[f,channel]for f in frames]
    need(all(q['loop']==q['paused']==q['writes']=='0'for q in stream),'Finite unpaused channels, no item writes')
    if channel not in range(base,base+len(names)):need(all(q['length']=='0'and float(q['pos'])==0 for q in stream),'Other physical player and unused channel never play')
    else:
     length=assets['assets'][names[channel-base]]['frames'];positive=[q for q in stream if int(q['length'])>0]
     need(positive and all(int(q['length'])==length for q in positive),'Exact complete original asset loaded in physical channel')
     need(int(positive[0]['frame'])==state['entry']+1 and float(positive[0]['pos'])>0,'Actual channel begins immediately after native startup')
     positions=[float(q['pos'])for q in positive];need(all(a<=b for a,b in zip(positions,positions[1:]))and positions[-1]==length,'Whole finite cue actually reaches final source sample')
     completed=next(int(q['frame'])for q in positive if float(q['pos'])==length);active.append(dict(channel=channel,asset=names[channel-base],length=length,completedFrame=completed))
   last=max(q['completedFrame']for q in active)
   for f in frames:
    for slot in(1,2):
     q=ob[f,slot];need(q['writes']=='0','Read-only audio ownership')
     if slot!=side or f<=state['entry']or f>=last+3:need(q['actor']==q['main']=='00000000'and q['health']=='0','Other owner remains clear; finite owned cleanup')
     elif q['actor']!='00000000':need(int(q['actor'],16)==owner['actor']and int(q['main'],16)==owner['main']and q['health']=='161','Own real native Sonya, not proxy')
   need(int(ob[state['entry']+1,side]['actor'],16)==owner['actor'],'Ownership actually published')
   channels.append(dict(case=case.name,move=move,side=side,actualFullFiniteChannels=active,ownershipCleared=True,opponentChannelsUntouched=True))
   for p in case.rglob('*'):
    if p.is_file():pin(p)
 for module in tuple(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p and Path(p).suffix=='.py'and Path(p).resolve().is_relative_to(ROOT/'tools'):pin(p)
 return dict(passed=True,candidate=NAME,cases=cases,liveChannels=channels,originalReferences=originalcases,relocatedNativeBranches=branches,inputHashes=pins,wholeGuestIndependentlyReconstructed=True,launcherPromoted=False,fullPortAccepted=False,allMoveAudioAccepted=False,interruptionsAccepted=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite proof')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'passed':report['passed'],'error':report.get('error'),'cases':len(report.get('cases',[])),'liveChannels':len(report.get('liveChannels',[]))}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
