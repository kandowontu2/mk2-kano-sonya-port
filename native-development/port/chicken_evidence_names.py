"""Keep matched, mirrored and isolated audio evidence in separate reports."""
def event_filename(*,matched=False,mirror=False,track=0):
    assert track in (0,1,2,3)
    assert not track or matched
    kind=f'TRACK{track}' if track else ('MATCHED' if matched else '')
    suffix='_'.join(part for part in (kind,'MIRROR' if mirror else '') if part)
    return 'DCS_CHICKEN'+('_'+suffix if suffix else '')+'_EVENTS.json'
