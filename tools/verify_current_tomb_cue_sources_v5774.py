"""Actual native Tomb cue producers and emitted queue words, eight contexts.

Keep complete held/pressed earned-state, voice and native waveform evidence.
Bind every general cue to its original literal or packed helper; all observed
emitted general queues retain original priority/duration/base and slot packet.
Without pre-call priority/RNG snapshots, suppression/variant choice itself is
not accepted here. Do not confuse native-nosamples with enabled winner mixing.
"""
import datetime,gzip,json,re,struct,subprocess,traceback
from decimal import Decimal
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5775_current_tomb_native_cue_source_checked'
off=lambda address:(address-0xff800000)//8


def records(text):
 result={}
 for line in text.splitlines():
  if not line.startswith('MK2_MAUDIO_'):continue
  tag=line.split(' ',1)[0].removeprefix('MK2_MAUDIO_')
  pairs=re.findall(r'(\w+)=([^\s]+)',line);row=dict(pairs)
  need(len(row)==len(pairs),'Every native cue source row unique keys')
  result.setdefault(tag,[]).append(row)
 return result


def gate(text,guest,stock,fighter,side,pressed):
 rs=records(text);routes=[r for r in rs['ROUTE']if r['entry']in ('FFA12530','FFA12430')]
 general=[r for r in routes if r['entry']=='FFA12530']
 first=next(l for l in text.splitlines()if l.startswith('MK2_STAGE_FIELD '))
 field=dict(re.findall(r'(\w+)=([^\s]+)',first))
 identity=17 if fighter=='kano'else 18
 need(field['id']==field['victim_id']==str(identity),'Actual true mirror native field')
 def exact(address,words,label):
  raw=struct.pack('<'+'H'*len(words),*words);at=off(address)
  need(guest[at:at+len(raw)]==stock[at:at+len(raw)]==raw,'Entire original '+label+' cue source')
 for a,b in ((0xffa0ef20,0xffa10ee0),(0xffa12530,0xffa12bd0),(0xff80eae0,0xff80f000)):
  need(guest[off(a):off(b)]==stock[off(a):off(b)],'Whole original general command table, dispatcher/queue and native RNG source')
 exact(0xffa12180,(0x4c01,0x2e00,0x0521,0x0d5f,0xeae0,0xff80,0x1420,0x4020,0xc032),
  'packed count/base extraction, native RNG call, decrement/add, original dispatcher jump')
 proof=[]
 queues=rs['QUEUE'];packets=rs['PACKET'];claimed=set()
 for i,r in enumerate(routes):
  if r['entry']!='FFA12530':continue
  caller=int(r['return_pc'],16);command=int(r['a0'],16)
  need(r['writes']=='0'and r['assistance']=='none'and r['owner']==r['a8'],'Actual native cue owner, not fabricated dispatcher')
  if caller in (0xff870e30,0xff8eaa30,0xff8eaea0):
   value={0xff870e30:4,0xff8eaa30:0x1b,0xff8eaea0:0x44}[caller]
   exact(caller-80,(0x09c0,value,0x0d5f,0x2530,0xffa1),'literal command and CALLA')
   need(command==value,'Actual cue equals original literal producer')
   victim=caller!=0xff870e30
   need(r['a8']==field['victim'if victim else'own']and r['a13']==field['victim_main'if victim else'main']and
    r['id']==str(identity),'Literal cue owns real performer or victim task')
   kind='original literal'
  elif caller==0xff8eaed0:
   exact(caller-48,(0x0d5f,0x20b0,0xffa1),'ceiling voice CALLA')
   exact(0xffa120b0,(0x09e1,0xb8b7,0x8585,0xc012),'packed one-variant ceiling voice selector')
   need(command==(0xb7 if identity==18 else 0x85)and int(r['a1'],16)==command and
    int(r['a2'],16)==(18 if identity==18 else 3-side)and
    r['a8']==field['victim']and r['a13']==field['victim_main']and r['id']==str(identity),
    'Source-owned current gender/Main role initial victim voice, never Liu proxy')
   kind='original role/female ceiling voice'
  elif caller in (0xff9b0cb0,0xff9ac6d0):
   displacement=0xffc9 if caller==0xff9b0cb0 else 0x0427
   exact(caller-32,(0x0d3f,displacement),'particle CALLR to three-choice gore helper')
   signed=displacement if displacement<0x8000 else displacement-0x10000
   need((caller+signed*16)&0xffffffff==0xff9b0940,'Actual signed CALLR reaches original packed gore helper')
   exact(0xff9b0940,(0x09e0,0x0073,0x0003,0xc080,0x2180,0xffa1),'original packed base73/count3 and dispatch jump')
   need(command in (0x73,0x74,0x75)and r['a1']=='00000073'and r['id']=='0',
    'Observed particle actor uses original three-choice domain/base, not any extra sound command')
   kind='original three-choice particle'
  elif caller==0xff8eb2c0:
   need(pressed,'No falling voice attributed to held branch')
   exact(caller-48,(0x0d5f,0x1fd0,0xffa1),'late victim scream CALLA')
   exact(0xffa11fd0,(0x1840,0x09e1,0x3638,0x3234,0xc020),'original two-variant role/female packed selector')
   base=0x38 if identity==18 else (0x32 if 3-side==1 else 0x34)
   need(command in (base,base+1)and int(r['a1'],16)==base and
    int(r['a2'],16)==(18 if identity==18 else 3-side)and
    r['a8']==field['victim']and r['a13']==field['victim_main']and r['id']==str(identity),
    'Actual native falling voice source-selected physical Main role or genuine female extension')
   kind='original two-choice late victim voice'
  elif caller==0xff8eb3f0:
   need(pressed,'No floor landing cue attributed to held branch')
   exact(caller-48,(0x0d5f,0xa3f0,0xff8e),'original Tomb landing helper CALLA')
   exact(0xff8ea3f0,(0x09eb,6,6,0x0d5f,0x1290,0xff9e,0xc080,0x1e60,0xffa1),
    'whole original landing/helper/packed floor jump')
   exact(0xffa11e60,(0x09e0,0x001f,4,0xc02e),'packed original landing base1F/count4')
   need(0xffa11e60+64+0x2e*16==0xffa12180 and 0x1f<=command<=0x22 and r['a1']=='0000001F'and
    r['a8']==field['victim']and r['a13']==field['victim_main']and r['id']==str(identity),
    'Actual landing uses complete native four-choice domain and real victim task')
   kind='original four-choice floor landing'
  else:raise ValueError('Unexplained native general Tomb cue producer '+r['return_pc'])
  header,base=struct.unpack_from('<HH',stock,off(0xffa0ef20+command*32))
  need(header and not header&0x8000,'Actual source-owned simple native general cue record')
  limit=Decimal(routes[i+1]['seconds'])if i+1<len(routes)else Decimal(rs['RESULT'][0]['seconds'])
  qs=[(n,q)for n,q in enumerate(queues)if Decimal(r['seconds'])<Decimal(q['seconds'])<limit]
  need(len(qs)<=1,'At most one actual emitted general queue before next dispatcher; no ignored descendants')
  emitted=None
  if qs:
   n,q=qs[0];need(n not in claimed,'Native general queue only owned by one actual dispatcher');claimed.add(n)
   slot=('FFA12A10','FFA12A80','FFA12B00').index(q['entry'])
   need(q['frame']==r['frame']and all(q[k]==r[k]for k in('a8','a13'))and
    int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==base,
    'Actual emitted original header priority/duration/base and owned native slot registers')
   found=[p for p in packets if Decimal(q['seconds'])<Decimal(p['seconds'])<limit and
    all(p[k]==q[k]for k in('frame','a8','a13'))]
   need(len(found)==1 and int(found[0]['a3'],16)==base+slot and
    all(found[0][k]==q[k]for k in('a1','a4')),
    'Actual full queue emits exactly source base+native slot word and preserves priority/duration')
   emitted=dict(actualQueue=q,actualPacket=found[0],slot=slot,sourceHeader=header,sourceBase=base)
  proof.append(dict(actualCall=r,sourceKind=kind,emitted=emitted))
 need(len(general)==len(proof)==(12 if pressed else 21),'Whole actual general cue inventory, no selected-only filtering')
 return dict(passed=True,fighter=fighter,physicalSlot=side,branch='pressed'if pressed else'held',
  actualGeneralCalls=len(proof),actualGeneralEmittedQueues=len(claimed),producers=proof,
  allCapturedGeneralCueProducersSourceAccounted=True,allEmittedGeneralQueueWordsSourceExact=True,
  nativePriorityChoiceAndSuppressionAccepted=False,actualRNGVariantChoiceAccepted=False,
  announcerAndDirectProducersAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False)


