"""Clarify censored runtime extent without rewriting executed predecessor evidence."""
import json
import verify_native_source_sync as sync
sync.verify()
source=sync.ROOT/'audit_current_sonya_p2_kitana_projectile_guard_v2_checked/report.json'
out=sync.ROOT/'audit_current_sonya_p2_kitana_projectile_guard_partial_scope';assert not out.exists()
r=json.loads(source.read_text());assert r['targetPolicyUntested'] and not r['entire104518PrefixVerified'] and r['earlierNativePhysicalPrefixVerifiedThrough']==89040
report=dict(passedFiniteRuntimeChronology=True,runtimeExactNativeAndPhysicalPrefixThrough=89040,
            intended104518RuntimePrefixObserved=False,intended104518SourceConservationOnly=True,
            targetKitanaPolicyUntested=True,fullPortAcceptance=False,
            clarification='Predecessor scope sentence mentioning104518 describes the intended gate, not observed runtime coverage. Runtime was wall-censored at89040 before the target encounter. Neither success nor failure of the Kitana guard policy was tested; no strategy-result/game-defect claim.',
            predecessorSHA256=sync.sha(source),predecessorRewritten=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
