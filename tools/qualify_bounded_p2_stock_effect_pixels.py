"""P2 native stock-effect census, duplicate DMA and full source footprints."""
import collections,json,re
from pathlib import Path
from qualify_bounded_p2_stock_head_body_pixels import driver
from qualify_bounded_stock_head_finisher import gate as control_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def fifo_at(folder,sources):
    result=collections.Counter()
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if r['physical']!='0' or r['source'] not in sources:continue
            size=int(r['size'],16);xy=int(r['xy'],16)
            result[(int(r['frame']),r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
    return result

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_effect_pixels_checked';assert not out.exists();results={}
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_native_census_checked/report.json').read_text())
    source_proof=json.loads((sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified/report.json').read_text())
    assert proof['passed'] and source_proof['passed']
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_effect_pixels_runtime'
        census=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_effect_census_runtime'
        assert sync.sha(census/'run.log')==proof['results'][fighter]['logHashes']['effect_census']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        states=driver(folder,fighter);assert states==driver(census,fighter)
        control=control_gate(states,fighter,ident);ready=control['nativeActionFrame']
        sources=set(source_proof['results'][fighter]['stockEffectSources'])
        expected=fifo_at(census,sources);assert fifo_at(folder,sources)==expected
        assert sum(expected.values())==438 and len(expected)==219 and all(n==2 for n in expected.values())
        dma=collections.Counter()
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_MAPPING_DMA '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['pc']=='FF804640'
                dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
        groups=summaries_at(folder);opaque=[r for r in groups['IDLE_OPAQUE'] if 1<=int(r['frame'])-ready<=174]
        actual=collections.Counter((int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in opaque)
        assert expected==dma==actual
        summaries=groups['COMPLETE_FOOTPRINT'];expected_frames={key[0] for key in expected}
        assert len(summaries)==len(expected_frames)==115 and {int(r['frame'])-1 for r in summaries}==expected_frames
        for r in summaries:
            frame=int(r['frame'])-1
            assert r['source_fail']==r['display_fail']=='0' and int(r['source_age'])==frame-ready
            assert int(r['points'])==int(r['slot1'])==sum(int(x['opaque']) for x in opaque if int(x['frame'])==frame)>0 and r['slot2']=='0'
            assert 0<=int(r['offscreen'])<=int(r['points'])
        total=sum(int(r['points']) for r in summaries);cropped=sum(int(r['offscreen']) for r in summaries)
        results[fighter]=dict(nativeEffectDraws=438,nativeDrawFields=115,opaqueComponentPixels=total,
            visibleComponentPixels=total-cropped,croppedComponentPixels=cropped,independentFifoAndDmaCoverage=True,
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        subjectiveArtAccepted=False,heardAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
