import unittest
from qualify_ending_capture import static_state

def rows():
    return [dict(age=str(age),displayon='1',noflip='65535',autoerase='0',
                 objlst='00000000',objlst2='00000000',pageaddr='00000038',
                 scrntl='00000000',scrnlr='00fe0190') for age in range(1734,1746)]

class StaticEnding(unittest.TestCase):
    def test_native_frozen_page_state(self):static_state(rows())

    def test_flip_erase_active_lists_and_changed_view_are_rejected(self):
        for change in ({'noflip':'0'},{'autoerase':'1'},{'displayon':'0'},
                       {'objlst2':'0102d6f0'},{'pageaddr':'01000038'},
                       {'scrnlr':'00000000'},{'age':'1747'}):
            case=rows();case[5].update(change)
            with self.assertRaises(AssertionError):static_state(case)

    def test_missing_or_duplicate_frames_are_rejected(self):
        with self.assertRaises(AssertionError):static_state(rows()[:-1])
        case=rows();case[5]=case[4]
        with self.assertRaises(AssertionError):static_state(case)

if __name__=='__main__':unittest.main()
