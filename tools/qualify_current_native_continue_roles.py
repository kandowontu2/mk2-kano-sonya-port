"""Four CPU-earned losses, initialized native cursor routes, actual resumed IDs."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(rows,fighter,side):
 identity=17 if fighter=='kano' else 18
 assert all(r['writes']=='0' and r['assistance']=='none' and r['fighter']==fighter and int(r['human_slot'])==side for group in rows.values() for r in group)
 losses=rows['LOSS'];assert len(losses)==1
 lossframe=int(losses[0]['frame'])
 wins=[r for r in rows['WIN'] if int(r['frame'])<lossframe]
 assert len(wins)==2 and all(int(r['slot'])==3-side and r['pc']=='FF8296B0' for r in wins)
 assert all(int(r['health'].split(',')[side-1])==0 and int(r['health'].split(',')[2-side])>0 for r in wins)
 selections=rows['SELECT'];assert len(selections)==2 and selections[1]['continue']==str(lossframe)
 initialized=rows['SELECT_INITIALIZED'];assert len(initialized)==2
 assert initialized[1]['target']==str(identity)
 assert int(initialized[1]['frame'])-int(selections[1]['frame'])==56
 ids=[r for r in rows['SELECT_ID'] if r['number']=='2']
 assert len(ids)==2 and all(int(r['roster'])==identity and r['state']=='3' for r in ids)
 fight=next(r for r in rows['FIGHT'] if r['selection']=='2')
 assert fight['human']==f'{identity}:{identity}'
 fields=rows['CONTINUE_PAIR']
 assert [int(r['age']) for r in fields]==list(range(161))
 assert all(int(r['id'])==int(r['roster'])==identity and r['state']=='1' and r['owner']==r['actor'] for r in fields)
 assert len({(r['actor'],r['main']) for r in fields})==1
 assert rows['CONTINUE_COMPLETE'][0]['fields']=='161'
 return {'fighter':fighter,'side':side,'nativeCpuRoundWins':2,'paidContinue':True,
         'actualResumedID':identity,'consecutiveResumedFields':161}


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_native_continue_roles_checked';assert not out.exists()
 cases=[]
 for fighter in ('kano','sonya'):
  for side in (1,2):
   folder=sync.ROOT/f'audit_current_native_continue_{fighter}_p{side}_runtime'
   terminal=json.loads((folder/'terminal.json').read_text())
   assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
   assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
   rows=chronology.load(folder/'run.log')
   case=gate(rows,fighter,side)
   bad=copy.deepcopy(rows);bad['CONTINUE_PAIR'][0]['id']='1'
   try:gate(bad,fighter,side)
   except AssertionError:pass
   else:raise AssertionError('Proxy accepted')
   case.update(logSHA256=sync.sha(folder/'run.log'),terminalSHA256=sync.sha(folder/'terminal.json'),proxyFaultRejected=True)
   cases.append(case)
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
  'allVisualAudioContinueCasesAccepted':False,'gameSourceChanged':False,'fullPortAccepted':False},indent=2))
 print('PASS all four native CPU-earned loss / paid continue / real-ID resumed actor cases')
