"""Evidence collection must not turn missing, false or numeric gates into passes."""
import unittest
from prepare_native_release_evidence import require_report


class ReleaseEvidenceTests(unittest.TestCase):
    def test_exact_true_gate_and_count(self):
        require_report({'passed': True, 'cases': [{}, {}]}, ['passed'], 2)

    def test_missing_false_and_integer_are_not_passes(self):
        for value in [None, False, 1, 'true']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                require_report({'passed': value}, ['passed'])

    def test_case_count_required(self):
        for data in [{}, {'cases': [{}]}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                require_report(data, count=2)


if __name__ == '__main__':
    unittest.main()
