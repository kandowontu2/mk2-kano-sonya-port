"""Synthetic codec tests, including malformed inputs and the reserved EOF offset."""
import random
import unittest
from ips_codec import create_patch,apply_patch,RESERVED

class IPSTests(unittest.TestCase):
    def roundtrip(self,a,b): self.assertEqual(apply_patch(a,create_patch(a,b)),b)
    def test_equal_empty_truncate_extend(self):
        for a,b in [(b'',b''),(b'abc',b'abc'),(b'abcdef',b'a'),(b'a',b'a'+bytes(300)),(b'',bytes(70000))]:
            self.roundtrip(a,b)
    def test_literal_and_rle_boundaries(self):
        self.roundtrip(b'x'*140000,b'z'*140000)
        self.roundtrip(bytes(140000),bytes(range(256))*546+bytes(224))
    def test_reserved_eof_address(self):
        a=bytes(RESERVED+16);b=bytearray(a);b[RESERVED]=123
        self.roundtrip(a,bytes(b))
    def test_random(self):
        rng=random.Random(321)
        for _ in range(80):
            a=rng.randbytes(rng.randrange(0,4000));b=bytearray(a)
            for _ in range(20):
                if b: b[rng.randrange(len(b))]=rng.randrange(256)
            self.roundtrip(a,bytes(b))
    def test_malformed(self):
        for patch in [b'',b'PATCH',b'PATCHEO',b'PATCH\0\0\0\0\2x',
                      b'PATCH\0\0\0\0\0\0\0xEOF',b'PATCHEOFjunk',
                      b'PATCH\xff\xff\xff\0\2xxEOF']:
            with self.assertRaises(ValueError): apply_patch(b'',patch)

if __name__=='__main__': unittest.main()
