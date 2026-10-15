"""Bound the timing/readiness repair to proven ordinary HUMAN107 physical inputs."""
import hashlib
import inspect
import json
import re
import subprocess
from pathlib import Path
import qualify_guard_uppercut_source_v4140 as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT = ROOT / 'audit_v4149_guard_uppercut_ready_source_preflight'


def source_boundary():
    code = inspect.getsource(previous.source_boundary)
    need(code.count('mk2ks_guard_uppercut_campaign_ram_v4134.lua') == 1, 'Unique fresh source path')
    code = code.replace('mk2ks_guard_uppercut_campaign_ram_v4134.lua', 'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua')
    scope = dict(vars(previous))
    exec(compile(code, __file__ + '::original_source_boundary_new_wrapper_only', 'exec'), scope)
    report = scope['source_boundary']()
    old = (ROOT / 'mk2ks_guard_uppercut_campaign_ram_v4134.lua').read_text()
    changes = [
        ('and human.flags&0x18==0', 'and human.flags&(other.roster==18 and 0x18 or 0x1c)==0'),
        ("""     if age<7 then press('Down')end
     if age>=3 and age<7 then
      if gp_move=='leg' then press('Low Punch');press('Block')else press('High Punch')end
     end""", """     if gp_move=='leg' then
      if age<7 then press('Down')end
      if age>=3 and age<7 then press('Low Punch');press('Block')end
     else
      -- Same Down9/HP6..8 physical command as the proven clean HUMAN107 test.
      if age<9 then press('Down')end
      if age>=6 and age<9 then press('High Punch')end
     end""")]
    for a, b in changes:
        need(old.count(a) == 1, 'Unique strict-ready/ordinary-uppercut command repair')
        old = old.replace(a, b)
    need(old == (ROOT / 'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua').read_text(),
         'Only native block-stun readiness and declared physical Down/HP timing change')
    ordinary = (ROOT / 'tools/verify_current_human_uppercut_clean_v2153.py').read_text()
    need("plan=[('Down',0,9),('High_Punch',6,3)]" in ordinary and 'Actual HUMAN uppercut107 action' in ordinary,
         'Use original accepted HUMAN107 physical timing; no CPU106 substitute')
    return report


def main():
    need(not OUT.exists(), 'Fresh immutable timing source proof')
    report = source_boundary()
    folder = ROOT / 'audit_v4138_sonya_guard_uppercut_p2_campaign'
    result = json.loads((folder / 'result.json').read_text())
    failed = json.loads((ROOT / 'audit_v4139_sonya_guard_uppercut_campaign_observed/report.json').read_text())
    need(result['exit_code'] != 0 and failed['passed'] is False, 'Exact intentionally stopped wrong-timing capture retained as false')
    text = (folder / 'run.log').read_text()
    actions = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines()
               if line.startswith('MK2_NAT_CAMPAIGN_GUARD_ACTION ')]
    decisions = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines()
                 if line.startswith('MK2_NAT_CAMPAIGN_GUARD_DECISION ')]
    attempts = sum(r['reason'] == 'uppercut_attempt' for r in decisions)
    need(attempts >= 30 and not any(r['after'] == '263' for r in actions),
         'Actual original action observer confirms intended uppercuts never activated; not a mere elapsed timeout')
    report.update(passed=True, actualPriorBufferedUppercutAttempts=attempts,
                  actualPriorHumanUppercut107Stores=0, stoppedKnownWrongTimingTest=True,
                  highPunchPreparationFields=6, physicalDownHoldFields=9,
                  actualOriginalNativeHumanUppercutObservationRetained=True, runtimeSyntaxProven=False,
                  mirrorSonyaLegStrategyUnchanged=True, campaignClearAccepted=False,
                  inputHashes={str(p.resolve()): sha(p) for p in
                    (Path(__file__), Path(previous.__file__), ROOT / 'mk2ks_guard_uppercut_ready_campaign_ram_v4144.lua',
                     ROOT / 'mk2ks_guard_uppercut_campaign_ram_v4134.lua', ROOT / 'tools/run_sonya_guard_uppercut_ready_campaign_v4145.py',
                     ROOT / 'tools/verify_current_human_uppercut_clean_v2153.py',
                     folder / 'run.log', folder / 'result.json',
                     ROOT / 'audit_v4139_sonya_guard_uppercut_campaign_observed/report.json',
                     ROOT / 'audit_v4141_guard_uppercut_source_preflight/report.json')})
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress before writing evidence')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputHashes'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
