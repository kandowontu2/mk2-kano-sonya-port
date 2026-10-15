"""Fresh live case after complete source-only compile; exact terminal field gate."""
import run_native_tomb_transition_rejoin_checked as checked

source = checked.once(checked.source,
    "PREFIX = 'audit_native_tomb_transition_rejoin'",
    "PREFIX = 'audit_native_tomb_transition_rejoin_live'")
source = checked.once(source, "records[-1]['frame'] >= cf",
    "records[-1]['frame'] == int(re.search(r'MK2_STAGE_RESULT frame=(\\d+)',text)[1])")
scope = dict(__name__=__name__, __file__=__file__)
exec(compile(source,__file__+'::whole_checked_trial_fresh_case_exact_terminal','exec'),scope)
globals().update({k:v for k,v in scope.items() if not k.startswith('__')})
