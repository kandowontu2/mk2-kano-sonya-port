"""Fresh current candidate native command rejections and stock fallbacks.

Normal controller buttons only; no native actor/CPU/health/seed assistance.
"""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
ROOT=assembly.ROOT
OUT=ROOT/'audit_v3189_current_morph_command_dispatch'
PWSH=Path('C:/Users/kando/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
RUNNER=ROOT/'tools/run_human_shang_probe_v3187.ps1'

def run():
    assembly.need(not OUT.exists(),'Never overwrite evidence')
    cases=[]
    for side in(1,2):
        for target,profiles in(
          ('kano',('wrong_button','reversed','expired','extra_button','airborne')),
          ('sonya',('no_down','no_lp','no_block','extra_button','airborne','block2','block_first','lp_first'))):
            for profile in profiles:cases.append((target,side,profile))
        for profile in('stock_lp','stock_lk','stock_block'):cases.append(('kano',side,profile))
    assembly.need(len(cases)==32 and len(set(cases))==32,'Exactly32new unique real-input cases')
    for target,side,profile in cases:
        assembly.need(not(ROOT/f'audit_v3190_current_morph_{target}_p{side}_{profile}').exists(),
          'All cases must be new immutable evidence')
    OUT.mkdir();records={}
    pins={str(RUNNER):assembly.sha(RUNNER),str(PWSH):assembly.sha(PWSH),str(Path(__file__).resolve()):assembly.sha(__file__)}
    def execute(case):
        target,side,profile=case;leaf=f'audit_v3190_current_morph_{target}_p{side}_{profile}'
        result=subprocess.run([str(PWSH),'-NoProfile','-File',str(RUNNER),
          '-CaseName',leaf,'-Target',target,'-Side',str(side),'-Profile',profile],
          cwd=ROOT,capture_output=True,text=True)
        (OUT/(leaf+'.txt')).write_text(result.stdout+result.stderr)
        meta=ROOT/leaf/'result.json'
        record=dict(target=target,side=side,profile=profile,exitCode=result.returncode,
          nativeExitCode=json.loads(meta.read_text(encoding='utf-8-sig'))['exit_code']if meta.exists()else None)
        print(leaf+' terminal '+str(record['exitCode'])+'/'+str(record['nativeExitCode']),flush=True)
        return leaf,record
    with ThreadPoolExecutor(max_workers=4)as pool:
        for future in as_completed([pool.submit(execute,case)for case in cases]):
            leaf,record=future.result();records[leaf]=record
    for file,wanted in pins.items():assembly.need(assembly.sha(file)==wanted,'Unchanged dispatcher input')
    terminal=all(r['exitCode']==r['nativeExitCode']==0 for r in records.values())
    report=dict(passed=terminal,captures=len(records),cases=records,fullPortAcceptance=False,
      independentGameplayVerificationPending=True,inputHashes=pins)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    assembly.need(terminal,'Every native process terminal without launch/observer failure')
    print('32actual command fixtures terminal; independent verification pending',flush=True)

if __name__=='__main__':run()
