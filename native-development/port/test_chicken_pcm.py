import hashlib
import unittest
from prepare_chicken_pcm import encode,ROOT

class ChickenPCM(unittest.TestCase):
    def test_four_captured_inputs(self):
        expected={
            'a5':(10187,'61FF1F22BBE6E586881E33F0EEF19770708B98897B843BFF3FC193DEF8FAF7C6','2CB72F850124AF01035FF7D8B5B5F43A83EF98D297E52524E9479859DE3C0A76'),
            'aa':(14023,'097B4E38BC35DDFF499F12121F10613AD69C9ED8A33BB54EE76DD0C24B96763E','AB544B4E8485FF0606B190F9BE519F609E15DCE8AB9E50196B26605CFFECCFF5'),
            'af':(12321,'1C8C42329AEB8B95F2BFC299DB020E34B5051F1A8815629EFC0FC134B75F73C6','60BEAC9A43075DA6A0EF68F9A1BAB964603A7064ED530495E0FE0CDA27C6A02C'),
            '96':(11390,'EA5BF1A631AA43CD371DEA6D77A20598E75454629C599498A7B9A9784BC54864','FB7F5564F526C7F456D8DCCB9A3DB1A67F1BBC318E658AD64233DCC2EE64EA58')}
        for suffix,(count,source,pcm) in expected.items():
            with self.subTest(suffix=suffix):
                data,metadata=encode(ROOT/'samples/mk2ks'/f'sonya_chicken_{suffix}.wav')
                self.assertEqual(metadata['sourceSHA256'],source)
                self.assertEqual(metadata['unpaddedSamples'],count)
                self.assertEqual(len(data)//2%240,0)
                self.assertFalse(any(data[count*2:]))
                self.assertEqual(hashlib.sha256(data[:count*2]).hexdigest().upper(),pcm)

if __name__=='__main__':unittest.main()
