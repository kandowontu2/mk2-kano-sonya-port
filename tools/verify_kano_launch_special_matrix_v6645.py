"""Complete original 194-fault two-cycle matrix on the Kano launch candidate."""
import inspect,json,subprocess
from pathlib import Path
import capture_kano_launch_native_identity_v6648 as capture
import verify_current_projectile_repeat_v5295 as context
import verify_special_repeat_v5115 as original
import kano_ball_launch_context_v6642 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6646_kano_launch_special_matrix_checked'

def main():
 need(not OUT.exists()and not capture.identity.census(),'Fresh full matrix gate, actual native jobs terminal')
 check,_,_=context.bindings();check.__globals__['native']=candidate
 _,load=capture.bindings()
 for move in original.SPECS:
  for side in(1,2):
   b=load(move,side);r=b['report'];terminal=json.loads((b['folder']/'native_terminal.json').read_text());identity=json.loads((b['folder']/'native_identity.json').read_text())
   need(r['passed']and not r['canonicalCMDUsed']and r['isolatedCandidateCMDUsed']and r['nativeStderrEmpty']and terminal['exitCode']==0 and not terminal['observationErrors'],
        'Actual new candidate natural terminal; not a canonical user-CMD claim')
   need(identity['ParentProcessId']==terminal['cmdPID']and identity['ProcessId']==terminal['nativePID']and Path(identity['ExecutablePath']).resolve()==(ROOT/candidate.NAME/'mkport_candidate.exe').resolve(),
        'Exact actual compiled native executable child identity')
   need('-skip_gameinfo'not in identity['CommandLine']and '-nocheat'in identity['CommandLine']and '-samples'in identity['CommandLine'],
        'Ordinary native cold boot with samples enabled and cheats disabled')
   need(all(sha(p)==h for p,h in r['inputHashes'].items()),'Every actually executed input intact')
 baseline=json.loads((ROOT/'audit_v5116_special_repeat_checked/report.json').read_text())
 need(sha(original.__file__)==baseline['inputHashes'][str(Path(original.__file__).resolve())],'Whole original independently qualified semantic/fault gate unchanged')
 source=inspect.getsource(original.main)
 scope=dict(original.main.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT,native=candidate,check=check,load=load)
 exec(compile(source,__file__+'::whole_original_194_fault_new_candidate_matrix','exec'),scope);scope['main']()
 p=OUT/'report.json';report=json.loads(p.read_text())
 report.update(actualNewCandidateColdBoots=16,canonicalUserCMDUsed=False,publicPlayableChanged=False,fullPortAcceptance=False)
 p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving full matrix proof compression')
 print(json.dumps(dict(passed=report['passed'],coldBoots=16,cycles=report['actualVerifiedSpecialCycles'],faults=len(report['actualSemanticFaultsRejected']),fields=report['actualContiguousPostFields'],publicPlayableChanged=False)),flush=True)

if __name__=='__main__':main()
