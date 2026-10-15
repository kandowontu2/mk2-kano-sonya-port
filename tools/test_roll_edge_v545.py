"""Current native edge fit and non-vacuous malformed-evidence checks."""
import re
import unittest
import verify_roll_edge_v545 as audit
import verify_human_special_negative_v5 as n

class Edge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log=(n.ROOT/'audit_v546_cannonball_duck_p1_liu_kang/run.log').read_text(encoding='utf-8-sig')
        n.verify_log(cls.log,'ball',1,'miss','liu_kang')
    def reject(self,tag,key=None,value=None,predicate=lambda line:True):
        changed=False
        def replace(m):
            nonlocal changed
            if changed or not predicate(m[0]):return m[0]
            changed=True
            return '' if key is None else re.sub(r'(\b'+key+r'=)[^\s]+',lambda r:r[1]+value,m[0],count=1)
        log=re.sub(r'^MK2_HSPECIAL_'+tag+r' [^\r\n]*',replace,self.log,flags=re.M)
        self.assertTrue(changed and log!=self.log)
        with self.assertRaises(ValueError):n.verify_log(log,'ball',1,'miss','liu_kang')
    def test_exact_source_operand_and_native_comparisons(self):self.assertEqual(audit.source_delta({})['operandAfter'],8)
    def test_targets_and_unresolved_contacts_are_distinguished(self):
        r=audit.verify_targets({});self.assertTrue(r['targetedCorrectionVerified']);self.assertFalse(r['fullPortAcceptance']);self.assertEqual(len(r['unresolvedDuckContacts']),5)
    def test_actual_edge_miss(self):
        g=next(x for x in n.rows(self.log,'GEOMETRY') if x['frame']==1627)
        self.assertEqual(g['attack_max']>>16,g['victim_min']>>16)
        self.assertEqual(n.verify_log(self.log,'ball',1,'miss','liu_kang')['nativeContactDamage'],0)
    def test_old_contact_is_not_reclassified(self):
        old=(n.ROOT/'audit_v518_cannonball_duck_p1_liu_kang/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaises(ValueError):n.verify_log(old,'ball',1,'miss','liu_kang')
    def test_missing_rectangle(self):self.reject('GEOMETRY')
    def test_old_bottom_plane(self):self.reject('GEOMETRY','attack_max','008A02D6',lambda l:'frame=1627 ' in l)
    def test_actual_overlap_without_damage_rejected(self):self.reject('GEOMETRY','victim_min','00880285',lambda l:'frame=1627 ' in l)
    def test_wrong_native_pc(self):self.reject('GEOMETRY','pc','00000000')
    def test_proxy_identity(self):self.reject('FIELD','id','1',lambda l:'slot=1 ' in l)
    def test_missing_recovery(self):self.reject('RECOVERED')
    def test_wrong_speed(self):self.reject('GEOMETRY','vx','00050000')
    def test_false_duck(self):self.reject('GEOMETRY','victim_action','0303')
    def test_missing_actual_input(self):self.reject('INPUT',predicate=lambda l:'button=Down' in l and 'frame=1627 ' in l)

if __name__=='__main__':unittest.main()
