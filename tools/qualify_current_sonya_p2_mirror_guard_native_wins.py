"""Include native higher-health victories; do not invent a timer observation."""
import inspect
from pathlib import Path
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_p2_native_start_campaign as base

if __name__=='__main__':
    # Preserve the executed KO-only check. Native FF8296B0 supplies winner;
    # non-KO admission additionally requires strictly greater positive HP.
    code=inspect.getsource(chronology.check)
    old='health[side - 1] > 0 and health[2 - side] == 0'
    assert code.count(old)==1
    code=code.replace(old,'health[side - 1] > health[2 - side] >= 0')
    context={};exec(compile(code,__file__+'::higher-health chronology','exec'),context)
    adjusted=type('NativeChronology',(),{'load':staticmethod(chronology.load),'check':staticmethod(context['check'])})
    code=Path(base.__file__).read_text().replace('import check_campaign_stage_chronology as chronology','')
    for suffix in ('runtime','checked'):
        replacement='audit_current_sonya_p2_mirror_guard_'+('native_wins_checked' if suffix=='checked' else suffix)
        code=code.replace('audit_current_sonya_p2_native_start_'+suffix,replacement)
    code=code.replace('audit_current_sonya_p2_native_start_preparation/campaign.lua','audit_current_sonya_p2_mirror_guard_preparation/campaign.lua')
    code=code.replace('existing leg-grab controls','historical physical mirror guard/leg sequence; existing leg elsewhere')
    code=code.replace("earnedOwnRoundWins=len(wins),","earnedOwnRoundWins=len(wins),nativeNonKOWins=[r for r in wins if all(int(v)>0 for v in r['health'].split(','))],timerDirectlyObserved=False,")
    code=code.replace('earned native health/wins qualify observed stage advances','native FF8296B0 winner with own HP strictly greater than opponent qualifies observed advances, including non-KO higher-health wins; timer expiry itself not directly observed')
    exec(compile(code,__file__+'::native winners','exec'),{'__name__':'__main__','chronology':adjusted})
