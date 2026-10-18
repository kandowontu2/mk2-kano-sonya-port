import unittest
from inspect_sub_neutral_uppercut import request_case, damage_window, opponent_roles, boss_evidence


class NeutralUppercutEvidence(unittest.TestCase):
    def test_ready_knife_requires_stance_dispatch_and_proven_spaced_command(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif (subBallRecovery.kintaroKnifeReady or',1)[1].split('elseif (subBallRecovery.kintaroKnife',1)[0]
        self.assertIn('subBallRecovery.knifeBody>=120',branch)
        self.assertIn('subBallRecovery.knifeButtons==subBallRecovery.knifeStance',branch)
        self.assertIn('n-subBallRecovery.knifeReadySince>=4',branch)
        command=source.split("elseif plan=='readyknife' then",1)[1].split("elseif plan=='knife'",1)[0]
        self.assertIn('planAge>=7 and planAge<=9',command)
        self.assertIn('planAge>=13 and planAge<=15',command)
        self.assertNotIn(':write_u',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-knife-ready' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-kintaro-knife-midrange' in sys.argv",setup)
        self.assertIn("stance_buttons=joy_origin+joy_local('bt_stance')",wrapper)
    def test_ready_boss_counter_requires_real_duck_dispatch(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subBallRecovery.kintaroReady and target==17 and c2==12',1)[1].split('elseif (subBallRecovery.kintaroKnife',1)[0]
        for condition in ('distance<=subBallRecovery.readyRange','subBallRecovery.readyBody<=96',
                          'subBallRecovery.readyButton==subBallRecovery.readyDuck','(u16(proc1+0x210)&0x1c)==0'):
            self.assertIn(condition,branch)
        self.assertIn('kintaro_ready_counter.csv',source)
        self.assertNotIn(':write_u',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-ready-counter' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-boss-guard' in sys.argv",setup)
        self.assertIn("'--campaign-kano-kintaro-fast-pulse'",setup)
    def test_fast_pulse_is_explicit_and_kano_kintaro_only(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("kintaroFastPulse=os.getenv('KS_CAMPAIGN_KANO_KINTARO_FAST_PULSE')=='1'",source)
        self.assertIn('(subBallRecovery.kintaroFastPulse and target==17 and c2==12) and 12 or 24',source)
        self.assertNotIn(':write_u',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-fast-pulse' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-boss-guard' in sys.argv",setup)
        self.assertIn("'--campaign-kano-kintaro-mixed'",setup)
    def test_midrange_knife_is_opt_in_and_retains_retreat_without_block(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("kintaroKnifeMidrange=os.getenv('KS_CAMPAIGN_KANO_KINTARO_KNIFE_MIDRANGE')=='1'",source)
        self.assertIn("subBallRecovery.kintaroKnifeMidrange and distance<175 then set(away,1);set('P1 Block',0)",source)
        self.assertIn('subBallRecovery.kintaroKnifeMidrange and 48 or 80',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-knife-midrange' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-kintaro-knife' in sys.argv",setup)
    def test_mixed_guard_is_explicit_and_only_outside_uppercut_range(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("kintaroMixedGuard=os.getenv('KS_CAMPAIGN_KANO_KINTARO_MIXED_GUARD')=='1'",source)
        self.assertIn("if subBallRecovery.kintaroMixedGuard and distance>115 then set('P1 Block',1) end",source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-mixed-guard' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-kintaro-mixed' in sys.argv",setup)

    def test_mixed_boss_policy_keeps_actual_duck_readiness(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif (subBallRecovery.kintaroKnife or subBallRecovery.kintaroMixed)',1)[1].split('elseif subBallRecovery.kintaroBlade',1)[0]
        self.assertIn('subBallRecovery.kintaroMixed and distance<175',branch)
        self.assertIn('distance<=115',branch)
        self.assertIn('(renderedHeight(a) or 999)<=96',branch)
        self.assertIn('KS_CAMPAIGN_DUCK_BUTTONS',branch)
        self.assertIn('n-subBallRecovery.uppercutAt>=24',branch)
        self.assertIn('n-subBallRecovery.uppercutAt<3',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-mixed' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-boss-guard' in sys.argv",setup)
        self.assertIn("'--campaign-kano-kintaro-knife'",setup)
        self.assertNotIn(':write_u',source)

    def test_boss_knife_policy_keeps_range_and_actual_stance(self):
        from pathlib import Path
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif (subBallRecovery.kintaroKnife or subBallRecovery.kintaroMixed)',1)[1].split('elseif subBallRecovery.kintaroBlade',1)[0]
        self.assertIn('and target==17 and c2==12 and not plan',branch)
        self.assertIn("not subBallRecovery.kintaroKnifeMidrange and not subBallRecovery.kintaroMixed and distance<260 then set(away,1);set('P1 Block',0)",branch)
        self.assertIn('cpuProjectileActive()',branch)
        self.assertIn('(renderedHeight(a) or -1)>=96',branch)
        self.assertIn("plan='knife';planAge=0;planToward=away",branch)
        self.assertNotIn(':write_u',source)

    def test_blade_spacing_policy_is_boss_only_and_reuses_command(self):
        from pathlib import Path
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subBallRecovery.kintaroBlade',1)[1].split('elseif subBallRecovery.kintaroJumpkick',1)[0]
        self.assertIn('and target==17 and c2==12 and not plan',branch)
        self.assertIn("distance<175 then set(away,1);set('P1 Block',0)",branch)
        self.assertIn('distance>240',branch)
        self.assertIn("plan='blade';planAge=0;planToward=toward",branch)
        self.assertIn('(renderedHeight(a) or -1)>=96',branch)
        self.assertNotIn(':write_u',source)

    def test_endurance_limits_are_explicit_not_new_defaults(self):
        from pathlib import Path
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("elif '--campaign-extra-continues' in sys.argv:\n                assert 0<=continue_count<=32",wrapper)
        self.assertIn("if '--campaign-boss-endurance' in sys.argv: wall_limit=720",wrapper)
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('assert(extraContinues and continueLimit>=0 and continueLimit<=64)',source)
        self.assertIn('assert(continueLimit>=0 and continueLimit<=(extraContinues and 32 or 20))',source)
        self.assertIn('fieldLimit==300000',source)
        self.assertNotIn(':write_u',source)

    def test_boss_health_windows_do_not_become_round_wins(self):
        cases=[dict(opponent=12,nativeUppercutWithin8=True,observedHPDropWithin55=20),
               dict(opponent=12,nativeUppercutWithin8=False,observedHPDropWithin55=20),
               dict(opponent=8,nativeUppercutWithin8=True,observedHPDropWithin55=40)]
        report=boss_evidence(cases,[])
        self.assertEqual(report['kintaroRequests'],2)
        self.assertEqual(report['kintaroNativeActivationsWithin8'],1)
        self.assertEqual(report['kintaroActivationWithObserved20HPDropWindows'],1)
        self.assertEqual(report['kintaroNativeRoundWins'],[])
        self.assertEqual(report['kintaroCompletedMatches'],[])

    def test_kintaro_jumpkick_is_explicit_and_uses_existing_plan(self):
        from pathlib import Path
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-jumpkick' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-boss-guard' in sys.argv",setup)
        self.assertIn("assert '--campaign-kano-kintaro-prepare' not in sys.argv",setup)
        controller=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=controller.split('elseif subBallRecovery.kintaroJumpkick',1)[1].split('elseif plan then',1)[0]
        self.assertIn('and target==17 and c2==12 and not plan',branch)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',branch)
        self.assertIn("plan='jumpkick';planAge=0;planToward=toward",branch)
        self.assertNotIn(':write_u',controller)

    def test_kintaro_prepare_requires_explicit_boss_policy(self):
        from pathlib import Path
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        setup=wrapper.split("if '--campaign-kano-kintaro-prepare' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("assert '--campaign-kano-boss-guard' in sys.argv",setup)
        controller=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('(subBallRecovery.kintaroPrepare and c2==12)',controller)
        self.assertIn('distance<=84 or (subBallRecovery.kintaroWide and c2==12 and distance<=105)',controller)
        self.assertIn('n-subBallRecovery.uppercutPrepare>=4',controller)
        self.assertNotIn(':write_u',controller)

    def test_kintaro_is_not_a_legal_shang_morph(self):
        self.assertEqual(opponent_roles(dict(opponent='12',activeOpponent='12')),(12,12))
        with self.assertRaises(AssertionError):
            opponent_roles(dict(opponent='6',activeOpponent='12'))

    def test_boss_range_does_not_widen_human_requests(self):
        row=self.row();row.update(opponent='12',activeOpponent='12',distance='105')
        self.assertIsNone(request_case({100:row},100,boss_range=105)['nativeUppercutWithin8'])
        with self.assertRaises(AssertionError):request_case({100:row},100)
        row['distance']='106'
        with self.assertRaises(AssertionError):request_case({100:row},100,boss_range=105)
        row.update(opponent='8',activeOpponent='8',distance='95')
        with self.assertRaises(AssertionError):request_case({100:row},100,boss_range=105)

    def row(self):
        return dict(phase='uppercut', ownHeight='0', enemyHeight='0', ownFlags='0',
                    enemyFlags='0', distance='71', projectile='0', block='0', away='0',
                    toward='0', lp='0', down='1', hp='1', ownAction='771',
                    bodyHeight='80', buttonTable='1234', duckTable='1234')

    def test_request_is_not_activation(self):
        index = {i: self.row() for i in range(100, 109)}
        self.assertFalse(request_case(index, 100)['nativeUppercutWithin8'])
        index[102]['ownAction'] = str(0x107)
        self.assertTrue(request_case(index, 100)['nativeUppercutWithin8'])

    def test_truncated_observation_is_unknown(self):
        self.assertIsNone(request_case({100: self.row()}, 100)['nativeUppercutWithin8'])

    def test_invalid_request_rejected(self):
        for key, value in (('distance', '85'), ('block', '1'), ('hp', '0'), ('projectile', '1'),
                           ('bodyHeight', '-1'), ('bodyHeight', '97'), ('buttonTable', '12')):
            row = self.row()
            row[key] = value
            with self.assertRaises(AssertionError):
                request_case({100: row}, 100)

    def test_counter_phase_is_explicit(self):
        row = self.row()
        row['phase'], row['enemyFlags'] = 'uppercut_counter', '16'
        self.assertIsNone(request_case({100: row}, 100)['nativeUppercutWithin8'])
        row['phase'] = 'uppercut'
        with self.assertRaises(AssertionError):
            request_case({100: row}, 100)

    def test_damage_does_not_cross_attempt_or_round(self):
        def row(frame, hp, attempt='1', round='1', action='771'):
            return dict(frame=str(frame), p2hp=str(hp), attempt=attempt, map='6',
                        round=round, p1char='17', p2char='8', p2action=action)
        rows=[row(100,161),row(102,121,action=str(0x503)),row(104,0,attempt='2'),row(106,0,round='2'),row(200,0,attempt='2')]
        result=damage_window(rows,100)
        self.assertEqual(result['observedHPDropWithin55'],40)
        self.assertTrue(result['victimHitTagObserved'])
        self.assertEqual(result['sampledFields'],1)
        self.assertFalse(result['complete55FieldWindow'])

    def test_mileena_is_explicit_not_mislabelled_subzero(self):
        request=self.row();request['opponent']='5'
        self.assertEqual(request_case({100:request},100)['opponent'],5)
        rows=[dict(frame='100',p2hp='161',attempt='1',map='7',round='1',
                   p1char='17',p2char='5',p2action='771')]
        self.assertEqual(damage_window(rows,100,5)['observedHPDropWithin55'],0)
        with self.assertRaises(AssertionError):damage_window(rows,100,8)
        request['opponent']='7'
        with self.assertRaises(AssertionError):request_case({100:request},100)

    def test_shang_morph_keeps_selected_and_active_roles(self):
        self.assertEqual(opponent_roles(dict(opponent='6',activeOpponent='17')),(6,17))
        self.assertEqual(opponent_roles(dict(opponent='2',activeOpponent='2')),(2,2))
        with self.assertRaises(AssertionError):opponent_roles(dict(opponent='2',activeOpponent='17'))
        with self.assertRaises(AssertionError):opponent_roles(dict(opponent='6',activeOpponent='13'))


if __name__ == '__main__':
    unittest.main()
