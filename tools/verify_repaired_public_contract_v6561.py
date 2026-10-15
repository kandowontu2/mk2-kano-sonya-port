"""Whole physical projectile/recovery/actual-record fault suite on normal CMD.

Four actual cases, two cycles each: both real characters in both player slots.
The wider freshly qualified eight-move matrix remains separate; this proves
the promoted launch route, not all gameplay/audio/arena/campaign integration.
"""
import inspect,json,subprocess
from pathlib import Path
import capture_repaired_public_contract_v6559 as capture
import capture_repaired_specials_v6512 as private
import verify_current_projectile_repeat_v5295 as context
import verify_special_repeat_v5115 as original
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6562_repaired_public_contract_checked'

def main():
 need(not OUT.exists()and not capture.prior.original.prior.census(),'Fresh qualification; every actual native job terminal')
 _,load=capture.bindings();_,oldload=private.bindings()
 check,_,_=context.bindings();check.__globals__['native']=candidate
 comparisons=[]
 for move,side in [(m,s)for m in ('knife','ring')for s in (1,2)]:
  b=load(move,side);r=b['report'];t=json.loads((b['folder']/'native_terminal.json').read_text());i=json.loads((b['folder']/'native_identity.json').read_text())
  need(r['passed']and r['canonicalCMDUsed']and r['nativeStderrEmpty']and t['exitCode']==0 and not t['observationErrors'],
       'Whole actual normal CMD cold boot and gameplay terminal without observer errors')
  need(i['ProcessId']==t['nativePID']and i['ParentProcessId']==t['cmdPID']and
       Path(i['ExecutablePath']).resolve()==(ROOT/candidate.NAME/'mkport_candidate.exe').resolve(),
       'Actual repaired native executable child of canonical CMD')
  need('-skip_gameinfo'not in i['CommandLine']and '-nocheat'in i['CommandLine']and '-samples'in i['CommandLine'],'Ordinary unsuppressed checked launch arguments')
  old=oldload(move,side)
  need(r['actualScenes']==old['report']['actualScenes']and r['independentSemantics']==old['report']['independentSemantics']and
       b['rows']==old['rows'],'Every actual captured selection/combat pixel digest and full physical/state/health/body/publication chronology matches private repaired candidate')
  comparisons.append(dict(move=move,side=side,wholeCapturedChronologyAndPixelsIdentical=True,fullRGBDigests=len(r['actualScenes'])))
 baseline=json.loads((ROOT/'audit_v5116_special_repeat_checked/report.json').read_text())
 need(sha(original.__file__)==baseline['inputHashes'][str(Path(original.__file__).resolve())],'Whole original physical/art/health/ownership and negative test source intact')
 source=inspect.getsource(original.main)
 changes={'for move in SPECS:':"for move in ('knife','ring'):",'actualVerifiedSpecialCycles=32':'actualVerifiedSpecialCycles=8',
          'allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True':'allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=False,currentProjectileMovesBothSlotsRepeatTwiceAndRecoverVerified=True',
          'stationarySquareWhiffsExplicit=True':'stationarySquareWhiffsExplicit=False'}
 for a,b in changes.items():need(source.count(a)==1,'Only explicit four-case current-CMD scope; all corresponding gates/faults retained');source=source.replace(a,b,1)
 scope=dict(original.main.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT,native=candidate,check=check,load=load)
 exec(compile(source,__file__+'::whole_original_corresponding_projectile_fault_suite','exec'),scope);scope['main']()
 p=OUT/'report.json';r=json.loads(p.read_text());need(r['actualCases']==4 and len(r['actualSemanticFaultsRejected'])==50,'All four full native cases and corresponding original fifty actual-record faults')
 r.update(actualNormalCMDColdBoots=4,canonicalUserCMDUsed=True,checkedWIPPromotion=True,
          actualWholePrivateRepairedTrajectoryComparisons=comparisons,finishedReleasePromotion=False,goalStatus='active')
 for pth in (Path(__file__),Path(capture.__file__),Path(private.__file__),Path(original.__file__),ROOT/'audit_v6554_repaired_default_launcher_checked/report.json'):
  r['inputHashes'][str(pth.resolve())]=sha(pth)
 need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Every current launch, native evidence and independent gate pin intact')
 p.write_text(json.dumps(r,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact public-CMD proof compression')
 print(json.dumps(dict(passed=True,nativeCases=4,specialCycles=8,actorFields=r['actualContiguousPostFields'],actualFaultsRejected=50)),flush=True)

if __name__=='__main__':main()
