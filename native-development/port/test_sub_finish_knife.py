import unittest
from inspect_sub_neutral_uppercut import knife_case


class FinishKnifeEvidence(unittest.TestCase):
    def rows(self):
        rows={f:dict(phase='guard', hp='0', lp='0', down='0', away='0', toward='0', block='0',
                     ownAction='771', bodyHeight='68',buttonTable='1234',duckTable='1234')
              for f in range(93,109)}
        rows[93]['phase']='knife_prepare'
        for f in range(94,97):rows[f].update(phase='knife_down',down='1')
        for f in range(97,100):rows[f].update(phase='knife_back',away='1')
        rows[100].update(phase='knife_punch',hp='1')
        return rows

    def test_command_is_not_activation(self):
        rows=self.rows()
        self.assertFalse(knife_case(rows,100)['nativeKnifeWithin8'])
        rows[102]['ownAction']=str(0x211)
        self.assertTrue(knife_case(rows,100)['nativeKnifeWithin8'])

    def test_wrong_back_or_down_rejected(self):
        for frame,key in ((98,'away'),(95,'down')):
            rows=self.rows();rows[frame][key]='0'
            with self.assertRaises(AssertionError):knife_case(rows,100)

    def test_truncated_window_unknown(self):
        rows={f:r for f,r in self.rows().items() if f<=100}
        self.assertIsNone(knife_case(rows,100)['nativeKnifeWithin8'])

    def test_spaced_standing_recipe(self):
        rows=self.rows()
        rows.update({f:dict(rows[93]) for f in range(88,93)})
        for f in range(88,100):
            rows[f].update(hp='0',down='0',away='0')
        for f in range(88,91):rows[f].update(phase='knife_down',down='1')
        rows[88].update(bodyHeight='124',buttonTable='5678')
        for f in range(91,94):rows[f]['phase']='knife_gap_down'
        for f in range(94,97):rows[f].update(phase='knife_back',away='1')
        for f in range(97,100):rows[f]['phase']='knife_gap_back'
        self.assertEqual(knife_case(rows,100)['recipe'],'spaced-standing')
        rows[98]['down']='1'
        with self.assertRaises(AssertionError):knife_case(rows,100)


if __name__=='__main__':unittest.main()
