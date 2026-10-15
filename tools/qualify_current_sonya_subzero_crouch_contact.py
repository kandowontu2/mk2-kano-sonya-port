"""Current native Sonya uppercut activation/contact, not campaign acceptance."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

def gate(rows):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 entries=rows['SUBZERO_UPPERCUT_ENTRY']
 assert len(entries)==4 and all(r['id']=='18' and r['pc']=='FF870DD0' for r in entries)
 first=entries[0]
 contact=[r for r in rows['HEALTH'] if int(first['frame'])<=int(r['frame'])<=int(first['frame'])+10 and r['slot']=='1' and r['pc']=='FF836700']
 assert len(contact)==1 and int(contact[0]['before'])-int(contact[0]['after'])==40 and contact[0]['a8']==first['actor']
 own=[r for r in rows['SUBZERO_COMMAND_FIELD'] if r['actor']==first['actor'] and int(first['frame'])-1<=int(r['frame'])<=int(contact[0]['frame'])]
 assert own and all(r['id']==r['roster']=='18' and r['owner']==r['actor'] for r in own)
 assert contact[0]['a13']==own[0]['main']
 assert any(r['action']=='263' for r in own)
 assert not [r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']
 return {'nativeUppercutEntries':4,'firstContactDamage':40,'contactFrame':int(contact[0]['frame']),'nativeContactPC':contact[0]['pc'],'subzeroRoundClear':False}

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_crouch_settle_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log');result=gate(rows)
 bad=copy.deepcopy(rows);bad['SUBZERO_UPPERCUT_ENTRY'][0]['id']='1'
 try:gate(bad)
 except AssertionError:pass
 else:raise AssertionError('Proxy activation accepted')
 result.update(passed=True,proxyFaultRejected=True,logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False,gameSourceChanged=False)
 out=sync.ROOT/'audit_current_sonya_subzero_crouch_contact_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps(result,indent=2))
 print('PASS four actual native uppercuts, first owned native contact40; no SubZero round win')
