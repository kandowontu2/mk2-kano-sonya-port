"""Original physical fixtures for seven changed blade addresses on both builds.

Two completed pilots are retained, not rerun. Twelve remaining fresh cases use
the same read-only allocation observer and unchanged original physical drivers.
"""
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_friendship_palette_assembly_v2750 as assembly

ROOT = assembly.ROOT
OUT = ROOT / 'audit_v2897_blade_allocation_dispatch'
FIXTURES = [('interrupt', 1, 'sonya'), ('interrupt', 2, 'sonya'), ('ko', 1, 'kano'),
            ('ko', 1, 'sonya'), ('ko', 2, 'kano'), ('ko', 2, 'sonya'), ('ko', 2, 'kitana')]
BUILDS = {'new': assembly.NAME, 'old': assembly.prior.NAME}
PWSH = r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'


def leaf(build, kind, side, victim):
    if (kind, side, victim) == FIXTURES[0]:
        return f'audit_v{2894 if build == "new" else 2895}_blade_allocation_pilot_{build}'
    return f'audit_v2898_blade_allocation_{build}_{kind}_p{side}_{victim}'


def run(case):
    build, kind, side, victim = case
    name = leaf(*case)
    command = [PWSH, '-NoProfile', '-File', str(ROOT/'tools/run_blade_allocation_v2893.ps1'),
               '-CaseName', name, '-Kind', kind, '-Move', 'blade', '-Side', str(side),
               '-Victim', victim, '-CandidateName', BUILDS[build]]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    print(name+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(), flush=True)
    return dict(case=name, build=build, kind=kind, side=side, victim=victim,
                runnerExit=result.returncode, stdout=result.stdout, stderr=result.stderr)


if __name__ == '__main__':
    cases = [(build, *fixture) for fixture in FIXTURES[1:] for build in BUILDS]
    assembly.need(not OUT.exists() and all(not (ROOT/leaf(*case)).exists() for case in cases), 'Immutable new blade allocation captures')
    pilots = []
    for build in BUILDS:
        name = leaf(build, *FIXTURES[0])
        result = json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))
        assembly.need(result['observer_passed'] and result['exit_code'] == 0 and result['candidate'] == BUILDS[build] and
                      (result['kind'], result['move'], result['side'], result['victim']) == ('interrupt', 'blade', 1, 'sonya'),
                      'Actual completed pilots retained without rerunning')
        pilots.append(dict(case=name, build=build, kind='interrupt', side=1, victim='sonya', runnerExit=0, alreadyTerminalPilot=True))
    OUT.mkdir()
    before = assembly.sha(__file__)
    (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = pilots + list(pool.map(run, cases))
    assembly.need(assembly.sha(__file__) == before, 'Executed dispatcher never changed')
    report = dict(cases=results, allRunnersTerminal=True, allRunnerExitsZero=all(r['runnerExit'] == 0 for r in results),
                  sourceSHA256=before, bothActualBuilds=BUILDS, inputStrategiesUnchanged=True,
                  noGuestStateOrRNGInjection=True, independentVerificationPending=True, fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    raise SystemExit(0 if report['allRunnerExitsZero'] else 1)
