"""Actual native ring-child damage linkage, not inferred shooter ownership."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_ring_hit_owner_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_sonya_mirror_ring_spacing_runtime/run.log')
assert rows['RESULT'][0]['frame']=='18500'
for tag in set(old)|set(rows):
    if tag in ('RING_CHILD','HIT_OWNER','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in old.get(tag,[]) if int(r['frame'])<18500]==[r for r in rows.get(tag,[]) if int(r['frame'])<18500]
linked=[]
for hit in rows['HIT_OWNER']:
    if hit['slot']!='2' or hit['ring_born']=='-1':continue
    child=next(r for r in rows['RING_CHILD'] if r['frame']==hit['ring_born'] and r['main']==hit['a13'])
    assert child['actor']==child['owner']==hit['a8']==hit['ring_actor']
    assert child['actor_id']=='18' and child['actor'] not in (hit['p1_actor'],hit['p2_actor'])
    assert 0<=int(hit['frame'])-int(child['frame'])<160
    health=next(r for r in rows['HEALTH'] if r['frame']==hit['frame'] and r['slot']=='2' and r['pc']=='FF836700')
    assert health['before']==hit['before'] and health['after']==hit['after'] and health['a8']==hit['a8'] and health['a13']==hit['a13']
    linked.append(dict(frame=int(hit['frame']),damage=int(hit['before'])-int(hit['after']),child=child,health=health))
assert [(r['frame'],r['damage']) for r in linked]==[(17241,6),(18400,22)]
report=dict(passedNativeRingChildDamageLinkage=True,contacts=linked,
            ordinaryRouteExactThrough=18499,logSHA256=sync.sha(folder/'run.log'),
            shooterSideAttributionProven=False,
            scope='Two actual ring-child contacts reduce CPU mirror health via native damage writer:6chip/22hit. Main+290 is not used to infer shooter side; other/reflected projectile ownership remains open.',
            fullPortAccepted=False)
out=sync.ROOT/'audit_current_sonya_mirror_ring_hit_owner_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print('PASS: native ring child linked to CPU mirror damage6/22; unchanged ordinary route through18499')
