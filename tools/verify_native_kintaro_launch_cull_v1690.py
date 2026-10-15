"""Actual original Kintaro launch and complete owned off-top clipping proof.
Distinct from preserved v1589 uppercut predicates; only the fresh read-only
counter capture can supply this causal evidence. Not full boss/campaign proof.
"""
import json,re,struct
from pathlib import Path
from collections import defaultdict
import verify_native_ground_throw_arena_v1614 as arena
ROOT=arena.ROOT
HEX={'at','pc','actor','main','owner','victim','victimMain','descriptor','vx','vy','gravity','pose','action','flags','body','facing','cache','cpuActor','cpuMain','a8','a13','mask'}
def parse(line):
 row=dict(re.findall(r'(\w+)=([^\s]+)',line))
 for k,v in tuple(row.items()):
  if k not in ('words','assistance','fighter','fullPortAcceptance'):
   row[k]=int(v,16 if k in HEX else 10)
 return row
def signed(v):return v-(1<<32)if v&(1<<31)else v
def build_context(folder,guest,payload):
 assert folder.name=='audit_v1664_current_kano_p1_native_counter','Exact fresh causal capture required'
 pins={};arena.campaign.matched(folder,pins)
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 assert meta['exit_code']==0 and meta['player']=='kano'and meta['human_slot']==1 and meta['cpu_slot']==2 and meta['assistance']=='none'
 guest_evidence=ROOT/'audit_v1602_kano_ground_throw_p1/guest_maincpu.bin'
 assert guest_evidence.read_bytes()==guest,'Exact same-candidate actual initialized guest; not a campaign-time dump'
 observer=folder/'input_sources/mk2ks_native_counter_cull_v1663.lua'
 text=observer.read_text()
 assert text.count("dofile('mk2ks_natural_campaign_floor_v1566.lua')")==1
 assert not re.search(r'write_u\d+|:write_|\.value\s*=(?!=)|load_?state',text)
 assert observer.read_bytes()==(ROOT/observer.name).read_bytes()
 driver=folder/'input_sources/mk2ks_natural_campaign_floor_v1566.lua'
 assert driver.read_bytes()==(ROOT/driver.name).read_bytes()
 assert "if mask==0xffff and first_live then" in driver.read_text(),'Every emitted health record is an actual full-word native write'
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 off=lambda a:(a-0xff800000)//8
 slices=((0xff835440,0xff836030),(0xff8364c0,0xff836710),(0xff8d8330,0xff8d88e0),(0xff876650,0xff876b40),(0xff8042a0,0xff804340))
 comparison=bytearray(original)
 # The sole collision-code difference relocates the outer roster table.
 # Prove the opcode, exact operand and every old row, including Kintaro,
 # before comparing the complete instruction paths.
 assert struct.unpack_from('<HI',guest,off(0xff835dd0))==(0x0b20,0xfffe4800)
 assert guest[off(0xfffe4800):off(0xfffe4800)+17*4]==original[off(0xff8d2bd0):off(0xff8d2bd0)+17*4]
 struct.pack_into('<I',comparison,off(0xff835de0),0xfffe4800)
 for a,b in slices:assert guest[off(a):off(b)]==comparison[off(a):off(b)],'Original path except independently verified table relocation '+hex(a)
 u32=lambda a:struct.unpack_from('<I',guest,off(a))[0]
 descriptor=0xff8ec2b0;words=struct.unpack_from('<9H',guest,off(descriptor))
 assert words==(122,32,96,48,0x120,0x280d,0,0,1)and guest[off(descriptor):off(descriptor)+18]==original[off(descriptor):off(descriptor)+18]
 root=u32(u32(0xff835de0)+12*32)
 assert root==0xff8d2e50 and u32(root+((words[4]>>8)*32))==0xff8d8330
 # Original MOVI A0=x speed, A1=y speed, A2=gravity; no fitted trajectory.
 assert struct.unpack_from('<9H',guest,off(0xff8d8440))==(0x09e0,0,2,0x09e1,0,0xffed,0x09e2,0x8000,0)
 fields={};hits=[];health=[];results=[]
 with (folder/'run.log').open(encoding='utf-8-sig')as stream:
  for line in stream:
   if line.startswith('MK2_NATIVE_COUNTER_FIELD '):
    r=parse(line);assert r['frame']not in fields;fields[r['frame']]=r
   elif line.startswith('MK2_NATIVE_COUNTER_HITBOX '):hits.append(parse(line))
   elif line.startswith('MK2_NATIVE_COUNTER_RESULT '):results.append(parse(line))
   elif line.startswith('MK2_NAT_CAMPAIGN_HEALTH '):health.append(parse(line))
 assert len(results)==1 and results[0]['observedFields']==len(fields)>3000
 for r in fields.values():
  assert r['writes']==0 and r['assistance']=='none'and r['id']==r['roster']==17 and r['owner']==r['actor']and r['cpuID']==12 and r['floor']==r['stageY']-134
 for r in hits:
  assert r['at']==0xff835440 and r['pc']==0xff835450 and r['descriptor']==descriptor and tuple(int(w,16)for w in r['words'].split(','))==words
  assert r['id']==12 and r['victimID']==17 and r['owner']==r['actor'] and r['writes']==0 and r['assistance']=='none'
 for p in (folder/'result.json',guest_evidence,folder/'run.log',observer,Path(__file__),ROOT/'mk2/mk2-maincpu.bin'):
  pins[str(p.resolve())]=arena.campaign.digest(p)
 return dict(fields=fields,hits=hits,health=health,pins=pins,descriptor=descriptor,originalSlices=slices)

