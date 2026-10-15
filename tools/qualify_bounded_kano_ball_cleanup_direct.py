"""Direct actual Kano ball cue/hit/cleanup gate; no rewritten Sonya predicates."""
import copy
import json
import re
import wave
from decimal import Decimal
import verify_native_source_sync as sync


def gate(rows,side,length):
 stopped=2318 if side==1 else 2319
 fields=rows['FIELD']
 assert len(fields)==842 and all(r['id']==r['roster']==('17' if int(r['slot'])==side else '18') and r['owner']==r['actor'] for r in fields)
 cues=rows['CUE']
 assert len(cues)==1 and cues[0]['value']=='6B03' and cues[0]['frame']=='1459'
 hits=rows['HEALTH']
 assert len(hits)==2 and all(r['pc']=='FF836700' for r in hits)
 own=[r for r in hits if int(r['slot'])==side]
 other=[r for r in hits if int(r['slot'])==3-side]
 assert len(own)==len(other)==1
 assert own[0]['frame']=='1461' and own[0]['before']=='161' and own[0]['after']=='121'
 assert other[0]['before']=='161' and other[0]['after']=='155'
 owners=[r for r in rows['VOICE_OWNER'] if int(r['slot'])==side]
 active=[r for r in owners if r['actor']!='00000000']
 assert active and all(r['id']=='17' and r['health']=='161' and r['mode']=='2' for r in active)
 cleared=[r for r in owners if int(r['frame'])>=1462]
 assert len(cleared)>200 and all(all(int(r[k],16 if k in ('actor','main') else 10)==0 for k in ('actor','main','health','id','mode')) for r in cleared)
 assert 0<Decimal(cleared[0]['seconds'])-Decimal(own[0]['seconds'])<Decimal(1)/60
 channels=[r for r in rows['VOICE_CHANNEL'] if int(r['channel'])==10+(side-1)*2 and int(r['length'])>0]
 assert channels and all(int(r['length'])==length and r['paused']==r['loop']=='0' for r in channels)
 before=[r for r in channels if int(r['frame'])<1462]
 after=[r for r in channels if int(r['frame'])>=1462]
 assert before and after and max(Decimal(r['pos']) for r in before)>min(Decimal(r['pos']) for r in before)
 assert all(Decimal(r['pos'])==stopped for r in after) and 0<stopped<length
 assert Decimal(after[-1]['seconds'])>Decimal(cues[0]['seconds'])+Decimal(length)/48000
 return {'stoppedSample':stopped,'unplayedSamples':length-stopped,'postStopObservations':len(after)}


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_bounded_kano_ball_cleanup_direct_checked'
 assert not out.exists()
 clip=sync.ROOT/'samples/mk2ks/kano_ball_launch.wav'
 with wave.open(str(clip)) as wav:
  length=wav.getnframes();assert wav.getframerate()==48000
 cases=[]
 for side in (1,2):
  folder=sync.ROOT/f'audit_bounded_kano_ball_p{side}_guard_counter_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None
  rows={}
  for line in (folder/'run.log').read_text().splitlines():
   assert '[LUA ERROR]' not in line
   if line.startswith('MK2_HSPECIAL_'):
    tag=line.split()[0].removeprefix('MK2_HSPECIAL_')
    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
    assert r['writes']=='0' and r['assistance']=='none'
    rows.setdefault(tag,[]).append(r)
  case=gate(rows,side,length)
  for label in ('lingering_owner','advancing_playback'):
   bad=copy.deepcopy(rows)
   if label=='lingering_owner':next(r for r in bad['VOICE_OWNER'] if int(r['slot'])==side and int(r['frame'])>=1462)['id']='17'
   else:next(r for r in bad['VOICE_CHANNEL'] if int(r['channel'])==10+(side-1)*2 and int(r['frame'])>=1462)['pos']=str(case['stoppedSample']+1)
   try:gate(bad,side,length)
   except AssertionError:pass
   else:raise AssertionError('Cleanup fault accepted')
  case.update(side=side,logSHA256=sync.sha(folder/'run.log'),faultsRejected=True)
  cases.append(case)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'clipSHA256':sync.sha(clip),'heardMixQualityVerified':False,'fullPortAccepted':False},indent=2))
 print(json.dumps({'passed':True,'cases':cases}))
