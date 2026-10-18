import unittest
from split_contract import extract


class SplitContractTests(unittest.TestCase):
    def test_script_parts_and_synchronization(self):
        report=extract()
        for poses in report['sequences'].values():
            self.assertEqual(len(poses),10)
            self.assertEqual([p['part'] for p in poses],['together']*3+['peel']*7)
            self.assertTrue(all(p['width']>0 and p['height']>0 for p in poses))
        self.assertTrue(report['secondaryPeelPointerReplacedByRestoredPrimaryPointer'])
        self.assertFalse(report['ownStanceReplacementRequiredByThisContract'])

    def test_component_unions_are_exact(self):
        for poses in extract()['sequences'].values():
            for p in poses:
                for w,h,x,y in p['headers']:
                    l,t,r,b=p['unionBounds']
                    self.assertLessEqual(l,-x)
                    self.assertLessEqual(t,-y)
                    self.assertGreaterEqual(r,w-x)
                    self.assertGreaterEqual(b,h-y)
                self.assertEqual(p['xOffset'],-p['unionBounds'][0])
                self.assertEqual(p['yOffset'],-p['unionBounds'][1])


if __name__=='__main__':unittest.main()
