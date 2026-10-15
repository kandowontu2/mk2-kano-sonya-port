"""Independent split FIFO/DMA/opaque/native-clip/visible pixels, both slots."""
import collections,copy,inspect,json,re,sys
from pathlib import Path
import qualify_bounded_jax_clap_effect_pixels as previous
from qualify_bounded_kung_lao_split_draw_census import states
from qualify_bounded_kung_lao_split_followthrough_palette import palette_gate
import verify_native_source_sync as sync

namespace=dict(previous.__dict__)
exec(compile(inspect.getsource(previous.coverage_gate).replace('<=188','<=299'),__file__+'::complete_followthrough','exec'),namespace)
coverage_gate=namespace['coverage_gate']

def fifo_at(folder,sources,ident):
    counter=collections.Counter()
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if not line.startswith('MK2_EFFECT_CENSUS_FIFO '):continue
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if r['source'] not in sources:continue
            assert int(r['id'])==ident
            size=int(r['size'],16);xy=int(r['xy'],16)
            counter[(int(r['frame']),r['source'],size&1023,(size>>16)&1023,xy&1023,(xy>>16)&511,(int(r['command'],16)>>16)&65535)]+=1
    return counter

def main(side):
    assert side in (1,2);out=sync.ROOT/f'audit_bounded_kung_lao_split_pixels_p{side}_checked';assert not out.exists()
    descriptor_path=sync.ROOT/'audit_bounded_kung_lao_split_descriptors_checked/report.json'
    descriptors=json.loads(descriptor_path.read_text());assert descriptors['passed']
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_followthrough_palette_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        key=f'{fighter}P{side}';sources={r['source'] for r in descriptors['descriptors'][str(ident)]}
        folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_pixels_runtime'
        base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_followthrough_palette_runtime'
        assert sync.sha(base/'run.log')==proof['results'][key]['logSha256']
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        old=states(base,fighter,side);tags={tag for tag,r in old}
        assert [r for r in states(folder,fighter,side) if r[0] in tags]==old
        ready=int(next(r for tag,r in old if tag=='ACTION')['frame'])
        expected=fifo_at(base,sources,ident);assert sum(expected.values())==126
        assert fifo_at(folder,sources,ident)==expected
        dma=collections.Counter();palettes=[];draws=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                if line.startswith('MK2_CLAP_EFFECT_DMA '):
                    assert r['pc']=='FF804640'
                    dma[(int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16))]+=1
                elif line.startswith('MK2_SPLIT_PALETTE '):palettes.append(r)
                elif line.startswith('MK2_EFFECT_CENSUS_FIFO ') and r['source'] in sources:draws.append(r)
        assert dma==expected;palette=palette_gate(draws,palettes,ident,side)
        groups=previous.summaries_at(folder);accepted=coverage_gate(groups,ready,expected);faults=[]
        for fault in ('visible_mismatch','missing_draw','wrong_clip'):
            bad=copy.deepcopy(groups)
            if fault=='visible_mismatch':bad['COMPLETE_FOOTPRINT'][0]['display_fail']='1'
            elif fault=='missing_draw':bad['IDLE_OPAQUE'].pop(0)
            else:bad['IDLE_OPAQUE'][0]['native_clipped']='9999'
            try:coverage_gate(bad,ready,expected)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Pixel fault accepted')
        results[fighter]=dict(**accepted,**palette,originalControlUnchanged=True,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,physicalVictimSlot=side,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        descriptorProofSha256=sync.sha(descriptor_path),followthroughProofSha256=sync.sha(proof_path),
        fullBodyOrdinaryFramesAccepted=False,stockBloodEffectsAccepted=False,subjectiveAllArtAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,side=side,results={f:{k:v for k,v in r.items() if k not in ('terminal','logSha256')} for f,r in results.items()})))

if __name__=='__main__':main(int(sys.argv[1]))
