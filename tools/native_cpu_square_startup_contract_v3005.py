"""Native actual CPU Square miss phases including true startup entry locks.

Original v2045 eight-field rise, 26-check flight, exact drop/landing/hold and
individual lock/ready checks retained. True mirror identity and independently
captured initial write chains accepted, not a fabricated initial FIELD. Later
native signature branches truncate only the ordinary tail and stay explicitly
unaccepted as thirty-one-callback ordinary followup. Not hit/art/audio proof.
"""
import re,struct
import verify_native_cpu_square_inventory_v2998 as inventory
import verify_current_physical_p2_cpu_v1916 as launch
import verify_current_cpu_overlap_v1911 as original
ROOT=launch.ROOT;P=launch.original;one=original.one
INTRO=(0xfe835c80,)
POSE_DONORS={0xfe835c80:0xff835c80,0xff031340:0xff836160,
 0xff031380:0xff8361a0,0xff0313c0:0xff840880,0xfe835c20:0xff835c20,
 0xfe835bc0:0xff835bc0}
POSES=set(POSE_DONORS)
HEX=original.HEX|set('opcode schedule status mask a0 a1 a2 a3 floor actor main owner'.split())-{'floor'}
TEXT=original.TEXT
def rows(log,prefix):
 result=[]
 for line in log.splitlines():
  if not line.startswith(prefix+' '):continue
  pairs=re.findall(r'(\w+)=([^\s]+)',line)
  assert len(pairs)==len(dict(pairs))
  result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
 return result

def source(log,guest):
 base=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 windows=original.rows(log,'CODE')+rows(log,'MK2_CPU_CHOICE_CODE')+rows(log,'MK2_SQUARE_NATIVE_CODE')
 expected={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),(0xff861350,0xff861700),
  (0xfffc3800,0xfffc5800),(0xfffc6000,0xfffc8000),(0xfffbc200,0xfffbc350),
  (0xff80ec20,0xff80ed40),(0xffffca00,0xffffd200),(0xff876420,0xff876b60)}
 assert len(windows)==len(expected)and {(r['start'],r['stop'])for r in windows}==expected
 for r in windows:
  lo,hi=((r[k]-0xff800000)//8 for k in('start','stop'))
  words=[int(v,16)for v in r['words'].split(',')]
  assert len(words)==(hi-lo)//2 and struct.pack('<'+'H'*len(words),*words)==guest[lo:hi]
  if r['start']<0xfff00000:assert guest[lo:hi]==base[lo:hi],'Original RNG/fall/cleanup/ready code unchanged'
 def check(at,words):
  assert struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words)
 check(0xfffbc200,(0x09c0,250,0x0d5f,0xec20,0xff80,0xc80c,0x09c0,400,
  0x0d5f,0xec20,0xff80,0xc803,0xc080,0xb400,0xffff,0xc080,0xca00,0xffff,0xc080,0xa400,0xfff9))
 check(0xff80ec20,(0x098f,0x6000,0x4c02,0x0d5f,0xe980,0xff80,0x09c1,1000,0x5e20,0x4840,0x09af,6,0x0960))
 check(0xffffca00,(0x09e1,0x207,0,0x0d5f,0x7ba0,0xff87))
 check(0xffffcb50,(0x09e0,0,0xfff4,0xb208,0x60))
 check(0xffffcc30,(0x0b40,0xff9f,0xc880,0xcba0,0xffff))
 check(0xffffcd70,(0x09e0,0,0x000a,0x0d5f,0x6c80,0xff87,0x09eb,26,0))
 check(0xffffcff0,(0x09e0,0,0,0x09e1,0,2,0x09e2,0x8000,0,0x09e3,0xfff,0))
 check(0xffffd0f0,(0xc080,0x6650,0xff87))
 check(0xffffd160,(0xc080,0x6420,0xff87,0xc080,0x1350,0xff86))

