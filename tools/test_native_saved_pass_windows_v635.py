"""Actual compact-pass anchors and explicit replay boundaries, not full erasure proof."""
import copy
import re
import unittest
from unittest.mock import patch
import numpy as np
import inspect_natural_arena_floor_v635_v4 as v
from verify_native_ui_flow_v635 import ROOT


class SavedPasses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v641_compact_native_floor_kano_p2'
        cls.actual=v.data(cls.folder)
        cls.groups,cls.buffers,_,_,cls.owners=cls.actual
        cls.latches=sorted((r for r in cls.groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']),key=lambda r:r['event'])
        cls.first=cls.latches[0]
        cls.anchor=next(r for r in cls.groups['FLOOR_PRE_FRAME']if r['frame']==cls.first['snapshot']-1)
        # Real P1 CPU-write parameters; the unit precondition test below uses
        # actual retained VRAM with deliberately adapted expected-before words.
        with(ROOT/'audit_v646_native_floor_kano_p1/run.log').open(encoding='utf-8-sig')as stream:
            for line in stream:
                if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_CPU '):continue
                raw=dict(re.findall(r'(\w+)=([^\s]+)',line))
                hx=v.HEX|{'op','before0','before1','before','after','first_source','row'}
                st=v.STR|{'register'}
                cls.cpu={k:value if k in st else int(value,16 if k in hx else 10)for k,value in raw.items()}
                break
        assert hasattr(cls,'cpu'),'Actual observed CPU-write fixture'

    def replay(self,groups):
        with patch.object(v,'data',return_value=(groups,self.buffers,None,None,self.owners)):
            return v.inspect(self.folder)

    def reject(self,mutate):
        groups=copy.deepcopy(self.groups);mutate(groups)
        with self.assertRaises((AssertionError,KeyError)):self.replay(groups)

    def find_anchor(self,groups):
        return next(r for r in groups['FLOOR_PRE_FRAME']if r['frame']==self.anchor['frame'])

    def test_actual_fifteen_saved_passes(self):
        proof=self.replay(self.groups)
        self.assertEqual(proof['frames'],15)
        self.assertTrue(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in proof['records']))
        self.assertFalse(proof['floorAcceptance'])

    def test_missing_exact_anchor(self):
        self.reject(lambda g:g['FLOOR_PRE_FRAME'].remove(self.find_anchor(g)))

    def test_shifted_anchor_field(self):
        self.reject(lambda g:self.find_anchor(g).update(frame=self.anchor['frame']+1))

    def test_wrong_before_pass_phase(self):
        self.reject(lambda g:self.find_anchor(g).update(phase='after_first_frame_dma'))

    def test_anchor_after_tested_flip(self):
        self.reject(lambda g:self.find_anchor(g).update(event=self.first['event']+1))

    def test_overlapping_saved_windows(self):
        second=self.latches[1]['snapshot']-1
        self.reject(lambda g:next(r for r in g['FLOOR_PRE_FRAME']if r['frame']==second).update(event=self.anchor['event']))

    def test_cpu_pre_write_assertion_is_not_waived(self):
        replay=v.Replay(self.folder,self.groups,self.buffers,self.owners)
        replay.words=np.fromfile(self.folder/self.anchor['file'],dtype='<u2').reshape(512,512).copy()
        replay.body=np.zeros((512,512),dtype=np.uint8)
        replay.shadow=np.zeros((512,512),dtype=bool)
        record=copy.deepcopy(self.cpu)
        for part in(0,1):
            y,x=divmod(record['index']+part,512);record[f'before{part}']=int(replay.words[y,x])
        invalid=copy.deepcopy(record);invalid['before0']^=1
        with self.assertRaisesRegex(AssertionError,'CPU pre-write VRAM'):replay.cpu(invalid)
        replay.cpu(record)

    def test_unsaved_cpu_writes_are_explicitly_outside_proof(self):
        groups=copy.deepcopy(self.groups);outside=copy.deepcopy(self.cpu)
        outside['event']=max(r['event']for r in self.latches)+100
        outside['before0']^=1;groups['FLOOR_CPU'].append(outside)
        proof=self.replay(groups)
        self.assertEqual(proof['cpu_writes'],len(self.groups['FLOOR_CPU'])+1)
        self.assertTrue(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in proof['records']))
        self.assertIn('unsaved inter-pass',proof['scope'])


if __name__=='__main__':unittest.main()