def faults(text,guest,stock,fighter,side,pressed):
 good=gate(text,guest,stock,fighter,side,pressed);faults=[]
 def reject(label,bad,bad_guest=guest):
  need(bad!=text or bad_guest!=guest,'Actual nonvacuous Tomb cue fault')
  try:gate(bad,bad_guest,stock,fighter,side,pressed)
  except (ValueError,KeyError)as error:faults.append(dict(label=label,rejectedBy=str(error)))
  else:raise ValueError('Altered actual cue source admitted '+label)
  need(gate(text,guest,stock,fighter,side,pressed)==good,'Entire actual cue positive restored after each fault')
 targets=[(0xff870de0,'performer literal4'),(0xff8ea9e0,'Tomb literal1B'),(0xff8eae50,'impact literal44'),
  (0xffa120b0,'original packed ceiling selector'),(0xff9b0c90,'particle signed CALLR'),
  (0xff9b0940,'packed gore base/count'),(0xffa12180,'native packed helper'),(0xff80eae0,'native RNG source'),
  (0xffa0ef20+0x1b*32,'actual source command header'),(0xffa12a10,'actual original queue source')]
 if not pressed:targets.append((0xff9ac6b0,'held late particle CALLR'))
 else:targets.extend([(0xffa11fd0,'packed two-choice falling voice'),(0xff8eb290,'late voice caller'),
  (0xff8ea3f0,'native landing helper'),(0xffa11e60,'native four-choice landing domain')])
 for address,label in targets:
  altered=bytearray(guest);altered[off(address)]^=1;reject(label,text,bytes(altered))
 def mutate(tag,where,key,value):
  row=next(l for l in text.splitlines()if l.startswith('MK2_MAUDIO_'+tag+' ')and where in l and
   (tag!='ROUTE'or 'entry=FFA12530 'in l))
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,row,count=1)
  need(n==1 and bad!=row,'Effective actual cue register fault');return text.replace(row,bad,1)
 for tag,where,key,value,label in [
  ('ROUTE','return_pc=FF8EAA30','a0','0000001C','wrong literal command'),
  ('ROUTE','return_pc=FF8EAED0','a1','00000047','wrong ceiling voice source base'),
  ('ROUTE','return_pc=FF9B0CB0','a0','00000076','outside original particle variant domain'),
  ('ROUTE','return_pc=FF9B0CB0','return_pc','00000000','unowned particle caller'),
  ('QUEUE','','a1','00000000','emitted priority corrupted'),
  ('QUEUE','','a4','00000000','emitted duration corrupted'),
  ('QUEUE','','a3','00000000','emitted source base corrupted'),
  ('QUEUE','','a13','00000000','foreign emitted queue task'),
  ('PACKET','a3=00000082','a3','00000083','wrong source base plus slot packet')]:
  reject(label,mutate(tag,where,key,value))
 if pressed:
  reject('wrong landing source domain',mutate('ROUTE','return_pc=FF8EB3F0','a0','00000023'))
  reject('wrong native late voice domain',mutate('ROUTE','return_pc=FF8EB2C0','a0','00000047'))
 return faults


