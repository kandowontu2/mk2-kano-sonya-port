"""Nonvacuous FIFO ownership/composite and actual saved-pass regressions.

Mutates in-memory evidence only. Never writes game state or retained captures.
Whole-port artistic/audio acceptance is not implied by these tests.
"""
import unittest
from collections import defaultdict
import numpy as np
import verify_cpu_pair_display_v635_v3 as v


class Display(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases={}
        cls.payload=(v.ROOT/v.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.original=(v.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        for name,(player,profile) in v.CASES.items():
            folder=v.ROOT/name
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            proof=v.ordinary.verify_log(log,player) if profile=='ordinary' else v.special.verify_log(log,player,profile)
            assert proof['passed'],(name,proof)
            groups,buffers,_,_,owners=v.raster.data(folder)
            cls.cases[name]=(folder,groups,buffers,owners,{**proof,'log':log})

    def check(self,name,groups=None):
        _,baseline,_,_,proof=self.cases[name]
        return v.check_composites(groups if groups is not None else baseline,self.payload,self.original,proof)

    def changed(self,name,tag,field,value,predicate=lambda r:True,remove=False):
        groups=self.cases[name][1]
        result=defaultdict(list,groups)
        result[tag]=[dict(r) for r in groups[tag]]
        index=next((i for i,r in enumerate(result[tag]) if predicate(r)),None)
        self.assertIsNotNone(index,'Actual recorded mutation target must exist')
        if remove:result[tag].pop(index)
        else:
            self.assertNotEqual(result[tag][index][field],value,'Mutation must change evidence')
            result[tag][index][field]=value
        return result

    def reject(self,name,groups):
        with self.assertRaises((ValueError,KeyError,IndexError)):self.check(name,groups)

    def test_all_five_actual_composites(self):
        self.assertEqual(len(self.cases),5)
        for name in self.cases:
            proof=self.check(name)
            self.assertGreater(proof['body_draws'],300)
            self.assertGreater(len(proof['distinct_held_CPU_poses']),1)

    def test_same_palette_effect_is_not_body(self):
        for name,(_,groups,_,_,_) in self.cases.items():
            banks={r['palette'] for r in groups['FLOOR_DMA'] if r['slot'] in (1,2)}
            effect=next(r for r in groups['FLOOR_DMA'] if r['slot']==0 and r['command']&15==2 and r['palette'] in banks)
            self.reject(name,self.changed(name,'FLOOR_DMA','slot',1,lambda r:r['event']==effect['event']))

    def test_queue_body_cannot_be_hidden_as_scenery(self):
        for name,(_,groups,_,_,_) in self.cases.items():
            body=next(r for r in groups['FLOOR_DMA'] if r['slot']==1)
            altered=self.changed(name,'FLOOR_DMA','slot',0,lambda r:r['event']==body['event'])
            altered['FLOOR_QUEUE_DISPATCH']=[r for r in altered['FLOOR_QUEUE_DISPATCH'] if r['event']!=body['event']]
            self.reject(name,altered)

    def test_duplicate_publication_is_ambiguous(self):
        name=next(iter(self.cases));groups=defaultdict(list,self.cases[name][1])
        groups['FLOOR_QUEUE']=groups['FLOOR_QUEUE']+[groups['FLOOR_QUEUE'][0]]
        self.reject(name,groups)

    def test_duplicate_dispatch_is_ambiguous(self):
        name=next(iter(self.cases));groups=defaultdict(list,self.cases[name][1])
        groups['FLOOR_QUEUE_DISPATCH']=groups['FLOOR_QUEUE_DISPATCH']+[groups['FLOOR_QUEUE_DISPATCH'][0]]
        self.reject(name,groups)

    def test_corrupted_owned_fifo_iterator(self):
        for name,(_,groups,_,_,_) in self.cases.items():
            event=groups['FLOOR_QUEUE_DISPATCH'][0]['event']
            self.reject(name,self.changed(name,'FLOOR_DMA_REGS','b14',0,lambda r:r['event']==event))

    def replay(self,mutate=False):
        name=next(iter(self.cases));folder,groups,buffers,owners,_=self.cases[name]
        latch=groups['FLOOR_LATCH'][0]
        pre=next(r for r in groups['FLOOR_PRE_FRAME'] if r['frame']==latch['snapshot']-1)
        events=sorted([(tag,r) for tag in ('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU')
                       for r in groups[tag] if pre['event']<=r['event']<latch['event']],key=lambda e:e[1]['event'])
        replay=v.raster.Replay(folder,groups,buffers,owners);changed=0
        for tag,row in events:
            if mutate and tag=='FLOOR_DMA' and row['slot'] in (1,2):
                row={**row,'palette':row['palette']^0x100};changed+=1
            replay.apply(tag,row)
        if mutate:self.assertGreater(changed,0)
        actual=np.frombuffer((folder/latch['file']).read_bytes(),dtype='<u2').reshape(512,512)
        return replay,actual

    def test_exact_actual_prior_pass_vram(self):
        replay,actual=self.replay()
        self.assertTrue(np.array_equal(replay.words,actual))
        for slot in (1,2):self.assertGreater(np.count_nonzero(replay.body==slot),100)

    def test_wrong_body_palette_changes_actual_pixels(self):
        replay,actual=self.replay(True)
        self.assertGreater(np.count_nonzero(replay.words!=actual),100)


def mutation_test(tag,field,value,predicate):
    def test(self):
        for name in self.cases:
            self.reject(name,self.changed(name,tag,field,value,predicate))
    return test


for label,tag,field,value,predicate in (
    ('cursor','FLOOR_QUEUE_DISPATCH','cursor',0,lambda r:True),
    ('actor','FLOOR_QUEUE_DISPATCH','actor',0,lambda r:True),
    ('main','FLOOR_QUEUE_DISPATCH','main',0,lambda r:True),
    ('queue_frame','FLOOR_QUEUE_DISPATCH','queue_frame',0,lambda r:True),
    ('id','FLOOR_QUEUE','id',1,lambda r:r['slot']==1),
    ('roster','FLOOR_QUEUE','roster',1,lambda r:r['slot']==1),
    ('owner','FLOOR_QUEUE','owner',0,lambda r:True),
    ('iterator','FLOOR_QUEUE','row',0,lambda r:True),
    ('part','FLOOR_QUEUE','part',99,lambda r:True),
    ('pc','FLOOR_QUEUE','pc',0,lambda r:True),
    ('pose','FLOOR_QUEUE','pose',0,lambda r:True),
    ('source','FLOOR_QUEUE','source',0,lambda r:True),
    ('size','FLOOR_QUEUE','size',0,lambda r:True),
    ('xy','FLOOR_QUEUE','xy',0,lambda r:True),
    ('command','FLOOR_QUEUE','command',0,lambda r:True),
    ('cache_source','FLOOR_QUEUE_PART','source',0,lambda r:True),
    ('cache_dx','FLOOR_QUEUE_PART','dx',-999,lambda r:True),
    ('cache_dy','FLOOR_QUEUE_PART','dy',-999,lambda r:True),
    ('cache_width','FLOOR_QUEUE_PART','width',0,lambda r:True),
    ('cache_height','FLOOR_QUEUE_PART','height',0,lambda r:True),
    ('cache_flip','FLOOR_QUEUE_PART','command',0,lambda r:True),
    ('dma_source','FLOOR_DMA','source',0,lambda r:r['slot']==1),
    ('dma_width','FLOOR_DMA','width',0,lambda r:r['slot']==1),
    ('dma_height','FLOOR_DMA','height',0,lambda r:r['slot']==1),
    ('dma_x','FLOOR_DMA','x',0,lambda r:r['slot']==1),
    ('dma_y','FLOOR_DMA','y',0,lambda r:r['slot']==1),
    ('dma_palette','FLOOR_DMA','palette',0,lambda r:r['slot']==1),
    ('dma_command','FLOOR_DMA','command',0,lambda r:r['slot']==1),
):
    setattr(Display,'test_corrupted_'+label,mutation_test(tag,field,value,predicate))


if __name__=='__main__':unittest.main(verbosity=2)
