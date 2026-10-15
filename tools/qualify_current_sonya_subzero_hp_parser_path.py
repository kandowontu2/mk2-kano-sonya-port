"""Verify actual special-parser path; do not confuse helper exit with attack."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

if __name__=='__main__':
 sync.verify()
 folder=sync.ROOT/'audit_current_sonya_subzero_hp_dispatch_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
 rows=chronology.load(folder/'run.log')
 old=chronology.load(sync.ROOT/'audit_current_sonya_subzero_uppercut_spacing_runtime/run.log')
 for tag in set(rows)|set(old):
  if tag=='SUBZERO_HP_DISPATCH':continue
  assert rows.get(tag,[])==old.get(tag,[])
 events=rows['SUBZERO_HP_DISPATCH']
 assert len(events)<=200
 first=events[0]['start']
 firstevents=[r for r in events if r['start']==first and r['a8']==r['actor'] and r['age']=='4']
 assert [r['entry'] for r in firstevents]==['FF861D70','FFFAA400','FFFFC800','FF8775D0','FF877420']
 assert all(r['action']=='770' and r['flags']=='0001' and r['body']=='0012' for r in firstevents)
 assert not rows.get('SUBZERO_UPPERCUT_ENTRY')
 out=sync.ROOT/'audit_current_sonya_subzero_hp_parser_path_checked';assert not out.exists();out.mkdir()
 (out/'report.json').write_text(json.dumps({'passed':True,'firstAttemptFrame':int(first),'actualOwnedParserEntries':[r['entry'] for r in firstevents],'specialCommandMissExitsNativeHelper':True,'ordinaryUppercutEntryObserved':False,'fullScalarBaselineIdentical':True,'logSHA256':sync.sha(folder/'run.log'),'nativeHelperReturnIsNotOrdinaryAttackAcceptance':True,'characterDefectEstablished':False,'fullPortAccepted':False},indent=2))
 print('PASS actual own-actor HP special parser miss/native helper exit; all prior scalar observations exact')
