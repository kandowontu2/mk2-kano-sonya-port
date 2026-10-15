"""24fresh normal-human adversity/repeat cases including stock transition controls."""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT;OUT=ROOT/'audit_v3219_morph_adversity_dispatch'
RUNNER=ROOT/'tools/run_morph_adversity_v3216.ps1'
PWSH=Path('C:/Users/kando/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
def main():
    assembly.need(not OUT.exists(),'Never overwrite evidence')
    cases=[(target,side,phase,'added')for target in('kano','sonya')for side in(1,2)
      for phase in('forward','formed','reverse','ko','repeat_morph')]
    cases += [('kano',side,phase,'stock_cage')for side in(1,2)for phase in('forward','reverse')]
    assembly.need(len(cases)==24,'24fresh independently specified cases')
    for target,side,phase,form in cases:
        assembly.need(not(ROOT/f'audit_v3217_morph_adversity_{target}_p{side}_{phase}_{form}').exists(),'New immutable capture')
    pins={str(p):assembly.sha(p)for p in(RUNNER,PWSH,Path(__file__).resolve())}
    OUT.mkdir();records={}
    def run(case):
        target,side,phase,form=case;leaf=f'audit_v3217_morph_adversity_{target}_p{side}_{phase}_{form}'
        result=subprocess.run([str(PWSH),'-NoProfile','-File',str(RUNNER),'-CaseName',leaf,
          '-Target',target,'-Side',str(side),'-Phase',phase,'-Form',form],cwd=ROOT,capture_output=True,text=True)
        (OUT/(leaf+'.txt')).write_text(result.stdout+result.stderr)
        path=ROOT/leaf/'result.json';record=dict(target=target,side=side,phase=phase,form=form,
          exitCode=result.returncode,nativeExitCode=json.loads(path.read_text(encoding='utf-8-sig'))['exit_code']if path.exists()else None)
        print(leaf+' terminal '+str(record['exitCode'])+'/'+str(record['nativeExitCode']),flush=True)
        return leaf,record
    with ThreadPoolExecutor(max_workers=4)as pool:
        for future in as_completed([pool.submit(run,case)for case in cases]):
            leaf,record=future.result();records[leaf]=record
    for file,wanted in pins.items():assembly.need(assembly.sha(file)==wanted,'Immutable input')
    passed=all(r['exitCode']==r['nativeExitCode']==0 for r in records.values())
    (OUT/'report.json').write_text(json.dumps(dict(passed=passed,captures=len(records),cases=records,
      independentGameplayVerificationPending=True,fullPortAcceptance=False,inputHashes=pins),indent=2)+'\n')
    assembly.need(passed,'All cold real-human processes terminal')
if __name__=='__main__':main()

