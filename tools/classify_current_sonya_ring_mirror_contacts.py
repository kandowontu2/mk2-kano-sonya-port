"""Existing finite contact outcomes, without inventing projectile ownership."""
import collections
import json
import classify_current_sonya_mirror_damage as previous
import verify_native_source_sync as sync

sync.verify()
source=sync.ROOT/'audit_current_sonya_mirror_ring_spacing_runtime/run.log'
events=previous.classify(source.read_text().splitlines())
assert events
own=[e for e in events if e['slot']==1]
cpu=[e for e in events if e['slot']==2]
assert len(cpu)==10
assert collections.Counter(e['damage'] for e in cpu)=={6:2,22:3,26:5}
checked=json.loads((sync.ROOT/'audit_current_sonya_mirror_ring_spacing_checked/report.json').read_text())
assert checked['nativeRingEntries']==43 and checked['mirrorRoundWins']==[]
report=dict(logSHA256=sync.sha(source),nativeRingEntries=43,
            nativeCPUHealthReductions=cpu,
            humanDamageCounts=dict(collections.Counter(e['damage'] for e in own)),
            cpuDamageCounts=dict(collections.Counter(e['damage'] for e in cpu)),
            exactProjectileOwnershipAtDamageProven=False,
            interpretation='The mirror opponent takes native damage, including three22-point and two6-point reductions consistent with ring hit/chip, plus five26-point reductions. Sampled actor actions cannot establish exact projectile attribution. Activation-only proof is not contact coverage.',
            nextAction='Observe actual projectile contact ownership and airborne CPU attack windows; do not change game collision rules based on this controller losing.',
            newEmulatorRuns=0,fullPortAccepted=False)
out=sync.ROOT/'audit_current_sonya_ring_mirror_contacts'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='nativeCPUHealthReductions'},indent=2))
