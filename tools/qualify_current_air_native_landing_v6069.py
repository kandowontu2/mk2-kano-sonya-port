"""Whole recorded air trajectories with source-owned landing and body separation.

Preserve every6067 pre/post field and source argument. Normal living getup uses
animation15's third sequence, skipping two entries; different victims may draw
a different pose in the landing field. Stock Jax writes requested horizontal
speed, but original close-body suppression can defer publishing actor speed.
No ROM change, new emulator boot, fitted delay or discarded landing field.
"""
import inspect,json,struct,traceback
from pathlib import Path
import qualify_current_air_trajectories_v6067 as prior
import verify_move_phase_shadow_v5089 as pictures
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6070_current_air_native_landing_checked'

def word(address,guest,payload):
 raw,base=(payload,0xfe800000)if 0xfe800000<=address<0xff800000 else(guest,0xff800000)
 need(address>=base and(address-base)%8==0,'Complete aligned source animation word')
 return struct.unpack_from('<I',raw,(address-base)//8)[0]

def landing_pose(identity,guest,payload):
 root=word(0xfffe4000+identity*32,guest,payload)
 at=word(root+15*32,guest,payload)
 for sequence in range(2):
  for index in range(16):
   value=word(at,guest,payload);at+=32
   if value==0:break
  else:raise ValueError('Source landing sequence missing bounded native terminator')
 # FF8EA550 ADDI40 bits skips two DWORD entries after the two scans.
 return word(at+64,guest,payload)

def bounds(row,y,guest,payload):
 parts=pictures.native_group(dict(pose=row['pose'],facing=row['body']),payload,guest)
 return min(y-p['dy']for p in parts),max(y-p['dy']+p['height']for p in parts)-48

def stock_horizontal(row,peer,x,y,previous_vx,requested,guest,payload):
 # FF827D70..FF827E60 and FF828910 source-native descriptor bounds.
 own_bounds=bounds(row,y,guest,payload)
 peer_bounds=bounds(peer,int(peer['y']),guest,payload)
 separated=own_bounds[1]<peer_bounds[0]or peer_bounds[1]<own_bounds[0]
 gap=abs(x//65536-prior.signed(prior.h(peer,'xraw'))//65536)
 need(gap<304,'Recorded Jax flight never enters unsampled maximum-separation correction')
 if separated:return requested
 if gap<61:
  # FF8285F0 checks suppression and returns to sleep without storing actorVX.
  need(int(row['suppression'])>0,'Actual close Jax flight uses native suppression, not unsampled forced push')
  return previous_vx
 need(int(row['suppression'])>0 or gap>=64,
      'Recorded overlapping flight avoids unsampled close half-speed sharing')
 return requested

def source_contract(guest,payload):
 source=prior.source_contract(guest,payload)
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff827c40,0xff828b10),(0xff8ea320,0xff8ea670),
               (0xff838650,0xff838790),(0xff831ac0,0xff831bf0),
               (0xff876be0,0xff876c80)):
  need(guest[prior.off(lo):prior.off(hi)]==original[prior.off(lo):prior.off(hi)],
       'Whole actual original separation/getup/velocity-publication instruction kernels unchanged')
 need(word(0xff8ea4a0,guest,payload)==0x9000f and
      struct.unpack_from('<H',guest,prior.off(0xff8ea560))[0]==0x0040,
      'Original normal-ID animation15 and exact two-entry landing skip')
 expected={4:0xff94de20,11:0xff993030,17:0xff00f8c0,18:0xff02f980}
 need({i:landing_pose(i,guest,payload)for i in expected}==expected,
      'Every represented original/true own landing pose derived from actual source root and native scans')
 source.update(nativeLivingLandingGroups={str(i):f'{p:08X}'for i,p in expected.items()},
               originalCloseBodyDeferredVelocityPublicationQualified=True)
 source['inputHashes'][str(Path(pictures.__file__).resolve())]=sha(pictures.__file__)
 return source

def check(b,guest,payload):
 source=inspect.getsource(prior.check)
 substitutions=(
  ('callback=False,pose=None,next_phase=False):',
   'callback=False,pose=None,next_phase=False,stock=False):'),
  ('integer_callback=(vx//65536)*65536 if callback else 0',
   'integer_callback=(vx//65536)*65536 if callback else 0\n  expected_x=x;published=0 if stock else vx'),
  ("need(h(r,'xraw')==(x+(vx+integer_callback)*tick)&MASK and h(r,'yraw')==raw,",
   "if stock:\n    if tick>0:expected_x=(expected_x+published)&MASK\n    if tick<ticks and tick>0:published=stock_horizontal(r,post[f,3-slot],prior.signed(expected_x),prior.signed(raw)//65536,published,vx,guest,payload)\n   else:expected_x=(x+(vx+integer_callback)*tick)&MASK\n   need(h(r,'xraw')==expected_x and h(r,'yraw')==raw,"),
  ("need(h(r,'vx')==vx&MASK and h(r,'vy')==(vy+g*tick)&MASK",
   "need(h(r,'vx')==published&MASK and h(r,'vy')==(vy+g*tick)&MASK"),
  ("if pose is not None and tick>0:need(h(r,'pose')==pose,'Every living-victim horizontal knockdown pose, including landing')",
   "if pose is not None and tick>0:\n    expected_pose=landing_pose(int(r['id']),guest,payload)if tick==ticks and not next_phase else pose\n    need(h(r,'pose')==expected_pose,'Every living-victim source flight pose and native landing transition')"),
  ('phase(victimfall,int(getup[\'frame\']),victim,-direction*0x38000,-0x80000,0xa000)',
   "phase(victimfall,int(getup['frame']),victim,direction*0x38000,-0x80000,0xa000,pose=word(prior.h(victimfall,'a9')-32,guest,payload),stock=True)"))
 for before,after in substitutions:
  need(source.count(before)==1,'One exact source-native landing/separation adaptation')
  source=source.replace(before,after,1)
 scope=dict(prior.check.__globals__,prior=prior,landing_pose=landing_pose,
            stock_horizontal=stock_horizontal,word=word)
 exec(compile(source,__file__+'::whole_native_air_trajectories','exec'),scope)
 return scope['check'](b,guest,payload)

def run():
 failure=prior.OUT/'report.json'
 need(not json.loads(failure.read_text())['passed'],'Retain executed landing-assumption failure')
 source=inspect.getsource(prior.run)
 scope=dict(prior.run.__globals__,check=check,source_contract=source_contract,__file__=__file__)
 exec(compile(source,__file__+'::whole_eight_context_trajectory_matrix','exec'),scope)
 report=scope['run']()
 report['inputHashes'].update({str(failure):sha(failure),str(Path(prior.__file__).resolve()):sha(prior.__file__)})
 report.update(nativeLivingLandingTransitionAccepted=True,
               stockJaxSourceBodySeparationAccepted=True,retainedAssumptionFailure=str(failure),scope=__doc__)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole current air landing/separation qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
