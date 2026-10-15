"""Require actual native CPU damage while owned cry still active, not EOF."""
import copy,json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT
folder=R/'audit_current_cpu_sonya_voice_late_upper_runtime'
out=R/'audit_current_cpu_sonya_voice_late_upper_checked';assert not out.exists()
t=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert t['exitCode']==0 and t['limitReason'] is None and t['peakWorkingSetBytes']<=320*1024*1024
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
def gate(r):
 cues=r['CPU_BICYCLE_CUE'];c=cues[0];launch=int(c['frame'])
 assert [x['cue'] for x in cues[:2]]==['6B01','6B02'] and all(x['id']=='18' and x['actor']==c['actor'] and x['main']==c['main'] for x in cues[:2])
 owners={int(x['frame']):x for x in r['CPU_BICYCLE_OWNER'] if x['launch']==str(launch)}
 cry={int(x['frame']):x for x in r['CPU_BICYCLE_CHANNEL'] if x['launch']==str(launch) and x['channel']=='11'}
 hits=[x for x in r['HEALTH'] if x['slot']=='1' and launch<int(x['frame'])<launch+76 and x['pc']=='FF836700' and int(x['after'])<int(x['before'])<=161]
 assert hits,'No actual CPU damage before old voice EOF'
 h=hits[0];hf=int(h['frame']);before=owners[hf-1];cb=cry[hf-1]
 assert before['actor']==c['actor'] and before['main']==c['main'] and before['id']==before['guest_id']=='18' and before['mode']=='2'
 assert before['guest_hp']==before['stored_health']==h['before']
 assert cb['length']=='66523' and cb['paused']==cb['loop']=='0' and 0<float(cb['pos'])<66523
 assert float(cb['pos'])>float(cry[hf-2]['pos'])
 cut=next(x for f,x in sorted(owners.items()) if f>=hf and x['actor']=='00000000');cf=int(cut['frame'])
 assert hf<=cf<=hf+2 and cut['main']=='00000000' and cut['id']=='0' and cut['mode']=='2' and cut['guest_actor']==c['actor'] and cut['guest_main']==c['main'] and int(cut['guest_hp'])<=int(h['after'])
 assert all(not(hf-2<=int(x['frame'])<=cf+8) for tag in ['LOSS','SELECT'] for x in r.get(tag,[]))
 pos=float(cry[cf]['pos']);assert 0<pos<66523
 tail=[x for f,x in cry.items() if cf<=f<=cf+8];assert len(tail)==9 and all(float(x['pos'])==pos for x in tail)
 assert all(x['actor']==x['main']=='00000000' for f,x in owners.items() if cf<=f<=cf+8)
 for n in (10,11):
  tailn=[x for x in r['CPU_BICYCLE_CHANNEL'] if x['launch']==str(launch) and x['channel']==str(n) and cf<=int(x['frame'])<=cf+8]
  assert len(tailn)==9 and len({x['pos'] for x in tailn})==1
 return dict(cue=c,nativeHP=h,lastOwnedActive=before,lastActiveCry=cb,firstCleared=cut,stoppedCryPosition=pos,unplayedCrySamples=66523-pos,tailFields=9)
try:
 proof=gate(rows);accepted=True;error=None
except AssertionError as e:
 proof=None;accepted=False;error=str(e)
faults=[]
if accepted:
 for name in ['no_cpu_hit','wrong_owner','EOF_substitution','continued_voice']:
  b=copy.deepcopy(rows)
  if name=='no_cpu_hit':b['HEALTH']=[x for x in b['HEALTH'] if x['slot']!='1']
  elif name=='wrong_owner':
   for x in b['CPU_BICYCLE_OWNER']:x['actor']='01000000'
  elif name=='EOF_substitution':
   for x in b['CPU_BICYCLE_CHANNEL']:
    if x['channel']=='11':x['pos']='66523'
  else:
   for x in b['CPU_BICYCLE_CHANNEL']:
    if int(x['frame'])==int(proof['firstCleared']['frame'])+1 and x['channel']=='11':x['pos']=str(float(x['pos'])+1)
  try:gate(b)
  except AssertionError:faults.append(name)
  else:raise AssertionError('Fault accepted:'+name)
out.mkdir();report=dict(finiteObservationPassed=True,actualCpuActiveVoiceHealthInterruptionAccepted=accepted,failureReason=error,proof=proof,faultsRejected=faults,terminal=t,logSHA256=sync.sha(folder/'run.log'),heardMixAccepted=False,allCpuContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
