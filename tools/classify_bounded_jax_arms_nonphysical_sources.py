"""Classify current custom-source prop candidates versus stock effect sources."""
import json
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_arms_nonphysical_sources';assert not out.exists()
    path=sync.ROOT/'audit_bounded_jax_arms_draw_census_checked/report.json'
    proof=json.loads(path.read_text());assert proof['passed'];results={}
    for key,case in proof['results'].items():
        custom={};stock={}
        for actor,value in case['newNonphysicalActors'].items():
            sources=[int(s,16) for s in value['sources']]
            assert value['ids']==['0']
            if all(0x0f000000<=s<0x10000000 for s in sources):custom[actor]=value
            else:
                assert all(0x04000000<=s<0x05000000 for s in sources);stock[actor]=value
        assert len(custom)==2
        first=list(custom.values())[0];second=list(custom.values())[1]
        assert first['sources']==second['sources'] and len(first['sources'])==5
        assert first['firstAge']==second['firstAge'] and first['lastAge']==second['lastAge']==147
        assert first['fields']==second['fields']==148-first['firstAge']
        assert first['draws']==second['draws']==first['fields']
        results[key]=dict(customSourcePropCandidates=custom,stockEffectActors=stock,
            customDraws=sum(a['draws'] for a in custom.values()),stockEffectDraws=sum(a['draws'] for a in stock.values()))
    assert results['sonyaP1']['customSourcePropCandidates'].values()!=results['kanoP1']['customSourcePropCandidates'].values()
    report=dict(passed=True,results=results,censusProofSha256=sync.sha(path),checkerSha256=sync.sha(Path(__file__)),
        sourceSync=sync.verify(),descriptorPaletteOwnershipVerified=False,semanticArmArtworkVerified=False,renderedPixelsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={key:dict(customActors=len(r['customSourcePropCandidates']),customDraws=r['customDraws'],stockEffectDraws=r['stockEffectDraws']) for key,r in results.items()})))

if __name__=='__main__':main()
