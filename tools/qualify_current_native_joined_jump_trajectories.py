"""Verify real neutral jump trajectories after physical Up in joined matches."""
import copy
import json
import check_campaign_stage_chronology as chronology
import qualify_current_native_joined_controls_scoped as controls
import verify_native_source_sync as sync


def gate(rows,targets):
 result=controls.gate(rows,targets)
 jumps=[]
 for side in (1,2):
  start=min(int(r['age']) for r in rows['JOINED_CONTROL'] if int(r['slot'])==side and r['button']=='Up')
  fields=[r for r in rows['JOINED_MATCH_PAIR'] if int(r['slot'])==side and start<=int(r['age'])<=start+70]
  assert [int(r['age']) for r in fields]==list(range(start,start+71))
  floor=int(fields[0]['y'])
  airborne=[r for r in fields if int(r['y'])<floor-5]
  assert len(airborne)>25 and all(r['action']=='779' for r in airborne)
  apex=min(int(r['y']) for r in fields)
  assert floor-apex>=90
  first=int(airborne[0]['age']);last=int(airborne[-1]['age'])
  assert start<first<start+20 and last>first+20
  assert any(int(r['age'])>last and int(r['y'])==floor and r['action']=='771' for r in fields)
  assert all(r['hp']==fields[0]['hp'] for r in fields)
  jumps.append({'slot':side,'actualID':targets[side-1],'physicalUpAge':start,'nativeNeutralJumpAction':779,'risePixels':floor-apex,'landingObserved':True,'noDamageDuringJump':True})
 result.update(jumpActivationProven=True,jumps=jumps)
 return result


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_native_joined_jump_trajectories_checked';assert not out.exists()
 cases=[]
 for targets in ([17,18],[18,17]):
  folder=sync.ROOT/f'audit_current_native_joined_controls_scoped_{targets[0]}_{targets[1]}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  rows=chronology.load(folder/'run.log');result=gate(rows,targets)
  bad=copy.deepcopy(rows)
  for row in bad['JOINED_MATCH_PAIR']:
   if row['slot']=='1':row['y']='82'
  try:gate(bad,targets)
  except AssertionError:pass
  else:raise AssertionError('No-rise jump fault accepted')
  result.update(logSHA256=sync.sha(folder/'run.log'),noRiseFaultRejected=True)
  cases.append(result)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'newEmulatorRuns':0,'gameSourceChanged':False,'fullPortAccepted':False,'allJoinedSpecialMovesVerified':False},indent=2))
 print('PASS four real joined-player neutral jumps: physical Up, native airborne action, rise and landing')
