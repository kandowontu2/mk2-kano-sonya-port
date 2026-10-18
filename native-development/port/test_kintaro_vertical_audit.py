import unittest
from inspect_kintaro_vertical import valid_request


class VerticalRequestTests(unittest.TestCase):
    def test_only_ready_grounded_requests_pass(self):
        row=dict(decision='upkick',distance='110',ownAction='771',ownFlags='1',ownHeight='0',
                 bodyHeight='130',buttonTable='123',stanceTable='123',ownHP='161')
        self.assertTrue(valid_request(row))
        for field,value in (('ownAction','0'),('ownFlags','4'),('ownHeight','2'),
                            ('bodyHeight','90'),('buttonTable','456'),('distance','116'),('ownHP','0')):
            self.assertFalse(valid_request(dict(row,**{field:value})),field)


if __name__=='__main__':unittest.main()
