import unittest
from inspect_stomp_refresh import validate_walk_requests


class WalkRequestsTests(unittest.TestCase):
    def test_requires_actual_direction_and_no_jump_request(self):
        self.assertEqual(validate_walk_requests([dict(up='0',direction='P1 Left')]),1)
        for rows in ([],[dict(up='1',direction='P1 Left')],[dict(up='0',direction='P1 Up')]):
            with self.assertRaises(AssertionError):validate_walk_requests(rows)


if __name__=='__main__':unittest.main()
