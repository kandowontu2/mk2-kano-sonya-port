"""Current real-ID kick recovery and counter/pose/store mutations."""
import unittest
from pathlib import Path
import verify_cpu_roundhouse_flow as flow
import verify_cpu_roundhouse_recovery as pair
from verify_cpu_air_runtime import matched_launch
from test_cpu_action_recovery import change

KANO=pair.ROOT/'audit_v417_cpu_roundhouse_kano604'
STOCK=pair.ROOT/'audit_v417_cpu_roundhouse_stock_baraka601'
MUTATIONS=[
    ('native_entry_missing','FLOW',2128,None,None,'entry=FF9B9470',True),
    ('native_seq_alias','FLOW',2128,'a9','00000014','entry=FF9B9470',False),
    ('native_counter_arg','FLOW',2128,'a0','00000006','entry=FF9B9470',False),
    ('fake_writer_not_skip','FLOW',2128,'entry','FF83C320','entry=FF83C340',False),
    ('wrong_sequence_pointer','SEQUENCE',2128,'at','FF93E8F0',None,False),
    ('sequence_alias','SEQUENCE',2128,'id','1',None,False),
    ('sequence_missing','SEQUENCE',2150,None,None,None,True),
    ('counter_does_not_decrement','FIELD',2138,'attack_count','7',None,False),
    ('counter_wrong_second_phase','FIELD',2149,'attack_count','6',None,False),
    ('wrong_native_delay','FIELD',2140,'attack_delay','1',None,False),
    ('walk_not_cleared','FIELD',2110,'flags','00000010',None,False),
    ('wrong_first_loop_pose','FIELD',2140,'pose','FF00FCC0',None,False),
    ('wrong_return_pose','FIELD',2153,'pose','FF00FEA0',None,False),
    ('missing_last_recovery_field','FIELD',2165,None,None,None,True),
    ('stale_main_flags','FIELD',2166,'flags','00000010',None,False),
    ('stale_body_flags','FIELD',2166,'body','00000016',None,False),
    ('wrong_walk_speed','FIELD',2166,'vx','00030000',None,False),
    ('fake_new_action','FIELD',2140,'action','262',None,False),
    ('wrong_real_id','FIELD',2140,'id','1',None,False),
    ('wrong_real_main','FIELD',2140,'main','0106BF30',None,False),
    ('wrong_real_owner','FIELD',2140,'owner','010350A0',None,False),
    ('chip_missing','HEALTH',2137,None,None,None,True),
    ('chip_amount','HEALTH',2137,'after','23',None,False),
    ('chip_wrong_writer','HEALTH',2137,'pc','FF8366F0',None,False),
    ('chip_wrong_owner','HEALTH',2137,'a13','0106BF30',None,False),
    ('health_fake','FIELD',2141,'vhp','25',None,False),
    ('action_clear_missing','ACTION',2165,None,None,'before=0303',True),
    ('body_cleanup_missing','FLAG',2165,None,None,'before=0016',True),
    ('flags_cleanup_missing','FLAG',2165,None,None,'before=0010',True),
    ('wrong_cleanup_state','FLAG',2165,'action','771','before=0016',False),
    ('wrong_saved_register_return','FLOW',2165,'a9','00000014','entry=FF861350',False),
    ('native_resume_missing','FLOW',2165,None,None,'entry=FF9B9B50',True),
    ('wrong_miss_branch','FLOW',2159,'entry','FF9B9950','entry=FF9B9A30',False),
    ('fake_setup_state','FLAG',2128,'action','273','before=0012',False),
    ('wrong_setup_target','FLAG',2128,'at','01035000','kind=body',False),
    ('assisted_store','FLAG',2128,'writes','1','kind=body',False),
    ('cycles_spliced','FLOW',2137,'cycle','2','entry=FF9B95C0',False),
    ('duplicate_key','FIELD',2140,'id','17 id=17',None,False),
    ('terminal_missing','FIELD',2311,None,None,None,True),
]


class NativeRoundhouse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _,cls.log,cls.original=matched_launch(KANO,'mk2ks_cpu_roundhouse_v2_probe.lua','run_cpu_roundhouse_v2_probe.ps1')

    def test_full_current_choke_and_first_roundhouse(self):
        proof=pair.verify(KANO,'kano')
        self.assertTrue(proof['passed'],proof)
        self.assertEqual((proof['held_fields'],proof['damage']),(70,32))
        self.assertEqual(proof['original_roundhouse_followup']['native_pose_fields'],37)

    def test_second_native_roundhouse(self):
        proof=flow.verify(self.log,2172,self.original)
        self.assertEqual((proof['clear'],proof['chip_damage']),(2209,6))

    def test_longer_native_loop_then_late_miss(self):
        proof=flow.verify(self.log,2260,self.original,late_miss=True)
        self.assertEqual((proof['native_pose_fields'],proof['chip_damage']),(45,9))

    def test_stock_original_roundhouse(self):
        _,log,original=matched_launch(STOCK,'mk2ks_cpu_roundhouse_v2_probe.lua','run_cpu_roundhouse_v2_probe.ps1')
        proof=flow.verify(log,1767,original,3,'STOCK_FIELD')
        self.assertEqual((proof['clear'],proof['chip_damage']),(1804,6))

    def test_short_old_capture_rejected(self):
        log=(pair.ROOT/'audit_v412_cpu_action_kano_mirror604/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(pair.verify_log(log,'kano')['passed'])

    def test_native_tailcall_must_skip_state_writer(self):
        original=bytearray(self.original)
        original[(0xff9b95a0-0xff800000)//8]^=0x60
        with self.assertRaises(ValueError):flow.instructions(original)

    def test_authored_sequence_opcode_loop_required(self):
        from verify_cpu_air_gate import rows
        seq=rows(self.log,'MK2_CPU_PAIR_SEQUENCE')
        r=next(r for r in seq if r['frame']=='2128')
        bad=change(self.log,'SEQUENCE',2128,'words',r['words'].replace('00000001','00000000',1))
        self.assertFalse(pair.verify_log(bad,'kano')['passed'])

    def test_actual_setup_order_required(self):
        lines=self.log.splitlines(keepends=True)
        a=next(i for i,l in enumerate(lines)if l.startswith('MK2_CPU_PAIR_FLOW frame=2128')and'entry=FF9B9470'in l)
        b=next(i for i,l in enumerate(lines)if l.startswith('MK2_CPU_PAIR_FLAG frame=2128')and'kind=flags'in l)
        lines[a],lines[b]=lines[b],lines[a]
        self.assertFalse(pair.verify_log(''.join(lines),'kano')['passed'])

    def test_late_miss_cannot_use_early_return(self):
        bad=change(self.log,'FLOW',2302,'entry','FF9B9A30',contains='entry=FF9B9950')
        with self.assertRaises(ValueError):flow.verify(bad,2260,self.original,late_miss=True)

    def test_incomplete_disk_full_capture_rejected(self):
        log=(pair.ROOT/'audit_v416_cpu_roundhouse_kano604/run.log').read_text(encoding='utf-8-sig')
        self.assertFalse(pair.verify_log(log,'kano')['passed'])


def make_test(case):
    def test(self):
        name,tag,frame,key,value,contains,remove=case
        bad=change(self.log,tag,frame,key,value,contains=contains,remove=remove)
        self.assertFalse(pair.verify_log(bad,'kano')['passed'],name)
    return test


for case in MUTATIONS:
    setattr(NativeRoundhouse,'test_reject_'+case[0],make_test(case))

if __name__=='__main__':unittest.main()
