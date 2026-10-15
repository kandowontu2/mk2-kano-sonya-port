"""Finite current5219 table/ladder/AI inventory; never universal runtime proof.

Use the actual frozen compiled source and independently reconstructed whole
guest, bound to actual current-CMD captures. Do not reuse the old3172 inventory
as a current runtime pass, or infer coverage from a human special test.
"""
import datetime,hashlib,json,re,struct,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import capture_current_cmd_specials_v6263 as cmd_capture
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6271_current_native_branch_inventory'
PARENT=ROOT/'audit_v6268_current_cmd_gameplay_progress/progress.json'
SOURCE=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
def at(address):return(address-0xff800000)//8
def addr(offset):return 0xff800000+offset*8
def u32(raw,offset):return struct.unpack_from('<I',raw,offset)[0]
def digest(raw):return hashlib.sha256(raw).hexdigest().upper()

# Explicit types and original consumers from the compiled constructor.
TABLES=[
 ('P1 lifebar',0xfdc00,19,8,0xff806480,(0xff805a70,),17,None),
 ('P2 lifebar',0xfdd00,19,8,0xff8068c0,(0xff805bf0,),17,None),
 ('winner text',0xfdf00,19,4,0xff822280,(0xff829680,),17,None),
 ('damage scaling',0xfe100,19,4,0xff8367b0,(0xff836750,),17,(0,0)),
 ('AI decision',0xf4400,19,4,0xff9b1db0,(0xff9b1d60,),17,(0xff9b20d0,)*2),
 ('AI round reset',0xf4500,19,4,0xff9b2210,(0xff9b21c0,),17,(0xff9b91b0,)*2),
 ('AI action follow-up: ACTION index, not fighter ID',0xf4800,24,4,0xff9b76d0,(0xff9b7680,),17,(0xff9b91b0,)*7),
 ('AI action dispatch: ACTION index, not fighter ID',0xf4480,24,4,0xff8a5960,(0xff8a5920,),22,(addr(0xf7800),addr(0xf7840))),
 ('Babality commands',0xf97a0,19,4,0xff87e3a0,(0xff87e250,),17,(addr(0xf97f0),addr(0xf9810))),
 ('Friendship commands',0xf98a0,19,4,0xff880a70,(0xff8808a0,),17,(addr(0xf9940),addr(0xf9960))),
 ('Friendship actions',0xf98f0,19,4,0xff880d90,(0xff880d40,),17,(addr(0xf9a00),addr(0xf9c00))),
 ('Reptile victim offsets',0xfa800,19,8,0xff8c9900,(0xff8c8a70,),17,None),
 ('Jax head-clap offsets',0xfb600,19,4,0xff8c7ff0,(0xff8c7b50,),17,None),
 ('Kitana inflation sequence',0xfac40,19,4,0xff9ed0f0,(0xff9ec840,),17,None),
 ('Kitana inflation first palette',0xfac90,19,4,0xff9eca40,(0xff9ec8b0,),17,None),
 ('Kitana inflation second palette',0xface0,19,4,0xff9ecc30,(0xff9ecbd0,),17,None),
 ('Kung Lao split sequence',0xfbf40,19,4,0xff8cf110,(0xff8cea70,),17,None),
 ('projectile reactions outer',0xfc900,19,4,0xff8d2bd0,(0xff835de0,),17,(addr(0xfca00),addr(0xfcb00))),
 ('attack descriptors outer',0xfcc00,19,4,0xff8eba90,(0xff8eba30,),17,(addr(0xfcd00),addr(0xf8f00))),
 ('normal palettes',0xfd800,19,4,0xff907910,(0xff906f40,0xff907760,0xff8954e0),17,(addr(0xfda00),addr(0xfdb00))),
 ('alternate palettes',0xfd880,19,4,0xff907b30,(0xff907060,0xff907810,0xff895520),17,(addr(0xf1500),addr(0xf1600))),
 ('shock/freeze palettes',0xfd900,19,4,0xff9109e0,(0xff8dada0,0xff910970),17,(addr(0xf59a0),addr(0xf5a40))),
 ('Babality victim images',0xf9600,19,4,0xff87f020,(0xff87eb30,),17,(addr(0xf9680),addr(0xf96a0))),
 ('stock airborne-throw victim offsets',0xffdc0,19,4,0xff8b7d20,(0xff8b7410,),17,None),
]
PARAMETERS=[
 ('get-up',0xff8e7340,(0xff8e6b90,0xff8e6bf0),4,4),
 ('idle cadence',0xff9066a0,(0xff906620,),5,5),
 ('roundhouse cadence',0xff8729c0,(0xff8727d0,),3,3),
 ('knee recovery',0xff8733c0,(0xff872ca0,),20,20),
 ('elbow cadence',0xff873e10,(0xff873a20,),2,2),
 ('elbow recovery',0xff873d00,(0xff873bb0,),14,14),
 ('reaction displacement',0xff8e65a0,(0xff8e6380,),32,32),
 ('floor anchor',0xff908010,(0xff907f70,),134,135),
 ('entrance alignment',0xff905f40,(0xff905ef0,),2,0),
 ('winner voice',0xff8224a0,(0xff8209e0,),254,253),
 ('paired throw cadence',0xff8b9460,(0xff8b8870,0xff8b8a20),4,4),
 ('human thrown alignment',0xff8b9a30,(0xff8b98b0,),0,0),
 ('CPU action selection',0xff9b9360,(0xff9b90c0,0xff9b9260),22,23),
 ('paired victim shape',0xff892d60,(0xff8923a0,),0,1),
 ('Kitana victim cursor',0xff8cd3b0,(0xff8cc790,),64,64),
 ('Kitana victim alignment',0xff8cd2f0,(0xff8ccc80,),(-73)&65535,(-73)&65535),
]

