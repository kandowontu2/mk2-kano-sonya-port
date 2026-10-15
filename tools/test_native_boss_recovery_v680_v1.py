"""In-memory corruptions of retained native boss recovery captures."""
import re
import unittest
from verify_native_boss_recovery_v680_v1 import ROOT, verify


class RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / 'audit_v710_boss_stomp_kano_p2'
        cls.text = (cls.folder / 'run.log').read_text(encoding='utf-8-sig')

    def check(self, text):
        return verify(self.folder, check_hashes=False, text_override=text)

    def reject(self, pattern, replacement):
        changed, count = re.subn(pattern, replacement, self.text, count=1, flags=re.M)
        self.assertEqual(count, 1, 'Mutation must hit actual evidence')
        self.assertFalse(self.check(changed)['passed'])

    def test_all_six_baselines(self):
        for folder in sorted(ROOT.glob('audit_v710_boss_stomp_*')):
            with self.subTest(case=folder.name):
                report = verify(folder, check_hashes=False)
                self.assertTrue(report['passed'], report['errors'])
                self.assertFalse(report['unassisted_clear_proven'])
                self.assertFalse(report['fullPortAcceptance'])
                self.assertEqual(report['native_held_fields'], 148 + report['human_slot'])

    def test_setup_during_live_match(self): self.reject(r'(BOSS_SETUP[^\n]*mode=)4 ', r'\g<1>2 ')
    def test_setup_wrong_character(self): self.reject(r'(BOSS_SETUP[^\n]*own_roster=)17 ', r'\g<1>1 ')
    def test_setup_cpu_already_constructed(self): self.reject(r'(BOSS_SETUP[^\n]*cpu_roster=)65535 ', r'\g<1>12 ')
    def test_fixture_not_single(self): self.reject(r'(BOSS_RESULT[^\n]*prep_writes=)1 ', r'\g<1>2 ')
    def test_boss_health_assisted(self): self.reject(r'(BOSS_BEGIN[^\n]*health_writes=)0', r'\g<1>1')
    def test_wrong_native_damage_writer(self): self.reject(r'(BOSS_STOMP[^\n]*pc=)FF836700', r'\g<1>FF836710')
    def test_wrong_A8_victim(self): self.reject(r'(BOSS_STOMP[^\n]*attacker=)01038A60', r'\g<1>01038850')
    def test_wrong_execution_Main(self): self.reject(r'(BOSS_STOMP[^\n]*attacker_main=)0106CD10', r'\g<1>0106D400')
    def test_missing_actual_store(self): self.reject(r'^MK2_NAT_CAMPAIGN_HEALTH[^\n]*frame=1666[^\n]*slot=2[^\n]*after=65[^\n]*\n', '')
    def test_missing_held_field(self): self.reject(r'^MK2_NAT_CAMPAIGN_BOSS_FIELD[^\n]*age=120 slot=2[^\n]*\n', '')
    def test_false_physical_slot(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=)2 ', r'\g<1>1 ')
    def test_wrong_true_id(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=2[^\n]*id=)17 ', r'\g<1>1 ')
    def test_wrong_owner(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=2[^\n]*owner=)01038A60', r'\g<1>01038850')
    def test_new_round_health_not_recovery(self): self.reject(r'(BOSS_FIELD[^\n]*age=150 slot=2[^\n]*hp=)65 ', r'\g<1>161 ')
    def test_wrong_saved_wait_callback(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=2[^\n]*0E0:)FF8392B0', r'\g<1>FF82F270')
    def test_wrong_waited_action(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=2[^\n]*060:)00000407', r'\g<1>00000408')
    def test_wrong_waited_Main(self): self.reject(r'(BOSS_FIELD[^\n]*age=0 slot=2[^\n]*170:)0106CD10', r'\g<1>0106D400')
    def test_premature_boss_release(self): self.reject(r'(BOSS_FIELD[^\n]*age=148 slot=1[^\n]*action=)0407', r'\g<1>0000')
    def test_wrong_recovery_entry_PC(self): self.reject(r'(BOSS_ENTRY[^\n]*pc=)FF861360', r'\g<1>FF861370')
    def test_wrong_recovery_owned_Main(self): self.reject(r'(BOSS_ENTRY[^\n]*a13=)0106D400', r'\g<1>0106CD10')
    def test_missing_ordinary_input(self): self.reject(r'^MK2_NAT_CAMPAIGN_INPUT[^\n]*frame=1818[^\n]*button=Right[^\n]*\n', '')
    def test_no_actual_movement(self): self.reject(r'(BOSS_FIELD[^\n]*age=152 slot=2[^\n]*x=)876 ', r'\g<1>874 ')
    def test_runtime_error(self): self.assertFalse(self.check(self.text + '\n[LUA ERROR] broken observer\n')['passed'])
    def test_forbidden_guest_write_source(self):
        source = (self.folder / 'input_sources/mk2ks_native_boss_recovery_v680_v3.lua').read_text()
        report = verify(self.folder, check_hashes=False, source_override=source + '\np:write_u16(0x010602f0,161)\n')
        self.assertFalse(report['passed'])


if __name__ == '__main__': unittest.main()
