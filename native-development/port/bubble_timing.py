"""Predict finite Orb duration from native two-pixel travel and contact177."""
def expected_fields(travel_start,victim_side):
    raw=int(travel_start['childxval'],16)
    signed=(raw+0x80000000)%0x100000000-0x80000000
    target=(int(travel_start[f'p{victim_side}x'])+32768)%65536-32768
    direction=-1 if int(travel_start['childflags'])&16 else 1
    distance=(target-(signed>>16))*direction
    assert 177<distance<=177+512,'Expected a forward nonzero native Orb travel window'
    travel=(distance-177+1)//2
    assert 1<=travel<=256
    return 137+travel
