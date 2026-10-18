"""Keep explicitly loaded-state planning out of continuous campaign evidence."""
import re


def require_no_state_load(observer,arguments):
    assert not re.search(r'[:.]\s*load\s*\(',observer), 'State/image load call disallowed in campaign acceptance'
    assert not any(a in ('--planning-state','--campaign-state-load','-state','-autosave') or
                   a.startswith(('--planning-state=','--campaign-state-load=','-state='))
                   for a in arguments), 'Loaded-state planning is not continuous campaign evidence'

