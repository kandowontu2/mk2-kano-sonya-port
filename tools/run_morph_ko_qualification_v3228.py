"""Four native morphed KO qualifiers after one real premorph uppercut."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT;OUT=ROOT/'audit_v3230_morph_ko_dispatch'
RUNNER=ROOT/'tools/run_morph_adversity_v3227.ps1'
PWSH=Path('C:/Users/kando/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
def main():
    assembly.need(not OUT.exists(),'New immutable evidence')
    OUT.mkdir();pins={str(p):assembly.sha(p)for p in(RUNNER,PWSH,Path(__file__).resolve())}
    def run(case):
        target,side=case;leaf=f'audit_v3229_morph_adversity_{target}_p{side}_ko_added'
        result=subprocess.run([str(PWSH),'-NoProfile','-File',str(RUNNER),'-CaseName',leaf,'-Target',target,'-Side',str(side),'-Phase','ko'],cwd=ROOT,capture_output=True,text=True)
        (OUT/(leaf+'.txt')).write_text(result.stdout+result.stderr)
        path=ROOT/leaf/'result.json';record=dict(target=target,side=side,phase='ko',form='added',exitCode=result.returncode,
          nativeExitCode=json.loads(path.read_text(encoding='utf-8-sig'))['exit_code']if path.exists()else None)
        print(leaf+' terminal '+str(record['exitCode'])+'/'+str(record['nativeExitCode']),flush=True);return leaf,record
    with ThreadPoolExecutor(max_workers=4)as pool:records=dict(pool.map(run,[(t,s)for t in('kano','sonya')for s in(1,2)]))
    passed=all(r['exitCode']==r['nativeExitCode']==0 for r in records.values())
    for p,h in pins.items():assembly.need(assembly.sha(p)==h,'Immutable input')
    (OUT/'report.json').write_text(json.dumps(dict(passed=passed,cases=records,captures=4,
      normalActualPremorphDamageOnly=True,independentGameplayVerificationPending=True,fullPortAcceptance=False,inputHashes=pins),indent=2)+'\n')
    assembly.need(passed,'Four cold native processes terminal')
if __name__=='__main__':main()

