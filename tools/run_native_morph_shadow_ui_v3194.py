"""Four cold corrected-build real CSS/ladder/first-match runs, no assistance."""
import json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT;OUT=ROOT/'audit_v3195_native_morph_shadow_ui_dispatch'
RUNNER=ROOT/'tools/run_native_morph_shadow_ui_v3193.ps1'
PWSH=Path('C:/Users/kando/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
def main():
    assembly.need(not OUT.exists(),'Never overwrite evidence')
    OUT.mkdir();records={}
    def run(case):
        target,side=case;leaf=f'audit_v3196_ui_{target}_p{side}'
        assembly.need(not(ROOT/leaf).exists(),'Immutable fresh case')
        result=subprocess.run([str(PWSH),'-NoProfile','-File',str(RUNNER),'-CaseName',leaf,
          '-Fighter',target,'-Side',str(side)],cwd=ROOT,capture_output=True,text=True)
        (OUT/(leaf+'.txt')).write_text(result.stdout+result.stderr)
        path=ROOT/leaf/'result.json'
        record=dict(exitCode=result.returncode,nativeExitCode=json.loads(path.read_text(encoding='utf-8-sig'))['exit_code']if path.exists()else None)
        print(leaf+' terminal '+str(record),flush=True);return leaf,record
    with ThreadPoolExecutor(max_workers=4)as pool:
        records=dict(pool.map(run,[(target,side)for target in('kano','sonya')for side in(1,2)]))
    passed=all(r['exitCode']==r['nativeExitCode']==0 for r in records.values())
    value=dict(passed=passed,cases=records,independentVerificationPending=True,fullPortAcceptance=False,
      inputHashes={str(p):assembly.sha(p)for p in(RUNNER,PWSH,Path(__file__).resolve())})
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    assembly.need(passed,'Four native processes terminal')
if __name__=='__main__':main()
