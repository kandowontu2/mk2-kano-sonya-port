import csv
import tempfile
import unittest
from pathlib import Path
from finisher_eligibility import verify_punch_rejection,verify_command


class EligibilityTests(unittest.TestCase):
    def check_case(self, actor, kind, directions, button, punch=123, valid=True, facing_right=True,expect_punch=True,distance=200):
        with tempfile.TemporaryDirectory() as folder:
            run = Path(folder)
            row = dict(frame='100', hpTimestamp=str(punch), lpTimestamp='0',
                       actorX='100' if facing_right else str(100+distance),
                       victimX=str(100+distance) if facing_right else '100')
            row.update({f'j{i}':f'{code << 16 | 90:08x}' for i,code in enumerate((directions+[0]*4)[:4])})
            row.update({f'b{i}':f'{(button if i==0 else 0) << 16 | 95:08x}' for i in range(4)})
            with (run/'eligibility_inputs.csv').open('w',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(row));writer.writeheader();writer.writerow(row)
            check=verify_punch_rejection if expect_punch else lambda r,a,k,w:verify_command(r,a,k,w,False)
            if valid:
                self.assertEqual(check(run,actor,kind,{'100'})[1],[100])
            else:
                with self.assertRaises(AssertionError):check(run,actor,kind,{'100'})

    def test_positive_babality_requires_zero_punch_history(self):
        for right in (True,False):
            forward=8 if right else 7
            self.check_case(17,'baby',[6,6,forward,forward],4,punch=0,facing_right=right,expect_punch=False)
            self.check_case(17,'baby',[6,6,forward,forward],4,punch=123,valid=False,facing_right=right,expect_punch=False)

    def test_command_below_native_minimum_distance_is_not_eligibility_proof(self):
        self.check_case(18,'baby',[8,6,6],4,distance=159,valid=False)

    def test_valid_commands_both_facings(self):
        for right in (True,False):
            forward=8 if right else 7;back=15-forward
            self.check_case(18,'friend',[6,back,forward,back],2,facing_right=right)
            self.check_case(17,'baby',[6,6,forward,forward],4,facing_right=right)
            self.check_case(18,'baby',[forward,6,6],4,facing_right=right)

    def test_missing_command_rejected(self):
        self.check_case(18,'friend',[6,8,7,8],2,valid=False)

    def test_missing_final_button_rejected(self):
        self.check_case(17,'baby',[6,6,8,8],3,valid=False)

    def test_no_punch_timestamp_rejected(self):
        self.check_case(18,'baby',[8,6,6],4,punch=0,valid=False)


if __name__=='__main__':unittest.main()
