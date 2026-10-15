"""Locate actual first CPU-state divergence; do not assume timer causality."""
import json
from pathlib import Path
import verify_repeated_sonya_cpu_v1463 as model
import verify_active_launch_timer_v1520 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1540_cpu_audio_divergence'
def inspect():
 pins={};logs={};fields={};results={}
 cases={'previous':'audit_v1539_previous_cpu_repeated_kano_p1','new':'audit_v1519_cpu_repeated_p1_human_kano','new_always_polling':'audit_v1506_cpu_repeated_p1_human_kano'}
 for key,name in cases.items():
  folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert meta['exit_code']==0 and meta['player']=='kano'and meta['boot_frame']==605 and meta['confirm_age']==264 and meta['approach']=='guard_until_close'and not meta['cheats_enabled']and meta['assistance']=='none'
  for p,h in meta['input_hashes'].items():assert source.sha(p)==h;pins[p]=h
  for p in (folder/'result.json',folder/'run.log'):pins[str(p)]=source.sha(p)
  logs[key]=(folder/'run.log').read_text(encoding='utf-8-sig')
  fields[key]={r['frame']:r for r in model.rows(logs[key],'FIELD')}
  assert len(fields[key])==len(model.rows(logs[key],'FIELD'))
  results[key]=model.rows(logs[key],'RESULT')[0]
 previous=fields['previous'];new=fields['new'];common=sorted(set(previous)&set(new))
 differences=[]
 for frame in common:
  a,b=previous[frame],new[frame]
  if a!=b:
   differences.append(dict(frame=frame,changed={k:dict(previous=a.get(k),new=b.get(k))for k in set(a)|set(b)if a.get(k)!=b.get(k)}))
   break
 assert differences,'Actually locate native CPU divergence'
 first=differences[0]['frame']
 starts={key:[dict(frame=r['frame'],action=r['action'])for i,r in enumerate(model.rows(logs[key],'FIELD'))if r['action']in(0x204,0x207)and (i==0 or model.rows(logs[key],'FIELD')[i-1]['action']!=r['action'])]for key in cases}
 # Compare all callback states shared by the two audio successors. Same zero
 # pair result is not proof of the cause, but the active-only timer did not
 # restore the old repeated-pair scenario.
 shared=sorted(set(fields['new'])&set(fields['new_always_polling']))
 exact_new=all(fields['new'][f]==fields['new_always_polling'][f]for f in shared)
 pins[__file__]=source.sha(__file__)
 return dict(passed=True,scope=__doc__,cases=cases,physicalInputsSame=True,firstActualStateDivergence=differences[0],priorCallbacksExact=first-common[0],launchActionEntries=starts,results=results,activeOnlyAndAlwaysPollingSharedCPUStatesExact=exact_new,oldRepeatReproduced=results['previous']['complete_count']==2,newRepeatedCPUFixtureAccepted=False,idleTimerAsCauseProven=False,inputHashes=pins,fullPortAccepted=False)
if __name__=='__main__':
 assert not OUT.exists()
 report=inspect();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in('firstActualStateDivergence','launchActionEntries','activeOnlyAndAlwaysPollingSharedCPUStatesExact','oldRepeatReproduced')},indent=2),flush=True)
