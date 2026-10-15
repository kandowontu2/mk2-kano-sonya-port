"""Canonical user CMD, all eight specials, both slots, two cycles and recovery.

Retain the complete original 194-fault semantic gate. This is normal launcher
integration evidence, not blanket every-arena/art/audio/finisher acceptance.
The test controller is supplied only by isolated test command arguments.
"""
import inspect,json,subprocess
from pathlib import Path
import capture_current_cmd_specials_v6263 as capture
import verify_current_projectile_repeat_v5295 as context
import verify_special_repeat_v5115 as original
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6266_current_cmd_special_matrix_checked'

def main():
 need(not OUT.exists(),'Fresh full original semantic matrix gate')
 check,_,_=context.bindings();_,load=capture.bindings()
 for move in original.SPECS:
  for side in(1,2):
   b=load(move,side);r=b['report'];terminal=json.loads((b['folder']/'native_terminal.json').read_text());identity=json.loads((b['folder']/'native_identity.json').read_text())
   need(r['passed']and r['canonicalCMDUsed']and not r['skipGameInfoUsed']and r['nativeStderrEmpty']and terminal['exitCode']==0 and not terminal['observationErrors'],'Actual natural current canonical-CMD terminal')
   need(identity['ParentProcessId']==terminal['cmdPID']and identity['ProcessId']==terminal['nativePID']and Path(identity['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve(),'Full actual checked native executable child identity')
   need('-skip_gameinfo'not in identity['CommandLine']and '-nocheat'in identity['CommandLine']and '-samples'in identity['CommandLine'],'Actual normal startup with cheats disabled and all samples enabled')
   need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Actual compiled/controller/production CMD inputs unchanged')
 baseline=json.loads((ROOT/'audit_v5116_special_repeat_checked/report.json').read_text())
 need(sha(original.__file__)==baseline['inputHashes'][str(Path(original.__file__).resolve())],'Entire original previously qualified semantic gate unchanged')
 source=inspect.getsource(original.main)
 source=source.replace('allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True','allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified=True,canonicalUserCMDAllEightMovesBothSlotsIntegrated=True',1)
 scope=dict(original.main.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT,native=current,check=check,load=load)
 exec(compile(source,__file__+'::entire_original_194_fault_matrix','exec'),scope);scope['main']()
 report=json.loads((OUT/'report.json').read_text())
 report.update(actualCanonicalCMDColdBoots=16,normalStartupWithoutSkipGameInfo=True,newBuilds=0,newZIPs=0,
               priorHostQuotingFailurePreserved=str(ROOT/'audit_v6262_current_cmd_special_knife_p1/result.json'),priorFailureStartedNativeGame=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT/'report.json')],capture_output=True).returncode==0,'Exact terminal report compression')
 print(json.dumps(dict(passed=report['passed'],canonicalCMDBoots=16,cycles=report['actualVerifiedSpecialCycles'],faults=len(report['actualSemanticFaultsRejected']),fields=report['actualContiguousPostFields'],fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
