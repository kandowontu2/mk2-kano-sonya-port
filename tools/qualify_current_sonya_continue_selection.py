"""Actual paid continue, post-init cursor ID, constructed own actor and followthrough."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows):
 assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
 assert len(rows['LOSS'])==1
 selections=rows['SELECT']
 assert len(selections)==2 and selections[1]['continue']==rows['LOSS'][0]['frame']
 initialized=rows['SELECT_INITIALIZED']
 assert len(initialized)==2 and initialized[1]['roster']=='9' and initialized[1]['target']=='18' and initialized[1]['path']=='Right'
 ids=[r for r in rows['SELECT_ID'] if r['number']=='2']
 assert len(ids)==2 and all(r['roster']=='18' and r['state']=='3' for r in ids)
 fight=next(r for r in rows['FIGHT'] if r['selection']=='2')
 assert fight['human']=='18:18'
 fields=rows['CONTINUE_PAIR']
 assert [int(r['age']) for r in fields]==list(range(161))
 assert all(r['id']==r['roster']=='18' and r['state']=='1' and r['owner']==r['actor'] for r in fields)
 assert len({(r['actor'],r['main']) for r in fields})==1
 assert rows['CONTINUE_COMPLETE'][0]['fields']=='161'
 return {'paidContinueObserved':True,'postInitializationRouteVerified':True,'trueSonyaMatchFields':161}


if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_continue_selection_runtime'
 out=sync.ROOT/'audit_current_sonya_continue_selection_checked'
 assert not out.exists()
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 result=gate(rows)
 fault=copy.deepcopy(rows);fault['CONTINUE_PAIR'][0]['id']='1'
 try:gate(fault)
 except AssertionError:pass
 else:raise AssertionError('Proxy accepted')
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'result':result,
  'proxyFaultRejected':True,'terminal':terminal,'logSHA256':sync.sha(folder/'run.log'),
  'gameSourceChanged':False,'allContinueSlotsCovered':False,'fullPortAccepted':False},indent=2))
 print(json.dumps({'passed':True,'result':result}))
