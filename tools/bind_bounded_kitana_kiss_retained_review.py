"""Finite retained inflation sheets: current physical source/pose bridge only."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_kitana_kiss_retained_review_bound'
    assert not out.exists()
    history_path=sync.ROOT/'audit_v6117_current_kitana_scene_checked/report.json'
    history=json.loads(history_path.read_text());assert history['passed']
    pins=history['inputHashes'];results={}
    payload=sync.ROOT/'diagnostic_v5219_current_payload_rom_metadata/roms/mk2ks/mk2ks.mdata'
    assert sync.sha(sync.BUILD/'roms/mk2ks/mk2ks.mdata')==pins[str(payload)]
    for side in (1,2):
        proof_path=sync.ROOT/f'audit_bounded_kitana_kiss_all_actor_census_p{side}_checked/report.json'
        proof=json.loads(proof_path.read_text());assert proof['passed']
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}'
            old=sync.ROOT/f'audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram'
            new=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kitana_kiss_draw_census_runtime'
            png=sync.ROOT/'art_review_inflation_v3923'/f'{fighter}-p{side}-native-inflation-review.png'
            assert sync.sha(png)==pins[str(png)]
            assert sync.sha(old/'run.log')==pins[str(old/'run.log')]
            assert sync.sha(new/'run.log')==proof['results'][key]['logSha256']
            ready=3118 if side==1 else 3054
            counters=[]
            for folder,prefix in [(old,'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE '),(new,'MK2_EFFECT_CENSUS_FIFO ')]:
                counter=collections.Counter()
                with (folder/'run.log').open() as stream:
                    for line in stream:
                        if not line.startswith(prefix):continue
                        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                        age=int(r['frame'])-ready;identity=int(r['id'])
                        if not 1<=age<=276 or identity not in (ident,4):continue
                        if folder==new and r['physical']=='0':continue
                        counter[(age,identity,r['source'],r['pose'])]+=1
                counters.append(counter)
            assert counters[0]==counters[1]
            assert {k[0] for k in counters[1]}==set(range(1,277))
            assert sum(counters[1].values())==(1179 if side==1 else 1180)
            results[key]=dict(reviewPath=str(png),reviewSha256=sync.sha(png),nativeFields=276,
                sourcePoseBoundDraws=sum(counters[1].values()),censusProofSha256=sync.sha(proof_path),
                observations=['Sampled normal, inflation, burst, and native fatality phases reviewed.',
                    'Correct lifebar names and no selector portrait overlays in retained sheets.',
                    'Some inflated arm extents are offscreen at the corner.'])
    report=dict(passed=True,results=results,sourceSync=sync.verify(),
        checkerSha256=sync.sha(Path(__file__)),historicalProofSha256=sync.sha(history_path),
        currentWholeFramebufferEquivalenceAccepted=False,currentPalettePositionBridgeAccepted=False,
        postRemovalCurrentBridgeAccepted=False,subjectiveAllContextsAccepted=False,
        heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:r['sourcePoseBoundDraws'] for k,r in results.items()})))

if __name__=='__main__':main()
