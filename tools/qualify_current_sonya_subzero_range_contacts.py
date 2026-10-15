"""Finite native contact improvement; no round or campaign success asserted."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_range_uppercut_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 entries=rows['SUBZERO_UPPERCUT_ENTRY'];assert len(entries)==11
 assert all(r['id']=='18' and r['pc']=='FF870DD0' for r in entries)
 cutoff=int(rows['STAGE'][1]['frame'])
 contacts=[r for r in rows['HEALTH'] if int(r['frame'])>cutoff and r['slot']=='1' and r['pc']=='FF836700']
 assert len(contacts)==6
 for contact in contacts:
  assert int(contact['before'])-int(contact['after'])==40
  entry=next(r for r in entries if int(r['frame'])==int(contact['frame'])-6)
  assert entry['actor']==contact['a8']
  fields=[r for r in rows['SUBZERO_COMMAND_FIELD'] if r['actor']==entry['actor'] and int(entry['frame'])<=int(r['frame'])<=int(contact['frame'])]
  assert fields and all(r['id']==r['roster']=='18' and r['owner']==r['actor'] for r in fields)
  assert contact['a13']==fields[0]['main']
 assert not [r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 out=sync.ROOT/'audit_current_sonya_subzero_range_contacts_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'nativeUppercutEntries':11,'ownedUppercutContacts':6,'damagePerContact':40,'subzeroOwnRoundWins':0,'logSHA256':sync.sha(folder/'run.log'),'gameSourceChanged':False,'fullPortAccepted':False},indent=2))
 print('PASS11native uppercuts/6owned contacts40; SubZero round clearance still unproven')
