import unittest
from fetch_stock_mame_source import SIZE,check_chunk


class SourceFetchTests(unittest.TestCase):
    def test_download_is_bounded_by_published_size(self):
        self.assertEqual(check_chunk(SIZE-3,b'abc'),SIZE)
        with self.assertRaises(AssertionError):check_chunk(SIZE,b'x')
        with self.assertRaises(AssertionError):check_chunk(-1,b'x')


if __name__=='__main__':unittest.main()
