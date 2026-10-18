"""Exact own-victim Friendship/Babality fixture roles and eligibility mode."""
def profile(arguments,negative=False):
    kinds=[k for k in ('friend','baby') if '--'+k in arguments]
    assert len(kinds)==1
    kind=kinds[0]
    assert ('--punch-wins' in arguments)==negative
    assert ('--finisher-rejoin' in arguments)==(not negative)
    assert '--stock-victim' not in arguments
    if kind=='friend':
        assert '--sonya' not in arguments
        actor=17 if '--kano' in arguments else 18
        if actor==18 and not negative:assert '--friend-lifecycle' in arguments
    else:
        assert '--own-victim' in arguments and '--kano' not in arguments
        actor=18 if '--sonya' in arguments else 17
    return kind,actor,2 if '--mirror' in arguments else 1,18 if actor==17 else 17
