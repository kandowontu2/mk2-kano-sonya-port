"""Candidate collision-core fixtures and falsified-evidence rejection tests."""
import re
import struct
import unittest
from pathlib import Path
from verify_restart_lifecycle import verify_projectile_join

ROOT=Path(__file__).resolve().parents[1]


class ProjectileCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={(t,s,c):(ROOT/f'audit_v291_native_core_{t}_{c}_p{s}/run.log').read_text(encoding='utf-8-sig')
                  for t in ('kano','sonya') for s in (1,2) for c in ('hit','block','miss')}

    def altered(self,tag,key,value,where='',target='kano',scenario='hit'):
        log=self.logs[target,1,scenario];changed=False
        def change(m):
            nonlocal changed
            if changed or where not in m[0]:return m[0]
            new=re.sub(r'(\b'+key+r'=)[^\s]+',lambda n:n[1]+str(value),m[0],count=1)
            changed=new!=m[0];return new
        result=re.sub(r'^MK2_PROJ_CONTACT_'+tag+r' [^\r\n]*',change,log,flags=re.M)
        self.assertTrue(changed,'Mutation must modify actual evidence')
        return result

    def reject(self,log,target='kano',scenario='hit'):
        result=verify_projectile_join(log,target,1,False)
        self.assertFalse(result['passed'],result)

    def test_all_twelve_actual_input_only_contacts(self):
        for (t,s,c),log in self.logs.items():
            r=verify_projectile_join(log,t,s,False);self.assertTrue(r['passed'],((t,s,c),r))
    def test_cold_contacts_cannot_prove_ending(self):
        for (t,s,c),log in self.logs.items():self.assertFalse(verify_projectile_join(log,t,s)['passed'])
    def test_original_wrong_fireball_geometry_is_not_accepted(self):
        self.reject((ROOT/'audit_v291_cold_knife_block/run.log').read_text(encoding='utf-8-sig'))
    def test_full_visual_envelope_duck_regression_is_not_accepted(self):
        self.reject((ROOT/'audit_v291_guarded_geometry_kano_miss_p1/run.log').read_text(encoding='utf-8-sig'))
    def test_false_pass_marker_is_not_contact_evidence(self):
        self.reject(re.sub(r'^MK2_PROJ_CONTACT_(FIELD|EVENT|EFFECT|HEALTH|GEOMETRY|OWNER|CONTROL)[^\r\n]*\r?\n','',self.logs['kano',1,'hit'],flags=re.M))
    def test_real_stock_descriptor_region_required(self):self.reject(self.altered('STOCK','checksum','00000000'))
    def test_real_donor_core_width_required(self):self.reject(self.altered('DESCRIPTOR','width',70))
    def test_real_donor_core_height_required(self):self.reject(self.altered('DESCRIPTOR','height',63))
    def test_actual_original_damage_preserved(self):self.reject(self.altered('DESCRIPTOR','damage','1F06'))
    def test_actual_component_pixels_geometry_not_replaced(self):self.reject(self.altered('COMPONENT','dx',-1))
    def test_facing_aware_native_rectangles_required(self):self.reject(self.altered('GEOMETRY','attack_min','00000000'))
    def test_actual_converted_pivot_origin_required(self):self.reject(self.altered('EFFECT','x',497))
    def test_detached_child_must_keep_own_identity(self):self.reject(self.altered('EFFECT','id',0))
    def test_native_creation_owner_required(self):self.reject(self.altered('OWNER','main_owner','01000000'))
    def test_own_live_actor_required(self):self.reject(self.altered('FIELD','id',0))
    def test_human_controller_required(self):self.reject(self.altered('FIELD','state',0))
    def test_every_actual_field_required(self):
        self.reject(re.sub(r'^MK2_PROJ_CONTACT_FIELD[^\r\n]*\r?\n','',self.logs['kano',1,'hit'],count=1,flags=re.M))
    def test_actual_native_damage_writer_required(self):self.reject(self.altered('HEALTH','pc','FF80DB40'))
    def test_damage_must_come_from_actual_child(self):self.reject(self.altered('HEALTH','a8','01034E90'))
    def test_actual_health_ledger_required(self):self.reject(self.altered('FIELD','hp',160,'age=100 '))
    def test_health_assistance_rejected(self):self.reject(self.altered('HEALTH','writes',1))
    def test_native_retirement_instruction_required(self):self.reject(self.altered('EVENT','pc','FF80DB40','kind=cleanup '))
    def test_actual_cleanup_timing_required(self):self.reject(self.altered('EVENT','age',500,'kind=cleanup '))
    def test_original_sound_request_required(self):self.reject(self.altered('EVENT','a0','00000064','kind=sound '))
    def test_input_pulse_only_evidence_required(self):self.reject(self.altered('CONTROL','button','hk'))
    def test_both_fighters_recover(self):self.reject(self.altered('FIELD','action','0604','age=600 '))
    def test_original_game_read_taps_prove_donor_core_indices(self):
        program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        def ptr(a):return struct.unpack_from('<I',program,(a-0xff800000)//8)[0]
        for name,fighter,index,address,geometry in [('knife',0,21,0xffa5b590,(35,-24,51,50)),('ring',1,18,0xffa5a9a0,(108,35,36,11))]:
            self.assertEqual(ptr(ptr(0xffa516d0+fighter*32)+index*32),address)
            self.assertEqual(struct.unpack_from('<4h',program,(address-0xff800000)//8),geometry)
            case=ROOT/f'audit_v291_original_{name}_duck'
            log=(case/'run.log').read_text(encoding='utf-8-sig')
            self.assertIn(f'MK3_KNIFE_DESCRIPTOR address={address:08X} edge={geometry[0]} top={geometry[1]} width={geometry[2]} height={geometry[3]} writes=0',log)
            self.assertIn('kind=lookup pc=FFA516D0',log)
            self.assertIn('kind=rectangle pc=FFA5CC40',log)
            self.assertNotIn('MK3_KNIFE_HEALTH',log)
            self.assertIn(f'slot=1 actor=',log)
            archived=(case/'input_sources/mk3_knife_geometry_reference.lua').read_text()
            self.assertNotIn(':write_',archived)
            self.assertIn('P2 Down',archived)


if __name__=='__main__':unittest.main()
