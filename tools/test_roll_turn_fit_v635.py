"""Actual current sprite fit/provenance and nonvacuous fitting corruptions."""
import copy
import unittest
import verify_roll_turn_fit_v635 as v


class RollFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.actual=v.verify()
    def test_six_actual_current_cases(self):
        self.assertTrue(self.actual['decision']['observedTurnFitAccepted'])
        self.assertFalse(self.actual['fullPortAcceptance'])
    def reject(self,change):
        cases=copy.deepcopy(self.actual['cases']);change(cases)
        with self.assertRaises(ValueError):v.check_fit(cases)
    def test_missing_mirrored_control(self):self.reject(lambda c:c.pop())
    def test_no_exposed_target_pixels(self):self.reject(lambda c:c[0]['comparison_sprite_rows'][-1]['roles']['victim'].update(pixels_in_positive_comparator_intersection=0))
    def test_proxy_target(self):self.reject(lambda c:c[0]['comparison_sprite_rows'][-1]['roles']['victim'].update(id=8))
    def test_wrong_own_actor(self):self.reject(lambda c:c[0]['comparison_sprite_rows'][-1]['roles']['own'].update(id=1))
    def test_raised_box_above_rolling_art(self):self.reject(lambda c:c[0]['comparison_sprite_rows'][-1].update(attack_top=100,attack_bottom=131))
    def test_no_own_roll_art_inside_box(self):self.reject(lambda c:c[0]['comparison_sprite_rows'][-1]['roles']['own'].update(pixels_in_attack_rectangle=0))
    def test_mirrored_miss_is_not_contact(self):self.reject(lambda c:c[-1]['native']['lastComparison'].update(horizontal=2))
    def test_contact_cannot_be_invented_from_held_down(self):self.reject(lambda c:c[0]['native']['lastComparison'].update(horizontal=-1))


if __name__=='__main__':unittest.main()
