"""Mutations of real native records for the Reptile overrun acceptance gate."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_reptile_campaign_v865 as proof

class ReptileRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_guest=proof.OLD_GUEST.read_bytes()
        cls.new_guest=(proof.NEW/'guest_maincpu.bin').read_bytes()
        cls.old_text=(proof.OLD/'run.log').read_text(encoding='utf-8-sig')
        cls.new_text=(proof.NEW/'run.log').read_text(encoding='utf-8-sig')

    def report(self,**changes):
        args=dict(old_guest=self.old_guest,new_guest=self.new_guest,
                  old_text=self.old_text,new_text=self.new_text,check_hashes=False)
        args.update(changes);return proof.verify(**args)

    def reject(self,label,**changes):
        report=self.report(**changes)
        self.assertFalse(report['passed']);self.assertIn(label,report['errors'])

    def test_real_baseline_is_only_memory_repair(self):
        report=self.report()
        self.assertTrue(report['passed'],report['errors'])
        self.assertTrue(report['native_table_overrun_repair_proven'])
        self.assertFalse(report['full_native_reptile_art_acceptance'])
        self.assertFalse(report['full_port_acceptance'])
        self.assertTrue(all(v['stillStockLiu']for v in report['remaining_head_art_gap'].values()))

    def test_unrelated_code_change_is_rejected(self):
        data=bytearray(self.new_guest);data[proof.at(0xff8366c0)]^=1
        self.reject('Only 19-row table and one pointer changed; native code/timing untouched',new_guest=data)

    def test_stock_victim_row_change_is_rejected(self):
        data=bytearray(self.new_guest);data[0xfa800+4*8]^=1
        self.reject('Only 19-row table and one pointer changed; native code/timing untouched',new_guest=data)

    def test_kano_row_cannot_remain_adjacent_code(self):
        data=bytearray(self.new_guest);data[0xfa800+17*8:0xfa800+18*8]=self.old_guest[proof.at(0xff8c9900)+17*8:proof.at(0xff8c9900)+18*8]
        self.reject('Only 19-row table and one pointer changed; native code/timing untouched',new_guest=data)

    def test_real_input_timeline_cannot_change(self):
        text=self.new_text.replace('button=High_Punch selection=0','button=Low_Punch selection=0',1)
        self.assertNotEqual(text,self.new_text)
        self.reject('Identical actual campaign/input/state chronology before original fault',new_text=text)

    def test_observer_rom_dump_is_not_native_table_read(self):
        text=self.new_text.replace('field=0 at=FFFD4480 data=FF3F mask=FFFF pc=FF8C8AA0',
                                   'field=0 at=FFFD4480 data=FF3F mask=FFFF pc=FFA59F10',1)
        self.assertNotEqual(text,self.new_text)
        self.reject('Exact original runtime consumer/registers, never observer-generated ROM-dump reads',new_text=text)

    def test_wrong_table_animation_is_rejected(self):
        text=self.new_text.replace('field=2 at=FFFD44A0 data=0010','field=2 at=FFFD44A0 data=2710',1)
        self.reject('Actual native four-field read of independent true Sonya victim row',new_text=text)

    def test_missing_native_draw_is_rejected(self):
        text=re.sub(r'^MK2_NAT_CAMPAIGN_REPTILE_DRAW .*\n','',self.new_text,flags=re.M)
        self.reject('Original animation interpreter receives real Sonya high-hit stream, not descriptor/code data',new_text=text)

    def test_wrong_fatality_age_is_rejected(self):
        text=self.new_text.replace('age=90 pc=FF8C9690','age=79435 pc=FF8C9690',1)
        self.reject('Original Reptile fatality reaches native completion at its actual age',new_text=text)

    def test_reset_is_not_waived(self):
        text=self.new_text+'\nMK2_NAT_CAMPAIGN_REENTRY duplicate_callbacks_prevented=true writes=0 assistance=none\n'
        self.reject('No body overrun or machine reset',new_text=text)

    def test_no_post_fault_true_character_is_rejected(self):
        def change(m):
            return m[0].replace('human=18:18','human=1:1')if int(m[1])>proof.FAIL_FRAME else m[0]
        text=re.sub(r'^MK2_NAT_CAMPAIGN_FIGHT frame=(\d+) .*$',change,self.new_text,flags=re.M)
        self.reject('Actual paid continue/reselection returns real Sonya to combat after original fault',new_text=text)

    def test_finisher_pictures_cannot_be_boot_pictures(self):
        text=self.new_text.replace('REPTILE_DISPLAY frame=79346','REPTILE_DISPLAY frame=1',1)
        self.reject('Sixteen snapshots follow the actual native finisher, not the boot ROM dump',new_text=text)

    def test_remaining_liu_head_gap_cannot_be_hidden(self):
        text=re.sub(r'^MK2_NAT_CAMPAIGN_REPTILE_HEAD .*\n','',self.new_text,flags=re.M)
        self.reject('Record the actual remaining Liu head art rather than hiding its fidelity gap',new_text=text)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve existing unit evidence')
    args.output.mkdir();stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReptileRepairTests))
    (args.output/'run.log').write_text(stream.getvalue())
    report={'passed':result.wasSuccessful(),'methods':result.testsRun,'failures':len(result.failures),
            'errors':len(result.errors),'scope':'memory-repair verifier mutations, not full native art or port'}
    (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    raise SystemExit(0 if result.wasSuccessful()else 1)

if __name__=='__main__':main()
