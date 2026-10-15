"""Kano contemporaneous stock-effect FIFO/DMA/pixel proof."""
import collections,json,re
from pathlib import Path
import qualify_bounded_stock_head_body_footprints_driver as driver
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    folder=sync.ROOT/'audit_bounded_kano_stock_effect_duplicate_queue_runtime'
    out=sync.ROOT/'audit_bounded_kano_stock_effect_duplicate_queue_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    baseline=sync.ROOT/'audit_bounded_kano_stock_head_finisher_runtime'
    prior=json.loads((sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json').read_text())
    assert prior['passed'] and sync.sha(baseline/'run.log')==prior['results']['kano']['logSha256']
    rows=driver.driver_states(folder,'kano');assert rows==driver.driver_states(baseline,'kano')
    control=driver.scoped.original.state_gate(rows,'kano',17);ready=control['nativeActionFrame']
    classified=json.loads((sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified/report.json').read_text())
    assert classified['passed'];sources=set(classified['results']['kano']['stockEffectSources'])
    fifo=collections.Counter();dma=collections.Counter()
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_EFFECT_CENSUS_FIFO ') and r['physical']=='0' and r['source'] in sources:
                size=int(r['size'],16);xy=int(r['xy'],16)
                fifo[(int(r['frame']),r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
            elif line.startswith('MK2_EFFECT_MAPPING_DMA '):
                assert r['pc']=='FF804640'
                dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
    assert fifo==dma and sum(dma.values())==440 and all(n==2 for n in dma.values())
    groups=summaries_at(folder)
    opaque=[r for r in groups['IDLE_OPAQUE'] if 59<=int(r['frame'])-ready<=174]
    actual=collections.Counter((int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in opaque)
    assert actual==dma
    summaries=groups['COMPLETE_FOOTPRINT'];assert len(summaries)==116
    assert {int(r['frame'])-1-ready for r in summaries}==set(range(59,175))
    for r in summaries:
        frame=int(r['frame'])-1
        assert r['source_fail']==r['display_fail']=='0' and int(r['source_age'])==frame-ready
        assert int(r['points'])==int(r['slot1'])==sum(int(x['opaque']) for x in opaque if int(x['frame'])==frame)>0
        assert r['slot2']=='0' and 0<=int(r['offscreen'])<=int(r['points'])
    report=dict(passed=True,nativeEffectDraws=440,uniqueDrawKeys=220,duplicateMultiplicity=2,nativeDrawFields=116,
        opaqueComponentPixels=sum(int(r['points']) for r in summaries),croppedComponentPixels=sum(int(r['offscreen']) for r in summaries),
        terminal=terminal,logSha256=sync.sha(folder/'run.log'),checkerSha256=sync.sha(Path(__file__)),sourceSync=sync.verify(),
        subjectiveArtAccepted=False,fullFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','nativeEffectDraws','uniqueDrawKeys','nativeDrawFields','opaqueComponentPixels','croppedComponentPixels')}))

if __name__=='__main__':main()
