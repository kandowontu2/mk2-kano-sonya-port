"""Direct native Main+140 stock8 movie/impact/voice ownership.

Add to, never replace, the whole5949 window/PCM/DAC/ROM/ADSP matrix. The
actual chosen queue slot is observed, not priority alternatives or RNG state.
No original/current pixel comparison or all-victim audio acceptance.
"""
import gzip,json,re,struct,traceback
from decimal import Decimal
from pathlib import Path
import verify_current_subzero_pit_mix_v5948 as whole
ROOT,need,sha=whole.ROOT,whole.need,whole.sha
OUT=ROOT/'audit_v5951_current_subzero_pit_owner_checked'

def gate(text,guest,stock,fighter,side):
 tags=('MK2_PIT140_', 'MK2_MAUDIO_ROUTE ', 'MK2_MAUDIO_QUEUE ',
       'MK2_MAUDIO_PACKET ', 'MK2_MAUDIO_SOUND ', 'MK2_STAGE_FIELD ')
 records=whole.predecessor.inventory('\n'.join(l for l in text.splitlines()if l.startswith(tags)))
 get=lambda name:records.get(name,[])
 pit=lambda name:get('MK2_PIT140_'+name)
 audio=lambda name:get('MK2_MAUDIO_'+name)
 need(all(r['writes']=='0'and r['assistance']=='none'for key,rows in records.items()for r in rows),
      'Every direct native ancestry/ownership event is passive')
 need(len(pit('BEGIN'))==len(pit('RESULT'))==len(pit('CONSTRUCTOR'))==1,'One real stage admission/constructor/terminal')
 first=get('MK2_STAGE_FIELD')[0];begin=pit('BEGIN')[0];end=pit('RESULT')[0];ctor=pit('CONSTRUCTOR')[0]
 own=17 if fighter=='kano'else 18;origin=int(begin['frame'])
 need(begin['actor']==first['own']and begin['main']==first['main']and begin['id']==first['id']==str(own)and
      first['victim_id']=='8'and begin['arena']=='6'and end['origin']==str(origin)and
      int(end['frame'])==origin+1101 and end['raw_files']=='0','Real own17/18, defeated original8 and full1101 terminal')
 need(ctor['a0']=='00000008'and ctor['a11']==first['victim']and ctor['a8']=='00000000'and ctor['mode']=='9',
      'Original movie constructor receives actual defeated physical actor, not own or proxy')
 look=pit('LOOKUP');draw=pit('DRAW');fields=pit('FIELD');off=lambda a:(a-0xff800000)//8
 sequence=struct.unpack_from('<I',stock,off(0xff85e6b0+8*32))[0]
 need(sequence==0xff8609f0 and struct.unpack_from('<I',guest,off(0xff85c4a0))[0]==0xff180800,
      'Original stock8 sequence and current native extended table operand')
 stream=struct.unpack_from('<10I',stock,off(sequence))
 need(stream[5:8]==(1,sequence,0)and stream[9]==0 and
      guest[off(sequence):off(0xff860e50)]==stock[off(sequence):off(0xff860e50)],
      'Whole original stock8 movie stream/groups unchanged; five-frame self-loop and impact')
 need(len(look)==2 and len(draw)==21,'Both actual movie lookups, twenty falling draws and impact')
 actor,main=look[0]['actor'],look[0]['main'];enter=int(look[0]['frame']);impact=int(look[1]['frame'])
 need(actor not in(first['own'],first['victim'])and main==ctor['a13']and enter==int(ctor['frame'])and impact==enter+59,
      'Separate original cinematic actor/Main ancestry and native fall duration')
 for r in look:
  need(r['at']=='FF180900'and int(r['low'],16)|(int(r['high'],16)<<16)==sequence and
       r['mask']=='FFFF'and r['pc']=='FF83B850'and r['actor']==r['owner140']==actor and r['main']==main and r['id']=='8',
       'Actual original stock8 table word fetch and directly read Main140 self-owner')
 for i,r in enumerate(draw):
  group=stream[i%5]if i<20 else stream[8];frame=enter+1+3*i if i<20 else impact
  preceding=0 if i==0 else(stream[(i-1)%5]if i<=20 else stream[8])
  need(r['frame']==str(frame)and int(r['group'],16)==group and r['actor']==r['owner140']==actor and
       r['main']==main and r['id']=='8'and r['body']=='0002'and r['bank']=='0202'and
       r['x']=='192'and r['y']=='64'and int(r['pose'],16)==preceding and
       r['cache']==draw[0]['cache'],'Every actual original movie phase, preceding pose, body and native centered cadence')
 need([int(r['age'])for r in fields]==list(range(1101))and
      [int(r['frame'])for r in fields]==list(range(origin,origin+1101))and fields[-1]['mode']=='3',
      'All1101 completed field observations, genuine next-screen retirement')
 active=[r for r in fields if enter<int(r['frame'])<=impact]
 need(len(active)==59 and all(r['mode']=='9'and r['cine_actor']==r['owner140']==actor and r['cine_main']==main and
      r['id']=='8'and r['body']=='0002'and r['p1']==r['p2']=='00000000'for r in active),
      'Direct Main140 owns original8 throughout falling/impact fields after physical pointers retire')
 routes=[r for r in audio('ROUTE')if r['return_pc']in('FF85C5B0','FF85C610')]
 need([r['entry']for r in routes]==['FFA12530','FFA12220','FFA122D0','FFA123D0','FFA12530']and
      all(r['a8']==r['owner140']==actor and r['a13']==main and r['id']=='8'and r['mode']=='9'and
          r['frame']==str(impact)for r in routes)and
      all(Decimal(a['seconds'])<Decimal(b['seconds'])for a,b in zip(routes,routes[1:])),
      'Actual impact and every male packed-voice route own the genuine movie actor via Main140')
 need(routes[0]['return_pc']=='FF85C5B0'and routes[0]['a0']=='000000CF'and
      all(r['return_pc']=='FF85C610'for r in routes[1:])and
      routes[1]['a0']==routes[2]['a0']==routes[3]['a0']=='00000001'and
      routes[1]['a1']==routes[2]['a1']=='CCCCCCCE'and routes[2]['a2']=='00000008'and
      routes[3]['a1']==routes[4]['a0']==routes[4]['a1']=='000000CC',
      'Original literal CF impact and stock8 native CC packed-voice branch, not own-winner voice')
 for lo,hi in ((0xff85c4c0,0xff85c700),(0xffa12530,0xffa12b90),(0xffa13ba0,0xffa13ed0)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Whole original impact/queue-slot/packet program unchanged')
 queues=[r for r in audio('QUEUE')if r['a8']==actor and r['a13']==main]
 packets=[r for r in audio('PACKET')if r['a8']==actor and r['a13']==main]
 sounds=[r for r in audio('SOUND')if r['a8']==actor and r['a13']==main]
 need(len(queues)==len(packets)==2 and len(sounds)==4,'Exactly actual owned impact/voice queues, packets and both port bytes')
 increments={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}
 for i,(q,p)in enumerate(zip(queues,packets,strict=True)):
  word=int(q['a3'],16)+increments[q['entry']];stores=sounds[2*i:2*i+2]
  need(int(p['a3'],16)==word and q['a1']==p['a1']and q['a4']==p['a4']and p['entry']=='FFA13BA0'and
       q['frame']==p['frame']==str(impact)and Decimal(routes[0 if i==0 else 4]['seconds'])<Decimal(q['seconds'])<Decimal(p['seconds']),
       'Actual native queue slot contributes0/1/2 to its packet base; not an inferred RNG choice')
  need([int(r['word'],16)for r in stores]==[0xff00|(word>>8),0xff00|(word&255)]and
       [r['pc']for r in stores]==['FFA13C90','FFA13D60']and
       all(r['owner140']==actor and r['mode']=='9'and r['mask']=='FFFF'and r['frame']==str(impact)for r in stores)and
       Decimal(p['seconds'])<Decimal(stores[0]['seconds'])<Decimal(stores[1]['seconds']),
       'Both full native sound-port bytes directly read the same cinematic Main140 owner')
 return dict(passed=True,fighter=fighter,physicalSlot=side,ownID=own,originalVictimID=8,
             actualCinematicActor=actor,actualCinematicMain=main,origin=origin,terminal=int(end['frame']),
             sourceStockSequence=sequence,actualMovieDraws=21,actualDirectOwnerFields=59,
             actualOwnedCueRoutes=5,actualOwnedPackets=2,actualOwnedPortBytes=4,
             directlyObservedMain140OwnershipAccepted=True,actualChosenSlotAdditionAccepted=True,
             allNativePitCuePriorityAndRNGAccepted=False,stockVictimRGBAccepted=False,
             completeStageVictimAudioAccepted=False,fullPortAcceptance=False)

def run():
 whole.observed.current.expected();basepath=whole.OUT/'report.json';base=json.loads(basepath.read_text())
 need(base['passed']and len(base['cases'])==4 and base['exactStereoPCMFrames']==3863040 and
      base['actualSourceAudioFaultsRejected']==116 and base['actualEarnedStateFaultsRejected']==48,
      'Whole four5949 native audio/source/clock/ADSP/state and fault matrix remains accepted')
 pins=dict(base['inputHashes']);pins[str(basepath)]=sha(basepath);guest=whole.observed.current.expected()
 stockpath=ROOT/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes();cases=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v5947_current_subzero_pit_mix_{fighter}_p{side}_samples'
   with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
   good=gate(text,guest,stock,fighter,side);faults=[]
   def reject(label,bad,bad_guest=guest):
    need(bad!=text or bad_guest!=guest,'Effective direct native ownership/source counterexample')
    try:gate(bad,bad_guest,stock,fighter,side)
    except(ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
    else:raise ValueError('Corrupted direct native owner/cue admitted '+label)
    need(gate(text,guest,stock,fighter,side)==good,'Whole actual direct owner positive restored after every fault')
   for tag,key,value,where in(
    ('CONSTRUCTOR','a0','00000011',''),('CONSTRUCTOR','a11','00000000',''),('CONSTRUCTOR','mode','2',''),
    ('LOOKUP','owner140','00000000',''),('LOOKUP','low','0000',''),('LOOKUP','id','17',''),
    ('LOOKUP','at','FF180800',''),('LOOKUP','main','00000000',''),
    ('DRAW','body','0000',''),('DRAW','bank','0000',''),('DRAW','group','FF000000',''),
    ('DRAW','actor','00000000',''),('DRAW','x','191',''),('FIELD','age','1','age=0 '),
    ('MK2_MAUDIO_ROUTE','owner140','00000000','return_pc=FF85C5B0'),
    ('MK2_MAUDIO_ROUTE','a8','00000000','return_pc=FF85C610'),
    ('MK2_MAUDIO_ROUTE','mode','2','return_pc=FF85C610'),
    ('MK2_MAUDIO_ROUTE','a0','000000CE','return_pc=FF85C5B0'),
    ('MK2_MAUDIO_SOUND','owner140','00000000',f'a8={good["actualCinematicActor"]} '),
    ('MK2_MAUDIO_SOUND','word','0000',f'a8={good["actualCinematicActor"]} '),
    ('MK2_MAUDIO_PACKET','a3','00000000',f'a8={good["actualCinematicActor"]} ')):
    prefix=tag if tag.startswith('MK2_')else'MK2_PIT140_'+tag
    line=next(l for l in text.splitlines()if l.startswith(prefix+' ')and where in l)
    changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
    need(n==1 and changed!=line,'Actual direct native row/key mutation');reject(prefix+'/'+key,text.replace(line,changed,1))
   line=[l for l in text.splitlines()if l.startswith('MK2_PIT140_DRAW ')][-1]
   reject('Missing actual impact draw',text.replace(line+'\n','',1))
   for address,label in((0xff85c4a0,'extended table operand'),(0xff8609f0,'original movie sequence'),
                         (0xff85c560,'original literal impact command'),(0xffa12a80,'original queue slot increment')):
    bad=bytearray(guest);bad[(address-0xff800000)//8]^=1;reject(label,text,bytes(bad))
   need(len(faults)==26,'All26 actual ancestry/owner/movie/cue/packet/source faults rejected')
   good['actualFaultsRejected']=faults;cases.append(good)
 for p in(Path(__file__).resolve(),Path(whole.__file__).resolve(),stockpath):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every compiled/protected/executed/native/previous qualification byte intact')
 return dict(passed=True,cases=cases,inputHashes=pins,actualOriginalVictimID=8,
             directlyObservedMain140OwnershipAccepted=True,actualDirectNativeFaultsRejected=104,
             whole5949NativeAudioAndAllFaultsRetained=True,allNativePitCuePriorityAndRNGAccepted=False,
             stockVictimRGBAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,
             newNativeBoots=0,newBuilds=0,rawRecordingsWritten=0,publicPlayableChanged=False)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable direct native stock-victim ownership qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
