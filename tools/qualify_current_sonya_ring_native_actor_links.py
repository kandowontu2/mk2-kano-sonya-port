"""True mirror projectile creator/target pointers at birth and native damage."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync


def gate(links):
    damages=[]
    for row in links:
        creator=next(slot for slot in ('1','2') if row['creator']==row['p'+slot+'_actor'])
        target='2' if creator=='1' else '1'
        assert row['target_actor']==row['p'+target+'_actor']
        assert row['target_main']==row['p'+target+'_main']
        assert row['object'] not in (row['p1_actor'],row['p2_actor'])
        if row['phase']=='damage':
            assert row['slot']==target
            damages.append((int(row['frame']),creator,target,int(row['before'])-int(row['after'])))
    assert damages==[(17241,'1','2',6),(17980,'2','1',22),(18400,'1','2',22)]
    return damages


sync.verify()
folder=sync.ROOT/'audit_current_sonya_ring_native_actor_links_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_ring_native_actor_links_preparation/campaign.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_sonya_mirror_ring_hit_owner_runtime/run.log')
for tag in set(rows)|set(old):
    if tag=='RING_NATIVE_LINKS':continue
    assert rows.get(tag,[])==old.get(tag,[])
links=rows['RING_NATIVE_LINKS'];damages=gate(links)
bad=copy.deepcopy(links)
next(r for r in bad if r['phase']=='damage')['creator']=next(r for r in bad if r['phase']=='damage')['target_actor']
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Self-targeting projectile mutation accepted')
report=dict(passedNativeCreatorTargetLinks=True,records=len(links),damageContacts=damages,
            unchangedOrdinaryAndEarlierObserverRecords=True,selfTargetMutationRejected=True,
            observedPlayerHitWasCPUCreatedRing=True,reflectionObserved=False,
            logSHA256=sync.sha(folder/'run.log'),
            scope='Observed mirror ring births and three damage contacts only. No universal projectile ownership/reflect/secret/arena certification.',
            fullPortAccepted=False)
out=sync.ROOT/'audit_current_sonya_ring_native_actor_links_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
