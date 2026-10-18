"""Source contract and exhaustive signed-coordinate arithmetic regression."""
from pathlib import Path
import struct
import unittest

class CampaignCoordinates(unittest.TestCase):
    def test_sub_ball_charge_release_is_scoped_and_not_forced(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif kanoSubBall and target==17 and c2==8 then',1)[1].split('elseif kanoSubJump',1)[0]
        for condition in ('age>85 and not subBallReleased','height==0 and (ownFlags&0x1c)==0',
                          '(enemyFlags&0x1c)==0','distance>=80 and distance<=260 and not projectile',
                          'if not eligible then subBallReleaseAt=nil','subBallReleaseAt=n+4'):
            self.assertIn(condition,branch)
        self.assertIn("set('P1 Low Kick',1);set(away,1)",branch)
        self.assertIn("if not kanoSubStandingCharge then set('P1 Down',1) end",branch)
        self.assertIn('if subBallReleased and ownAction==0x303 and n-subBallReleaseAt>=16',branch)
        self.assertNotIn(':write_u',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("assert '--campaign-kano-sub-jump' not in sys.argv",wrapper)

    def test_kano_sub_jump_is_scoped_and_kick_timing_uses_actual_takeoff(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif kanoSubJump and target==17 and c2==8 then',1)[1].split('elseif (target==17',1)[0]
        self.assertIn('if jumping and not subJumpStart then subJumpStart=n end',branch)
        self.assertIn('n-subJumpStart>=18 and n-subJumpStart<24',branch)
        self.assertIn('kanoSubRangeKick and distance<=110 and height>=16',branch)
        self.assertIn('n-subJumpStart>=4 and n-subJumpStart<40',branch)
        self.assertIn('if jumping and kickWindow then',branch)
        self.assertIn('ownAction==0x303 and (u16(proc1+0x210)&0x1c)==0',branch)
        self.assertIn('buttons==duck and body>=0 and body<=96',branch)
        self.assertIn('kanoSubJumpHold and n-subJumpRequest<8 and height==0 and not jumping',branch)
        self.assertNotIn(':write_u',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("'--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv",wrapper)
        self.assertIn("if '--campaign-kano-sub-jump-hold' in sys.argv:\n        assert '--campaign-kano-sub-jump' in sys.argv",wrapper)
        self.assertIn("if '--campaign-kano-sub-range-kick' in sys.argv:\n        assert '--campaign-kano-sub-jump-hold' in sys.argv",wrapper)

    def test_all_signed_words(self):
        for raw in range(65536):
            observed=raw if raw<0x8000 else raw-0x10000
            self.assertEqual(observed,struct.unpack('<h',struct.pack('<H',raw))[0])
        self.assertEqual(110-(65533-65536),113)
        self.assertEqual(abs((-20)-30),50)

    def test_controller_coordinate_reads_are_signed(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('return value<0x8000 and value or value-0x10000',source)
        for expression in ('a+0x90','b+0x90','a+0xb0','b+0xb0','proc1+0x200','proc2+0x200'):
            self.assertNotIn('u16('+expression+')',source)
            self.assertIn('s16('+expression+')',source)
        # Health/actions/identities must remain unsigned; this is not a
        # blanket replacement of all native words with signed observations.
        self.assertIn('u16(0x010602f0)',source)
        self.assertIn('u16(proc1+0x1f0)',source)

    def test_takeoff_timer_uses_native_action(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('(ownAction==0x308 or ownAction==0x30b)',source)
        self.assertIn('counterAir=n;counterPrepare=nil',source)
        self.assertIn('local age=n-counterAir',source)
        self.assertIn('age>=9 and age<15',source)
        self.assertIn('elseif not counterTakeoff and n-counterJump>=48',source)

    def test_bicycle_waits_for_native_stance(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wait=source.split("if raidenPlan=='bike_ready' then",1)[1].split("elseif raidenPlan=='bike' then",1)[0]
        self.assertIn('grounded and ownAction==0x303',wait)
        self.assertIn("raidenPlan='bike';raidenStart=n;age=0;set(away,1)",wait)
        self.assertNotIn("ownAction==0x701",wait)

    def test_interrupted_guard_releases_physically(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('ownAction==0x219 and',source)
        self.assertIn("n-raidenRetry>100 and n%96<12 then set('P1 Block',0)",source)
        observer=(Path(__file__).parent/'diagnostics/campaign_damage_observer.lua').read_text()
        self.assertIn("os.getenv('KS_DAMAGE_GROUND')",observer)
        self.assertIn('ds(obj+0xb0)-ds(part+96)',observer)
        self.assertIn('part=part+112',observer)
        self.assertNotIn('write_u',observer)

    def test_guard_readiness_uses_observed_native_wake(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('u32(proc1+0xe0)==guardWake',source)
        self.assertIn('nativeGuard or ownAction==0x303',source)
        self.assertIn("raidenPlan=raidenSweep and 'sweep_ready' or 'leg'",source)
        self.assertIn("raidenPlan=='sweep_ready' or raidenPlan=='ring_ready'",source)

    def test_knife_waits_for_stance_and_is_bounded(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wait=source.split('if knifeGuardWait then',1)[1].split("elseif age<3 then",1)[0]
        self.assertIn('height==0 and ownAction==0x303',wait)
        self.assertIn('knifeGuardWait=false;knifeGuardStart=n',wait)
        self.assertIn('age>=45 then knifeGuardStart=nil',wait)
        self.assertNotIn('write_u',source)

    def test_fan_guard_uses_bounded_read_only_scan(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        scan=source.split('local function cpuProjectileActive()',1)[1].split('local raidenCounter=',1)[0]
        self.assertIn('count<512',scan)
        self.assertIn('not seen[cursor]',scan)
        self.assertIn('local pid=u16(cursor+0x20)',scan)
        self.assertIn('pid==0x800 or ((subzeroGuard or sonyaSubGuardLeg) and pid==0x803)',scan)
        self.assertIn('cursor=u32(cursor)',scan)
        self.assertNotIn('write_u',scan)

    def test_liu_opening_guard_is_scoped_physical_input(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        guard=source.split('if combat<=60 and liuKnifeGuard',1)[1].split('if combat>60',1)[0]
        self.assertIn('target==17 and c2==1',guard)
        self.assertIn("set('P1 Block',1);set(away,1)",guard)
        self.assertNotIn('write_u',guard)

    def test_sonya_ring_uses_own_physical_command(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('(sonyaRaidenRing and target==18 and c2==7)',source)
        self.assertIn("set(target==18 and toward or away,1)",source)
        self.assertIn("set(target==18 and 'P1 Low Punch' or 'P1 High Punch',1)",source)
        self.assertNotIn('write_u',source)

    def test_pressure_guard_uses_observed_damage_and_bounded_timer(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('usePressureGuard and u16(0x010602f0)<lastHealth then projectileGuardUntil=n+postHitGuardFields',source)
        self.assertIn('postHitGuardFields>=0 and postHitGuardFields<=64',source)
        self.assertIn('local pressureGuard=usePressureGuard and n<projectileGuardUntil',source)
        self.assertIn('guardAfterHit and (postHitOpponent<0 or c2==postHitOpponent)',source)
        self.assertIn('if fanThreat or pressureGuard then',source)
        self.assertNotIn('write_u',source)

    def test_liu_ball_is_physical_charge_and_release(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('liuBall and target==17 and c2==1',source)
        self.assertIn("if planAge<=81 then set('P1 Block',1) end",source)
        self.assertIn("if planAge<=85 then set('P1 Low Kick',1) end",source)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',source)
        self.assertIn('if eligible then liuBallReleased=true else liuBallRelease=nil end',source)
        self.assertNotIn('write_u',source)

    def test_full_campaign_has_consistent_bounded_runtime(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(Path(__file__).parent.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn('fieldLimit>=9000 and fieldLimit<=(endingWindow and 150000 or 120000)',source)
        self.assertIn("'90000' if '--campaign-full' in sys.argv",wrapper)
        self.assertIn("('1800' if '--campaign-full' in sys.argv",wrapper)
        self.assertIn("if '--campaign-full' in sys.argv: wall_limit=300",wrapper)
        self.assertIn("assert game_candidate and '--campaign' in sys.argv and '--cpu-attract' not in sys.argv",wrapper)
        self.assertIn("continue_count<=(20 if '--campaign-full' in sys.argv else 5)",wrapper)
        self.assertIn('continueLimit<=5 or fieldLimit>=90000',source)

    def test_rapid_punch_observation_is_bounded_to_native_process_stack(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        helper=source.split('local function cpuRapidPunch(proc)',1)[1].split('local sonyaRaidenRing=',1)[0]
        self.assertIn('(u16(proc+0x210)&0x10)==0',helper)
        self.assertIn('stack<proc+0x3d0 or stack>proc+0x6f0',helper)
        self.assertIn('math.min(stack+7*32,proc+0x6f0-32)',helper)
        self.assertIn('cursor+64<=proc+0x6f0',helper)
        self.assertIn('local count=u16(proc+0x2a0)',helper)
        self.assertNotIn('write_u',helper)
        self.assertIn('if not rfpRecovering and punchesLeft>1 and punchAnimation==0x13 then',source)
        self.assertIn('local counterReady=ownAction==0x302',source)
        self.assertIn('counterReady and height==0 and distance<105',source)
        self.assertIn('(kitanaRfpDuck and c2==4) or (liuRfpDuck and c2==1)',source)
        self.assertIn('not useRfp or distance>=120',source)
        self.assertIn('and not pressureGuard and not rapidPunch and not retreating and not approachingSubzero and not usingRecoveryCounter and not usingGuardLeg then',source)

    def test_knife_interval_experiment_preserves_other_matchups(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(Path(__file__).parent.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("os.getenv('KS_CAMPAIGN_KITANA_KNIFE_INTERVAL') or '60'",source)
        self.assertIn('kitanaKnifeInterval%1==0',source)
        self.assertIn('((target==17 and c2==4) and kitanaKnifeInterval or 60)',source)
        self.assertIn('assert len(knife_intervals)<=1',wrapper)
        self.assertIn('assert 24<=knife_interval<=120',wrapper)
        self.assertIn('if knife_intervals else 60',wrapper)
        self.assertIn("os.getenv('KS_CAMPAIGN_LIU_KNIFE_INTERVAL') or '60'",source)
        self.assertIn('(target==17 and c2==1) and liuKnifeInterval',source)
        self.assertIn('assert len(liu_intervals)<=1',wrapper)
        self.assertIn('assert 24<=liu_interval<=120',wrapper)
        self.assertIn('if liu_intervals else 60',wrapper)

    def test_sonya_kitana_ring_is_optional_and_actor_scoped(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(Path(__file__).parent.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("os.getenv('KS_CAMPAIGN_SONYA_KITANA_RING')=='1'",source)
        self.assertIn('(sonyaKitanaRing and target==18 and c2==4)',source)
        self.assertIn('(sonyaRaidenRing and target==18 and c2==7)',source)
        self.assertIn("if '--campaign-sonya-kitana-ring' in sys.argv: assert '--sonya' in sys.argv",wrapper)

    def test_sonya_ring_interval_does_not_change_raiden(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(Path(__file__).parent.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("os.getenv('KS_CAMPAIGN_SONYA_KITANA_RING_INTERVAL') or '60'",source)
        self.assertIn('if target==18 and c2==4 then knifeInterval=sonyaKitanaRingInterval end',source)
        self.assertIn('sonyaKitanaRingInterval%1==0',source)
        self.assertIn('assert len(ring_intervals)<=1',wrapper)
        self.assertIn('assert 24<=ring_interval<=120',wrapper)
        self.assertIn("if ring_intervals: assert '--campaign-sonya-kitana-ring' in sys.argv",wrapper)

    def test_sonya_leg_counter_keeps_native_recovery_and_input_order(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        helper=source.split('local usingKitanaLeg=false',1)[1].split('elseif rapidPunch then',1)[0]
        self.assertIn('sonyaKitanaLegCounter and target==18 and c2==4',helper)
        self.assertIn('height==0 and distance<=72 and n-kitanaLegRetry>=90',helper)
        self.assertIn('not sonyaKitanaLegCounter or target~=18 or c2~=4 or distance>=120',source)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',helper)
        self.assertIn('(u16(proc2+0x210)&0x1c)==0',helper)
        self.assertIn('elseif age<4 then',helper)
        self.assertIn("if age>=8 then set('P1 Low Punch',1) end",helper)
        self.assertIn('and not usingKitanaLeg and not usingLiuChoke and not fanThreat',source)
        self.assertNotIn('write_u',helper)

    def test_liu_retreat_preserves_guard_and_command_priority(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif liuRetreat and target==17 and c2==1',1)[1].split('elseif height==0 and n-knifeGuardRetry',1)[0]
        self.assertIn('height==0 and distance<220',branch)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',branch)
        self.assertIn("set(away,1)",branch)
        self.assertIn('retreating=true',branch)
        self.assertNotIn('write_u',branch)

    def test_subzero_knife_is_not_shadowed_by_generic_uppercut(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        gate=source.split("elseif (style=='uppercut'",1)[1].split(' then',1)[0]
        self.assertIn('and not (subzeroKnife and c2==8 and target==17)',gate)
        self.assertLess(source.index('elseif fanThreat or pressureGuard then'),source.index('elseif liuRetreat'))
        self.assertLess(source.index('elseif knifeGuardStart then'),source.index('elseif liuRetreat'))
        self.assertIn('and not retreating and not approachingSubzero and not usingRecoveryCounter and not usingGuardLeg then',source)

    def test_liu_retreat_stall_is_contiguous_bounded_and_reset(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('retreatLastFrame==n-1 and retreatLastX==x1',source)
        self.assertIn('if retreatStill>=12 then retreatUntil=n+60;retreatStill=0 end',source)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0 and n>=retreatUntil then',source)
        self.assertIn('retreatLastX=x1;retreatLastFrame=n',source)
        self.assertIn('retreatLastX=nil;retreatLastFrame=-1;retreatStill=0;retreatUntil=-1000',source)

    def test_liu_choke_is_optional_bounded_and_waits_for_native_stance(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('local closeChokeMatch=target==17 and ((liuChoke and c2==1) or (subzeroChoke and c2==8))',source)
        branch=source.split('if closeChokeMatch and',1)[1].split('elseif sonyaKitanaLegCounter',1)[0]
        self.assertIn('(c2~=8 or not fanThreat)',branch)
        self.assertIn('local closeChokeDistance=(subzeroApproach and c2==8) and 60 or 85',source)
        for expected in ('height==0 and distance<=closeChokeDistance','n-liuChokeRetry>=100',
                         '(u16(proc1+0x210)&0x1c)==0','height==0 and ownAction==0x303',
                         'elseif age>=45 then liuChokeStart=nil',
                         "elseif age>=6 and age<9 then set(toward,1)",
                         "elseif age>=12 and age<16 then set('P1 Low Punch',1)",
                         'elseif age>=16 then liuChokeStart=nil'):
            self.assertIn(expected,branch)
        self.assertNotIn('write_u',branch)
        self.assertIn('liuChokeStart=nil;liuChokeRetry=-1000;liuChokeReady=false',source)

    def test_subzero_knife_is_optional_kano_only_existing_pattern(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local subzeroKnife=os.getenv('KS_CAMPAIGN_SUBZERO_KNIFE')=='1'",source)
        branch=source.split('or subzeroKnife and c2==8',1)[1].split('elseif jaxSafeRing',1)[0]
        self.assertIn('and target==17 then',branch)
        self.assertIn("plan=distance>100 and 'knife' or 'blade';planAge=0",branch)
        self.assertIn('planToward=distance>100 and away or toward',branch)
        self.assertNotIn('write_u',branch)

    def test_subzero_guard_uses_native_ice_slide_and_keeps_low_block(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('or (subzeroGuard and c2==8))) or',source)
        self.assertIn('((subzeroGuard or sonyaSubGuardLeg) and c2==8 and (enemyAction==0x10 or enemyAction==0x20c))',source)
        self.assertIn("if distance>=120 or ((subzeroGuard or sonyaSubGuardLeg) and c2==8) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) then set('P1 Down',1)",source)
        self.assertIn("if distance<120 and not ((subzeroGuard or sonyaSubGuardLeg) and c2==8) and not (sonyaMileenaGuardLeg and c2==5) and not (sonyaCageGuardLeg and c2==2) and not (sonyaLaoGuardLeg and c2==0) and not (sonyaScorpionGuardLeg and c2==10) and not ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) then set('P1 Down',0)",source)
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        self.assertRegex(equates,r'act_throw_ice\s+\.set\s+010H')
        self.assertRegex(equates,r'act_slide\s+\.set\s+020cH')
        self.assertRegex(equates,r'pid_ice2\s+\.set\s+0803H')
        self.assertIn('if pid==0x800 or ((subzeroGuard or sonyaSubGuardLeg) and pid==0x803) then return true end',source)
        zap=(here.parent/'baseline/mk2-rebuild-main/srcp/MKZAP.ASM').read_text()
        ice=zap.split('\ndo_throw_ice\n',1)[1].split('\nice_proc\n',1)[0]
        self.assertIn('pid_ice2,a1',ice)
        self.assertIn('*a5(procid)',ice)

    def test_subzero_approach_is_guarded_bounded_physical_walk(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif subzeroApproach and target==17 and c2==8',1)[1].split('elseif knifeGuardStart then',1)[0]
        for expected in ('not knifeGuardStart','height==0 and distance>60 and distance<=100',
                         '(u16(proc1+0x210)&0x1c)==0','s16(proc2+0x200)-s16(b+0xb0)==0',
                         "if n%(subzeroWalkFields+12)<subzeroWalkFields then set('P1 Down',0);set('P1 Block',0);set(away,0);set(toward,1)",
                         "else set('P1 Down',1);set('P1 Block',1);set(away,1) end"):
            self.assertIn(expected,branch)
        self.assertNotIn('write_u',branch)
        self.assertLess(source.index('elseif fanThreat or pressureGuard then'),source.index('elseif subzeroApproach'))

    def test_subzero_walk_duration_is_bounded_with_unchanged_default(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local subzeroWalkFields=tonumber(os.getenv('KS_CAMPAIGN_SUBZERO_APPROACH_FIELDS') or '6')",source)
        self.assertIn('subzeroWalkFields%1==0 and subzeroWalkFields>=6 and subzeroWalkFields<=30',source)
        for width in range(6,31):
            cycle=[n%(width+12)<width for n in range(width+12)]
            self.assertEqual(sum(cycle),width)
            self.assertEqual(cycle.count(False),12)
        for field in range(180):self.assertEqual(field%(6+12)<6,field%18<6)

    def test_subzero_context_observer_does_not_set_controls(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('if subzeroObservationLog and target==17 and c2==8 then',1)[1].split('local usingKitanaLeg=false',1)[0]
        for expected in ('cpuRapidPunch(proc2)','u16(proc2+0x210)','u32(proc2+0xe0)',
                         'observedRapid and 1 or 0','observedRecovery and 1 or 0'):
            self.assertIn(expected,branch)
        self.assertNotIn('set(',branch)
        self.assertNotIn('write_u',branch)
        self.assertNotIn('rapidPunch=observedRapid',branch)
        self.assertIn('if subzeroObservationLog then subzeroObservationLog:close() end',source)

    def test_subzero_rfp_policy_is_optional_and_uses_native_context(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local subzeroRfpDuck=os.getenv('KS_CAMPAIGN_SUBZERO_RFP_DUCK')=='1'",source)
        self.assertIn('local nativeDuckCounter=(subzeroRfpDuck and c2==8) or (sonyaKitanaRfpDuck and target==18 and c2==4)',source)
        self.assertIn('if useRfp then rapidPunch,punchesLeft,rfpRecovering,punchAnimation=cpuRapidPunch(proc2)',source)
        branch=source.split('elseif rapidPunch then',1)[1].split('elseif fanThreat or pressureGuard',1)[0]
        self.assertIn('not rfpRecovering and punchesLeft>1 and punchAnimation==0x13',branch)
        self.assertIn("set('P1 Block',1)",branch)
        self.assertIn("if nativeDuckCounter then set('P1 Down',1) end",branch)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',branch)
        self.assertNotIn('write_u',branch)

    def test_subzero_counter_uses_bounded_native_rendered_height(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        helper=source.split('local function renderedHeight(object)',1)[1].split('local sonyaRaidenRing',1)[0]
        for expected in ('for index=0,63 do','image+index*112','s16(part+96)',
                         's16(groundAddress)-highest','return nil','u32(object+0x1a0)'):
            self.assertIn(expected,helper)
        self.assertNotIn('write_u',helper)
        self.assertIn('if nativeDuckCounter then',source)
        self.assertIn('counterReady=counterBodyHeight>=0 and counterBodyHeight<=96',source)
        self.assertIn('local counterReady=ownAction==0x302',source)
        native=(here.parent/'baseline/mk2-rebuild-main/srcp/MKUTIL.ASM').read_text()
        self.assertRegex(native,r'am_i_short\s+calla\s+get_my_height.*?\n\s*cmpi\s+060H,a1')

    def test_subzero_counter_triggers_on_readiness_with_cooldown(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif rapidPunch then',1)[1].split('elseif fanThreat or pressureGuard',1)[0]
        for expected in ('local counterPulse=n%12<3','counterPulse=n-subzeroCounterRetry>=12',
                         "set(away,0)",'subzeroCounterRetry=n',
                         "if nativeDuckCounter then set('P1 Down',1) end"):
            self.assertIn(expected,branch)
        self.assertGreaterEqual(source.count('subzeroCounterRetry=-1000'),2)
        ready_fields=[82997,82998]
        self.assertFalse(any(frame%12<3 for frame in ready_fields))
        retry=-1000;presses=[]
        for frame in ready_fields:
            if frame-retry>=12:presses.append(frame);retry=frame
        self.assertEqual(presses,[82997])

    def test_subzero_counter_requires_real_linked_duck_button_table(self):
        import re
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('counterButtonTable=u32(assert(tonumber(os.getenv(\'KS_CAMPAIGN_P1_BUTTONS\'))))',source)
        self.assertIn('counterReady=counterBodyHeight>=0 and counterBodyHeight<=96 and counterButtonsReady',source)
        src=here.parent/'baseline/mk2-rebuild-main/srcp'
        listing=(src/'JOY.LST').read_text()
        symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(src/'MK2P.MAP').read_text())}
        def local(label):
            return int(re.search(r'^\s+\d+\s+([0-9a-fA-F]{8})\s+(?:[0-9a-fA-F]{4,8}\s+)?'+label+r'\b',listing,re.M)[1],16)
        origin=symbols['bt_null']-local('bt_null')
        image=bytearray(1048576)
        for lane in (0,1):image[lane::2]=b''.join((src/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        read=lambda address:struct.unpack_from('<I',image,(address-0xff800000)//8)[0]
        for index,label in enumerate(('joy_uppercut','joy_duck_punch','joy_duck_block','joy_duck_kickh','joy_duck_kickl')):
            self.assertEqual(read(origin+local('bt_duck')+index*32),origin+local(label))
        self.assertTrue(all(read(symbols['bt_null']+index*32)==0 for index in range(5)))

    def test_sonya_kitana_counter_is_scoped_and_uses_native_input_readiness(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local sonyaKitanaRfpDuck=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RFP_DUCK')=='1'",source)
        self.assertIn('(sonyaKitanaRfpDuck and target==18 and c2==4)',source)
        self.assertIn('or nativeDuckCounter',source)
        branch=source.split('if nativeDuckCounter then',1)[1].split('\n      end',1)[0]
        self.assertIn('renderedHeight(a)',branch)
        self.assertIn('counterButtonsReady',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-sonya-kitana-rfp-duck' in sys.argv: assert '--sonya' in sys.argv and '--campaign-sonya-kitana-ring' in sys.argv",wrapper)

    def test_sonya_recovery_counter_is_bounded_and_waits_for_dispatch(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif sonyaRecoveryCounter and target==18 and c2==4 and',1)[1].split('elseif rapidPunch then',1)[0]
        for expected in ('rapidPunch and rfpRecovering and distance<105',
                         '(u16(proc1+0x210)&0x1c)==0 and not fanThreat and not pressureGuard',
                         'age>=18 or height~=0 or distance>=110 or fanThreat or pressureGuard',
                         '(u16(proc1+0x210)&0x1c)~=0',
                         'counterBodyHeight<=96 and counterButtonsReady',
                         'n-subzeroCounterRetry>=12',
                         "phase='fired'",
                         "if sonyaRecoveryKick then set('P1 Low Kick',1) else set('P1 High Punch',1) end"):
            self.assertIn(expected,branch)
        self.assertNotIn('write_u',branch)
        self.assertIn('and not usingRecoveryCounter and not usingGuardLeg then',source)
        self.assertIn('if recoveryCounterLog then recoveryCounterLog:close() end',source)

    def test_sonya_recovery_does_not_rearm_during_counter_cooldown(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('elseif sonyaRecoveryCounter and target==18 and c2==4 and',1)[1].split('elseif rapidPunch then',1)[0]
        arming=branch.split(' then',1)[0]
        self.assertIn('n-subzeroCounterRetry>=12',arming)
        cancellation=branch.split("phase='cancelled'",1)[0]
        self.assertIn('(u16(proc1+0x210)&0x1c)~=0',cancellation)
        # Recorded678 request41572 must not re-arm waiting at41573.
        self.assertFalse(41573-41572>=12)
        self.assertTrue(41584-41572>=12)

    def test_sonya_recovery_kick_uses_existing_duck_low_kick(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local sonyaRecoveryKick=os.getenv('KS_CAMPAIGN_SONYA_KITANA_RECOVER_KICK')=='1'",source)
        self.assertIn("if sonyaRecoveryKick then set('P1 Low Kick',1) else set('P1 High Punch',1) end",source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-sonya-kitana-recover-kick' in sys.argv: assert '--campaign-sonya-kitana-recover-counter' in sys.argv",wrapper)
        native=(here.parent/'baseline/mk2-rebuild-main/srcp/MOVES.ASM').read_text()
        move=native.split('\ndo_duck_kickl\n',1)[1].split('\ndo_uppercut\n',1)[0]
        self.assertIn('act_duck_kickl,a1',move)
        self.assertIn('01aH,a9',move)

    def test_sonya_liu_guard_leg_is_explicit_and_uses_native_readiness(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaLiuGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_LIU_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaLiuGuardLeg and target==18 and c2==1)',source)
        self.assertIn("if '--campaign-sonya-liu-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        self.assertIn("environment['KS_CAMPAIGN_SONYA_LIU_GUARD_LEG']='1' if '--campaign-sonya-liu-guard-leg' in sys.argv else '0'",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            before=wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1]
            self.assertIn("'--campaign-sonya-liu-guard-leg' in sys.argv",before)

    def test_sonya_sub_guard_leg_is_opt_in_with_linked_readiness(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaSubGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SUB_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaSubGuardLeg and target==18 and c2==8)',source)
        self.assertIn("if '--campaign-sonya-sub-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            before=wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1]
            self.assertIn("'--campaign-sonya-sub-guard-leg' in sys.argv",before)

    def test_sonya_guard_leg_keeps_block_first_live_chord(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('local guardLegMatch=target==18 and ((sonyaGuardLeg and c2==4) or (sonyaLiuGuardLeg and c2==1) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6)) or (sonyaSubGuardLeg and c2==8))',source)
        branch=source.split('elseif guardLegMatch and',1)[1].split('elseif sonyaRecoveryCounter',1)[0]
        for expected in ('(rapidPunch and rfpRecovering or neutralLegWindow) and lowGuardFields>=4',
                         'distance<=85 and height==0','n-guardLegRetry>=90',
                         'bodyHeight>=0 and bodyHeight<=96',
                         "set('P1 Down',1);set('P1 Block',1)",
                         "guardLegStart and age<4 then phase='chord';set('P1 Low Punch',1)"):
            self.assertIn(expected,branch)
        self.assertNotIn('counterButtonsReady',branch)
        self.assertNotIn('write_u',branch)
        native=(here.parent/'baseline/mk2-rebuild-main/srcp/KSCMD.ASM').read_text()
        gate=native.split('\nks_leg_chord\n',1)[1].split('\nks_projectile_free\n',1)[0]
        for mask in ('f1b1,a0','f1b2,a0','ks_leg_down,a0'):
            self.assertIn(mask,gate)
        self.assertIn('and not usingGuardLeg then',source)

    def test_sub_neutral_leg_is_optional_bounded_and_standing_victim_only(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        window=source.split('local neutralLegWindow=',1)[1].split('if subzeroObservationLog',1)[0]
        self.assertLess(source.index('if useRfp then rapidPunch,'),source.index('local neutralLegWindow='))
        for gate in ('target==18 and ((sonyaSubNeutralLeg and c2==8) or (sonyaMileenaGuardLeg and c2==5) or (sonyaCageGuardLeg and c2==2) or (sonyaLaoGuardLeg and c2==0) or (sonyaScorpionGuardLeg and c2==10) or ((sonyaOwnGuardLeg and (c2==17 or c2==18)) or (sonyaShangGuardLeg and c2==6))) and not rapidPunch',
                     'distance<=neutralLegDistance','s16(proc2+0x200)-s16(b+0xb0)==0',
                     '(u16(proc2+0x210)&0x1c)==0','(renderedHeight(b) or -1)>96'):
            self.assertIn(gate,window)
        self.assertIn("if '--campaign-sonya-sub-neutral-leg' in sys.argv: assert '--sonya' in sys.argv and '--campaign-sonya-sub-guard-leg' in sys.argv",wrapper)
        self.assertNotIn('write_u',window)

    def test_mileena_policy_is_opt_in_with_native_sai_roll_teleport_gates(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaMileenaGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaMileenaGuardLeg and target==18 and c2==5)',source)
        self.assertIn("if '--campaign-sonya-mileena-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        self.assertIn('(sonyaMileenaGuardLeg and c2==5 and (enemyAction==0x0a or enemyAction==0x0b or enemyAction==0x208 or enemyAction==0x20e))',source)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            before=wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1]
            self.assertIn("'--campaign-sonya-mileena-guard-leg' in sys.argv",before)
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        for name,value in (('act_throw_tsai','00a'),('act_air_tsai','00b'),('act_fntele','0208'),('act_kano','020e')):
            self.assertRegex(equates,r'(?i)'+name+r'\s+\.set\s+'+value+r'H')

    def test_mileena_no_ring_cancels_only_lua_command_and_disables_new_starts(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaMileenaNoRing=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_NO_RING')=='1'",source)
        cancellation=source.split('if sonyaMileenaNoRing and target==18 and c2==5 then',1)[1].split('end',1)[0]
        self.assertIn('knifeGuardStart=nil;knifeGuardWait=false',cancellation)
        self.assertNotIn('write_u',cancellation)
        initiation=source.split('elseif height==0 and n-knifeGuardRetry>=knifeInterval and',1)[1].split('then',1)[0]
        self.assertIn('not (sonyaMileenaNoRing and target==18 and c2==5)',initiation)
        self.assertIn("if '--campaign-sonya-mileena-no-ring' in sys.argv: assert '--campaign-sonya-mileena-guard-leg' in sys.argv",wrapper)

    def test_mileena_leg85_changes_only_controller_neutral_distance(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn('local neutralLegDistance=((sonyaMileenaLeg85 and target==18 and c2==5) or (sonyaCageGuardLeg and target==18 and c2==2) or (sonyaLaoGuardLeg and target==18 and c2==0) or (sonyaScorpionGuardLeg and target==18 and c2==10) or ((sonyaOwnGuardLeg and target==18 and (c2==17 or c2==18)) or (sonyaShangGuardLeg and target==18 and c2==6))) and 85 or 80',source)
        self.assertIn("if '--campaign-sonya-mileena-leg85' in sys.argv: assert '--campaign-sonya-mileena-guard-leg' in sys.argv",wrapper)
        self.assertIn("local sonyaMileenaLeg85=os.getenv('KS_CAMPAIGN_SONYA_MILEENA_LEG85')=='1'",source)
        branch=source.split('elseif guardLegMatch and',1)[1].split('elseif sonyaRecoveryCounter',1)[0]
        for gate in ('distance<=85 and height==0','lowGuardFields>=4','n-guardLegRetry>=90'):
            self.assertIn(gate,branch)
        for enabled,target,enemy,expected in ((False,18,5,80),(True,18,5,85),(True,18,8,80),(True,17,5,80)):
            self.assertEqual(85 if enabled and target==18 and enemy==5 else 80,expected)

    def test_extended_campaign_is_explicit_and_keeps_host_continue_bounds(self):
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-extended' in sys.argv:\n        assert '--campaign-full' in sys.argv",wrapper)
        self.assertIn("environment['KS_CAMPAIGN_FIELDS']='120000' if '--campaign-extended' in sys.argv",wrapper)
        self.assertIn("guest_limit='2400' if '--campaign-extended' in sys.argv",wrapper)
        self.assertIn("if '--campaign-full' in sys.argv: wall_limit=300",wrapper)
        self.assertIn("continue_count<=(20 if '--campaign-full' in sys.argv else 5)",wrapper)
        self.assertIn('damage_end-damage_begin<=300',wrapper)

    def test_cage_guard_policy_is_scoped_to_native_cage_attacks(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaCageGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_CAGE_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaCageGuardLeg and target==18 and c2==2)',source)
        self.assertIn('(sonyaCageGuardLeg and c2==2 and (enemyAction==5 or enemyAction==6 or enemyAction==0x205 or enemyAction==0x206))',source)
        self.assertIn("if '--campaign-sonya-cage-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-cage-guard-leg' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        for name,value in (('act_jcsnot_lo','005'),('act_jcsnot_hi','006'),('act_shadk','0205'),('act_shoruken','0206')):
            self.assertRegex(equates,r'(?i)'+name+r'\s+\.set\s+'+value+r'H')

    def test_lao_policy_is_scoped_and_uses_native_hat_spin_teleport(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaLaoGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_LAO_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaLaoGuardLeg and target==18 and c2==0)',source)
        self.assertIn('(sonyaLaoGuardLeg and c2==0 and (enemyAction==1 or enemyAction==0x108 or enemyAction==0x202))',source)
        self.assertIn("if '--campaign-sonya-lao-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-lao-guard-leg' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        for name,value in (('act_throw_hat','001'),('act_hhspin','0108'),('act_hh_teleport','0202')):
            self.assertRegex(equates,r'(?i)'+name+r'\s+\.set\s+'+value+r'H')

    def test_scorpion_policy_is_scoped_and_uses_native_spear_teleport(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaScorpionGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SCORPION_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaScorpionGuardLeg and target==18 and c2==10)',source)
        self.assertIn('(sonyaScorpionGuardLeg and c2==10 and (enemyAction==0x11 or enemyAction==0x20a))',source)
        self.assertIn("if '--campaign-sonya-scorpion-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-scorpion-guard-leg' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        for name,value in (('act_spear','011'),('act_decoy','020a')):
            self.assertRegex(equates,r'(?i)'+name+r'\s+\.set\s+'+value+r'H')

    def test_added_npc_policy_is_scoped_and_uses_rom_actions_and_projectile_ids(self):
        from inventory_character_tables import source_tables
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaOwnGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_OWN_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaOwnGuardLeg and target==18 and (c2==17 or c2==18))',source)
        self.assertIn("if '--campaign-sonya-own-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-own-guard-leg' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        src=here.parent/'baseline/mk2-rebuild-main/srcp'
        table=source_tables((src/'MKZAP.ASM').read_text())['p1p2_proj_pids']
        values=[value.lower() for row in table['rows'] for value in row['values']]
        self.assertEqual(len(values),38)
        self.assertEqual(values[34:],['pid_proj1','pid_proj2']*2)
        projectile=(src/'KSPROJ.ASM').read_text()
        self.assertIn('calla spawn_proj_proc',projectile)
        self.assertIn('0211h,a1',projectile)
        self.assertIn('0212h,a1',projectile)
        for file,token in (('KANOMOV.ASM','020bh,a1'),('KSBLADE.ASM','0117h,a1'),('KSCHOKE.ASM','0216h'),('SONYAMOV.ASM','0207h,a1'),('KSLEG.ASM','0219h')):
            self.assertIn(token,(src/file).read_text())

    def test_kintaro_strategy_keeps_boss_immunity_and_requires_native_duck(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        boss=source.split('elseif ((sonyaKintaroGuard and target==18) or (subBallRecovery.kintaroEvadeCounter and target==17)) and c2==12 then',1)[1].split('elseif subBallRecovery.normalThrow',1)[0]
        self.assertIn('enemyAction==0x407 and enemyHeight>80 and grounded',boss)
        self.assertIn('bodyHeight>=0 and bodyHeight<=96 and duckButtons',boss)
        self.assertIn('n-bossCounterRetry>=36',boss)
        self.assertIn('n-bossCounterPrepare>=24',boss)
        self.assertNotIn("set('P1 Low Punch'",boss)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-sonya-kintaro-guard' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-kintaro-guard' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        src=here.parent/'baseline/mk2-rebuild-main/srcp'
        self.assertRegex((src/'MAINEQU.ASM').read_text(),r'(?i)act_psycho_goro\s+\.set\s+0407H')
        leg=(src/'KSLEG.ASM').read_text()
        self.assertIn('cmpi ft_goro,a0\n        jreq ks_leg_miss',leg)
        self.assertIn('cmpi ft_final_boss,a0\n        jreq ks_leg_miss',leg)

    def test_background_margin_is_host_only_and_requires_finale_profile(self):
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-background-margin' in sys.argv:\n        assert '--campaign-finale-window' in sys.argv",wrapper)
        self.assertIn("if '--campaign-full' in sys.argv: wall_limit=300",wrapper)
        self.assertIn("if '--campaign-background-margin' in sys.argv: wall_limit=420",wrapper)
        self.assertIn('subprocess.BELOW_NORMAL_PRIORITY_CLASS',wrapper)
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertNotIn('BACKGROUND_MARGIN',source)

    def test_kahn_contact_preparation_does_not_require_reaction_to_finish(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('if kahnContactReady then',1)[1].split('elseif charge and velocity==0',1)[0]
        self.assertIn('if contactRecovery then',branch)
        self.assertIn('distance<=105 and ownHeight==0 and (ownFlags&0x1c)==0',branch)
        self.assertIn('buttonTable==duckTable',branch)
        self.assertIn("else set('P1 Block',1) end",branch)
        self.assertNotIn('velocity==0',branch)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn('assert len(contact_sleeps)==1',wrapper)
        self.assertIn('contact_wake=boss_origin+contact_sleeps[0]+0x50',wrapper)

    def test_kahn_guard_uses_native_routine_and_actual_duck_readiness(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        opening=source.split('if combat<=60 and ((sonyaKahnGuard and target==18) or (subBallRecovery.kanoBoss and target==17)) and c2==13',1)[1].split('if combat<=60 and liuKnifeGuard',1)[0]
        self.assertIn("set('P1 Down',1);set('P1 Block',1)",opening)
        self.assertIn('u16(0x010602f0)>0 and u16(0x01060ec0)>0',opening)
        branch=source.split('if ((sonyaKahnGuard and target==18) or (subBallRecovery.kanoBoss and target==17)) and c2==13 then',1)[1].split('elseif sonyaKintaroEvade',1)[0]
        self.assertIn('nativeRoutineActive(proc2',branch)
        self.assertIn('charge and velocity==0 and distance<=140',branch)
        self.assertIn('ownHeight==0 and (ownFlags&0x1c)==0',branch)
        self.assertIn('bodyHeight>=0 and bodyHeight<=96 and buttonTable==duckTable',branch)
        self.assertIn('n-kahnCounterRetry>=36',branch)
        self.assertIn("else set('P1 Block',1) end",branch)
        routine=source.split('local function nativeRoutineActive',1)[1].split('local function renderedHeight',1)[0]
        self.assertIn('proc<0x01000000 or proc+0x6f0>0x01400000',routine)
        self.assertIn('math.min(stack+7*32,proc+0x6f0-32)',routine)
        self.assertNotIn(':write_u',routine)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("boss_origin=symbols['kahn_start']-boss_local('kahn_start')",wrapper)
        for label in ('kahn_charge','kahn_post_dont_walk'):
            self.assertIn("boss_local('"+label+"')",wrapper)
        setup=wrapper.split("environment['KS_GROUND_Y']",1)[0].rsplit('\n        if ',1)[1]
        self.assertIn("'--campaign-sonya-kahn-guard' in sys.argv",setup)
        boss=(here.parent/'baseline/mk2-rebuild-main/srcp/MKBOSS.ASM').read_text()
        charge=boss.split('\nkahn_charge\n',1)[1].split('\nkahn_post_dont_walk',1)[0]
        self.assertIn('movi\t080000H,a0',charge)
        self.assertIn('sleep\t020H',charge)

    def test_kano_boss_policy_is_explicit_and_keeps_native_states(self):
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        setup=wrapper.split("if '--campaign-kano-boss-guard' in sys.argv:",1)[1].split('\n    if ',1)[0]
        self.assertIn("'--campaign-kano-human-prepare' in sys.argv",setup)
        self.assertIn("'--campaign-subzero-rfp-duck' in sys.argv",setup)
        self.assertIn("assert '--sonya' not in sys.argv",setup)
        self.assertIn('subBallRecovery.kanoBoss and target==17',source)
        self.assertIn('and c2==13 then',source)
        self.assertIn('and c2==12 and u16(proc2+0x1f0)==0x407',source)
        self.assertIn("local earlyStompEvade=os.getenv('KS_CAMPAIGN_SONYA_KINTARO_EARLY_EVADE')=='1' or subBallRecovery.kanoBoss",source)
        self.assertNotIn(':write_u',source)

    def test_kahn_opening_jump_is_optional_physical_and_scoped(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        opening=source.split('if combat<=60 and ((sonyaKahnGuard and target==18) or (subBallRecovery.kanoBoss and target==17)) and c2==13',1)[1].split('if combat<=60 and liuKnifeGuard',1)[0]
        self.assertIn('if kahnOpeningJump then',opening)
        self.assertIn("set(away,1)",opening)
        self.assertIn("if combat<=4 then set('P1 Up',1) end",opening)
        self.assertIn("else set('P1 Down',1);set('P1 Block',1) end",opening)
        self.assertNotIn(':write_u',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-sonya-kahn-opening-jump' in sys.argv:\n        assert '--campaign-sonya-kahn-guard' in sys.argv",wrapper)

    def test_ending_capture_is_bounded_and_does_not_request_inputs(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        capture=source.split('if captureEnding and mode==11 then',1)[1].split('if mode~=previousMode',1)[0]
        self.assertIn('(n-endingFirst)%120==60 and endingCaptures<80',capture)
        self.assertIn("snapshot(string.format('ending_%06d_age%04d.png'",capture)
        self.assertNotIn('set(',capture)
        self.assertNotIn(':write_u',capture)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-capture-ending' in sys.argv:\n        assert game_candidate and '--campaign' in sys.argv",wrapper)

    def test_ending_state_is_read_only_with_two_bounded_dense_windows(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        observer=source.split('if endingStateLog and age<9600 then',1)[1].split('-- At most80',1)[0]
        self.assertIn('photo>=0x01000000 and photo+0x200<0x01400000',observer)
        self.assertIn('(age>=1734 and age<1746) or (age>=2454 and age<2466)',observer)
        self.assertIn('age>=2574 and age<2586',observer)
        self.assertIn('age>=2520 and age<2640',observer)
        self.assertIn('for y=32,224,16 do',observer)
        self.assertIn('for index=1,4095,17 do',observer)
        self.assertNotIn(':write_u',observer)
        self.assertNotIn("set('",observer)
        self.assertIn('if endingStateLog then endingStateLog:close() end',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-ending-state' in sys.argv:\n        assert '--campaign-capture-ending' in sys.argv",wrapper)
        self.assertIn('assert 0x01000000<=symbols[name]<0x01400000',wrapper)

    def test_kintaro_evade_uses_native_edges_and_keeps_direction_stable(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        branch=source.split('if sonyaKintaroEvade and (target==18 or (subBallRecovery.kanoBoss and target==17)) and c2==12',1)[1].split('elseif raidenCounter',1)[0]
        self.assertIn('u16(proc2+0x1f0)==0x407',branch)
        self.assertIn('enemyGround-enemyY>80',branch)
        self.assertIn('(u16(proc1+0x210)&0x1c)==0',branch)
        self.assertIn('if n-stompEscapeLast>1 then',branch)
        self.assertIn("leftDistance>=rightDistance and 'P1 Left' or 'P1 Right'",branch)
        self.assertNotIn("set('P1 High Punch'",branch)
        native=(here.parent/'baseline/mk2-rebuild-main/srcp/MKUTIL.ASM').read_text()
        self.assertIn('move\t@right_edge,a6,w\n\taddi\tscrrgt,a6',native)
        for left,right_scroll in ((0,800),(-300,500),(200,1000)):
            right=right_scroll+399
            for actor in range(left,right+1,17):
                walk_left=abs(actor-left)>=abs(right-actor)
                self.assertGreaterEqual(actor-left if walk_left else right-actor,(right-left)/2)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("environment['KS_KINTARO_SCREEN_RIGHT']=str(screen_right)",wrapper)

    def test_early_stomp_evade_tracks_takeoff_and_landing_without_rejump(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('if enemyGround-enemyY>0 then stompSawAir=true',source)
        self.assertIn('elseif stompSawAir then stompFlightActive=false end',source)
        self.assertIn('if ownHeight>0 then stompJumped=true end',source)
        self.assertIn("if ownHeight==0 and not stompJumped then set('P1 Up',1) end",source)
        self.assertIn('not earlyStompEvade and enemyGround-enemyY>80',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-sonya-kintaro-early-evade' in sys.argv:\n        assert '--campaign-sonya-kintaro-evade' in sys.argv",wrapper)

    def test_extra_paid_continues_are_explicit_and_keep_time_field_bounds(self):
        here=Path(__file__).parent
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-extra-continues' in sys.argv:\n        assert '--campaign-extended' in sys.argv",wrapper)
        self.assertIn('assert 0<=continue_count<=32',wrapper)
        self.assertIn("continue_count<=(20 if '--campaign-full' in sys.argv else 5)",wrapper)
        self.assertIn("if '--campaign-full' in sys.argv: wall_limit=300",wrapper)
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('assert(not extraContinues or fieldLimit>=120000)',source)
        self.assertIn('continueLimit<=(extraContinues and 32 or 20)',source)
        self.assertIn('assert(fieldLimit>=9000 and fieldLimit<=(endingWindow and 150000 or 120000))',source)
        self.assertIn('assert(not endingWindow or fieldLimit==150000)',source)
        self.assertIn("if '--campaign-ending-window' in sys.argv:\n        assert '--campaign-extended' in sys.argv",wrapper)
        self.assertIn("if '--campaign-ending-window' in sys.argv: guest_limit='3000'",wrapper)
        self.assertIn("if '--campaign-finale-window' in sys.argv:\n        assert '--campaign-ending-window' in sys.argv",wrapper)
        self.assertIn("if '--campaign-finale-window' in sys.argv: guest_limit='3600'",wrapper)
        self.assertIn('if finaleWindow then assert(endingWindow and fieldLimit==180000)',source)

    def test_subzero_knife_interval_is_scoped_and_keeps_default(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("os.getenv('KS_CAMPAIGN_SUBZERO_KNIFE_INTERVAL') or '60'",source)
        self.assertIn('if target==17 and c2==8 then knifeInterval=subzeroKnifeInterval end',source)
        self.assertIn('subzeroKnifeInterval%1==0 and subzeroKnifeInterval>=24 and subzeroKnifeInterval<=120',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn('assert len(subzero_intervals)<=1',wrapper)
        self.assertIn('assert 24<=subzero_interval<=120',wrapper)
        self.assertIn("assert '--campaign-subzero-guard' in sys.argv and '--sonya' not in sys.argv",wrapper)
        self.assertIn('n-knifeGuardRetry>=knifeInterval',source)
        self.assertIn('if height==0 and ownAction==0x303 then',source)

    def test_subzero_preemptive_duck_readiness_retains_threat_precedence(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        policy=source.split('if subzeroCrouchReady and target==17 and c2==8',1)[1].split('if rfpLog and rapidPunch',1)[0]
        for condition in ('distance<=180','height==0','(u16(proc1+0x210)&0x1c)==0','not rapidPunch','not fanThreat','not pressureGuard','not knifeGuardStart','not usingLiuChoke'):
            self.assertIn(condition,policy)
        launch=source.split('elseif height==0 and n-knifeGuardRetry>=knifeInterval',1)[1].split('knifeGuardStart=n;',1)[0]
        self.assertIn('not (subzeroCrouchReady and target==17 and c2==8 and distance<=180)',launch)
        self.assertIn("set('P1 Down',1);set('P1 Block',0);set(away,0)",policy)
        self.assertNotIn("set('P1 High Punch'",policy)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("assert '--campaign-subzero-rfp-duck' in sys.argv and '--campaign-subzero-guard' in sys.argv",wrapper)

    def test_campaign_fast_choke_waits_for_native_readiness_and_is_scoped(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn('local fastChoke=subzeroFastChoke and target==17 and c2==8',source)
        self.assertIn('chokeBodyHeight>=0 and chokeBodyHeight<=96 and chokeButtonTable==chokeDuckTable',source)
        self.assertIn('height==0 and (u16(proc1+0x210)&0x1c)==0 and (ownAction==0x303 or duckReady)',source)
        self.assertIn("liuChokeReady=true;liuChokeStart=n;set('P1 Down',0)",source)
        self.assertIn("if age>=1 and age<4 then set('P1 Down',1)",source)
        self.assertIn('elseif age>=4 and age<7 then set(toward,1)',source)
        self.assertIn("elseif age>=7 and age<11 then set('P1 Low Punch',1)",source)
        self.assertIn('if fastChokeLog then fastChokeLog:close() end',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--campaign-subzero-fast-choke' in sys.argv:\n                assert '--campaign-subzero-neutral-choke' in sys.argv",wrapper)

    def test_fast_choke_fixture_changes_only_physical_command_spacing(self):
        here=Path(__file__).parent
        fixture=(here/'diagnostics/choke_probe.lua').read_text()
        self.assertIn("local fastCommand=os.getenv('KS_CHOKE_FAST_COMMAND')=='1'",fixture)
        self.assertIn('local forwardBegin=fastCommand and 83 or 86',fixture)
        self.assertIn('local punchBegin=fastCommand and 86 or 92',fixture)
        self.assertIn('local downBegin=crouchEntry and 74 or 80',fixture)
        self.assertIn('t>=downBegin and t<83',fixture)
        self.assertIn('assert(not crouchEntry or fastCommand)',fixture)
        self.assertNotIn(':write_u',fixture)
        self.assertNotRegex(fixture,r'\.value\s*=(?!=)')

    def test_subzero_neutral_choke_is_scoped_and_preserves_native_move(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("local subzeroNeutralChoke=os.getenv('KS_CAMPAIGN_SUBZERO_NEUTRAL_CHOKE')=='1'",source)
        self.assertIn('not subzeroNeutralChoke or c2~=8 or (not rapidPunch and distance<=80',source)
        self.assertIn('(u16(proc2+0x210)&0x1c)==0 and (renderedHeight(b) or -1)>96',source)
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("assert '--campaign-subzero-choke' in sys.argv and '--campaign-subzero-rfp-duck' in sys.argv",wrapper)
        choke=(here.parent/'baseline/mk2-rebuild-main/srcp/KSCHOKE.ASM').read_text()
        self.assertIn('movk 6,a0\n        move a0,*a13(p_store1),w',choke)
        self.assertIn('move b2,b2\n        jrne ks_choke_miss',choke)

    def test_boss_context_is_passive_and_closed_on_exit(self):
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        observation=source.split('-- Passive bounded-context diagnostics;',1)[1].split('elseif subBallRecovery.normalThrow',1)[0]
        self.assertNotIn("set('",observation)
        self.assertNotIn(':write_u',observation)
        self.assertIn('renderedHeight(a) or -1',observation)
        self.assertIn("commands['P1 High Punch'] or 0",observation)
        self.assertIn('if bossContextLog then bossContextLog:close() end',source)

    def test_campaign_does_not_stop_on_native_ending_gameover_state(self):
        here=Path(__file__).parent
        src=here.parent/'baseline/mk2-rebuild-main/srcp'
        equates=(src/'MAINEQU.ASM').read_text()
        self.assertRegex(equates,r'(?i)gs_gameover\s+\.set\s+00bh')
        main=(src/'MAIN.ASM').read_text()
        finished=main.split('\ngame_finished\n',1)[1].split('\npf_entered',1)[0]
        self.assertIn('movi\tgs_gameover,a0',finished)
        self.assertIn('jsrp\tcongrats',finished)
        ending=(src/'MKEND.ASM').read_text().split('\ncongrats\n',1)[1]
        self.assertIn('jsrp\tshow_a0_ending',ending)
        self.assertIn('jsrp\tcast_of_characters',ending)
        controller=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertIn("elseif enteredCombat and (mode==1 or (mode==4 and not continuing)) then reason='left-campaign'",controller)
        # This protects observation duration only; it does not prove an earned ending.

    def test_shang_policy_is_opt_in_and_uses_native_skull_states(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        wrapper=(here.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("local sonyaShangGuardLeg=os.getenv('KS_CAMPAIGN_SONYA_SHANG_GUARD_LEG')=='1'",source)
        self.assertIn('(sonyaShangGuardLeg and target==18 and c2==6)',source)
        self.assertIn('(sonyaShangGuardLeg and c2==6 and (enemyAction==0x0c or enemyAction==0x0d or enemyAction==0x0e))',source)
        self.assertIn("if '--campaign-sonya-shang-guard-leg' in sys.argv: assert '--sonya' in sys.argv",wrapper)
        for setup in ("environment['KS_GROUND_Y']",'drone_listing='):
            self.assertIn("'--campaign-sonya-shang-guard-leg' in sys.argv",wrapper.split(setup,1)[0].rsplit('\n        if ',1)[1])
        equates=(here.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM').read_text()
        for name,value in (('act_throw_skull1','00c'),('act_throw_skull2','00d'),('act_throw_skull3','00e')):
            self.assertRegex(equates,r'(?i)'+name+r'\s+\.set\s+'+value+r'H')

if __name__=='__main__': unittest.main()
