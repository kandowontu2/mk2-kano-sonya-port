"""Head coverage boundary derived from independent all-actor native FIFO."""
import collections,json,re
from pathlib import Path
from qualify_bounded_p2_stock_head_body_pixels import driver
from qualify_bounded_stock_head_finisher import gate as control_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_head_native_census_checked';assert not out.exists()
    prior=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_control_checked/report.json').read_text())
    assert prior['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        baseline=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==prior['results'][fighter]['logSha256']
        folders={kind:sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_{kind}_runtime' for kind in ('effect_census','head_pixels')}
        terminals={}
        for kind,folder in folders.items():
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            states=driver(folder,fighter);assert states==driver(baseline,fighter)
            control=control_gate(states,fighter,ident);terminals[kind]=t
        ready=control['nativeActionFrame'];heads=[];allfields=set()
        with (folders['effect_census']/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));allfields.add(int(r['age']))
                if r['physical']=='0' and 0x0f600000<=int(r['source'],16)<0x10000000:
                    assert int(r['id'])==ident and r['pose']=='00000000';heads.append(r)
        assert allfields==set(range(1,175)) and len(heads)==115
        assert {int(r['age']) for r in heads}==set(range(60,175)) and len({r['actor'] for r in heads})==1
        expected=collections.Counter()
        for r in heads:
            size=int(r['size'],16);xy=int(r['xy'],16)
            expected[(int(r['frame']),r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
        groups=summaries_at(folders['head_pixels']);opaque=[r for r in groups['IDLE_OPAQUE'] if 1<=int(r['frame'])-ready<=174]
        actual=collections.Counter((int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in opaque)
        assert actual==expected and len({r['source'] for r in opaque})==7
        summaries=groups['COMPLETE_FOOTPRINT'];assert len(summaries)==115
        assert {int(r['frame'])-1-ready for r in summaries}=={int(r['age']) for r in heads}
        for r in summaries:
            frame=int(r['frame'])-1
            assert r['source_fail']==r['display_fail']=='0' and int(r['source_age'])==frame-ready
            assert int(r['points'])==int(r['slot1'])==sum(int(x['opaque']) for x in opaque if int(x['frame'])==frame)>0 and r['slot2']=='0'
            assert 0<=int(r['offscreen'])<=int(r['points'])
        total=sum(int(r['points']) for r in summaries);cropped=sum(int(r['offscreen']) for r in summaries)
        results[fighter]=dict(nativeFirstHeadAge=60,nativeHeadDrawFields=115,allSevenSourcesObserved=True,
            opaqueComponentPixels=total,visibleComponentPixels=total-cropped,croppedComponentPixels=cropped,
            exactIndependentFifoCoverage=True,terminals=terminals,
            logHashes={kind:sync.sha(folder/'run.log') for kind,folder in folders.items()})
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        stockEffectsAccepted=False,subjectiveArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
