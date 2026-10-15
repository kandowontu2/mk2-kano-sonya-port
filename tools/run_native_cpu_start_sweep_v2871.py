"""Fresh natural tower choices from real coin/start timing, not CPU state.

The previous confirmation-age sweep always drew Baraka. V2870's unwrapped
control drew the same Baraka order, so the extra whole-guest observer did not
change that choice. These fixtures change only the ordinary input start time.
All evidence remains diagnostic until the original CPU contract accepts it.
"""
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT = assembly.ROOT
OUT = ROOT / 'audit_v2872_native_cpu_start_dispatch'
CASES = [(player, boot) for boot in (605, 610, 650, 900) for player in ('kano', 'sonya')]
PWSH = r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'


def run(case):
    player, boot = case
    name = f'audit_v2873_native_cpu_human_{player}_boot{boot}'
    command = [PWSH, '-NoProfile', '-File', str(ROOT / 'tools/run_native_physical_p2_cpu_v2863.ps1'),
               '-CaseName', name, '-Player', player, '-BootFrame', str(boot), '-ConfirmAge', '264',
               '-Approach', 'guard_until_close', '-Seconds', '95', '-CandidateName', assembly.NAME]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    print(name + ' runner exit=' + str(result.returncode) + ' ' + result.stdout.strip() + ' ' + result.stderr.strip(), flush=True)
    return dict(case=name, player=player, bootFrame=boot, confirmAge=264,
                runnerExit=result.returncode, stdout=result.stdout, stderr=result.stderr)


if __name__ == '__main__':
    assembly.need(not OUT.exists() and all(not (ROOT / f'audit_v2873_native_cpu_human_{p}_boot{b}').exists()
                                          for p, b in CASES), 'Immutable physical start timing captures required')
    OUT.mkdir()
    before = assembly.sha(__file__)
    (OUT / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, CASES))
    assembly.need(assembly.sha(__file__) == before, 'Executed dispatcher never changed')
    report = dict(candidate=assembly.NAME, cases=results, allRunnersTerminal=True,
                  allRunnerExitsZero=all(r['runnerExit'] == 0 for r in results), sourceSHA256=before,
                  CPUChoicesPrescribed=False, naturalCoinStartAndSelectionInputsOnly=True,
                  independentVerificationPending=True, fullPortAcceptance=False)
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['allRunnerExitsZero'] else 1)
