"""Reject malformed native boss trajectories without changing actual evidence."""
import copy,json
from pathlib import Path
import verify_native_kintaro_launch_cull_v1692 as boss
ROOT=boss.ROOT;OUT=ROOT/'audit_v1695_native_kintaro_negative_checked'
if __name__=='__main__':
 assert not OUT.exists()
 guest,_,payload=boss.arena.corrected_source.expected()
 context=boss.build_context(ROOT/'audit_v1664_current_kano_p1_native_counter',guest,payload)
 hit=next(h for h in context['hits']if h['frame']==42379)
 accepted=boss.flight(context,hit);rejected=[]
 for label,frame,key,value in (
  ('wrong_original_launch_speed',42380,'vy',0xfff40000),
  ('wrong_original_gravity',42380,'gravity',0x6000),
  ('unexplained_damage',42380,'hp',82),
  ('proxy_hurt_actor',42380,'actor',0x01000000),
  ('vertical_position_drift',42408,'y',-100),
  ('horizontal_position_drift',42408,'x',400)):
  bad=copy.deepcopy(context);bad['fields'][frame][key]=value
  try:boss.flight(bad,hit)
  except (AssertionError,KeyError):rejected.append(label)
  else:raise AssertionError(label+' escaped strict causal check')
 bad=copy.deepcopy(context);del bad['fields'][42408]
 try:boss.flight(bad,hit)
 except (AssertionError,KeyError):rejected.append('missing_causal_callback')
 else:raise AssertionError('Missing callback accepted')
 # Do not accept an off-screen flight which never returns to ordinary play.
 bad=copy.deepcopy(context)
 for frame in range(42459,42498):bad['fields'][frame]['action']=0x503
 try:boss.flight(bad,hit)
 except (AssertionError,KeyError):rejected.append('no_normal_recovery')
 else:raise AssertionError('Missing normal recovery accepted')
 pins=context['pins'];pins[str(Path(__file__).resolve())]=boss.arena.campaign.digest(Path(__file__))
 for path,wanted in pins.items():assert boss.arena.campaign.digest(Path(path))==wanted
 report=dict(passed=True,acceptedNativeFlight=accepted,rejectedInMemoryCorruptions=rejected,
  actualCapturesUnmodified=True,acceptancePredicatesUnmodified=True,inputHashes=pins,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
