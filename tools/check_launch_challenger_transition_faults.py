"""Bounded counterexamples against the two existing terminal captures."""
import json
from pathlib import Path
import check_launch_ko_round_faults as mutations
import qualify_launch_challenger_transition as model
import qualify_launch_challenger_transition_v2 as packet
ROOT,need,sha=model.ROOT,model.need,model.sha

def check(c):
 out=ROOT/f"audit_launch_challenger_transition_faults_{c['move']}_p{c['side']}"
 need(not out.exists(),'Fresh finite fault evidence')
 proofpath=ROOT/f"audit_launch_challenger_transition_checked_{c['move']}_p{c['side']}/report.json"
 proof=json.loads(proofpath.read_text());need(proof['passed'],'Same terminal whole positive')
 pins=dict(proof['inputHashes']);pins[str(proofpath)]=sha(proofpath)
 text=c['text'];side=c['side'];boundary=proof['sourceEvents'][0]['nativeBoundaryFrame'];faults=[]
 def reject(label,tag,predicate,key,value,fn,remove=False):
  changed=mutations.change(text,tag,predicate,key,value,remove=remove)
  try:fn(dict(c,text=changed))
  except(ValueError,KeyError,AssertionError,StopIteration)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Changed actual evidence admitted: '+label)
 field=lambda r:r['frame']==str(boundary)and r['slot']==str(side)
 for key,value in(('mode','2'),('hp','160'),('writes','1'),('assistance','forced')):
  reject('actual teardown physical '+key,'MK2_KO_FIELD',field,key,value,lambda bad:model.physical_inventory(bad))
 reject('actual teardown field missing','MK2_KO_FIELD',field,'hp',None,lambda bad:model.physical_inventory(bad),True)
 for key,value in(('actor','01000000'),('main','01000000'),('id','17'if c['move']=='square'else'18'),('health','161')):
  reject('retired owner '+key,'MK2_INTERRUPT_OWNER',field,key,value,lambda bad:model.owners(bad,model.source_events(c,{})))
 for key,value in(('pc','FFFFCAC0'if c['move']=='ball'else'FFFFDEC0'),('a13','01000000')):
  reject('actual startup '+key,'MK2_MAUDIO_SOUND',lambda r:r['word'].startswith('6B'),key,value,lambda bad:model.source_events(bad,{}))
 reject('selection word changed','MK2_MAUDIO_SOUND',lambda r:r['pc']=='FFFF3DA0','word','FFFE',lambda bad:packet.packet_gate(bad['text']))
 reject('selection marker missing','MK2_MAUDIO_SOUND',lambda r:r['pc']=='FFFF3DA0','word',None,lambda bad:packet.packet_gate(bad['text']),True)
 for tag,key,value in(('MK2_MAUDIO_PACKET','a3','FFFFFFFF'),('MK2_MAUDIO_SOUND','word','FF01'),('MK2_MAUDIO_DELIVERY','word','0100')):
  reject('native packet '+tag,tag,lambda r:tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90',key,value,lambda bad:packet.packet_gate(bad['text']))
 restored,_=model.physical_inventory(c);need(restored==proof['completePhysicalAndHealthInventory']and model.owners(c,model.source_events(c,{}))==proof['completeIndependentOwnership']and packet.packet_gate(text)==proof['completeNativeDCSDelivery'],'Whole original positives restored')
 for p in(Path(__file__),Path(mutations.__file__),Path(model.__file__),Path(packet.__file__)):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Whole executed evidence stable')
 report=dict(passed=True,nativeTerminal=c['terminal'],actualFaultsRejected=faults,inputHashes=pins,fullPortAcceptance=False,newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(move=c['move'],side=side,faults=len(faults))),flush=True);return report
