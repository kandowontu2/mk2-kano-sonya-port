"""Actual P2 square voice interruption by source-bound original jump kick.
This is a distinct native counter, not a replacement of the preserved
40-point uppercut predicates in v1535; P2 uppercut coverage remains unproven.
"""
import json,re,hashlib,struct
from pathlib import Path
import verify_native_ground_throw_source_v1598 as current
import verify_active_launch_interruption_v1535 as prior
sound=prior.sound;need=prior.need;ROOT=current.ROOT
OUT=ROOT/'audit_v1652_p2_square_jumpkick_audio_checked'
def verify_hit_log(log,victim=8):
 h=sound.human;fields=h.rows(log,'FIELD');results=h.rows(log,'RESULT')
 need(len(results)==1 and not h.rows(log,'FAILED'),'Complete actual interrupted match')
 r=results[0];side=r['side'];move=r['move']
 need(move in ('square','bicycle')and side in(1,2),'Actual supported physical Sonya launch')
 by={(q['frame'],q['slot']):q for q in fields};frames=range(r['ready'],r['frame']+1)
 need(len(by)==len(fields)==len(frames)*2,'Every actual native fighter callback')
 actors={s:(by[r['ready'],s]['actor'],by[r['ready'],s]['main'])for s in(1,2)}
 for q in fields:
  s=q['slot'];need(q['id']==q['roster']==(18 if s==side else victim)and q['state']==1 and q['mode']==2 and q['owner']==q['actor']and(q['actor'],q['main'])==actors[s]and q['writes']==0,'Stable real physical fighters/humans, not proxy actors')
 health=h.rows(log,'HEALTH');incoming=[q for q in health if q['slot']==side and q['after']<q['before']]
 need(len(incoming)==1 and incoming[0]['before']==161 and incoming[0]['after']==135,'Actual single original 26-damage forward jump kick')
 for q in health:need(q['pc']==0xff836700 and q['mask']==0xffff and q['writes']==0,'Original native collision damage store')
 hit=incoming[0]['frame'];need(r['entry']<hit<r['recovered'],'The actual hit interrupts an already launched move')
 for frame in range(r['ready'],r['frame']):
  for s in(1,2):
   stores=[q for q in health if q['frame']==frame and q['slot']==s]
   a=by[frame,s]['hp'];b=by[frame+1,s]['hp']
   if stores:need(stores[0]['before']==a and stores[-1]['after']==b and all(x['after']==y['before']for x,y in zip(stores,stores[1:])),'Original damage ledger explains every callback HP transition')
   else:need(a==b,'No unexplained health transition')
 hurt=[f for f in range(hit+1,hit+3)if by[f,side]['action']==0x503 and by[f,side]['gravity']==0x8000 and by[f,side]['vy']==0xfffa0000]
 need(bool(hurt),'Actual original jump-kick hurt-task dispatch and knockdown trajectory')
 owners=sound.media.records(log,'MK2_LAUNCH_OWNER');channels=sound.media.records(log,'MK2_LAUNCH_CHANNEL')
 ob={(int(q['frame']),int(q['slot'])):q for q in owners};cb={(int(q['frame']),int(q['channel'])):q for q in channels}
 cframes=range(1450,r['frame']+1)
 need(len(ob)==len(owners)==len(cframes)*2 and len(cb)==len(channels)==len(cframes)*4,'Every actual ownership and source-position callback')
 actor,main=actors[side]
 for frame in cframes:
  for s in(1,2):
   q=ob[frame,s];need(q['writes']=='0','Read-only host owner observer')
   if s==side and r['entry']<frame<=hit:
    need(int(q['actor'],16)==actor and int(q['main'],16)==main and q['health']=='161','Real owned launch exists before damage')
   else:need(q['actor']==q['main']=='00000000'and q['health']=='0','Owner clears by first callback after damage; opponent untouched')
 base=10+(side-1)*2
 lengths={base:45512}if move=='square'else{base:40720,base+1:66523}
 stops={}
 for channel in range(10,14):
  stream=[cb[f,channel]for f in cframes]
  need(all(q['writes']==q['loop']==q['paused']=='0'for q in stream),'Finite unpaused channels; no observer writes')
  if channel not in lengths:
   need(all(q['length']=='0'and float(q['pos'])==0 for q in stream),'Other player and unused channels never start')
  else:
   length=lengths[channel]
   need(all(cb[f,channel]['length']=='0'and float(cb[f,channel]['pos'])==0 for f in range(1450,r['entry']+1)),'No cue before actual native startup')
   need(all(cb[f,channel]['length']==str(length)for f in range(r['entry']+1,r['frame']+1)),'Only complete exact original asset loads')
   positions=[float(cb[f,channel]['pos'])for f in range(r['entry']+1,hit+2)]
   stop=float(cb[hit+1,channel]['pos'])
   need(positions[0]>0 and all(a<=b for a,b in zip(positions,positions[1:]))and 0<stop<length,'Real source playback starts and advances before its mid-cue stop')
   # stop() synchronizes the audio stream to the timer callback, so the last
   # position can advance beyond the previous frame's read-only sample. It
   # must be frozen by the next callback and never resume after recovery.
   need(all(float(cb[f,channel]['pos'])==stop for f in range(hit+1,r['frame']+1)),'Actual voice stops by next callback and never restarts')
   stops[channel]=stop
 marks=[q for q in sound.sound_rows(log)if q['word']in('6B00','6B01','6B02')]
 wanted=['6B00']if move=='square'else['6B01','6B02']
 need([q['word']for q in marks]==wanted and all(int(q['frame'])==r['entry']for q in marks),'Exactly the native launched voice markers')
 for frame in (r['recovered'],r['frame']):need(all(h.clean(by[frame,s])for s in(1,2)),'Both fighters recover cleanly on their own floors')
 follow=r['followup'];need(follow==r['recovered']+16 and r['frame']==follow+160,'Complete ordinary follow-up horizon')
 need(any(by[f,side]['vx']!=0 for f in range(follow+3,follow+9))and any(by[f,side]['y']<by[f,side]['floor']for f in range(follow+42,follow+65))and any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),'Real walking, jumping and punch respond after interrupted recovery')
 return dict(move=move,side=side,entry=r['entry'],actualHit=hit,damage=26,hurtTaskFrame=min(hurt),cleanupByFrame=hit+1,stoppedSourcePositions=stops,recovered=r['recovered'],terminal=r['frame'],actualIncomingHitCleanupAccepted=True)