def run():
 need(not OUT.exists(),'Fresh immutable full native Tomb cue source check')
 guest=current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pins={};cases=[]
 specs=[(False,5756,5754,'actualCurrentBothCharactersBothSidesHeldTombNativeDCSAudioAccepted'),
  (True,5769,5765,'actualCurrentBothCharactersBothSidesPressedTombNativeDCSAudioAccepted')]
 for pressed,version,capture,key in specs:
  reportpath=ROOT/(f'audit_v{version}_current_'+('pressed_'if pressed else'')+'tomb_native_source_audio_matrix_checked/report.json')
  report=json.loads(reportpath.read_text())
  need(report['passed']and report[key]and len(report['cases'])==4 and report['exactStereoPCMFrames']==3863040,
   'Actual entire current four-case earned/state/source clock/voice/audio window and genuine fault matrix retained')
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent full current/native source pins');pins[p]=h
  pins[str(reportpath)]=sha(reportpath)
  for side in (1,2):
   for fighter in ('kano','sonya'):
    folder=ROOT/(f'audit_v{capture}_current_'+('pressed_'if pressed else'')+f'tomb_source_audio_{fighter}_p{side}_nosamples')
    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
    proved=gate(text,guest,stock,fighter,side,pressed);rejected=faults(text,guest,stock,fighter,side,pressed)
    need(len(rejected)==(25 if pressed else 20),'Every actual complete native cue source/register fault')
    cases.append(dict(**proved,actualCueSourceFaultsRejected=rejected,capture=str(folder)))
 for p in (Path(__file__),ROOT/'mk2/mk2-maincpu.bin'):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All original/actual current waveform, physical/phase and cue evidence unchanged')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  cases=cases,inputHashes=pins,actualGeneralProducerCalls=sum(c['actualGeneralCalls']for c in cases),
  actualEmittedGeneralQueueWords=sum(c['actualGeneralEmittedQueues']for c in cases),
  actualCueSourceFaultsRejected=sum(len(c['actualCueSourceFaultsRejected'])for c in cases),
  allCapturedGeneralCueProducersSourceAccounted=True,allEmittedGeneralQueueWordsSourceExact=True,
  retainedExactStereoPCMFrames=7726080,nativePriorityChoiceAndSuppressionAccepted=False,
  actualRNGVariantChoiceAccepted=False,announcerAndDirectProducersAccepted=False,
  samplesEnabled=False,importedWinnerMixedWaveformAccepted=False,completeStageVictimAudioAccepted=False,
  fullStageArtAccepted=False,fullPortAcceptance=False,newNativeBoots=0,newBuilds=0,rawMediaWritten=0,publicPlayableChanged=False)


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual cue source result');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
