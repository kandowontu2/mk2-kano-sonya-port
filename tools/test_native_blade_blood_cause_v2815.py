"""Actual original blood/RNG counterexamples; immutable captures are not edited."""
import copy,json
from pathlib import Path
import verify_native_blade_blood_cause_v2813 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v2816_native_blade_blood_cause_units'

def tests():
    proof_path=current.OUT/'report.json';proof=json.loads(proof_path.read_text())
    current.need(proof['passed'] and proof['candidate']==current.drawing.assembly.NAME and proof['bothPreviouslyUnresolvedBladeRecoveryScenesAccepted'],'Actual source-bound native blood proof')
    for file,wanted in proof['inputHashes'].items():current.need(current.drawing.phase.sha(file)==wanted,'Unchanged actual blood evidence '+file)
    pins={str(proof_path):current.drawing.phase.sha(proof_path)};rejected=[]
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    data=current.raster.data
    for version in (2802,2803):
        for side in (1,2):
            folder=ROOT/f'audit_v{version}_native_blade_blood_p{side}'
            groups,buffers,a,b,owners=data(folder)
            guest=(folder/'guest_maincpu.bin').read_bytes()
            current.rng_checked(groups['FLOOR_RNG'],guest,original)
            random_mutations=[
                ('opcode',3,'op',lambda n:n^1,'opcode'),
                ('read_mask',0,'mask',lambda n:n^1,'opcode'),
                ('native_seed_load',1,'a0',lambda n:n^1,'seed load'),
                ('overflow_branch',2,'status',lambda n:n^0x10000000,'overflow'),
                ('shift_result',2,'a0',lambda n:n^1,'overflow'),
                ('stored_seed',4,'seed',lambda n:n^1,'seed store'),
                ('carry',4,'status',lambda n:n^0x40000000,'carry'),
                ('HCOUNT_rotate',5,'a1',lambda n:(n+1)&65535,'rotate result'),
                ('random_result',6,'a0',lambda n:n^1,'rotate result'),
                ('stack_return',7,'sp',lambda n:n+32,'stack/return')]
            for label,index,key,change,expected in random_mutations:
                altered=copy.deepcopy(groups['FLOOR_RNG']);altered[index][key]=change(altered[index][key])
                try:current.rng_checked(altered,guest,original)
                except ValueError as error:
                    current.need(expected in str(error),'Specific original RNG rejection, not unrelated failure')
                    rejected.append(dict(case=folder.name,kind='original_RNG',label=label,error=str(error)))
                else:raise ValueError('Accepted incorrect original RNG '+label)
            publication=groups['FLOOR_BLOOD_PUBLICATION'][0];key=(publication['frame'],publication['cursor'])
            queue_index=next(i for i,r in enumerate(groups['FLOOR_ALL_QUEUE']) if (r['frame'],r['cursor'])==key)
            palette_index=next(i for i,r in enumerate(groups['FLOOR_ALL_PALETTE']) if (r['frame'],r['cursor'])==key)
            regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
            dma_index=next(i for i,r in enumerate(groups['FLOOR_DMA']) if r['frame']==publication['frame'] and r['source']==publication['source'] and regs[r['event']]['b14']+192==publication['cursor'] and r['command']&15==2)
            blood_mutations=[
                ('wrong_palette_source','FLOOR_ALL_PALETTE',palette_index,'palette_source',lambda n:n+16,'ownership substitution'),
                ('palette_reference_missing','FLOOR_ALL_PALETTE',palette_index,'refs',lambda n:0,'positive native palette'),
                ('palette_bank_mismatch','FLOOR_ALL_PALETTE',palette_index,'bank',lambda n:n^256,'palette source binding'),
                ('wrong_actor','FLOOR_BLOOD_PUBLICATION',0,'actor',lambda n:n+16,'original actor/cache/palette'),
                ('wrong_cache','FLOOR_BLOOD_PUBLICATION',0,'cache',lambda n:n+16,'original actor/cache/palette'),
                ('wrong_bitmap','FLOOR_ALL_QUEUE',queue_index,'source',lambda n:n+16,'dimensions/source'),
                ('wrong_dimensions','FLOOR_BLOOD_PUBLICATION',0,'size',lambda n:n+1,'single-sprite format'),
                ('publication_shift','FLOOR_BLOOD_PUBLICATION',0,'xy',lambda n:n+1,'blood projection'),
                ('DMA_shift','FLOOR_DMA',dma_index,'x',lambda n:n+1,'projection reaches DMA'),
                ('DMA_palette','FLOOR_DMA',dma_index,'palette',lambda n:n^256,'unchanged DMA')]
            for label,tag,index,field,change,expected in blood_mutations:
                altered=copy.deepcopy(groups);altered[tag][index][field]=change(altered[tag][index][field])
                current.raster.data=lambda path:(altered,buffers,a,b,owners)
                try:
                    try:current.case_checked(version,side,{})
                    except ValueError as error:
                        current.need(expected in str(error),'Specific blood provenance rejection, not an unrelated failure: '+str(error))
                        rejected.append(dict(case=folder.name,kind='native_blood',label=label,error=str(error)))
                    else:raise ValueError('Accepted incorrect native blood '+label)
                finally:current.raster.data=data
            print(folder.name+' twenty actual original blood/RNG corruptions rejected',flush=True)
    current.need(len(rejected)==80,'Ten original RNG plus ten blood corruptions for every actual new/control slot')
    for module in (current,current.drawing):pins[str(Path(module.__file__).absolute())]=current.drawing.phase.sha(module.__file__)
    pins[str(Path(__file__).absolute())]=current.drawing.phase.sha(__file__)
    return dict(passed=True,candidate=current.drawing.assembly.NAME,actualOriginalCounterexamplesRejected=80,
        rejected=rejected,actualCaptureFilesUnmodified=True,fullPortAccepted=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    current.need(not OUT.exists(),'Immutable original blood unit proof')
    try:report=tests()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report.get(k) for k in ('passed','error','actualOriginalCounterexamplesRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
