import io
import unittest
from unittest.mock import MagicMock
from finisher_morph_identity import verify

class MorphIdentity(unittest.TestCase):
    def run_case(self,selected=6,actual=17,prior=6):
        folder=MagicMock()
        folder.__truediv__.return_value.open.return_value=io.StringIO(
            'frame,selected,actual,winner,death,action\n'
            f'10,6,{prior},3,0,771\n20,{selected},{actual},3,1,540\n')
        return verify(folder,[dict(frame='20')],17)

    def test_selected_shang_is_not_active_kano_proof(self):
        self.assertTrue(self.run_case()['transformedFinisher'])
        for change in ({'selected':17},{'actual':6},{'actual':18},{'prior':17}):
            with self.assertRaises(AssertionError): self.run_case(**change)

if __name__=='__main__':unittest.main()
