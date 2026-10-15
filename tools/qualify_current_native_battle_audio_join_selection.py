"""Actual selector audio cleanup, preserving legitimate presentation announcements."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows):
 trigger=rows['JOIN_TRIGGER'];selection=rows['JOIN_SELECTION'];done=rows['JOIN_COMPLETE']
 assert len(trigger)==len(selection)==len(done)==1
 assert trigger[0]['id']=='18' and trigger[0]['cue']=='6B01' and trigger[0]['pc']=='FFF9A4C0'
 start=int(selection[0]['age'])
 assert int(done[0]['frame'])-int(selection[0]['frame'])==160
 inputs=rows['JOIN_INPUT']
 assert [(r['button'],int(r['age'])) for r in inputs]==[('Coin_1',i) for i in range(1,5)]+[('Start_1',i) for i in range(8,12)]
 owners=[r for r in rows['JOIN_OWNER'] if int(r['age'])>=start]
 assert len(owners)==322
 for side in (1,2):
  group=[r for r in owners if int(r['slot'])==side]
  assert [int(r['age']) for r in group]==list(range(start,start+161))
  assert all(r['mode']=='4' and r['actor']==r['main']=='00000000' and r['id']=='0' for r in group)
 channels=[r for r in rows['JOIN_CHANNEL'] if int(r['age'])>=start]
 assert len(channels)==19*161
 for n in range(19):
  group=[r for r in channels if int(r['channel'])==n]
  assert [int(r['age']) for r in group]==list(range(start,start+161))
  assert all(r['mode']=='4' for r in group)
  if n>=10:
   assert all(int(r['length'])==0 or int(r['sample']) in (-1,4294967295) for r in group)
   assert len({r['pos'] for r in group})==1
 first=[r for r in rows['JOIN_CHANNEL'] if r['age']=='0' and r['channel']=='10']
 assert len(first)==1 and int(first[0]['length'])>0 and int(first[0]['sample'])==14
 return {'selectorFields':161,'sampleChannelsObserved':19,'battleFinishChannelsSilent':9,
         'bothBattleOwnersCleared':True,'initialOwnedBicycleLaunchObserved':True,
         'activeClipCutByJoinProven':False}


if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_native_battle_audio_join_selection_runtime'
 out=sync.ROOT/'audit_current_native_battle_audio_join_selection_checked'
 assert not out.exists()
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 prior=chronology.load(sync.ROOT/'audit_current_native_battle_audio_join_runtime/run.log')
 for tag,group in rows.items():
  if tag=='JOIN_OWNER':group=[r for r in group if int(r['age'])<=300]
  if tag=='JOIN_CHANNEL':group=[r for r in group if int(r['age'])<=300 and 10<=int(r['channel'])<=13]
  assert group==prior.get(tag,[])
 result=gate(rows)
 for label in ('stale_owner','advancing_battle_channel'):
  bad=copy.deepcopy(rows)
  age=int(rows['JOIN_SELECTION'][0]['age'])
  if label=='stale_owner':next(r for r in bad['JOIN_OWNER'] if int(r['age'])>=age)['actor']='01034E90'
  else:next(r for r in bad['JOIN_CHANNEL'] if int(r['age'])>=age and r['channel']=='10')['pos']='999.00000000'
  try:gate(bad)
  except AssertionError:pass
  else:raise AssertionError('Scene cleanup fault accepted')
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'result':result,
  'physicalBaselineExact':True,'cleanupFaultsRejected':True,'terminal':terminal,
  'logSHA256':sync.sha(folder/'run.log'),'heardMixQualityVerified':False,'fullPortAccepted':False},indent=2))
 print(json.dumps({'passed':True,'result':result}))