def flight(context,hit):
 by=context['fields'];begin=hit['frame']+1
 assert begin in by and hit['frame']in by
 before,first=by[hit['frame']],by[begin]
 assert hit['victim']==first['actor']==before['actor']and hit['victimMain']==first['main']==before['main']
 assert hit['actor']==first['cpuActor']and hit['main']==first['cpuMain']
 stores=[r for r in context['health']if r['frame']==hit['frame']and r['slot']==1]
 assert len(stores)==1 and stores[0]['pc']==0xff836700 and stores[0]['at']==0x010602f0 and stores[0]['a8']==hit['actor']and stores[0]['a13']==hit['main'] and stores[0]['before']==before['hp']and stores[0]['after']==first['hp']and before['hp']-first['hp']==40
 assert first['hp']>0 and first['action']==0x503 and first['vy']==0xffed0000 and first['gravity']==0x8000 and abs(signed(first['vx']))==0x20000
 airborne=[first];land=None;fraction_lo,fraction_hi=0,65535;total_y=0
 for f in range(begin+1,begin+110):
  assert f in by,'Every causal trajectory callback required'
  a,b=by[f-1],by[f]
  assert (b['actor'],b['main'],b['owner'],b['id'],b['hp'],b['floor'])==(first['actor'],first['main'],first['actor'],17,first['hp'],first['floor'])
  if b['vy']==0:
   assert b['y']==b['floor'] and b['gravity']==b['vx']==0 and b['action']==0x503
   assert a['y']+signed((a['vy']+a['gravity'])&0xffffffff)/65536>=b['floor']
   land=b;break
  assert b['action']==0x503 and b['gravity']==0x8000 and b['vy']==(a['vy']+0x8000)&0xffffffff and b['vx']==first['vx']
  assert b['x']-a['x']==signed(b['vx'])//65536
  total_y+=signed(b['vy'])
  # Retain a single consistent unknown initial fractional Y for all fields.
  delta=b['y']-first['y']
  fraction_lo=max(fraction_lo,delta*65536-total_y)
  fraction_hi=min(fraction_hi,(delta+1)*65536-1-total_y)
  assert fraction_lo<=fraction_hi,'One native fixed-point integral explains complete Y trajectory'
  airborne.append(b)
 assert land is not None
 recovered=[by[f]for f in range(land['frame']+1,land['frame']+40)if f in by and by[f]['action']==0 and by[f]['y']==by[f]['floor']and by[f]['gravity']==by[f]['vx']==by[f]['vy']==0 and by[f]['flags']==1]
 assert recovered,'Original bounded grounded live recovery required'
 return dict(hitFrame=hit['frame'],firstHurtFrame=begin,landFrame=land['frame'],recoveredFrame=recovered[0]['frame'],fields=len(airborne),initialFractionBounds=[fraction_lo,fraction_hi])

