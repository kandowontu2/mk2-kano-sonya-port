"""Complete retained low-airkick history and bounded observed frontier, not normalized speed benchmark."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
old=root/'audit_current_sonya_p1_kintaro_low_airkick_runtime'
new=root/'audit_current_sonya_p1_kintaro_deferred_observers_runtime'
out=root/'audit_current_sonya_p1_deferred_observers_history_checked';assert not out.exists()
def retained(path):
 return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and not s.startswith('MK2_NAT_CAMPAIGN_SPECIAL ') and int(re.search(r'\bframe=(\d+)',s)[1])<=107644]
expected=retained(old/'run.log');actual=retained(new/'run.log')
assert actual==expected
faults=[]
for tag in ('INPUT_DIGEST','WIN','FIGHT'):
 index=next(i for i,s in enumerate(actual) if s.startswith('MK2_NAT_CAMPAIGN_'+tag+' '))
 broken=actual[:];broken[index]=broken[index]+' deliberate_fault=1'
 assert broken!=actual
 try:assert broken==expected
 except AssertionError:faults.append(tag)
 else:raise AssertionError('Retained prefix fault accepted')
rows=load(new/'run.log')
first15=next((r for r in rows['STATE'] if r['stage']=='15'),None)
first16=next((r for r in rows['STATE'] if r['stage']=='16'),None)
last=max(int(r['frame']) for entries in rows.values() for r in entries)
cpuwins=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='2']
losses=[r for r in rows['LOSS'] if r['stage']=='15']
term_old=json.loads((old/'terminal.json').read_text(encoding='utf-8-sig'));term_new=json.loads((new/'terminal.json').read_text(encoding='utf-8-sig'))
report=dict(retainedNativeAndPhysicalRecordsEquivalentThrough=107644,matchingRecords=len(actual),excludedOnlyIntentionalEarlySpecialEntryTags=True,
 rejectedFaults=faults,
 specialObserverInstallFrameInferredFromImmutableSourceAndObservedStage=first15['frame'] if first15 else None,
 endingObserverInstallFrameInferredFromImmutableSourceAndObservedStage=first16['frame'] if first16 else None,
 actualTapRegistrationTimestampLogged=False,stage16EndingObserversExercised=first16 is not None,
 earlierBaselineLastCompleteRecordFrame=107644,earlierBaselineLastTruncatedRecordFrame=107700,
 newLastObservedRecordFrame=last,previousTerminal=term_old,newTerminal=term_new,
 fartherObservedFrontierThisBoundedRun=last>107700,
 normalizedPerformanceBenchmarkAccepted=False,causalPerformanceAttributionAccepted=False,
 ownKintaroRoundWins=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],cpuKintaroRoundWins=cpuwins,actualStage15PaidLosses=losses,
 lowAirKickWinningRouteAccepted=False,fullPortAccepted=False,
 previousLogSHA256=sync.sha(old/'run.log'),newLogSHA256=sync.sha(new/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(matchingRecords=len(actual),prefixThrough=107644,rejectedFaults=faults,first15=report['specialObserverInstallFrameInferredFromImmutableSourceAndObservedStage'],first16=report['endingObserverInstallFrameInferredFromImmutableSourceAndObservedStage'],lastObserved=last,cpuKintaroRoundWins=len(cpuwins),paidKintaroLosses=len(losses),newLogSHA256=report['newLogSHA256'])))
