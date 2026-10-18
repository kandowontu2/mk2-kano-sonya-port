"""Own-pair native stage fixture families and physical roles."""
def profile(arguments):
    assert '--stage' in arguments and '--own-victim' in arguments
    deadpool='--deadpool' in arguments
    negative='--deadpool-no-chord' in arguments
    pit='--pit-progress' in arguments
    assert not (deadpool and pit)
    assert not negative or deadpool
    assert ('--pit-rejoin' not in arguments) or pit
    if deadpool:
        assert '--stage-rematch' not in arguments
        kind='negative' if negative else 'deadpool'
    else:
        assert '--stage-rematch' in arguments
        if pit:assert '--pit-rejoin' in arguments
        kind='pit' if pit else 'tomb'
    return kind,18 if '--sonya' in arguments else 17,2 if '--mirror' in arguments else 1
