import unittest
from inspect_punch_geometry import overlap

class PunchGeometryTests(unittest.TestCase):
    def test_mirrored_boxes_and_native_squeeze(self):
        a=dict(x='0',y='0',flags='0')
        v=dict(left='70',right='110',top='8',bottom='100')
        self.assertEqual(overlap(a,v),(-5,30))
        a=dict(x='200',y='0',flags='16')
        v=dict(left='90',right='130',top='8',bottom='100')
        self.assertEqual(overlap(a,v),(-5,30))
