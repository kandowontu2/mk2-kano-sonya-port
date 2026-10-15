"""Classify newly appearing native stock effects from already earned runs."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_stock_head_remaining_effects_classified';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_stock_head_effect_census_checked/report.json').read_text())
    assert proof['passed'];results={};sequences={}
    for fighter in ('sonya','kano'):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_effect_census_runtime'
        assert sync.sha(folder/'run.log')==proof['results'][fighter]['logSha256']
        actors={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if r['physical']!='0':continue
                actors.setdefault(r['actor'],[]).append(r)
        selected={actor:rows for actor,rows in actors.items() if min(int(r['age']) for r in rows)>1
                  and all(int(r['source'],16)<0x0f600000 for r in rows)}
        assert len(selected)==6
        summary={};by_age=collections.defaultdict(list);sources=set()
        for actor,rows in selected.items():
            ages={int(r['age']) for r in rows};hi=max(ages)
            assert min(ages)==59 and hi in (110,174) and ages==set(range(59,hi+1))
            assert len(rows)==len(ages) and all(r['id']=='0' and r['pose']=='00000000' for r in rows)
            actor_sources={r['source'] for r in rows};sources.update(actor_sources)
            for r in rows:by_age[int(r['age'])].append(r['source'])
            summary[actor]=dict(firstAge=59,lastAge=hi,nativeDrawFields=len(ages),sources=sorted(actor_sources))
        assert sorted(r['nativeDrawFields'] for r in summary.values())==[52,52,52,52,116,116]
        assert len(sources)==36
        sequences[fighter]={age:sorted(values) for age,values in by_age.items()}
        results[fighter]=dict(actors=summary,stockEffectSources=sorted(sources),stockEffectDraws=sum(len(r) for r in selected.values()),
            sourceLogSha256=sync.sha(folder/'run.log'))
    assert sequences['sonya']==sequences['kano']
    report=dict(passed=True,results=results,identicalPerAgeStockSourceMultiset=True,
        sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        renderedEffectPixelsAccepted=False,stockGoreSemanticLabelsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actorsPerCase=6,stockSourcesPerCase=36,drawsPerCase=440,identicalPerAgeStockSourceMultiset=True)))

if __name__=='__main__':main()
