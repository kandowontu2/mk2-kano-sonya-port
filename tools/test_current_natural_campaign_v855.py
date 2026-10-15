"""Current actual Sonya campaign and native ring-entry corruption checks."""
import hashlib
import io
import json
import re
import sys
import unittest
from pathlib import Path
import verify_current_natural_campaign_v854 as v
FOLDER=v.ROOT/'audit_v850_sonya_defensive_leg_p1'


class Campaign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.log=(FOLDER/'run.log').read_text(encoding='utf-8-sig')

    def check(self,text):return v.verify(FOLDER,check_hashes=False,text_override=text)

    def reject(self,pattern,replacement):
        altered,count=re.subn(pattern,replacement,self.log,count=1,flags=re.M)
        self.assertEqual(count,1,'Must alter actual retained evidence')
        self.assertNotEqual(altered,self.log)
        self.assertFalse(self.check(altered)['passed'])

    def test_actual_scout_does_not_clear_tower(self):
        proof=self.check(self.log)
        self.assertTrue(proof['passed'],proof['errors'])
        self.assertEqual(proof['stages_reached'],list(range(10)))
        self.assertEqual(proof['native_own_round_wins'],20)
        self.assertEqual(proof['paid_continue_losses'],6)
        self.assertEqual(proof['native_owned_special_entries'],184)
        self.assertEqual(proof['native_special_moves'],{'leg':184})
        self.assertFalse(proof['unassisted_clear_proven'])
        self.assertFalse(proof['fullPortAcceptance'])

    def test_missing_projectile_entries(self):
        altered=re.sub(r'^MK2_NAT_CAMPAIGN_SPECIAL[^\n]*\n','',self.log,flags=re.M)
        self.assertNotEqual(altered,self.log)
        self.assertFalse(self.check(altered)['passed'])

    def test_cannot_accumulate_wins_across_lost_matches(self):
        rows=v.parse(self.log)
        advance=next(r for r in rows if r['tag']=='STAGE'and r['stage']==1)
        wins=[r for r in rows if r['tag']=='WIN'and r['slot']==1 and r['stage']==0 and r['event']<advance['event']]
        self.assertEqual(len(wins),2)
        chosen=wins[-1]
        line=next(line for line in self.log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_WIN ')
                  and f'frame={chosen["frame"]} 'in line)
        altered=self.log.replace(line+'\n','',1)
        # Repair only terminal read accounting so the advance contract itself,
        # not an incidental summary-count difference, rejects the missing win.
        altered,count=re.subn(r'(MK2_NAT_CAMPAIGN_RESULT[^\n]*native_win_reads=)38',r'\g<1>37',altered)
        self.assertEqual(count,1)
        proof=self.check(altered)
        self.assertFalse(proof['passed'])
        self.assertIn('Advance after two wins in actual successful attempt, not accumulated failed matches',proof['errors'])

    def test_first_stage_cannot_be_forced_to_boss(self):
        self.reject(r'(MK2_NAT_CAMPAIGN_STAGE[^\n]*stage=)0 ',r'\g<1>15 ')

    def test_proxy_human(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*human=)18:18',r'\g<1>1:1')
    def test_wrong_cpu(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*cpu=)18:18',r'\g<1>8:8')
    def test_changed_schedule(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*schedule=)[0-9A-F]+',r'\g<1>00000000')
    def test_invalid_main(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*human_main=)[0-9A-F]+',r'\g<1>00000000')
    def test_missing_winner(self):self.reject(r'^MK2_NAT_CAMPAIGN_WIN[^\n]*\n','')
    def test_wrong_winner_instruction(self):self.reject(r'(MK2_NAT_CAMPAIGN_WIN[^\n]*pc=)FF8296B0',r'\g<1>FF8296C0')
    def test_wrong_win_entry(self):self.reject(r'(MK2_NAT_CAMPAIGN_WIN[^\n]*entry=)FFFEFA40',r'\g<1>FFFEFA20')
    def test_non_native_damage_writer(self):self.reject(r'(MK2_NAT_CAMPAIGN_HEALTH[^\n]*pc=)FF836700',r'\g<1>00000000')
    def test_wrong_continue_stage(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT[^\n]*number=2[^\n]*stage=)2 ',r'\g<1>0 ')
    def test_non_native_bar_writer(self):self.reject(r'(MK2_NAT_CAMPAIGN_HEALTH[^\n]*pc=)FF9DEF40',r'\g<1>00000000')
    def test_wrong_absolute_health_slot(self):self.reject(r'(MK2_NAT_CAMPAIGN_HEALTH[^\n]*at=)010602F0',r'\g<1>01060EC0')
    def test_wrong_continue_ancestry(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT[^\n]*number=2[^\n]*continue=)[0-9]+',r'\g<1>1')
    def test_wrong_selection_identity(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT_ID[^\n]*roster=)18 ',r'\g<1>1 ')
    def test_runtime_error(self):self.assertFalse(self.check(self.log+'\n[LUA ERROR] test\n')['passed'])
    def test_assisted_record(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*assistance=)none ',r'\g<1>health_only ')
    def test_duplicate_boot(self):
        line=next(line for line in self.log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_BOOT '))
        self.assertFalse(self.check(self.log+'\n'+line+'\n')['passed'])


def wrong_special(field,value):
    def test(self):self.reject(r'(MK2_NAT_CAMPAIGN_SPECIAL[^\n]*\b'+field+r'=)\S+',r'\g<1>'+value)
    return test


for field,value in(('entry','FFFFCA00'),('at','00000000'),('pc','00000000'),('a8','00000000'),('a13','00000000'),
                   ('id','1'),('roster','1'),('move','square')):
    setattr(Campaign,'test_projectile_'+field,wrong_special(field,value))


if __name__=='__main__':
    out=v.ROOT/'audit_v855_current_natural_campaign_units'
    if out.exists():raise ValueError('Refusing to overwrite evidence')
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Campaign))
    paths=[Path(__file__),Path(v.__file__),FOLDER/'run.log',v.ROOT/'audit_v854_sonya_defensive_leg_checked/verification.json']
    hashes={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths}
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'baseline_cases':1,'inputHashes':hashes,'unassisted_clear_proven':False,'fullPortAcceptance':False},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