def verify(log,guest,player):
 assert not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I)
 source(log,guest)
 orders=P.expected_orders();roms=P.rows(log,'ROM')
 assert len(roms)==6 and all(r['table']==0xfffa2c00 and r['order']==i and r['list']==0xfffa3000+i*0x180 and tuple(map(int,r['ids'].split(',')))==orders[i]for i,r in enumerate(roms))
 sel=one(P.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT '),'Cold native selection')
 cold=one(P.rows_prefix(log,'MK2_P2CPU_COLD_LIVE '),'Cold native fight')
 human_id=P.HUMANS[player]
 assert sel['human']==cold['human']==player and sel['human_id']==cold['human_id']==human_id
 assert 700<sel['css']<sel['exit']<sel['live']==cold['frame']and sel['checks']>=30 and sel['errors']==0
 assert sel['initial_cpu']==cold['cpu_id']==18 and cold['stage']==0
 order=(cold['schedule']-0xfffa3000)//0x180
 assert cold['schedule']==0xfffa3000+order*0x180 and orders[order][0]==18
 events=original.rows(log,'EVENT')
 entry=one([r for r in events if r['kind']=='square'],'One actually chosen Square')
 start=entry['frame'];actor,main=entry['a8'],entry['a13']
 assert(entry['entry'],entry['pc'],entry['id'],entry['main_owner'])==(0xffffca00,0xffffca10,18,actor)
 assert entry['action']==0x303 and entry['flags']&0x1c==entry['body']&0xc==0
 own=[r for r in events if r['a8']==actor and r['a13']==main and r['frame']>start]
 regain=next(r for r in own if r['kind']=='regain');ready=regain['frame']
 relevant=[r for r in own if r['frame']<=ready]
 later=[r['frame']for r in own if r['frame']>ready and r['kind']in ('leg','ring','square','bicycle','knife','ball','choke')]
 tailEnd=min([ready+31,*later])
 entry_boundary(log,guest,player,start,ready)
 for r in [entry,*relevant]:
  assert r['id']==18 and r['main_owner']==actor and r['pc']==r['entry']+16
  assert r['writes']==0 and r['assistance']=='none'
 choice=rows(log,'MK2_CPU_CHOICE_EVENT')
 chosen=one([r for r in choice if r['kind']=='square'],'Actual native branch selected Square')
 calls=[r for r in choice if r['serial']==chosen['serial']]
 assert [r['kind']for r in calls]==['entry','first_call','first_result','second_call','second_result','square']
 for r in calls:
  assert r['frame']==start and (r['actor'],r['main'],r['owner'],r['id'],r['roster'])==(actor,main,actor,18,18)
  assert(r['state'],r['human_state'],r['mode'],r['stage'],r['schedule'])==(0,1,2,0,cold['schedule'])
  assert r['pc']==r['entry']+16 and r['mask']==65535 and r['writes']==0 and r['assistance']=='none'
  assert r['carry']==(r['status']>>30)&1
 assert calls[1]['a0']==250 and calls[3]['a0']==400
 assert 250<=calls[2]['a0']<1000 and calls[2]['carry']==0
 assert 0<=calls[4]['a0']<400 and calls[4]['carry']==1
 assert calls[5]['a0']==calls[4]['a0']and calls[5]['entry']==0xfffbc2f0
 for r in calls:
  assert struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode']
 fields=P.rows(log,'FIELD');by={r['frame']:r for r in fields}
 assert len(by)==len(fields)and set(range(start+1,tailEnd+1))<=set(by),'Every live callback through post-regain tail'
 baseline=by[start+1]
 for at in range(start+1,tailEnd+1):
  r=by[at]
  assert all(r[k]==baseline[k]for k in('actor','main','owner','id','roster','state','vactor','vmain','vowner','vid','vroster','vstate','mode','stage','schedule','floor','vfloor','stage_floor','hp','vhp'))
  assert(r['id'],r['roster'],r['vid'],r['vroster'],r['state'],r['vstate'],r['cpu_slot'],r['human_slot'])==(18,18,human_id,human_id,0,1,2,1)
  assert r['owner']==actor and r['vowner']==r['vactor']and r['schedule']==cold['schedule']
  assert r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-(135 if human_id==18 else 134)
  assert r['hp']>0 and r['vhp']>0 and r['writes']==0 and r['assistance']=='none'
  signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
  assert(r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(signed(r[k]>>16)for k in('xraw','yraw','vxraw','vyraw'))
 assert not [r for r in inventory.rows(log,'MK2_SQUARE_LOCK_HEALTH')if start<=r['frame']<=tailEnd],'Miss and whole recovery tail have no invented damage'
 flags=[r for r in inventory.rows(log,'MK2_SQUARE_LOCK_FLAG')if start<=r['frame']<=ready]
 for r in flags:
  off=(r['pc']-32-0xff800000)//8
  assert struct.unpack_from('<HH',guest,off)==(r['op0'],r['op1'])
  assert r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210))
 ownflags=[r for r in flags if r['slot']==2]
 assert all((r['actor'],r['main'],r['a8'],r['a13'],r['id'],r['state'])==(actor,main,actor,main,18,0)for r in ownflags)
 actions=[r for r in ownflags if r['kind']=='action']
 land=one([r for r in relevant if r['kind']=='landing'],'First original landing')['frame']
 assert [(r['frame'],r['before'],r['after'],r['pc'])for r in actions]==[
  (start,0x303,0x207,0xff877bc0),(land,0x207,0x304,0xff876460),
  (ready,0x304,0,0xff83edd0),(ready,0,0,0xff83edd0),(ready,0,0x303,0xff9065d0)]
 for kind,mask,setpc,clearpc in(('body',4,0xff838cf0,0xff83eeb0),('flags',0x10,0xff877d50,0xff83efc0)):
  stores=[r for r in ownflags if r['kind']==kind]
  assert len(stores)==3 and stores[0]['frame']==start and stores[0]['pc']==setpc
  assert stores[0]['before']&mask==0 and stores[0]['after']==stores[0]['before']|mask
  assert all(r['frame']==ready and r['pc']==clearpc and r['after']==r['before']&~mask for r in stores[1:])
  assert stores[1]['before']&mask and not stores[2]['before']&mask
 for at in range(start+1,ready+1):
  r=by[at]
  assert r['flags']&0x1c==0x10 and r['body']&0xc==4 and r['trail']==0
  assert r['action']==(0x207 if at<=land else 0x304)
 origin=by[start+1];sign=-1 if origin['facing']&16 else 1
 assert origin['xraw']==entry['xraw']and origin['yraw']==entry['yraw']
 for age in range(8):
  r=by[start+1+age]
  assert r['pose']==0xfe835c80 and r['xraw']==origin['xraw']
  assert r['yraw']==(origin['yraw']-age*12*65536)&0xffffffff and r['vy']==0xfff40000 and r['vx']==r['gravity']==0
 flight=by[start+9]
 assert flight['floor']-flight['y']==96 and flight['vx']==(sign*0xa0000)&0xffffffff and flight['vy']==flight['gravity']==0
 for at in range(start+10,start+35):
  r=by[at]
  assert r['xraw']==(flight['xraw']+sign*(at-start-9)*10*65536)&0xffffffff
  assert r['yraw']==flight['yraw']and r['vx']==flight['vx']and r['vy']==r['gravity']==0
  assert r['pose']==(0xff031340 if at<start+13 else 0xff031380 if at<start+16 else 0xff0313c0)
 fling=one([r for r in relevant if r['kind']=='fling'],'One missed-flight drop')
 fall=one([r for r in rows(log,'MK2_SQUARE_NATIVE_FALL')if r['action']==0x207],'Owned native fall')
 split=start+34
 assert fling['frame']==fall['frame']==split and(fling['entry'],fling['pc'])==(0xff876650,0xff876660)
 assert(fall['entry'],fall['pc'],fall['actor'],fall['main'],fall['owner'],fall['id'])==(0xff876660,0xff876670,actor,main,actor,18)
 assert all(tuple(r['a'+str(n)]for n in range(4))==(0,0x20000,0x8000,0xfff)for r in(fling,fall))
 drop=by[split+1]
 assert drop['xraw']==(by[split]['xraw']+flight['vx'])&0xffffffff and drop['yraw']==flight['yraw']
 assert(drop['vx'],drop['vy'],drop['gravity'],drop['pose'])==(0,0x20000,0x8000,0xfe835c20)
 for at in range(split+2,land+1):
  a,b=by[at-1],by[at]
  assert b['vy']==(a['vy']+0x8000)&0xffffffff and b['yraw']==(a['yraw']+b['vy'])&0xffffffff
  assert b['xraw']==a['xraw']and b['vx']==0 and b['gravity']==0x8000 and b['pose']==0xfe835c20
 last=by[land];next_y=(last['yraw']+last['vy']+0x8000)&0xffffffff
 assert last['y']<last['floor']and next_y>>16>=last['floor']and ready==land+4
 for at in range(land+1,ready+1):
  r=by[at];assert r['yraw']==last['floor']<<16 and r['vx']==r['vy']==r['gravity']==0
  assert r['pose']==0xfe835c20 and r['action']==0x304
 assert(regain['entry'],regain['pc'],regain['action'])==(0xff861500,0xff861510,0)
 assert regain['flags']&0x1c==0 and regain['body']&0xc==0 and regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0
 assert regain['yraw']==last['floor']<<16 and regain['xraw']==drop['xraw']and regain['pose']==0xfe835bc0
 for at in range(ready+1,tailEnd+1):
  r=by[at];assert r['flags']&0x1c==0 and r['body']&0xc==0 and r['trail']==r['vy']==r['gravity']==0 and r['y']==r['floor']
  assert r['action']in(0,0x303),'Post-regain ordinary control, no retained special'
 return dict(passed=True,start=start,ready=ready,landing=land,fall=split,fields=ready-start,damage=0,
  nativeChoiceSerial=chosen['serial'],firstRandomResult=calls[2]['a0'],secondRandomResult=calls[4]['a0'],
  allTwentySixFlightChecks=True,nativeActionStores=len(actions),nativeLockStores=len(ownflags)-len(actions),
  everyReachedPostRegainCallback=True,postRegainOrdinaryCallbacks=tailEnd-ready,
  originalThirtyOneCallbackOrdinaryTailAccepted=tailEnd==ready+31,lastScene=tailEnd,allCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

def entry_boundary(log,guest,player,start,ready):
 snapshots=inventory.rows(log,'MK2_SQUARE_BOUNDARY_ENTRY_STATE')
 assert len(snapshots)==2 and {r['slot']for r in snapshots}=={1,2}
 fields={r['frame']:r for r in P.rows(log,'FIELD')}
 assert start+1 in fields
 stores=[r for r in inventory.rows(log,'MK2_SQUARE_LOCK_FLAG')if start<=r['frame']<=ready]
 health=[r for r in inventory.rows(log,'MK2_SQUARE_LOCK_HEALTH')if start<=r['frame']<=ready]
 for store in stores:
  assert store['mask']==65535 and store['writes']==0 and store['assistance']=='none'
  assert store['owner']==store['actor']
 for r in health:
  assert r['mask']==65535 and r['writes']==0 and r['assistance']=='none'
  assert struct.unpack_from('<3H',guest,(r['pc']-48-0xff800000)//8)==tuple(r['op'+str(i)]for i in range(3))
  assert r['at']==(0x010602f0 if r['slot']==1 else 0x01060ec0)
 for snapshot in snapshots:
  side=snapshot['slot'];prefix=''if side==2 else 'v'
  assert snapshot['frame']==start and snapshot['serial']==1
  nextrow=fields[start+1]
  for key in ('actor','main','owner','id','roster','state','floor'):
   assert snapshot[key]==nextrow[prefix+key]
  for kind in ('action','body','flags'):
   value=snapshot[kind]
   for store in stores:
    if store['slot']==side and store['kind']==kind and store['frame']==start:
     assert (store['actor'],store['main'])==(snapshot['actor'],snapshot['main'])
     assert store['before']==value
     value=store['after']
   assert value==nextrow[prefix+kind],'Every actual entry write agrees with first published native FIELD'
  hp=snapshot['hp']
  for store in health:
   if store['slot']==side and store['frame']==start:
    assert store['before']==hp;hp=store['after']
  assert hp==nextrow[prefix+'hp']
 # Original observers must agree whenever they overlap the new startup taps;
 # do not invent duplicated stores for the missing first-live binding window.
 old=[r for r in P.flag_rows(log)if start<r['frame']<=ready]
 keys=('frame','slot','kind','at','before','after','pc','a8','a13','actor','main','id','state','op0','op1')
 assert [tuple(r[k]for k in keys)for r in stores if r['frame']>start]==[tuple(r[k]for k in keys)for r in old]

