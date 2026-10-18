import unittest
from inspect_sub_normal_throw import request_case

def sample():
    base=dict(phase='throw',ownAction='771',ownFlags='1',ownHeight='0',enemyAction='771',
              enemyFlags='0',enemyHeight='0',distance='60',projectile='0',toward='1',away='0',block='0',down='0',lp='1')
    rows={frame:dict(base,frame=str(frame)) for frame in range(100,109)}
    rows[102]['ownAction']='1287'
    return rows

class NormalThrowRequestTests(unittest.TestCase):
    def test_actual_throw_observed(self):
        self.assertTrue(request_case(sample(),100)['throwObservedWithin8'])

    def test_request_is_not_activation(self):
        rows=sample();rows[102]['ownAction']='259'
        self.assertFalse(request_case(rows,100)['throwObservedWithin8'])
        self.assertIsNone(request_case({100:rows[100]},100)['throwObservedWithin8'])

    def test_reaction_projectile_airborne_or_outside_range_rejected(self):
        for change in ({'ownFlags':'5'},{'enemyFlags':'16'},{'projectile':'1'},{'enemyHeight':'1'},
                       {'ownAction':'1792'},{'distance':'61'},{'block':'1'},{'lp':'0'}):
            rows=sample();rows[100].update(change)
            with self.assertRaises(AssertionError):request_case(rows,100)
