import unittest
from compare_campaign_extension import compare,verify_profiles

class Extension(unittest.TestCase):
    def test_finale_window_changes_observation_only(self):
        old=['--campaign-full','--campaign-extended','--campaign-ending-window','--sonya','--campaign-continues=32']
        new=old+['--campaign-finale-window']
        report=verify_profiles(dict(testArguments=old),dict(testArguments=new),dict(reason='field-budget',frame='150000'))
        self.assertEqual(report['extensionType'],'150000-to-180000-fields')
        with self.assertRaises(AssertionError):
            verify_profiles(dict(testArguments=old),dict(testArguments=new+['--campaign-defense']),dict(reason='field-budget',frame='150000'))
        with self.assertRaises(AssertionError):
            verify_profiles(dict(testArguments=old),dict(testArguments=new),dict(reason='field-budget',frame='120000'))

    def test_ending_window_requires_unchanged_strategy_and_explicit_cap(self):
        args=['--campaign-full','--campaign-extended','--sonya','--campaign-continues=20']
        later=args[:-1]+['--campaign-ending-window','--campaign-extra-continues','--campaign-continues=32']
        report=verify_profiles(dict(testArguments=args),dict(testArguments=later),dict(reason='field-budget',frame='120000'))
        self.assertTrue(report['paidContinueBudgetChanged'])
        self.assertEqual(report['newContinueLimit'],32)
        with self.assertRaises(AssertionError):
            verify_profiles(dict(testArguments=args),dict(testArguments=later+['--campaign-defense']),dict(reason='field-budget',frame='120000'))
        with self.assertRaises(AssertionError):
            verify_profiles(dict(testArguments=args),dict(testArguments=[a for a in later if a!='--campaign-extra-continues']),dict(reason='field-budget',frame='120000'))
        with self.assertRaises(AssertionError):
            verify_profiles(dict(testArguments=args),dict(testArguments=later),dict(reason='left-campaign',frame='120000'))

    def test_exact_prefix_is_required(self):
        old=['frame,hp\n','2,161\n','4,150\n']
        report=compare(old,old+['6,140\n'])
        self.assertEqual(report['identicalThroughFrame'],4)
        self.assertEqual(report['identicalPreviousDataRows'],2)
        self.assertFalse(report['extendedOutcomeVerified'])

    def test_changed_earlier_state_rejects(self):
        with self.assertRaises(AssertionError):
            compare(['frame,hp\n','2,161\n'],['frame,hp\n','2,160\n','4,150\n'])

    def test_same_length_is_not_an_extension(self):
        rows=['frame,hp\n','2,161\n']
        with self.assertRaises(AssertionError):compare(rows,rows)

    def test_changed_columns_reject(self):
        with self.assertRaises(AssertionError):
            compare(['frame,hp\n','2,161\n'],['frame,health\n','2,161\n','4,150\n'])

if __name__=='__main__':unittest.main()
