"""Same-run native row, raster and grounding counterexamples in host RAM.

No controller replay or mutation of native guest/video/audio state.
"""
import copy, hashlib, json
from pathlib import Path
from unittest.mock import patch
import launch_ground_native_names as model
import launch_ground_native_names_v2 as oracle

ROOT,need,sha=model.ROOT,model.need,model.sha

def check(carriers):
 out=ROOT/'audit_launch_ground_faults';need(not out.exists(),'Fresh actual fault receipt')
 accepted_path=ROOT/'audit_launch_ground_native_names_checked/report.json'
 accepted=json.loads(accepted_path.read_text());need(accepted['passed']and len(carriers)==4,'Four actual terminal raster/ground cases')
 pins=dict(accepted['inputHashes']);pins[str(accepted_path)]=sha(accepted_path);pins[str(Path(__file__))]=sha(__file__)
 gfx=oracle.reconstruct(pins);cases=[]
 for carrier in carriers:
  local=dict(carrier,gfx=dict(carrier['gfx']))
  if carrier['side']==1 and carrier['fighter']=='kano':
   start=0x1e00000;size=173
   local['gfx']['0F000000_C002_33_10']=dict(key='0F000000_C002_33_10',offset=str(start*8),first=str(start),bytes=str(size),data=gfx[start:start+size].hex())
  baseline=model.check(local)
  evidence={tag:model.original.rows(local['text'],tag)for tag in('FIELD','PRE','OWNER','DMA','SNAP','SHADOW_COMPONENT')}
  buffers={k:{field:(int(v)if field in('offset','first','bytes')else v)for field,v in r.items()}for k,r in local['gfx'].items()}
  native=model.original.check_shadow_rows(local['text'],buffers);faults=[]
  def reject(label,fn):
   try:fn()
   except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
   else:raise ValueError('Actually changed ground/shadow evidence admitted: '+label)
  def row_fault(tag,key,delta):
   data={t:[r.copy()for r in evidence[t]]for t in('DMA','SHADOW_COMPONENT')}
   target=next(r for r in data[tag]if tag!='DMA'or 0x10000000<=r['source']<0x1a000000 and r['command']&15==8)
   target[key]+=delta
   with patch.object(model.original,'rows',side_effect=lambda text,name:data[name]):
    model.original.check_shadow_rows(local['text'],buffers)
  for tag,key,delta in(('DMA','y',1),('DMA','source',1),('DMA','color',1),('DMA','pc',16),
                        ('SHADOW_COMPONENT','id',-16),('SHADOW_COMPONENT','row',16)):
   reject('native '+tag+' '+key+' actual delta '+str(delta),lambda t=tag,k=key,d=delta:row_fault(t,k,d))
  def missing_row():
   data=dict(evidence,SHADOW_COMPONENT=evidence['SHADOW_COMPONENT'][1:])
   with patch.object(model.original,'rows',side_effect=lambda text,name:data[name]):model.original.check_shadow_rows(local['text'],buffers)
  reject('one missing actual native shadow row',missing_row)
  def raster_fault(tag,key,delta):
   data={t:[r.copy()for r in evidence[t]]for t in evidence}
   frame=data['SNAP'][0]['frame']-(0 if tag=='SNAP'else 1)
   target=next(r for r in data[tag]if r['frame']==frame and
               (tag!='DMA'or r['palette']==(0x200 if local['side']==1 else 0x300)and r['command']&15==2)and
               (tag!='FIELD'or r['slot']==local['side']))
   target[key]=f'{(int(target[key],16)+delta)&65535:04X}'if isinstance(target[key],str)else target[key]+delta
   with patch.dict(model.scope,rows=lambda text,name:data[name]),patch.object(model.original,'rows',side_effect=lambda text,name:data[name]):model.check(local)
  for tag,key,delta in(('DMA','y',1),('DMA','source',8),('FIELD','id',-16),('SNAP','start',0x1000)):
   reject('displayed '+tag+' '+key+' actual delta '+str(delta),lambda t=tag,k=key,d=delta:raster_fault(t,k,d))
  def no_pre():
   data=dict(evidence,PRE=evidence['PRE'][1:])
   with patch.dict(model.scope,rows=lambda text,name:data[name]),patch.object(model.original,'rows',side_effect=lambda text,name:data[name]):model.check(local)
  reject('missing actual pre-DMA VRAM pass',no_pre)
  snap=evidence['SNAP'][0]
  def image_corruption():
   changed=dict(local,images=dict(local['images']));image=local['images'][snap['file']].copy();image[0,0,0]^=1;changed['images'][snap['file']]=image;model.check(changed)
  reject('actual displayed RGB pixel changed',image_corruption)
  def vram_corruption():
   changed=dict(local,raw=dict(local['raw']));raw=bytearray(local['raw'][snap['vram_file']]);raw[0]^=1;changed['raw'][snap['vram_file']]=bytes(raw);model.check(changed)
  reject('actual native VRAM word changed',vram_corruption)
  def pen_corruption():
   changed=dict(local,raw=dict(local['raw']));raw=bytearray(local['raw'][snap['palette_file']]);raw[15*4]^=1;changed['raw'][snap['palette_file']]=bytes(raw);model.check(changed)
  reject('native black floor-shadow palette pen changed',pen_corruption)
  def no_shadow():
   changed=copy.deepcopy(baseline);changed['records'][0]['owned_shadow_pixels'][local['side']]=0;model.contract.check_ground(changed,local['fighter'],local['side'])
  reject('actual visible owned floor shadow erased',no_shadow)
  def wrong_sole():
   changed=copy.deepcopy(baseline);changed['idle_sole_rows'][local['side']]=[x-1 for x in changed['idle_sole_rows'][local['side']]];model.contract.check_ground(changed,local['fighter'],local['side'])
  reject('one-pixel higher native idle soles',wrong_sole)
  def source_corruption():
   record=next(r for r in local['gfx'].values()if int(r['bytes'])>0);raw=bytearray.fromhex(record['data']);raw[0]^=1;start,size=int(record['first']),int(record['bytes']);need(raw==gfx[start:start+size],'Entire source stream oracle, including native initialization')
  reject('actual retained graphics-source byte changed',source_corruption)
  restored=model.check(local);need(restored==baseline,'Whole same-run raster/ground positive restored after all faults')
  need(native['copies']==baseline['native_shadow_copies'],'Actual full native row count retained')
  cases.append(dict(fighter=local['fighter'],side=local['side'],nativePID=local['terminal']['pid'],actualFaultsRejected=faults,
                    actualNativeShadowCopies=native['copies'],actualGroundRGBDigests={name:hashlib.sha256(image.tobytes()).hexdigest().upper()for name,image in local['images'].items()}))
  print(json.dumps(dict(case=f"{local['fighter']}_p{local['side']}",actualFaultsRejected=len(faults))),flush=True)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/evidence pins stable')
 report=dict(passed=True,candidate=model.current.NAME,cases=cases,inputHashes=pins,actualFaultsRejected=sum(len(c['actualFaultsRejected'])for c in cases),
             nativeRAMOnly=True,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,allArenaGroundAcceptance=False,fullPortAcceptance=False)
 out.mkdir();model.previous.save(out/'report.json',report);return report
