"""Reject malformed native row stepping using actual v635 runtime evidence."""
import copy
import unittest
from unittest.mock import patch
import inspect_native_shadow_rows_v635 as v
from verify_native_ui_flow_v635 import ROOT


class NativeRows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / 'audit_v636_native_shadow_sonya_p2'
        cls.actual = v.data(cls.folder)

    def test_both_p2_observed_streams(self):
        for fighter in ('kano', 'sonya'):
            result = v.inspect(ROOT / f'audit_v636_native_shadow_{fighter}_p2')
            self.assertTrue(result['rowStreamVerified'])
            self.assertGreater(result['checked_copies'], 5000)
            self.assertFalse(result['fullPortAcceptance'])

    def test_both_p1_owned_and_mirror_streams(self):
        for fighter in ('kano', 'sonya'):
            result = v.inspect(ROOT / f'audit_v639_native_shadow_rows_{fighter}_p1')
            self.assertTrue(result['rowStreamVerified'])
            self.assertGreater(result['checked_copies'], 14000)
            self.assertIn([2,18], [list(pair) for pair in result['identities']])

    def test_missing_owned_component(self):
        evidence = copy.deepcopy(self.actual)
        evidence[0]['SHADOW_COMPONENT'].pop()
        with patch.object(v, 'data', return_value=evidence):
            with self.assertRaises(AssertionError): v.inspect(self.folder)

    def test_wrong_owned_fighter(self):
        evidence = copy.deepcopy(self.actual)
        evidence[0]['SHADOW_COMPONENT'][0]['id'] = 1
        with patch.object(v, 'data', return_value=evidence):
            with self.assertRaises(AssertionError): v.inspect(self.folder)

    def test_foreign_component_cache(self):
        evidence = copy.deepcopy(self.actual)
        evidence[0]['SHADOW_COMPONENT'][0]['cache'] += 112
        with patch.object(v, 'data', return_value=evidence):
            with self.assertRaises(AssertionError): v.inspect(self.folder)

    def reject(self, field, delta):
        evidence = copy.deepcopy(self.actual)
        event = evidence[0]['SHADOW_COMPONENT'][1]['event']
        row = next(r for r in evidence[0]['FLOOR_DMA'] if r['event'] == event)
        row[field] += delta
        with patch.object(v, 'data', return_value=evidence):
            result = v.inspect(self.folder)
        self.assertFalse(result['rowStreamVerified'])
        self.assertTrue(result['failures'])

    def test_source_walk_backward(self): self.reject('source', -128)
    def test_one_pixel_x_shift(self): self.reject('x', 1)
    def test_one_pixel_y_shift(self): self.reject('y', 1)
    def test_wrong_native_command(self): self.reject('command', 16)
    def test_wrong_height(self): self.reject('height', 1)
    def test_wrong_width(self): self.reject('width', 1)
    def test_wrong_palette(self): self.reject('palette', 256)
    def test_wrong_color(self): self.reject('color', 1)
    def test_non_native_caller(self): self.reject('pc', 16)


if __name__ == '__main__': unittest.main()
