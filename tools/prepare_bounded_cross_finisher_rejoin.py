"""Reuse corrected native both-selector rejoin for reciprocal added victims."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_cross_finisher_rejoin_preparation'
assert not out.exists()
out.mkdir()
for kind in ('primary','secondary'):
    for fighter in ('kano','sonya'):
        victim='sonya' if fighter=='kano' else 'kano'
        for side in (1,2):
            if side==1:
                old=sync.ROOT/'audit_bounded_secondary_rejoin_roster_ready_preparation'
                runner=(old/f'run_{fighter}.ps1').read_text()
                oldcase=f'audit_bounded_secondary_rejoin_roster_ready_{fighter}_p1_runtime'
            else:
                old=sync.ROOT/'audit_bounded_secondary_rejoin_p2_preparation'
                runner=(old/f'run_{fighter}.ps1').read_text()
                oldcase=f'audit_bounded_secondary_rejoin_roster_ready_{fighter}_p2_runtime'
            runner=runner.replace(oldcase,f'audit_bounded_cross_rejoin_{kind}_{fighter}_p{side}_runtime')
            assert "$env:MK2KS_TEST_FIGHTER='kitana'" in runner
            runner=runner.replace("$env:MK2KS_TEST_FIGHTER='kitana'",f"$env:MK2KS_TEST_FIGHTER='{victim}'")
            if kind=='primary':
                runner=runner.replace(f"$env:MK2KS_STOCK_COMMAND='{fighter}_"+('laser' if fighter=='kano' else 'orb')+"'",f"$env:MK2KS_STOCK_COMMAND='{fighter}_own'")
                runner=runner.replace("$env:MK2KS_STOCK_GAP='"+('150' if fighter=='kano' else '256')+"'","$env:MK2KS_STOCK_GAP='"+('64' if fighter=='kano' else '96')+"'")
            (out/f'run_{kind}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared eight text-only cross-victim finisher rejoin cases')
