"""Inspected finite retained sheets bound to current body/prop source-pose draws."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_arms_retained_review_bound';assert not out.exists()
    history_path=sync.ROOT/'audit_v6145_current_jax_arms_scene_checked/report.json'
    history=json.loads(history_path.read_text());assert history['passed'];pins=history['inputHashes']
    census_path=sync.ROOT/'audit_bounded_jax_arms_draw_census_checked/report.json'
    current=json.loads(census_path.read_text());assert current['passed']
    props=json.loads((sync.ROOT/'audit_bounded_jax_arm_descriptors_checked/report.json').read_text());assert props['passed']
    old_payload=sync.ROOT/'diagnostic_v5219_current_payload_rom_metadata/roms/mk2ks/mk2ks.mdata'
    assert sync.sha(sync.BUILD/'roms/mk2ks/mk2ks.mdata')==pins[str(old_payload)]
    results={}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';old=sync.ROOT/f'audit_v6142_current_jax_arms_{fighter}_p{side}_native_scene_ram'
            new=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime'
            png=old/'review'/f'{fighter}-p{side}-native-arms-review.png'
            assert sync.sha(png)==pins[str(png)] and sync.sha(old/'run.log')==pins[str(old/'run.log')]
            assert sync.sha(new/'run.log')==current['results'][key]['logSha256']
            ready=3121 if side==1 else 3132;custom=set(props['results'][key]['fiveDescriptorSources']);counters=[]
            for folder,prefix in [(old,'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE '),(new,'MK2_EFFECT_CENSUS_FIFO ')]:
                counter=collections.Counter()
                with (folder/'run.log').open() as stream:
                    for line in stream:
                        if not line.startswith(prefix):continue
                        r=dict(re.findall(r'(\w+)=([^\s]+)',line));age=int(r['frame'])-ready
                        if not 1<=age<=147:continue
                        identity=int(r['id'])
                        if identity not in (ident,11) and not(identity==0 and r['source'] in custom):continue
                        if folder==new and identity in (ident,11) and r['physical']=='0':continue
                        counter[(age,identity,r['source'],r['pose'])]+=1
                counters.append(counter)
            assert counters[0]==counters[1] and {k[0] for k in counters[1]}==set(range(1,148))
            assert sum(n for k,n in counters[1].items() if k[1]==0)==118
            results[key]=dict(reviewPath=str(png),reviewSha256=sync.sha(png),sourcePoseBoundDraws=sum(counters[1].values()),nativeFields=147,
                observations=['Arm pull and two detached-arm props are visible in sampled phases.','Blood and native win/fatality display are visible.','Correct lifebar name; no selector portrait overlay.','Victim partly offscreen in several panels; all-art and corner parity remain unproven.'])
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),historicalProofSha256=sync.sha(history_path),censusProofSha256=sync.sha(census_path),currentWholeFramebufferEquivalenceAccepted=False,currentPalettePositionBridgeAccepted=False,subjectiveAllContextsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:dict(nativeFields=r['nativeFields'],sourcePoseBoundDraws=r['sourcePoseBoundDraws']) for k,r in results.items()})))

if __name__=='__main__':main()
