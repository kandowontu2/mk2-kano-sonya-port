"""Full follow-through split descriptors and each actual native palette event."""
import collections,copy,json,re
from pathlib import Path
from qualify_bounded_kung_lao_split_draw_census import states
from qualify_bounded_kung_lao_split_descriptors import gate as descriptor_gate
import verify_native_source_sync as sync

def load(folder):
    fifo=[];palettes=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith('MK2_EFFECT_CENSUS_FIFO '):fifo.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
            elif line.startswith('MK2_SPLIT_PALETTE '):palettes.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return fifo,palettes

def palette_gate(draws,palettes,ident,side):
    assert collections.Counter((r['frame'],r['source']) for r in draws)==collections.Counter((r['frame'],r['source']) for r in palettes)
    assert palettes and all(r['writes']=='0' and r['assistance']=='none' for r in palettes)
    assert all(r['dma_bank']==r['victim_bank'] and int(r['victim_id'])==ident and r['victim_actor']==('01034E90' if side==1 else '010350A0') for r in palettes)
    return dict(paletteMatchedDraws=len(palettes),actualPaletteBanks=sorted({r['dma_bank'] for r in palettes}))

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_followthrough_palette_checked';assert not out.exists()
    descriptor_path=sync.ROOT/'audit_bounded_kung_lao_split_descriptors_checked/report.json'
    desc=json.loads(descriptor_path.read_text());assert desc['passed']
    census_path=sync.ROOT/'audit_bounded_kung_lao_split_draw_census_checked/report.json'
    census=json.loads(census_path.read_text());assert census['passed'];results={}
    all_sources={r['source'] for rows in desc['descriptors'].values() for r in rows}
    for side in (1,2):
        for fighter,ident in [('sonya',18),('kano',17)]:
            key=f'{fighter}P{side}';folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_followthrough_palette_runtime'
            base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_draw_census_runtime'
            assert sync.sha(base/'run.log')==census['results'][key]['logSha256']
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            assert states(folder,fighter,side)==states(base,fighter,side)
            fifo,palettes=load(folder);old,_=load(base)
            assert collections.Counter(tuple(sorted(r.items())) for r in fifo if int(r['age'])<=179)==collections.Counter(tuple(sorted(r.items())) for r in old)
            assert {int(r['age']) for r in fifo}==set(range(1,299))
            draws=[r for r in fifo if r['source'] in all_sources]
            specs={r['source']:r for r in desc['descriptors'][str(ident)]}
            accepted=descriptor_gate(draws,ident,specs,side)
            assert {r['source'] for r in draws}==set(specs)
            assert set(accepted['detachedPartSources'])=={r['source'] for r in desc['descriptors'][str(ident)] if int(r['index'])>=3}
            palette=palette_gate(draws,palettes,ident,side);faults=[]
            for label in ('wrong_bank','missing_palette_event','foreign_victim_id'):
                bad=copy.deepcopy(palettes)
                if label=='wrong_bank':bad[0]['dma_bank']='7F00'
                elif label=='missing_palette_event':bad.pop(0)
                else:bad[0]['victim_id']='0'
                try:palette_gate(draws,bad,ident,side)
                except AssertionError:faults.append(label)
                else:raise AssertionError('Palette fault accepted')
            results[key]=dict(**accepted,**palette,allSixSplitSourcesObserved=True,allThreeDetachedSourcesObserved=True,
                observedDrawFields=298,nativeTerminalAge=299,originalControlUnchanged=True,first179FieldInventoryUnchanged=True,
                rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        descriptorProofSha256=sync.sha(descriptor_path),censusProofSha256=sync.sha(census_path),
        renderedPixelsAccepted=False,paletteRGBContentsVerified=False,semanticArtworkAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:{a:r[a] for a in ('customDraws','detachedPartDraws','paletteMatchedDraws','actualPaletteBanks')} for k,r in results.items()})))

if __name__=='__main__':main()
