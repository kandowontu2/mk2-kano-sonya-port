import unittest
from chicken_control_playlist import control_playlist,verify_location_map,verify_sample_rom

def sample():
    return b''.join(f"playlist {n}, {(n-2036)%3+1}, 'Sonya Friendship {(n-2036)//3}'\n 0 setvol {(n-2036)%3+1}, 100\n 0 play SAME.CMP\n".encode() for n in range(2036,2048))

class PlaylistControls(unittest.TestCase):
    def test_sample_payload_and_header_checksum_are_preserved(self):
        source=bytearray(b'U3 10/16/126\0'+b'\x30'+bytes(1048576-14))
        output=source.copy();output[7]+=1;output[13]-=1
        verify_sample_rom(source,output,3)
        output[14]=1
        with self.assertRaises(AssertionError):verify_sample_rom(source,output,3)
        output[14]=0;output[13]+=1
        with self.assertRaises(AssertionError):verify_sample_rom(source,output,3)

    def test_only_generated_location_timestamp_may_change(self):
        source=b'; .LOC file for MK2.DEF, 10/16/126, 11:13:30\r\nACID 123\r\n'
        output=source.replace(b'10/16/126, 11:13:30',b'10/17/126, 21:07:13')
        verify_location_map(source,output)
        with self.assertRaises(AssertionError):verify_location_map(source,output.replace(b'ACID 123',b'ACID 124'))
        with self.assertRaises(AssertionError):verify_location_map(source,output.replace(b'.LOC file',b'OTHER file'))

    def test_only_volume_operands_change_and_one_track_can_remain(self):
        for track in (0,1,2,3):
            data,changed=control_playlist(sample(),track)
            self.assertEqual(len(changed),12 if track==0 else 8)
            self.assertEqual(data.count(b'play SAME.CMP'),12)
            self.assertEqual(data.count(b', 100'),0 if track==0 else 4)
            self.assertEqual(changed,[n for n in range(2036,2048) if (n-2036)%3+1!=track])

    def test_missing_calls_or_wrong_track_rejected(self):
        for bad in (sample().replace(b'playlist 2036',b'playlist 2035'),sample().replace(b'0 setvol 1',b'0 setvol 2',1)):
            with self.assertRaises(AssertionError):control_playlist(bad,1)

if __name__=='__main__':unittest.main()
