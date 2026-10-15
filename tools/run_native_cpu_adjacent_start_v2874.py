"""Natural adjacent coin/start timings; no prescribed CPU or ladder state.

V2871 reached Kano and Scorpion through actual normal start timings. This
bounded sweep covers the remaining adjacent physical timings 606..609.
Only independent whole-guest/role/phase/cleanup checks can accept a fixture.
"""
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT = assembly.ROOT
OUT = ROOT / 'audit_v2875_native_cpu_adjacent_start_dispatch'
CASES = [(player, boot) for boot in (606, 607, 608, 609) for player in ('kano', 'sonya')]
PWSH = r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'


def run(case):
    player, boot = case
    name = f'audit_v2876_native_cpu_human_{player}_boot{boot}'
    command = [PWSH, '-NoProfile', '-File', str(ROOT / 'tools/run_native_physical_p2_cpu_v2863.ps1'),
               '-CaseName', name, '-Player', player, '-BootFrame', str(boot), '-ConfirmAge', '264',
               '-Approach', 'guard_until_close', '-Seconds', '95', '-CandidateName', assembly.NAME]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    print(name + ' runner exit=' + str(result.returncode) + ' ' + result.stdout.strip() + ' ' + result.stderr.strip(), flush=True)
    return dict(case=name, player=player, bootFrame=boot, confirmAge=264,
                runnerExit=result.returncode, stdout=result.stdout, stderr=result.stderr)


if __name__ == '__main__':
    assembly.need(not OUT.exists() and all(not (ROOT / f'audit_v2876_native_cpu_human_{p}_boot{b}').exists()
                                          for p, b in CASES), 'Immutable adjacent physical start timing captures required')
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
