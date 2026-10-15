"""Reviewed retained ten-phase sheets, full current body/part source-pose bridge."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_retained_review_bound';assert not out.exists()
    history_path=sync.ROOT/'audit_v6131_current_kung_lao_scene_checked/report.json'
    history=json.loads(history_path.read_text());assert history['passed'];pins=history['inputHashes']
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_all_descriptors_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed']
    payload=sync.ROOT/'diagnostic_v5219_current_payload_rom_metadata/roms/mk2ks/mk2ks.mdata'
    assert sync.sha(sync.BUILD/'roms/mk2ks/mk2ks.mdata')==pins[str(payload)]
    results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';old=sync.ROOT/f'audit_v6126_current_kung_lao_{fighter}_p{side}_native_scene_ram'
            new=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_followthrough_palette_runtime'
            png=old/'review'/f'{fighter}-p{side}-native-split-review.png'
            assert sync.sha(png)==pins[str(png)] and sync.sha(old/'run.log')==pins[str(old/'run.log')]
            assert sync.sha(new/'run.log')==proof['results'][key]['censusLogSha256']
            ready=3096 if side==1 else 3059;winner='010350A0' if side==1 else '01034E90';counters=[]
            for folder,prefix in [(old,'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE '),(new,'MK2_EFFECT_CENSUS_FIFO ')]:
                counter=collections.Counter()
                with (folder/'run.log').open() as stream:
                    for line in stream:
                        if not line.startswith(prefix):continue
                        r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['frame'])-ready;identity=int(r['id'])
                        if not 1<=age<=298:continue
                        if identity!=ident and not(identity==0 and r['actor']==winner):continue
                        counter[(age,identity,r['source'],r['pose'])]+=1
                counters.append(counter)
            assert counters[0]==counters[1] and {k[0] for k in counters[1]}==set(range(1,299))
            results[key]=dict(reviewPath=str(png),reviewSha256=sync.sha(png),nativeFields=298,sourcePoseBoundDraws=sum(counters[1].values()),
                observations=['Ten sampled split poses: standing injury, opening halves, fall and prone.',
                    'Native blood, hat/winner/fatality display; correct lifebar names and no selector overlay.',
                    'Some corner corpse portions offscreen; no universal art acceptance.'])
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        historicalProofSha256=sync.sha(history_path),descriptorProofSha256=sync.sha(proof_path),
        currentWholeFramebufferEquivalenceAccepted=False,currentPalettePositionBridgeAccepted=False,
        subjectiveAllContextsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:r['sourcePoseBoundDraws'] for k,r in results.items()})))

if __name__=='__main__':main()
