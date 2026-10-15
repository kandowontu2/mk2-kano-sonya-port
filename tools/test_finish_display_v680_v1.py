"""Counterexamples using the actual current two-case fatality records.

Mutations stay in memory. Never alter captured inputs to obtain a pass.
"""
import copy
import unittest
import verify_finish_display_v680_v6 as v


class FinishEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=(v.ROOT/v.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.original=(v.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.guest=(v.ROOT/'audit_v684_pit_guest_rom_integrity'/v.NAME/'guest_maincpu.bin').read_bytes()
        cls.cases=[(v.raster.data(v.ROOT/name)[0],ids) for name,ids in v.CASES.items()]

    def cache(self,g,ids):return v.composites(g,self.payload,self.original,ids,self.guest)
    def state(self,g,ids):return v.retirement(g,g['FLOOR_BEGIN'][0],self.guest,ids)

    def reject_cache(self,tag,key,change,case=0,condition=lambda r:True):
        g,ids=self.cases[case];g=copy.deepcopy(g)
        row=next(r for r in g[tag] if condition(r));row[key]=change(row[key])
        with self.assertRaises(ValueError):self.cache(g,ids)

    def reject_state(self,tag,key,change):
        g,ids=self.cases[0];g=copy.deepcopy(g);g[tag][0][key]=change(g[tag][0][key])
        with self.assertRaises(ValueError):self.state(g,ids)

    def test_two_actual_cache_baselines(self):
        for g,ids in self.cases:self.cache(g,ids)
    def test_two_actual_retirement_baselines(self):
        for g,ids in self.cases:self.state(g,ids)
    def test_proxy_fighter(self):self.reject_cache('FLOOR_QUEUE','id',lambda x:0,condition=lambda r:r['slot']==1)
    def test_proxy_victim(self):self.reject_cache('FLOOR_QUEUE','roster',lambda x:0,condition=lambda r:r['slot']==2)
    def test_wrong_palette(self):self.reject_cache('FLOOR_QUEUE','bank',lambda x:x^256)
    def test_wrong_native_source(self):self.reject_cache('FLOOR_QUEUE','source',lambda x:x+1)
    def test_wrong_cached_component(self):self.reject_cache('FLOOR_QUEUE_PART','source',lambda x:x+1)
    def test_wrong_dimensions(self):self.reject_cache('FLOOR_QUEUE','size',lambda x:x+1)
    def test_wrong_position(self):self.reject_cache('FLOOR_QUEUE','xy',lambda x:x+1)
    def test_wrong_command(self):self.reject_cache('FLOOR_QUEUE','command',lambda x:x^(16<<16))
    def test_wrong_cache_iterator(self):self.reject_cache('FLOOR_QUEUE','row',lambda x:x+112)
    def test_wrong_publication_actor(self):self.reject_cache('FLOOR_QUEUE_DISPATCH','actor',lambda x:x+16)
    def test_wrong_native_FIFO_cursor(self):
        events={r['event'] for r in self.cases[0][0]['FLOOR_QUEUE_DISPATCH']}
        self.reject_cache('FLOOR_DMA_REGS','b14',lambda x:x+192,condition=lambda r:r['event'] in events)
    def test_omitted_body_classifier(self):self.reject_cache('FLOOR_DMA','slot',lambda x:0,condition=lambda r:r['slot']==1)
    def test_wrong_single_descriptor_bytes(self):
        self.reject_cache('FLOOR_SINGLE_DESCRIPTOR','data',lambda x:'00'+x[2:],case=1)
    def test_wrong_single_descriptor_pointer(self):
        self.reject_cache('FLOOR_SINGLE_DESCRIPTOR','descriptor',lambda x:x+256,case=1)
    def test_single_frame_as_fighter(self):
        self.reject_cache('FLOOR_QUEUE','slot',lambda x:1,case=1,condition=lambda r:r['multipart']==0)

    def test_wrong_single_branch(self):
        self.reject_cache('FLOOR_QUEUE','multipart',lambda x:1,case=1,condition=lambda r:r['multipart']==0)
    def test_wrong_effect_owner_kind(self):
        self.reject_cache('FLOOR_QUEUE','kind',lambda x:0,condition=lambda r:r['slot']==3)
    def test_missing_state(self):
        g,ids=self.cases[0];g=copy.deepcopy(g);g['FLOOR_STATE'].pop(1)
        with self.assertRaises(ValueError):self.state(g,ids)
    def test_wrong_retirement_mode(self):self.reject_state('FLOOR_RETIRED','mode',lambda x:5)
    def test_wrong_retirement_winner(self):self.reject_state('FLOOR_RETIRED','winner',lambda x:2)
    def test_wrong_retirement_health(self):self.reject_state('FLOOR_RETIRED','health2',lambda x:161)
    def test_wrong_native_store_PC(self):self.reject_state('FLOOR_POINTER_STORE','pc',lambda x:x+16)
    def test_wrong_native_store_previous_pointer(self):self.reject_state('FLOOR_POINTER_STORE','before',lambda x:x+16)
    def test_partial_native_store(self):self.reject_state('FLOOR_POINTER_STORE','mask',lambda x:255)
    def test_nonzero_native_store(self):self.reject_state('FLOOR_POINTER_STORE','value',lambda x:1)
    def test_wrong_guest_store_instruction(self):
        g,ids=self.cases[0];guest=bytearray(self.guest);guest[(0xff82bbb0-0xff800000)//8]^=1
        with self.assertRaises(ValueError):v.retirement(g,g['FLOOR_BEGIN'][0],guest,ids)


if __name__=='__main__':unittest.main()
