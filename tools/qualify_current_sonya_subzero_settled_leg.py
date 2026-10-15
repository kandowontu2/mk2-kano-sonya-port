"""Classify leg activation and native victim-owned throw damage accurately."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_settled_leg_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 entries=rows['SUBZERO_LEG_ENTRY'];assert len(entries)==3
 assert all(r['id']==r['roster']=='18' and r['pc']=='FFF80810' for r in entries)
 fight=next(r for r in rows['FIGHT'] if r['stage']=='1')
 assert fight['human']=='18:18' and fight['cpu']=='8:8'
 own,victim=fight['actors'].split(',')
 assert all(r['actor']==own for r in entries)
 damage=[r for r in rows['HEALTH'] if r['slot']=='1' and r['pc']=='FF836700' and 0<int(r['before'])<=161 and int(r['after'])<int(r['before']) and int(r['frame'])>int(fight['frame'])]
 assert len(damage)==2
 for contact,entry in zip(damage,entries):
  assert int(contact['frame'])-int(entry['frame'])==56
  assert int(contact['before'])-int(contact['after'])==35 and contact['a8']==victim
 assert not [r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 out=sync.ROOT/'audit_current_sonya_subzero_settled_leg_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'actualLegActivations':3,'nativeVictimOwnedDamageContacts':2,'damagePerGrab':35,'subzeroOwnRoundWins':0,'logSHA256':sync.sha(folder/'run.log'),'fullPortAccepted':False},indent=2))
 print('PASS3native leg activations/2victim-owned contacts35; no round win')
