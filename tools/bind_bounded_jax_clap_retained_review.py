"""Finite retained P1 art review, exact current body source/pose trace bridge."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_clap_retained_review_bound';assert not out.exists()
    historical_path=sync.ROOT/'audit_v6138_current_jax_clap_scene_checked/report.json'
    historical=json.loads(historical_path.read_text());assert historical['passed']
    pins=historical['inputHashes']
    current_path=sync.ROOT/'audit_bounded_jax_clap_draw_census_checked/report.json'
    current=json.loads(current_path.read_text());assert current['passed'];results={}
    payload=sync.BUILD/'roms/mk2ks/mk2ks.mdata'
    old_payload=sync.ROOT/'diagnostic_v5219_current_payload_rom_metadata/roms/mk2ks/mk2ks.mdata'
    assert sync.sha(payload)==pins[str(old_payload)]=='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'
    for fighter,ident in (('sonya',18),('kano',17)):
        old=sync.ROOT/f'audit_v6135_current_jax_clap_{fighter}_p1_native_scene_ram'
        new=sync.ROOT/f'audit_bounded_{fighter}_jax_clap_draw_census_runtime'
        png=old/'review'/f'{fighter}-p1-native-clap-review.png'
        assert sync.sha(png)==pins[str(png)] and sync.sha(old/'run.log')==pins[str(old/'run.log')]
        assert sync.sha(new/'run.log')==current['results'][fighter]['logSha256']
        counters=[]
        for folder,prefix in ((old,'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE '),(new,'MK2_EFFECT_CENSUS_FIFO ')):
            counter=collections.Counter()
            with (folder/'run.log').open() as stream:
                for line in stream:
                    if not line.startswith(prefix):continue
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(r['frame'])
                    if not 3127<=frame<=3314 or int(r['id']) not in (ident,11):continue
                    if folder==new and r['physical']=='0':continue
                    counter[(frame,int(r['id']),r['source'],r['pose'])]+=1
            counters.append(counter)
        assert counters[0]==counters[1]
        assert {key[0] for key in counters[1]}==set(range(3127,3315))
        results[fighter]=dict(reviewPath=str(png),reviewSha256=sync.sha(png),nativeBodyDraws=sum(counters[1].values()),
            exactCurrentBodySourcePoseFields=188,oldWholeGuestSha256=json.loads((old/'result.json').read_text())['ramGuestSHA256'],
            visualObservations=['Headless body remains visible during blood/debris phase.',
                'Body collapses through kneeling to prone pose beneath the winner.',
                'Names remain Kano/Sonya in reviewed lifebar panels; no selector portraits overlay the arena.'])
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        historicalProofSha256=sync.sha(historical_path),currentCensusProofSha256=sync.sha(current_path),
        currentWholeFramebufferEquivalenceAccepted=False,currentPaletteAndPositionBridgeAccepted=False,
        subjectiveAllContextsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
