import json
from pathlib import Path
import unittest
from finisher_observation_end import verify_end

CURRENT_REJOINS=('stock_wolf_6ae0_fatality_01','stock_wolf_6ae0_fatality_02',
                 'stock_wolf_6ae0_fatality_03','stock_wolf_6ae0_nonlethal_pos_01',
                 'stock_wolf_6ae0_nonlethal_pos_02',
                 'stock_wolf_6ae0_morph_extract_rejoin_p1',
                 'stock_wolf_6ae0_morph_kiss_rejoin_p1',
                 'stock_wolf_6ae0_morph_laser_rejoin_p1')

class ObservationEnd(unittest.TestCase):
    def test_ordinary_run_retains_full_9000_field_gate(self):
        execution={'testArguments':[]}
        verify_end(None,execution,9000)
        with self.assertRaises(AssertionError):verify_end(None,execution,8999)

    def test_current_pinned_rejoin_accepts_only_actual_complete_interval(self):
        base=Path(__file__).parent.parent/'baseline'
        for name in CURRENT_REJOINS:
            run=base/name
            execution=json.loads((run/'execution.json').read_text())
            proof=json.loads((run/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
            frame=proof['freshMatchFrame']+599
            verify_end(run,execution,frame)
            with self.assertRaises(AssertionError):verify_end(run,execution,frame-1)
            with self.assertRaises(AssertionError):verify_end(run,execution,frame+1)

    def test_changed_controller_receipt_is_rejected(self):
        run=Path(__file__).parent.parent/'baseline'/CURRENT_REJOINS[0]
        execution=json.loads((run/'execution.json').read_text())
        proof=json.loads((run/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
        verify_end(run,execution,proof['freshMatchFrame']+599)
        execution['controllerSHA256']='0'*64
        with self.assertRaises(AssertionError):
            verify_end(run,execution,proof['freshMatchFrame']+599)

if __name__=='__main__':unittest.main()
