"""Account for every sampled cache component; partial DMA is not sole parity."""
import collections,json,re
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
RX=re.compile(r'(\w+)=([^\s]+)')
def case(boot):
    base=ROOT/f'audit_bounded_native_late_sole_dma_boot{boot}_runtime'
    terminal=json.loads((base/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    parts=collections.defaultdict(dict);draws=collections.defaultdict(dict)
    with (base/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(RX.findall(line))
            if tag in ('MK2_BOUNDED_STANCE_PART','MK2_BOUNDED_SOLE_DMA'):
                key=int(r['frame']),int(r['slot']);part=int(r['part'])
                assert r['id']==('17' if key[1]==1 else ('18' if boot==608 else '3'))
                destination=parts if tag=='MK2_BOUNDED_STANCE_PART' else draws
                assert part not in destination[key],'Duplicate sparse component observation'
                destination[key][part]=r
    assert len(parts)==14 and draws
    inventory=[]
    for key,cache in sorted(parts.items()):
        observed=draws.get(key,{})
        assert set(observed)<=set(cache)
        for part,d in observed.items():
            c=cache[part]
            assert all(c[k]==d[k] for k in ('source','width','height','opaque','top','bottom'))
            assert int(d['opaque_bottom_y'])==(int(d['y'])+int(d['bottom']))&511
            assert d['palette']==('0200' if key[1]==1 else '0300')
        inventory.append(dict(frame=key[0],slot=key[1],id=int(next(iter(cache.values()))['id']),
            action=next(iter(cache.values()))['action'],
            cacheParts=len(cache),matchedDrawParts=len(observed),missingParts=sorted(set(cache)-set(observed)),
            allPartsMatched=set(cache)==set(observed)))
    return dict(boot=boot,terminal=terminal,inventory=inventory,
        matchedBodyCopies=sum(len(v) for v in draws.values()),
        incompleteCharacterFields=sum(not r['allPartsMatched'] for r in inventory),
        logSha256=sync.sha(base/'run.log'))
def main():
    out=ROOT/'audit_bounded_native_sole_dma_coverage_checked';assert not out.exists()
    cases=[case(608),case(604)]
    assert any(c['incompleteCharacterFields'] for c in cases)
    result=dict(passed=True,classification='verified_incomplete_draw_binding',cases=cases,
        paletteFilterRepairActuallyObserved=True,currentStockSoleParityAccepted=False,
        fullGoalComplete=False,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(classification=result['classification'],cases=[dict(boot=c['boot'],copies=c['matchedBodyCopies'],incompleteFields=c['incompleteCharacterFields']) for c in cases])))
if __name__=='__main__':main()
