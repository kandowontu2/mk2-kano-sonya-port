"""Source-bound arm FIFO/DMA/palette-bank/fullsource/presentation pixel proof."""
import collections,copy,inspect,json,re,sys
from pathlib import Path
import qualify_bounded_jax_clap_effect_pixels as previous
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

source=inspect.getsource(previous.coverage_gate).replace('188','147')
namespace=dict(previous.__dict__);exec(compile(source,__file__+'::147_fields','exec'),namespace)
coverage_gate=namespace['coverage_gate']

def main(side):
    assert side in (1,2)
    out=sync.ROOT/f'audit_bounded_jax_arm_prop_pixels_p{side}_checked';assert not out.exists();results={}
    proof=json.loads((sync.ROOT/'audit_bounded_jax_arm_descriptors_checked/report.json').read_text());assert proof['passed']
    for fighter,ident in [('sonya',18),('kano',17)]:
        key=f'{fighter}P{side}';sources=set(proof['results'][key]['fiveDescriptorSources'])
        census=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_draw_census_runtime'
        assert sync.sha(census/'run.log')==proof['results'][key]['censusLogSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arm_prop_pixels_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        old=states(census,fighter,side);tags={tag for tag,r in old}
        assert [row for row in states(folder,fighter,side) if row[0] in tags]==old
        ready=int(next(r for tag,r in old if tag=='ACTION')['frame'])
        expected=previous.fifo_at(census,sources);assert sum(expected.values())==118 and previous.fifo_at(folder,sources)==expected
        dma=collections.Counter();palettes=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if line.startswith('MK2_CLAP_EFFECT_DMA '):
                    assert r['pc']=='FF804640'
                    dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
                elif line.startswith('MK2_ARM_PROP_PALETTE '):palettes.append(r)
        assert dma==expected and len(palettes)==118
        assert collections.Counter((int(r['frame']),r['source']) for r in palettes)==collections.Counter({pair:sum(n for key,n in expected.items() if key[:2]==pair) for pair in {key[:2] for key in expected}})
        assert all(r['dma_bank']==r['victim_bank'] and int(r['victim_id'])==ident and r['victim_actor']==('01034E90' if side==1 else '010350A0') for r in palettes)
        groups=previous.summaries_at(folder);positive=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','missing_draw','wrong_clip'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
            else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted')
        results[fighter]=dict(**positive,paletteBankMatchesTrueVictimDraws=118,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,physicalVictimSlot=side,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),stockBloodEffectsAccepted=False,subjectiveAllArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,side=side,results={f:{k:v for k,v in r.items() if k not in ('terminal','logSha256')} for f,r in results.items()})))

if __name__=='__main__':main(int(sys.argv[1]))
