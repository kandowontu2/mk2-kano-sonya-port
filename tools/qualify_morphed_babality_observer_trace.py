"""Prove corrected passive winner observer leaves physical chronology intact."""
import json
import verify_native_source_sync as sync

if __name__=='__main__':
    out=sync.ROOT/'audit_morphed_babality_observer_trace_checked';assert not out.exists()
    cases={}
    for side in(1,2):
        old=sync.ROOT/f'audit_bounded_morphed_babality_sonya_p{side}_runtime/run.log'
        new=sync.ROOT/f'audit_bounded_morphed_babality_win_rows_sonya_p{side}_runtime/run.log'
        def keep(path):
            return [line for line in path.read_text().splitlines() if line.startswith('MK2_NATIVE_BABY_') and not line.startswith(('MK2_NATIVE_BABY_WIN ','MK2_NATIVE_BABY_RESULT '))]
        before,after=keep(old),keep(new)
        assert before==after
        cases[str(side)]=dict(identicalPhysicalAndNonWinnerEventLines=len(after),oldLogSHA256=sync.sha(old),newLogSHA256=sync.sha(new))
    report=dict(passed=True,cases=cases,fullPortAcceptance=False,
        scope='Exact whole original input/health/morph/eligibility/actor/retirement trace equality after excluding corrected WIN records and derived RESULT winner count. No gameplay/controller modification.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=2,physicalChronologyUnchanged=True)))
