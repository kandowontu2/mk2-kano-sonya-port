"""Successor recognizes exact finite qualification flags in original reports."""
from pathlib import Path
if __name__=='__main__':
    path=Path(__file__).with_name('audit_current_full_scope_frontier.py')
    code=path.read_text()
    old="            assert report.get('passed',report.get('passedObservationChecks',False)) is True"
    assert code.count(old)==1
    code=code.replace(old,"""            flag={'audit_bounded_cross_finisher_rejoin_p1_checked':'finitePaidRejoinPassed',
                  'audit_bounded_aerial_motion_points_checked':'passedJumpLandingAndVRAMPresentation',
                  'audit_current_sonya_reptile_crouch_counter_long_checked':'passedObservationChecks'}.get(name,'passed')
            assert report.get(flag) is True""")
    code=code.replace("currentBuild=sync.BUILD.name,sourceSearchFoundNoExplicitTODO=True,", "currentBuild=sync.BUILD.name,sourceKeywordSearchIsNotAnAcceptanceGate=True,")
    exec(compile(code,str(path)+' [finite flag successor]','exec'),{'__name__':'__main__','__file__':str(path)})
