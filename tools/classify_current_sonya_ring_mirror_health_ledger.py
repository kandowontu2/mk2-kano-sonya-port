"""Exact native health ledger; do not depend on stale 30-field pose samples."""
import collections
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

sync.verify()
source=sync.ROOT/'audit_current_sonya_mirror_ring_spacing_runtime/run.log'
rows=chronology.load(source)
cutoff=int(next(r for r in rows['FIGHT'] if r['stage']=='5')['frame'])
fights=[r for r in rows['FIGHT'] if int(r['frame'])>=cutoff]
assert fights and all(r['stage']=='5' and r['human']==r['cpu']=='18:18' for r in fights)
assert all(r['stage']=='5' for r in rows['STATE'] if int(r['frame'])>=cutoff)
events=[r for r in rows['HEALTH'] if int(r['frame'])>=cutoff
        and r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161]
counts={slot:collections.Counter(int(r['before'])-int(r['after']) for r in events if r['slot']==slot) for slot in ('1','2')}
assert counts['2']=={6:2,22:3,26:5}
checked=json.loads((sync.ROOT/'audit_current_sonya_mirror_ring_spacing_checked/report.json').read_text())
assert checked['logSHA256']==sync.sha(source) and checked['nativeRingEntries']==43
report=dict(nativeRingEntries=43,nativeDamageCountsBySlot=counts,
            nativeCPUHealthReductions=[r for r in events if r['slot']=='2'],
            logSHA256=sync.sha(source),allObservedMirrorFightsTrueIDs=True,
            exactProjectileAttributionProven=False,mirrorRoundWins=checked['mirrorRoundWins'],
            limitation='Three22-point and two6-point reductions are consistent with ring damage/chip, not proof of exact projectile ownership. Five26-point reductions are also present. No stale pose sample is used to identify a hit.',
            nextAction='Passive hit-time projectile/CPU airborne-window observation; no collision-rule edits warranted yet.',
            newEmulatorRuns=0,fullPortAccepted=False)
out=sync.ROOT/'audit_current_sonya_ring_mirror_health_ledger'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='nativeCPUHealthReductions'},indent=2))