def table_gate(raw,stock,spec):
 name,offset,rows,stride,source,consumers,native_rows,additions=spec
 need(raw[offset:offset+native_rows*stride]==stock[at(source):at(source)+native_rows*stride],name+': all original typed rows preserved')
 for consumer in consumers:need(u32(raw,at(consumer))==addr(offset),name+': native consumer points at full extended table')
 if additions is not None:
  fmt='H'if stride==2 else'I';actual=struct.unpack_from('<'+fmt*len(additions),raw,offset+native_rows*stride)
  need(actual==tuple(additions),name+': exact compiled-source appended entries')
 return dict(name=name,byteOffset=offset,rows=rows,strideBytes=stride,originalRowsPreserved=native_rows,originalSourceAddress=source,nativeConsumers=list(consumers),explicitAppendedEntriesChecked=additions is not None,sha256=digest(raw[offset:offset+rows*stride]))

def ladder_gate(raw,stock):
 need(u32(raw,at(0xff8a11f0))==addr(0xf4580),'Actual native ladder pointer consumer')
 inserts=((0,5),(0,7),(2,8),(3,9),(1,6),(0,8));rows=[]
 for order,(first,second)in enumerate(inserts):
  source=u32(stock,at(0xff8a1260)+order*4)
  need(source==0xff8a1320+order*0x100,'Original six native schedule pointers')
  old=list(struct.unpack_from('<16H',stock,at(source)));expected=[];regular=iter(old[:11])
  for slot in range(13):expected.append((18 if order&1 else 17)if slot==first else(17 if order&1 else 18)if slot==second else next(regular))
  expected+=old[11:16];offset=0xf4600+order*0x30
  actual=list(struct.unpack_from('<18H',raw,offset))
  need(actual==expected and u32(raw,0xf4580+order*4)==addr(offset),'Both real added IDs, original relative ordering and complete boss tail in every schedule')
  rows.append(dict(order=order,ownIDs=[17,18],ownInsertionSlots=[first,second],originalRegularIDs=old[:11],actualNativeSchedule=actual))
 positions=tuple(940-(754*i+7)//15 for i in range(16))+(128,)
 scroll=(784,784)+tuple(940-(754*i+7)//15-98 for i in range(2,14))+(940-(754*13+7)//15-98,88,4)
 need(struct.unpack_from('<17H',raw,0xf4740)==positions and struct.unpack_from('<17H',raw,0xf4780)==scroll and u32(raw,at(0xff8a05c0))==addr(0xf4740)and u32(raw,at(0xff8a0df0))==addr(0xf4780),'All native tower positions and scroll consumers')
 return rows

def ai_gate(raw):
 branches=[]
 for fighter,offset,destinations,names in(
  ('kano',0xf7800,(0xff600,0xffbc0,0xf1980),('knife','ball','blade')),
  ('sonya',0xf7840,(0xff680,0xff940,0xf3480),('ring','square','bicycle'))):
  words=[0x09c0,0xfa,0x0d5f,0xec20,0xff80,0xc80c,0x09c0,0x190,0x0d5f,0xec20,0xff80,0xc803]
  for destination in destinations:words.extend((0xc080,addr(destination)&65535,addr(destination)>>16))
  expected=struct.pack('<'+'H'*len(words),*words)
  need(raw[offset:offset+len(expected)]==expected,'Every actual final native RNG/branch opcode: '+fighter)
  branches.extend(dict(fighter=fighter,move=name,router=addr(offset),target=addr(destination),choice='original native RNG',runtimeAutomaticallyAccepted=False)for name,destination in zip(names,destinations))
 need(u32(raw,at(0xff9b71f0))==addr(0xf7880),'Actual shared grounded-close consumer')
 for fighter,offset,destination,name in(('sonya',0xf78a0,0xf0100,'leg'),('kano',0xf78c0,0xf2200,'choke')):
  words=(0x09c0,0xfa,0x0d5f,0xec20,0xff80,0xc980,addr(0xf78e0)&65535,addr(0xf78e0)>>16,0xc080,addr(destination)&65535,addr(destination)>>16)
  need(raw[offset:offset+22]==struct.pack('<11H',*words),'Actual independent native close-signature chance/target '+fighter)
  branches.append(dict(fighter=fighter,move=name,router=addr(offset),target=addr(destination),choice='original native RNG',runtimeAutomaticallyAccepted=False))
 return branches

def run():
 need(not OUT.exists(),'Fresh immutable current finite inventory')
 need(not cmd_capture.prior.census(),'Actual native census empty; no additional game needed')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();stockpath=ROOT/'mk2/mk2-maincpu.bin'
 need(sha(stockpath)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Whole original native reference ROM')
 stock=stockpath.read_bytes();source=SOURCE.read_text();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Entire original objective retained')
 need(len(re.findall(r'^\s*extend_parameters\(0x',source,re.M))==len(PARAMETERS),'All sixteen actual constructor parameter calls accounted, not an old subset')
 specs=TABLES+[(name,0xfd300+i*0x40,19,2,origin,consumers,17,(k,s))for i,(name,origin,consumers,k,s)in enumerate(PARAMETERS)]
 tables=[table_gate(guest,stock,spec)for spec in specs];ladders=ladder_gate(guest,stock);branches=ai_gate(guest)
 need(payload[0x130100:0x130100+17*4]==stock[at(0xff85e6b0):at(0xff85e6b0)+17*4]and all(u32(guest,at(c))==0xff180800 for c in(0xff85c330,0xff85c4a0)),'Pit sequence is a nineteen-row payload table, not a guest-table offset')
 faults=[]
 def reject(label,gate,raw):
  try:gate(raw)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual typed inventory fault accepted: '+label)
 for spec in specs:
  altered=bytearray(guest);altered[spec[1]]^=1;reject(spec[0]+' original row',lambda g:table_gate(g,stock,spec),altered)
  altered=bytearray(guest);altered[at(spec[5][0])]^=1;reject(spec[0]+' actual consumer',lambda g:table_gate(g,stock,spec),altered)
  if spec[7]is not None:
   altered=bytearray(guest);altered[spec[1]+spec[6]*spec[3]]^=1;reject(spec[0]+' own append',lambda g:table_gate(g,stock,spec),altered)
 for order in range(6):
  altered=bytearray(guest);altered[0xf4600+order*0x30]^=1;reject('ladder order '+str(order),lambda g:ladder_gate(g,stock),altered)
 for branch in branches:
  altered=bytearray(guest);altered[at(branch['router'])]^=1;reject(branch['fighter']+' '+branch['move']+' native route',ai_gate,altered)
 need(tables==[table_gate(guest,stock,s)for s in specs]and ladders==ladder_gate(guest,stock)and branches==ai_gate(guest),'All positives restored after real data mutations')
 proofpath=ROOT/'audit_v6266_current_cmd_special_matrix_checked/report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed']and proof['guestSHA256']==digest(guest)and proof['candidate']==current.NAME,'Entire current reconstructed guest bound to actual sixteen canonical-CMD captures')
 pins=dict(proof['inputHashes']);pins.update({str(p.resolve()):sha(p)for p in(PARENT,proofpath,SOURCE,stockpath,Path(__file__).resolve(),Path(current.__file__))})
 need(all(sha(p)==h for p,h in pins.items()),'Actual current compiled/guest/controller/evidence bindings unchanged')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=digest(guest),payloadSHA256=digest(payload),goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],tables=tables,actualTypedGuestTables=len(tables),payloadTable=dict(name='Pit victim sequences',rows=19,byteOffset=0x130100,nativeAddress=0xff180800,stockRowsPreserved=17),nativeLadderSchedules=ladders,nativeCPUSpecialBranches=branches,actualInventoryFaultsRejected=faults,inputHashes=pins,
  previousGoalTurnClassification='progress: sixteen actual canonical-CMD combat runs and original194fault gate',thisGoalTurnClassification='progress: current frozen source/whole guest bound to native captures; forty typed guest tables and all six native ladder schedules and eight CPU branches validated with actual corruption rejection; older3172 inventory not promoted',
  inventoryExhaustiveForEveryGameFeature=False,allEightCPUBranchesRuntimeAccepted=False,fullPortAcceptance=False,fullGoalComplete=False,newNativeBoots=0,newBuilds=0,newRawMedia=0,newZIPs=0,
  nextActions=['Requalify existing current CPU leg/ring branch evidence before adding a capture','Target current Kano knife/ball/blade CPU branches; human activation is not sufficient evidence','Finish remaining stage/victim branch fidelity and the combined visual/audio release handoff'])
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Only compact terminal inventory; no new raw data')
 print(json.dumps(dict(passed=True,tables=len(tables),ladderSchedules=len(ladders),CPUSpecialBranches=len(branches),actualInventoryFaultsRejected=len(faults),newNativeBoots=0,fullPortAcceptance=False)),flush=True)

if __name__=='__main__':
 try:run()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
