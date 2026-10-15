"""All observed native seed/rotation/multiply and sound-slot decisions.

Retain whole5966 audio and5950 movie ownership contracts. Qualify actual
empty-slot and replacement cases, not unobserved suppression/special71 paths.
No injected RNG/queue values; counterexamples operate on retained evidence.
"""
import gzip,json,re,struct,traceback
from decimal import Decimal
from pathlib import Path
from collections import Counter
import verify_current_pit_queue_rng_mix_v5965 as audio_matrix
import qualify_current_subzero_pit_owner_v5950 as ownership
ROOT,need,sha=audio_matrix.ROOT,audio_matrix.need,audio_matrix.sha
OUT=ROOT/'audit_v5968_current_pit_queue_rng_checked'
off=lambda a:(a-0xff800000)//8

def gate(text,guest,stock,fighter,side):
 rs=audio_matrix.prior_matrix.predecessor.inventory('\n'.join(l for l in text.splitlines()if l.startswith('MK2_PQR_')))
 get=lambda name:rs.get('MK2_PQR_'+name,[])
 integer=lambda r,key:int(r[key],16)
 clock=lambda r:Decimal(r['seconds'])
 same=lambda a,b:all(a[k]==b[k]for k in('frame','a8','a13'))
 need(all(r['writes']=='0'and r['assistance']=='none'for rows in rs.values()for r in rows),'Every actual native queue/RNG observation passive')
 addresses={'DISPATCH':0xffa12530,'HEADER':0xffa12620,'SELECT':0xffa126a0,'FINISH':0xffa12b90,
            'RNG_BEGIN':0xff80eae0,'RNG_SEED':0xff80e990,'RNG_STORE':0xff80ea40,'RNG_ROTATE':0xff80ea60,
            'RNG_WORD':0xff80eaa0,'RNG_MULTIPLY':0xff80eb20,'RNG_PRODUCT':0xff80eb30,'RNG_RETURN':0xff80eb60,
            'PACKED_BEGIN':0xffa12180,'PACKED_RETURN':0xffa121e0,'VOICE_BEGIN':0xffa123d0,'VOICE_RETURN':0xffa12400}
 for name,address in addresses.items():need(all(integer(r,'entry')==address for r in get(name)),'Exact original instruction-PC snapshot '+name)
 need(len(get('BEGIN'))==len(get('RESULT'))==1,'One actual Pit queue/RNG origin and complete terminal')
 begin,end=get('BEGIN')[0],get('RESULT')[0];origin=int(begin['frame']);identity=17 if fighter=='kano'else 18
 need(begin['entry']=='FF8BDDE0'and begin['id']==str(identity)and begin['arena']=='6'and
      end['origin']==str(origin)and int(end['frame'])==origin+1101 and end['raw_files']=='0','Actual own17/18 origin and native full1101 terminal')
 for lo,hi in((0xff80e980,0xff80eb70),(0xffa0ef20,0xffa12220),(0xffa123d0,0xffa12430),
              (0xffa12530,0xffa12bd0),(0xff8eb560,0xff8eb610),(0xff85c560,0xff85c610),
              (0xff9b0940,0xff9b09a0),(0xffa0d1b0,0xffa0d200)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Whole original native RNG/table/queue/packed caller source unchanged')
 def exact(address,words):
  raw=struct.pack('<'+'H'*len(words),*words)
  need(guest[off(address):off(address)+len(raw)]==stock[off(address):off(address)+len(raw)]==raw,'Original literal/packed cue source '+hex(address))
 for address,value in((0xff870de0,4),(0xff8eb560,0x1b),(0xff85c560,0xcf),(0xffa0d1b0,0xd0)):
  exact(address,(0x09c0,value,0x0d5f,0x2530,0xffa1))
 exact(0xff8eb5b0,(0x09e1,0xcbcd,0xcbcb,0x0d5f,0x2210,0xffa1))
 exact(0xff85c5b0,(0x09e1,0xccce,0xcccc,0x0d5f,0x2210,0xffa1))
 exact(0xffa12210,(0x1820,));exact(0xff9b0940,(0x09e0,0x73,3,0xc080,0x2180,0xffa1))
 cores=[get(n)for n in('RNG_SEED','RNG_STORE','RNG_ROTATE','RNG_WORD')]
 need(all(len(rows)==1121 for rows in cores),'Every1101 main-loop plus20 bounded native seed/rotation calls')
 core_proof=[];overflow_counts=Counter();rotation_counts=Counter()
 for seed,stored,rotated,word in zip(*cores,strict=True):
  need(all(same(seed,r)and all(seed[k]==r[k]for k in('sp','top','next'))for r in(stored,rotated,word))and
       clock(seed)<clock(stored)<clock(rotated)<clock(word),'Entire actual original RNG invocation ownership/stack/chronology')
  prior=integer(seed,'seed');shifted=(prior<<1)&0xffffffff;overflow=((prior>>31)^((prior>>30)&1))!=0
  saved=shifted if overflow else shifted|2;adjusted=(saved+(prior>>31))&0xffffffff
  amount=integer(word,'a1')&31;expected=((adjusted<<amount)|(adjusted>>((32-amount)&31)))&0xffffffff
  need(integer(stored,'a0')==integer(stored,'seed')==saved and integer(rotated,'a0')==adjusted and
       integer(rotated,'a1')==0 and integer(rotated,'seed')==integer(word,'seed')==saved and
       integer(word,'a0')==expected,'Actual original SLA overflow/conditional OR2/store/carry/beam-count rotate word exact')
  overflow_counts[overflow]+=1;rotation_counts[amount]+=1;core_proof.append((seed,word))
 need(integer(cores[0][0],'seed')==integer(begin,'seed')and
      all(integer(a,'seed')==integer(b,'seed')for a,b in zip(cores[1][:-1],cores[0][1:],strict=True))and
      integer(end,'seed')==integer(cores[1][-1],'seed'),'Every observed native stored-seed update chains through full untrimmed window')
 main=[r for r in cores[0]if r['next']=='FF811D20']
 need([int(r['frame'])for r in main]==list(range(origin,origin+1101))and
      len([r for r in cores[0]if r['next']=='FF80EB20'])==20 and set(overflow_counts)=={False,True},
      'One original main-loop core per completed field, all bounded cores, both actual native overflow paths')
 starts=get('RNG_BEGIN');multiply=get('RNG_MULTIPLY');products=get('RNG_PRODUCT');returns=get('RNG_RETURN')
 need(len(starts)==len(multiply)==len(products)==len(returns)==20,'All actual bounded RNG calls, full64bit products and restored returns')
 bounded=[]
 for start,mul,product,ret in zip(starts,multiply,products,returns,strict=True):
  need(all(same(start,r)for r in(mul,product,ret))and clock(start)<clock(mul)<clock(product)<clock(ret)and
       integer(mul,'sp')==integer(product,'sp')==integer(start,'sp')-32 and ret['sp']==start['sp']and
       mul['next']==product['next']==ret['top']==start['top']and mul['top']==product['top']==ret['a1']==start['a1'],
       'Every bounded source-count call, native saved-base stack and actual return ancestry')
  matches=[(s,w)for s,w in core_proof if clock(start)<clock(s)<clock(w)<clock(mul)]
  need(len(matches)==1,'One complete actual native core feeds each bounded multiply')
  s,w=matches[0];count=integer(start,'a0');number=integer(w,'a0');full=number*count;choice=(full>>32)+1
  need(same(start,s)and integer(s,'sp')==integer(start,'sp')-96 and s['next']=='FF80EB20'and
       integer(mul,'a0')==number and integer(mul,'a1')==count and integer(product,'a0')==full>>32 and
       integer(product,'a1')==full&0xffffffff and integer(ret,'a0')==choice and 1<=choice<=count,
       'Original unsigned64bit multiply high/low halves, native increment and exact count-domain choice')
  bounded.append(dict(start=start,returned=ret,count=count,choice=choice))
 selectors=[]
 for kind,retname in(('PACKED','FFA121E0'),('VOICE','FFA12400')):
  before,after=get(kind+'_BEGIN'),get(kind+'_RETURN');need(len(before)==len(after)==(6 if kind=='PACKED'else 2),'Every actual sound packed/base selector')
  for a,b in zip(before,after,strict=True):
   count=integer(a,'a0')>>16 if kind=='PACKED'else integer(a,'a0')
   base=integer(a,'a0')&65535 if kind=='PACKED'else integer(a,'a1')
   found=[r for r in bounded if r['start']['top']==retname and clock(a)<clock(r['start'])<clock(r['returned'])<clock(b)]
   need(len(found)==1 and same(a,b)and a['sp']==b['sp']and a['top']==b['top']and
        found[0]['count']==count and integer(b,'a0')==found[0]['choice']and integer(b,'a1')==base,
        'Whole actual original packed or role-voice count/base and genuine native selected variant')
   ds=[r for r in get('DISPATCH')if same(a,r)and r['sp']==a['sp']and r['top']==a['top']and clock(b)<clock(r)<clock(b)+Decimal('.00001')]
   need(len(ds)==1 and integer(ds[0],'a0')==base+found[0]['choice']-1,'Actual selected cue is original base plus native choice minus one')
   selectors.append(dict(kind=kind,base=base,count=count,choice=found[0]['choice'],command=integer(ds[0],'a0'),caller=a['top']))
 need([r['base']for r in selectors if r['kind']=='VOICE']==[0xcb,0xcc]and
      all(r['base']==0x73 and r['count']==3 and r['caller']=='FF9B0CB0'for r in selectors if r['kind']=='PACKED'),
      'All stock8 initial/cinematic one-variant voices and six original three-choice particle calls')
 dispatch=get('DISPATCH');headers=get('HEADER');select=get('SELECT');queues=get('QUEUE');finishes=get('FINISH')
 need(len(dispatch)==len(headers)==12 and len(select)==len(queues)==len(finishes)==18 and not get('SUPPRESS'),
      'Complete actual12 general callers and18 general/direct slot admissions; no unobserved suppression claim')
 branches=Counter();slots=Counter();selection=[]
 for r,q,endq in zip(select,queues,finishes,strict=True):
  pointer=integer(r,'a0')-32;header,base=struct.unpack_from('<HH',stock,off(pointer));priority,duration=header>>8,header&255
  need(0xffa0ef20<=pointer<0xffa12180 and 0<header<0x8000 and integer(r,'a1')==priority and
       integer(r,'a3')==base and integer(r,'a4')==duration,'Every general/direct selected cue register matches whole original source record')
  prior=[integer(r,'p'+str(n))for n in range(3)];deadlines=[integer(r,'d'+str(n))for n in range(3)]
  if priority==0x71 and 0x71 in prior:slot=prior.index(0x71);branch='special71'
  elif 0 in prior:slot=prior.index(0);branch='empty'
  else:
   eligible=[n for n,p in enumerate(prior)if priority>=p]
   need(eligible,'No observed admission of a source-suppressed lower-priority cue');slot=eligible[0];branch='replacement'
  need(q['entry']==('FFA12A10','FFA12A80','FFA12B00')[slot]and same(r,q)and same(r,endq)and
       r['sp']==q['sp']==endq['sp']and clock(r)<clock(q)<clock(endq)and
       all(r[k]==q[k]for k in('a1','a3','a4','p0','p1','p2','d0','d1','d2')),
       'Actual original first eligible slot branch from directly observed all-three pre-call priorities/deadlines')
  for n in range(3):
   need(integer(endq,'p'+str(n))==(priority if n==slot else prior[n])and
        integer(endq,'d'+str(n))==(duration if n==slot else deadlines[n]),'Exact native selected slot stores; all other priorities/deadlines preserved')
  need(integer(endq,'a3')==base+slot,'Native emitted packet includes source slot increment only')
  branches[branch]+=1;slots[slot]+=1;selection.append(dict(pointer=pointer,priority=priority,duration=duration,base=base,slot=slot,branch=branch))
 for r,h in zip(dispatch,headers,strict=True):
  pointer=0xffa0ef20+integer(r,'a0')*32;header,base=struct.unpack_from('<HH',stock,off(pointer))
  matches=[s for s in select if same(h,s)and h['sp']==s['sp']and clock(h)<clock(s)<clock(h)+Decimal('.00001')]
  need(same(r,h)and integer(h,'sp')==integer(r,'sp')-128 and integer(h,'a0')==pointer and
       integer(h,'header')==header and integer(h,'base')==base and len(matches)==1 and
       integer(matches[0],'a0')==pointer+32,'Every actual general dispatcher indexes original full record and exact decoded selection')
  literal={'FF870E30':4,'FF8EB5B0':0x1b,'FFA0D200':0xd0,'FF85C5B0':0xcf}
  if r['top']in literal:need(integer(r,'a0')==literal[r['top']],'Actual original literal cue producer')
  else:need(r['top']in('FF8EB610','FF85C610','FF9B0CB0'),'No unexplained general native cue caller')
 need(branches['empty']>0 and branches['replacement']>0 and not branches['special71'],'Actual empty and replacement coverage; special71 not exercised')
 return dict(passed=True,fighter=fighter,physicalSlot=side,ownID=identity,actualOriginalVictimID=8,
             nativeCoreCalls=1121,nativeMainLoopCalls=1101,nativeBoundedRNGCalls=20,
             actualSoundVariantSelectors=selectors,actualQueueSelections=selection,
             actualPriorityBranches=dict(branches),actualSelectedSlots=dict(slots),
             actualSeedOverflowBranches={str(k):v for k,v in overflow_counts.items()},
             actualBeamRotationCounts={str(k):v for k,v in rotation_counts.items()},
             allObservedNativeRNGWordsAndChoicesAccepted=True,allObservedEmptyReplacementSlotDecisionsAccepted=True,
             nativeSuppressionBranchAccepted=False,nativeSpecial71BranchAccepted=False,
             allNativePitCuePriorityAndRNGAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False)

def run():
 basepath=audio_matrix.OUT/'report.json';base=json.loads(basepath.read_text())
 need(base['passed']and len(base['cases'])==4 and base['actualSourceAudioFaultsRejected']==116 and
      base['actualEarnedStateFaultsRejected']==48,'Whole actual5966 audio/channel/DAC/ROM/ADSP/raw/state/fault scopes retained')
 guest=audio_matrix.observed.current.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes()
 pins=dict(base['inputHashes']);pins[str(basepath)]=sha(basepath);cases=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   folder=ROOT/f'audit_v5964_current_pit_queue_rng_{fighter}_p{side}_samples'
   with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
   retained_owner=ownership.gate(text,guest,stock,fighter,side)
   good=gate(text,guest,stock,fighter,side);faults=[]
   def reject(label,bad,bad_guest=guest):
    need(bad!=text or bad_guest!=guest,'Effective actual source/queue/RNG counterexample')
    try:gate(bad,bad_guest,stock,fighter,side)
    except(ValueError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
    else:raise ValueError('Altered actual native RNG/priority evidence admitted '+label)
    need(gate(text,guest,stock,fighter,side)==good,'Whole actual native positive restored after every source/queue/RNG fault')
   for tag,key,value in(('RNG_SEED','seed','00000000'),('RNG_STORE','a0','00000000'),
                         ('RNG_ROTATE','a0','00000000'),('RNG_WORD','a0','00000000'),('RNG_WORD','a1','00000000'),
                         ('RNG_MULTIPLY','a0','00000000'),('RNG_MULTIPLY','a1','00000000'),
                         ('RNG_PRODUCT','a1','00000000'),('RNG_RETURN','a0','00000000'),('RNG_RETURN','a1','00000000'),
                         ('RNG_BEGIN','top','00000000'),('PACKED_BEGIN','a0','00030074'),
                         ('VOICE_BEGIN','a1','000000CE'),('DISPATCH','top','00000000'),
                         ('HEADER','header','0000'),('HEADER','base','0000'),('SELECT','a1','00000000'),
                         ('SELECT','p0','FFFF'),('QUEUE','entry','FFA12B00'),('FINISH','p0','0000'),('FINISH','a3','00000000')):
    line=next(l for l in text.splitlines()if l.startswith('MK2_PQR_'+tag+' '))
    bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
    need(n==1 and bad!=line,'Actual native snapshot mutation');reject(tag+'/'+key,text.replace(line,bad,1))
   for tag in('RNG_WORD','RNG_BEGIN','HEADER','SELECT','QUEUE','FINISH'):
    line=next(l for l in text.splitlines()if l.startswith('MK2_PQR_'+tag+' '));reject('Missing '+tag,text.replace(line+'\n','',1))
   for address in(0xff80e9c0,0xff80ea50,0xff80ea90,0xff80eb20,0xffa121e0,0xffa0ef20+4*32,0xffa12820,0xffa12910,0xffa12ae0):
    bad=bytearray(guest);bad[off(address)]^=1;reject('Original source '+hex(address),text,bytes(bad))
   need(len(faults)==36,'Every36 actual native RNG/priority/source fault rejected')
   good.update(actualFaultsRejected=faults,retainedDirectCinematicOwnership=retained_owner,capture=str(folder));cases.append(good)
 for p in(Path(__file__).resolve(),Path(ownership.__file__).resolve(),Path(audio_matrix.__file__).resolve(),stockpath,
          ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'):
  pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every current/compiled/source/native/failed/prior evidence byte unchanged')
 return dict(passed=True,cases=cases,inputHashes=pins,actualNativeCoreCalls=4484,actualBoundedRNGCalls=80,
             actualSoundVariantSelectors=32,actualObservedSlotDecisions=72,actualNativeRNGPriorityFaultsRejected=144,
             whole5966AudioAndAllFaultsRetained=True,whole5950DirectOwnerContractRetained=True,
             allObservedNativeRNGWordsAndChoicesAccepted=True,allObservedEmptyReplacementSlotDecisionsAccepted=True,
             nativeSuppressionBranchAccepted=False,nativeSpecial71BranchAccepted=False,
             allNativePitCuePriorityAndRNGAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,
             newNativeBoots=0,newBuilds=0,rawRecordingsWritten=0,publicPlayableChanged=False)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual native RNG/priority qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
