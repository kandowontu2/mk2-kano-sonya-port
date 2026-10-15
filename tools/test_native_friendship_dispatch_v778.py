"""Baseline and corruption checks for the bounded native Friendship verifier."""
import copy
from pathlib import Path
import struct
import unittest
import verify_native_friendship_dispatch_v778 as verify

ROOT=Path(__file__).resolve().parent.parent
class Checks(unittest.TestCase):
    def load(self,winner='kano',side=1,case='positive'):
        suffix=f'{winner}_friendship_p{side}'if case=='positive'else f'{winner}_wrong_p1'if case=='wrong_command'else f'{winner}_punch_p2'
        return verify.parse(ROOT/f'audit_v777_{suffix}/run.log')
    def rejected(self,rows,winner='kano',side=1,case='positive'):
        with self.assertRaises(ValueError):verify.runtime(rows,winner,side,case)
    def mutate(self,tag,key,value,winner='kano'):
        rows=copy.deepcopy(self.load(winner))
        next(r for kind,r in rows if kind==tag)[key]=value
        self.rejected(rows,winner)
    def test_eight_baselines(self):
        for winner in('kano','sonya'):
            for side,case in((1,'positive'),(2,'positive'),(1,'wrong_command'),(2,'punch_used')):
                with self.subTest(winner=winner,side=side,case=case):verify.runtime(self.load(winner,side,case),winner,side,case)
    def test_guest_baseline(self):
        old=(ROOT/'audit_v738_kano_babality_p1/guest_maincpu.bin').read_bytes()
        new=(ROOT/'audit_v777_kano_friendship_p1/guest_maincpu.bin').read_bytes()
        self.assertGreater(verify.guest_check(old,new),0)
    def test_guest_corruptions(self):
        old=(ROOT/'audit_v738_kano_babality_p1/guest_maincpu.bin').read_bytes()
        new=(ROOT/'audit_v777_kano_friendship_p1/guest_maincpu.bin').read_bytes()
        for at in(0x14000,verify.off(0xff8808a0),0xf98a0,0xf98f0,0xf9942,0xf9962,0xf9980,0xf99a0,0xf99c0):
            bad=bytearray(new);bad[at]^=1
            with self.subTest(offset=at),self.assertRaises(ValueError):verify.guest_check(old,bad)
    def test_assistance(self):self.mutate('BOOT','assistance','health_fixture')
    def test_bad_selection(self):self.mutate('SELECT_ID','actual','1')
    def test_non_native_damage(self):self.mutate('DAMAGE','pc','FF000000')
    def test_wrong_body_identity(self):self.mutate('POSE','id','1')
    def test_wrong_owner(self):self.mutate('POSE','owner','01000000')
    def test_wrong_roster(self):self.mutate('POSE','roster','1')
    def test_ground_alignment(self):self.mutate('POSE','floor','999')
    def test_pose_order(self):
        rows=self.load();poses=verify.select(rows,'POSE');poses[1]['pose']='FE9D2790';self.rejected(rows)
    def test_pose_timing(self):
        rows=self.load();verify.select(rows,'POSE')[1]['age']='49';self.rejected(rows)
    def test_bubble_palette(self):
        rows=self.load();verify.select(rows,'PART')[1]['colors']=','.join(['0000']*16);self.rejected(rows)
    def test_bubble_order(self):self.mutate('PART','pose','FE9D2790')
    def test_bubble_origin(self):self.mutate('PART','x','0')
    def test_missing_cleanup(self):self.mutate('RESULT','cleanup','false')
    def test_missing_retirement(self):self.mutate('RESULT','retired','false')
    def test_bad_handoff(self):
        rows=self.load();next(r for r in verify.select(rows,'ENTRY')if r['entry']=='FF880CC0')['frame']='9999';self.rejected(rows)
    def test_chicken_cadence(self):
        rows=self.load('sonya');next(r for r in verify.select(rows,'POSE')if int(r['age'])>=83)['age']='84';self.rejected(rows,'sonya')
    def test_wrong_command_accepted(self):
        rows=self.load(case='wrong_command');verify.select(rows,'RESULT')[0]['action']='1234';self.rejected(rows,case='wrong_command')
    def test_unexercised_punch_gate(self):
        rows=self.load(side=2,case='punch_used');verify.select(rows,'WINDOW')[0]['hp_counters']='0,0';self.rejected(rows,side=2,case='punch_used')
    def test_no_screen_transition(self):
        rows=self.load();verify.select(rows,'FIELD')[-1]['mode']='7';self.rejected(rows)

if __name__=='__main__':unittest.main(verbosity=2)