def prove(context,groups,record,side,identity,guest,payload):
 assert side==1 and identity==17 and record['arena']==8
 frame=record['frame']-1;field=context['fields'][record['frame']]
 assert record['body'][side]['pixels']==record['body'][side]['mismatches']==0
 assert not any(q['frame']==frame and q['slot']==side for q in groups['FLOOR_QUEUE'])
 assert not any(q['frame']==frame and q['slot']==side for q in groups['FLOOR_QUEUE_DISPATCH'])
 causal=[h for h in context['hits']if h['frame']<record['frame']and h['victim']==field['actor']and h['victimMain']==field['main']]
 assert causal
 hit=max(causal,key=lambda r:r['frame']);trajectory=flight(context,hit)
 assert trajectory['firstHurtFrame']<record['frame']<trajectory['landFrame']and field['action']==0x503
 # Require real actual native FIFO and consumer draw before this hit.
 queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
 positive=[d for d in groups['FLOOR_QUEUE_DISPATCH']if d['slot']==side and hit['frame']-2<=d['frame']<=hit['frame']]
 assert positive
 for d in positive:
  q=queues[d['queue_frame'],d['cursor']]
  assert q['actor']==field['actor']and q['main']==field['main']and q['id']==q['roster']==17
 observations=[s for s in groups['SHADOW_COMPONENT']if s['frame']==frame and s['slot']==side]
 assert observations
 components={}
 keys=('actor','main','owner','id','row','cache','component','first_source','width','height','xoff','yoff','command','x','y','floor','stageY','displayY','cameraY')
 for s in observations:
  assert s['actor']==s['owner']==field['actor']and s['main']==field['main']and s['id']==17 and s['cache']==field['cache']
  assert all(s[k]==field[k]for k in ('x','y','floor','stageY','cameraY','displayY'))
  assert s['row']==s['cache']+s['component']*112
  if s['component']in components:assert all(s[k]==components[s['component']][k]for k in keys)
  components[s['component']]=s
 assert sorted(components)==list(range(len(components)))and 0<len(components)<12
 parts=[components[i]for i in sorted(components)]
 expected=arena.native.group(dict(pose=field['pose'],facing=field['facing']),payload,guest)
 assert len(expected)==len(parts)
 rectangles=[]
 for e,s in zip(expected,parts):
  assert (e['source'],e['width'],e['height'],e['dx'],e['dy'],e['command'])==(s['first_source'],s['width'],s['height'],s['xoff'],s['yoff'],s['command'])
  top=s['y']-s['yoff']-s['cameraY'];bottom=top+s['height']-1
  assert bottom<0,'Complete original cached body lies above viewport'
  rectangles.append(dict(component=s['component'],source=s['first_source'],top=top,bottom=bottom,width=s['width'],height=s['height']))
 return dict(frame=record['frame'],arena=8,slot=side,id=identity,actor=field['actor'],main=field['main'],actualPose=field['pose'],
  kind='original_kintaro_launch_cull',descriptor=context['descriptor'],nativeReaction=0xff8d8330,damage=40,trajectory=trajectory,
  priorActualDrawFrames=sorted({d['frame']for d in positive}),actualPartRectangles=rectangles,
  originalReactionFlightClippingUnchanged=True,collisionOnlyVerifiedOuterTableRelocation=True)
