"""Actual passing contact/miss baselines plus independent-source corruptions."""
import re
import struct
import unittest
import inspect_roll_turn_contacts_v545 as v

class TurnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=(v.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        cls.payload=(v.ROOT/v.build.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.cases={}
        for victim in ('kitana','mileena','raiden'):
            for side in (1,2):
                fresh=(v.ROOT/f'audit_v574_roll_pose_p{side}_{victim}'/'run.log').read_text(encoding='utf-8-sig')
                prior=(v.ROOT/f'audit_v547_cannonball_duck_p{side}_{victim}'/'run.log').read_text(encoding='utf-8-sig')
                proof=v.inspect_log(fresh,prior,side,victim,cls.original,cls.payload)
                if proof['nativeContactDamage']!=(0 if victim=='raiden'and side==2 else 24):raise AssertionError('Nonvacuous actual baseline')
                cls.cases[side,victim]=(fresh,prior)

    def inspect(self,fresh,prior,side=1,victim='kitana'):
        return v.inspect_log(fresh,prior,side,victim,self.original,self.payload)

    def mutate(self,tag,role,key,value,side=1,victim='kitana'):
        fresh,prior=self.cases[side,victim];lines=fresh.splitlines()
        match=next(i for i,line in enumerate(lines)if line.startswith('MK2_BALL_V2_'+tag+' ')and(role is None or 'role='+role+' 'in line))
        self.assertRegex(lines[match],r'\b'+key+r'=\S+')
        lines[match]=re.sub(r'\b'+key+r'=\S+',key+'='+value,lines[match],count=1)
        return '\n'.join(lines),prior

    def reject(self,fresh,prior,side=1,victim='kitana'):
        with self.assertRaises(ValueError):self.inspect(fresh,prior,side,victim)

    def test_six_actual_baselines(self):
        for (side,victim),(fresh,prior)in self.cases.items():
            with self.subTest(side=side,victim=victim):
                proof=self.inspect(fresh,prior,side,victim)
                self.assertFalse(proof['contactFidelityAccepted']);self.assertFalse(proof['planeCorrectionClaim'])
                self.assertFalse(proof['fullPortAcceptance']);self.assertEqual(proof['fields'],910)

    def test_contacts_are_not_accepted_misses(self):
        for key,(fresh,_)in self.cases.items():
            side,victim=key
            if key==(2,'raiden'):continue
            with self.subTest(side=side,victim=victim):
                with self.assertRaisesRegex(ValueError,'Own special contact damage'):
                    v.native.verify_log(fresh,'ball',side,'miss',victim)

    def test_miss_cannot_be_declared_contact(self):
        fresh,_=self.cases[2,'raiden']
        with self.assertRaisesRegex(ValueError,'Own special contact damage'):
            v.native.verify_log(fresh,'ball',2,'miss','raiden',duck_contact=True)

    def test_contact_flag_for_other_move_rejected(self):
        with self.assertRaisesRegex(ValueError,'Explicit roll/held-duck contact'):
            v.native.verify_log(self.cases[1,'kitana'][0],'leg',1,'miss','kitana',duck_contact=True)

    def test_changed_fixture_rejected(self):
        fresh,prior=self.cases[1,'kitana'];line=next(l for l in fresh.splitlines()if l.startswith('MK2_HSPECIAL_INPUT '))
        self.reject(fresh.replace(line,'',1),prior)

    def test_wrong_comparison_phase(self):
        fresh,prior=self.cases[1,'kitana'];self.reject(fresh.replace('phase=done','phase=before',1),prior)

    def test_missing_actor(self):
        fresh,prior=self.cases[1,'kitana'];line=next(l for l in fresh.splitlines()if l.startswith('MK2_BALL_V2_ACTOR '))
        self.reject(fresh.replace(line,'',1),prior)

    def test_missing_component(self):
        fresh,prior=self.cases[1,'kitana'];line=next(l for l in fresh.splitlines()if l.startswith('MK2_BALL_V2_PART ')and 'role=victim 'in l)
        self.reject(fresh.replace(line,'',1),prior)

    def test_old_mislabelled_main_as_cache(self):
        self.reject(*self.mutate('ACTOR','own','cache','0106B150'))

    def test_stale_callback_x_not_instruction_x(self):
        self.reject(*self.mutate('ACTOR','own','x','529'))

    def test_original_stock_descriptor_corruption(self):
        fresh,prior=self.cases[1,'kitana']
        original=bytearray(self.original)
        actor=next(a for a in v.rows(fresh,'ACTOR')if a['role']=='victim')
        ptr=struct.unpack_from('<I',original,(actor['pose']-0xff800000)//8)[0]
        at=(ptr-0xff800000)//8
        struct.pack_into('<H',original,at,struct.unpack_from('<H',original,at)[0]+1)
        with self.assertRaises(ValueError):v.inspect_log(fresh,prior,1,'kitana',original,self.payload)

    def test_first_contact_shared_edge_is_not_hit(self):
        fresh,prior=self.cases[1,'kitana']
        # At contact the native attack max Y is137 and victim min Y is136.
        # Move it to equality in BOTH redundant comparison records; the
        # native health store remains24 and must not be fitted as a valid hit.
        before='attack_max=008902D6';after='attack_max=008802D6'
        self.assertIn(before,fresh)
        fresh=fresh.replace(before,after);prior=prior.replace(before,after)
        self.reject(fresh,prior)

    def test_native_health_writer_changed(self):
        fresh,prior=self.cases[1,'kitana']
        fresh=fresh.replace('pc=FF836700','pc=FFF82200');prior=prior.replace('pc=FF836700','pc=FFF82200')
        self.reject(fresh,prior)

def mutation(tag,role,key,value):
    def test(self):self.reject(*self.mutate(tag,role,key,value))
    return test

for name,args in {
    'wrong_comparator_pc':('GEOMETRY',None,'pc','FF835B70'),
    'wrong_comparator_owner':('GEOMETRY',None,'actor','010350A0'),
    'wrong_comparator_bounds':('GEOMETRY',None,'bounds','0'),
    'wrong_victim_pointer':('GEOMETRY',None,'victim','01034E90'),
    'wrong_actor_id':('ACTOR','own','id','1'),
    'wrong_actor_main':('ACTOR','own','main','01068EA0'),
    'wrong_actor_owner':('ACTOR','victim','owner','01034E90'),
    'wrong_main_flags':('ACTOR','own','flags','0000'),
    'wrong_body_flags':('ACTOR','own','body','0012'),
    'wrong_actual_pose':('ACTOR','victim','pose','FF94B660'),
    'wrong_floor':('ACTOR','victim','floor','82'),
    'wrong_actual_action':('ACTOR','victim','action','0303'),
    'introduced_y_flip':('ACTOR','victim','facing','8032'),
    'changed_cache_width':('PART','victim','width','1'),
    'changed_cache_height':('PART','victim','height','1'),
    'changed_cache_offset':('PART','victim','dy','0'),
    'changed_cache_source':('PART','victim','source','102B66B4'),
    'changed_cache_command':('PART','victim','command','65B0'),
    'changed_component_order':('PART','victim','part','1'),
    'guest_write':('ACTOR','own','writes','1'),
    'wrong_snapshot_phase':('SNAPSHOT',None,'phase','before'),
    'wrong_snapshot_field':('SNAPSHOT',None,'frame','1615'),
}.items():setattr(TurnTests,'test_'+name,mutation(*args))

if __name__=='__main__':unittest.main()