def verify():
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=current.prior.sha(p)
  need(wanted is None or pins[key]==wanted,'Changed actual input '+key)
 proofpath=current.OUT/'report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed'] and proof['candidate']==current.NAME and proof['wholeActualGuestExactlyTwoPatches'],'Entire actual source-built current guest proof')
 pin(proofpath)
 for p,h in proof['inputHashes'].items():pin(p,h)
 buildpath=ROOT/current.NAME/'build-info.json';build=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
 guest,_,payload=current.expected()
 originalpath=ROOT/'mk2/mk2-maincpu.bin';original=originalpath.read_bytes();pin(originalpath,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 cases=[];logs=[]
 delegates={'mk2ks_launch_interruption_v1650.lua':['mk2ks_launch_interruption_v1648.lua'],
 'mk2ks_launch_interruption_v1648.lua':['mk2ks_launch_channels_v1483.lua'],
 'mk2ks_launch_channels_v1483.lua':['mk2ks_native_grab_audio_v1412.lua'],
 'mk2ks_native_grab_audio_v1412.lua':['mk2ks_human_special_audio_v1397.lua'],
 'mk2ks_human_special_audio_v1397.lua':['mk2ks_human_special_matrix_v3.lua'],
 'mk2ks_human_special_matrix_v3.lua':[]}
 for name in('audit_v1649_square_early_jumpkick_interruption_p2','audit_v1651_square_native_jumpkick_interruption_p2'):
  folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['move']=='square' and meta['side']==2 and meta['victim']=='sub_zero' and meta['counter']=='native_forward_jumpkick' and meta['counter_input_frame']==1578 and not meta['cheats_enabled'] and meta['assistance']=='none','Declared real cold current jump kick fixture')
  need(meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'],'Exact current candidate')
  before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  need(before==meta['input_hashes'] and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every actually executed compiled input pinned')
  for p,h in before.items():
   pin(p,h)
   if Path(p).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
  for script in(folder/'input_sources').glob('*.lua'):
   text=script.read_text()
   need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)',text),'No guest, task, sample or save-state mutation')
   called=re.findall(r"dofile\('([^']+)'\)",text)
   need(script.name in delegates and called==delegates[script.name],'Fully declared static read-only/physical driver delegation')
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actually initialized native program equals independent current model')
  log=(folder/'run.log').read_text(encoding='utf-8-sig')
  need(not re.search('WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation',log,re.I),'No actual native/emulator error')
  row=verify_hit_log(log);row['case']=name;cases.append(row);logs.append(log)
  for p in folder.rglob('*'):
   if p.is_file():pin(p)
 # The second cold fixture adds only a native descriptor observer. Real
 # identity, pose, damage, channels and recovery must reproduce byte-exactly.
 actual=lambda log:[q for q in log.splitlines()if q.startswith(('MK2_HSPECIAL_','MK2_LAUNCH_CHANNEL ','MK2_LAUNCH_OWNER '))]
 need(actual(logs[0])==actual(logs[1]),'Read-only added descriptor observer changes no gameplay or audio callback')
 fields=sound.human.rows(logs[1],'FIELD');first=next(r for r in fields if r['slot']==1)
 records=sound.media.records(logs[1],'MK2_NATIVE_COUNTER_DESCRIPTOR')
 need(len(records)==1,'One actual original jump-kick descriptor lookup')
 d=records[0];address=int(d['descriptor'],16);at=(address-0xff800000)//8
 need(address==0xff8eda40 and int(d['at'],16)==0xff835440 and int(d['pc'],16)==0xff835450 and int(d['frame'])==cases[1]['actualHit'] and d['writes']=='0' and d['assistance']=='none','Exact real collision fetch and contact chronology')
 need(int(d['actor'],16)==int(d['owner'],16)==first['actor'] and int(d['main'],16)==first['main'] and d['id']=='8','Physical stock P1 opponent owns actual jump kick, no proxy')
 words=tuple(int(w,16)for w in d['words'].split(','))
 need(words==struct.unpack_from('<9H',original,at) and guest[at:at+18]==original[at:at+18],'Entire actual descriptor identical to original MK2 ROM')
 need(words==(99,36,64,32,0x0b12,0x1a07,0,0,1) and words[5]>>8==cases[1]['damage']==26,'Original hitbox, hurt reaction and 26-point contact damage')
 for address,length in((0xff835440,64),(0xff8366c0,8)):
  at=(address-0xff800000)//8;need(guest[at:at+length]==original[at:at+length],'Actual original collision/damage entry code unchanged')
 negatives=[]
 for name,log in zip((c['case']for c in cases),logs):
  mutations={'wrong_damage':log.replace('before=161 after=135 mask=FFFF','before=161 after=136 mask=FFFF'),
   'wrong_store':log.replace('pc=FF836700','pc=FF000000'),
   'proxy_id':log.replace('id=18 roster=18','id=1 roster=1'),
   'missing_health':'\n'.join(q for q in log.splitlines()if not q.startswith('MK2_HSPECIAL_HEALTH')),
   'missing_channels':'\n'.join(q for q in log.splitlines()if not q.startswith('MK2_LAUNCH_CHANNEL ')),
   'looped_voice':log.replace('loop=0 paused=0','loop=1 paused=0'),
   'observer_writes':log.replace('writes=0','writes=1'),
   'missing_owner':'\n'.join(q for q in log.splitlines()if not q.startswith('MK2_LAUNCH_OWNER '))}
  for label,bad in mutations.items():
   need(bad!=log,'Effective in-memory counterexample')
   try:verify_hit_log(bad)
   except (ValueError,KeyError):negatives.append(dict(case=name,mutation=label,rejected=True))
   else:raise ValueError('Accepted corrupted actual native lifecycle '+label)
 pin(__file__);pin(prior.__file__)
 return dict(passed=True,candidate=current.NAME,cases=cases,actualOriginalJumpKickDescriptor=d,readOnlyObserverReplayExact=True,rejectedInMemoryCorruptions=negatives,inputHashes=pins,p2SquareActualIncomingHitAudioCleanupAccepted=True,p2SquareUppercutInterruptionAccepted=False,allHitTypesAccepted=False,KOAndSimultaneousAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Preserve existing evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),candidate=current.NAME,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','scope')},indent=2))
 raise SystemExit(0 if report['passed']else 1)

