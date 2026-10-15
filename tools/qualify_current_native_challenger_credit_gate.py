"""Actual credit comparison establishes insufficient native start credit."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_challenger_credit_gate_runtime'
out=sync.ROOT/'audit_current_native_challenger_credit_gate_checked';assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
rows=chronology.load(folder/'run.log')
gates=[r for r in rows['JOIN_CREDIT_GATE'] if r['age']=='26']
assert [r['entry'] for r in gates]==['FF8177B0','FF817990','FF8179B0','FF817A10','FFA53C50','FFA53C70','FFA53C80','FFA53CE0','FFA53CF0','FF817A40']
compare=next(r for r in gates if r['entry']=='FFA53CE0')
assert compare['a0']=='00000002' and compare['a1']=='00000001'
assert all(r['p1']=='0' and r['p2']=='1' and r['mode']=='2' for r in gates)
assert not any(r['entry']=='FF817A70' for r in gates)
prior=chronology.load(sync.ROOT/'audit_current_native_challenger_input_reader_runtime/run.log')
assert {tag:group for tag,group in rows.items() if tag!='JOIN_CREDIT_GATE'}==prior
report={'passed':True,'nativeStartEventReached':True,'nativePlayerStateInactive':True,
 'availableCredits':1,'nativeRequiredStartCredits':2,'insufficientCreditReturnObserved':True,
 'otherScalarBaselineExact':True,'logSHA256':sync.sha(folder/'run.log'),
 'addedCharacterSpecificDefectEstablished':False,'nextAction':'Provide a second genuine coin and retry native start; keep coinage settings unchanged.',
 'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
