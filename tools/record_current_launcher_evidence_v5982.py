"""Whole5980 receipt with the explicit5322 journal/physical-gate schema.

5322 is an additive receipt, not a report with a `passed` key. Validate its
actual18cases/20512fields against both original current physical matrices;
never invent a generic passed default or promote its finite scope.
"""
import inspect,json
from pathlib import Path
import record_current_launcher_handoff_v5980 as prior_receipt
ROOT,need,sha=prior_receipt.ROOT,prior_receipt.need,prior_receipt.sha
OUT=ROOT/'audit_v5983_current_launcher_handoff_progress'

def validate_evidence(key,value,pins):
 if key!='specials':
  need(value['passed'],'Retained actual current finite requirement proof '+key);return
 expected={(m,s,False)for m in('knife','ball','blade','choke','ring','square','bicycle','leg')for s in(1,2)}|{('square',s,True)for s in(1,2)}
 rows=value['currentActualCases']
 need(value['goalStatus']=='active'and len(rows)==18 and
      {(r['move'],r['physicalSlot'],r['air'])for r in rows}==expected and
      sum(r['completeActorFields']for r in rows)==20512 and all(r['trueVictimID']==8 and r['nativeShadowCopies']>0 for r in rows)and
      not value['fullPortAcceptance']and not value['allArenaCPUOrKOOverlapArtAudioAccepted'],
      'Actual5322 journal preserves complete18finite physical/body/shadow cases, no universal transfer')
 for leaf,admission,cases,cycles,faults in(
  ('audit_v5320_current_subzero_full_repeat_matrix_checked/report.json','currentTrueSubZeroNativeVictimBothRolesAllEightMovesVerified',16,32,194),
  ('audit_v5312_current_air_square_subzero_repeat_checked/report.json','currentTrueSubZeroBothRolesVerified',2,4,26)):
  path=ROOT/leaf;report=json.loads(path.read_text())
  need(report['passed']and report[admission]and report['actualCases']==cases and report['actualVerifiedSpecialCycles']==cycles and
       len(report['actualSemanticFaultsRejected'])==faults and report['candidate']==prior_receipt.current.NAME and
       report['executableSHA256']==prior_receipt.current.EXE_SHA and value['newInputHashes'][str(path)]==sha(path),
       'Actual current physical gates and all220 original faults bind finite journal')
  pins[str(path)]=sha(path)
 pins[str(Path(prior_receipt.__file__).resolve())]=sha(prior_receipt.__file__)

source=inspect.getsource(prior_receipt.run)
before="need(value['passed'],'Retained actual current finite requirement proof '+key)"
need(source.count(before)==1,'One explicit journal-versus-report schema correction')
source=source.replace(before,'validate_evidence(key,value,pins)',1)
scope=dict(prior_receipt.run.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT,validate_evidence=validate_evidence)
exec(compile(source,__file__+'::whole5980_validated_actual_journal_schema','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':run()
