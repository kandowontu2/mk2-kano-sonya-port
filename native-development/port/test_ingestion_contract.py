import unittest
from ingestion_contract import extract, number


class IngestionContractTests(unittest.TestCase):
    def test_typed_numbers(self):
        self.assertEqual(number('-24'), -24)
        self.assertEqual(number('045H'), 69)

    def test_composite_union_and_final_fragment(self):
        report = extract()
        frames = report['sequences']['female_ninja']
        self.assertEqual(frames[0]['unionBounds'], [-129, 13, -46, 136])
        self.assertEqual(frames[0]['unionWidth'], 83)
        self.assertEqual(frames[-1]['unionBounds'], [-63, 11, -45, 21])
        self.assertEqual([len(f['components']) for f in frames], [2,2,2,1,1,1,1,1])
        self.assertEqual(report['frameDelay'], 4)
        self.assertEqual(report['preAnimationShakeFields'], 24)


if __name__ == '__main__':
    unittest.main()
