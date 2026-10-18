import unittest
from bubble_timing import expected_fields

class BubbleTiming(unittest.TestCase):
    def sample(self,x,target,flags=0):
        return dict(childxval=f'{(x<<16)&0xffffffff:08x}',p2x=str(target&65535),childflags=str(flags))

    def test_native_short_and_long_travel_both_facings(self):
        self.assertEqual(expected_fields(self.sample(805,1000),2),146)
        self.assertEqual(expected_fields(self.sample(1195,1000,16),2),146)
        self.assertEqual(expected_fields(self.sample(745,1000),2),176)
        self.assertEqual(expected_fields(self.sample(-200,-5),2),146)

    def test_wrong_direction_and_outside_bounded_travel_rejected(self):
        for sample in (self.sample(1000,805),self.sample(900,1000),self.sample(0,1000)):
            with self.assertRaises(AssertionError):expected_fields(sample,2)

if __name__=='__main__':unittest.main()
