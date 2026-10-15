"""Reject corrupted proof of the actual Pit lookup/cache overrun defect."""
import unittest
import verify_pit_lookup_defect_v545 as v

class ProofBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log=(v.ROOT/'audit_v592_pit_actual_lookup_kano_p1/run.log').read_text(encoding='utf-8-sig')

    def reject_row(self,tag,selector,old,new):
        selectors=(selector,)if isinstance(selector,str)else selector
        selected=[line for line in self.log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')and all(s in line for s in selectors)]
        self.assertEqual(len(selected),1)
        self.assertIn(old,selected[0])
        changed=self.log.replace(selected[0],selected[0].replace(old,new))
        self.assertNotEqual(changed,self.log)
        self.assertTrue(v.contract(changed))

    def test_actual_baseline(self):self.assertFalse(v.contract(self.log))
    def test_missing_lookup(self):
        self.assertTrue(v.contract('\n'.join(line for line in self.log.splitlines()if not line.startswith('MK2_NAT_CAMPAIGN_PIT_LOOKUP '))))
    def test_wrong_id(self):self.reject_row('PIT_LOOKUP','frame=16784','id=17','id=1')
    def test_wrong_native_pc(self):self.reject_row('PIT_LOOKUP','frame=16784','pc=FF83B850','pc=FF83B840')
    def test_wrong_table_cell(self):self.reject_row('PIT_LOOKUP','frame=16784','at=FF85E8D0','at=FF85E8B0')
    def test_wrong_actual_value(self):self.reject_row('PIT_LOOKUP','frame=16784','value=00000001','value=FF85EDB0')
    def test_wrong_drawable(self):self.reject_row('PIT_LOOKUP','frame=16784','a8=0102D6F0','a8=01034020')
    def test_wrong_main(self):self.reject_row('PIT_LOOKUP','frame=16784','a13=0106AA60','a13=01069590')
    def test_wrong_scene_stream(self):self.reject_row('DRAW','entry=FF85C420','a9=00000001','a9=FF85EDB0')
    def test_wrong_component_destination(self):self.reject_row('DRAW',('frame=16785','entry=FF838790'),'cache=0105ED30','cache=0105ED50')
    def test_sonya_alias_removed(self):self.reject_row('PIT_ROM',' id=18 ','value=FF85E830','value=00000000')
    def test_health_target_wrong(self):self.reject_row('HEALTH',('frame=16785','slot=1'),'at=010602F0','at=010602E0')
    def test_health_store_not_native(self):self.reject_row('HEALTH',('frame=16785','slot=1'),'pc=FF838A10','pc=FF836700')
    def test_fake_reset(self):self.reject_row('BOUNDARY','frame=16955','entry=FFFFFFE0','entry=FF85CB10')
    def test_assistance_not_allowed(self):
        self.assertTrue(v.contract(self.log.replace('writes=0 assistance=none','writes=1 assistance=health')))
    def test_duplicate_callbacks_not_allowed(self):
        self.assertTrue(v.contract(self.log+'\n'+self.log))

if __name__=='__main__':unittest.main()
