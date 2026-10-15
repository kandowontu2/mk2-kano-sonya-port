"""All original 194 negative tests and both cycles, current native repair."""
import inspect
import json
import subprocess
from pathlib import Path
import capture_native_current_specials as capture
import verify_current_projectile_repeat_v5295 as context
import verify_special_repeat_v5115 as original
import native_ai_response_full_context as candidate
ROOT, need, sha = candidate.ROOT, candidate.need, candidate.sha
OUT = ROOT/'audit_native_current_special_matrix_checked'

def main():
    need(not OUT.exists() and not capture.identity.census(), 'Fresh full matrix, actual native jobs terminal')
    check, _, _ = context.bindings()
    check.__globals__['native'] = candidate
    _, load = capture.bindings()
    for move in original.SPECS:
        for side in (1,2):
            case = load(move,side)
            report = case['report']
            terminal = json.loads((case['folder']/'native_terminal.json').read_text())
            actual = json.loads((case['folder']/'native_identity.json').read_text())
            need(report['passed'] and not report['canonicalCMDUsed'] and report['isolatedCandidateCMDUsed'] and
                report['nativeStderrEmpty'] and terminal['exitCode']==0 and not terminal['observationErrors'],
                'Complete actual new-candidate natural terminal; no public CMD acceptance inference')
            need(actual['ParentProcessId']==terminal['cmdPID'] and actual['ProcessId']==terminal['nativePID'] and
                Path(actual['ExecutablePath']).resolve()==(ROOT/candidate.NAME/'mkport_candidate.exe').resolve(),
                'Exact current executable child, both actual CMD and native process identities')
            need('-skip_gameinfo' not in actual['CommandLine'] and '-nocheat' in actual['CommandLine'] and
                '-samples' in actual['CommandLine'], 'Ordinary physical cold boot, samples enabled, no cheats')
            need(all(sha(p)==h for p,h in report['inputHashes'].items()), 'Every actual executed input intact')
    baseline = json.loads((ROOT/'audit_v5116_special_repeat_checked/report.json').read_text())
    need(sha(original.__file__)==baseline['inputHashes'][str(Path(original.__file__).resolve())],
        'Entire original independently qualified semantic and fault suite unchanged')
    scope = dict(original.main.__globals__, __file__=__file__, __doc__=__doc__, OUT=OUT,
        native=candidate, check=check, load=load)
    exec(compile(inspect.getsource(original.main), __file__+'::whole_original_194_fault_matrix', 'exec'), scope)
    scope['main']()
    path = OUT/'report.json'
    report = json.loads(path.read_text())
    report.update(actualNewCandidateColdBoots=16, canonicalUserCMDUsed=False,
        publicPlayableChanged=False, fullPortAcceptance=False)
    path.write_text(json.dumps(report,indent=2)+'\n')
    digest = sha(path)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0
        and sha(path)==digest, 'Lossless bounded matrix evidence compression')
    print(json.dumps(dict(passed=report['passed'], coldBoots=16,
        cycles=report['actualVerifiedSpecialCycles'], faults=len(report['actualSemanticFaultsRejected']),
        fields=report['actualContiguousPostFields'], publicPlayableChanged=False)), flush=True)

if __name__=='__main__':
    main()
