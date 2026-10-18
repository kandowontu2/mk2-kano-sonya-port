"""Resolve local original Liu data labels through the linked module anchor."""
import re

LABELS=('a_torso_ripped','a_swipe_torso','LKSTUMBLE5',
        *('LKRIPTORSO'+str(index) for index in range(1,7)),'LKDEADLEG1')

def resolve(symbols,listing):
    def local(name):
        matches=re.findall(r'^\s*\d+\s+([0-9a-fA-F]{8})\s+'+re.escape(name)+r'\s*$',listing,re.M)
        assert len(matches)==1,('Expected one local data label',name)
        return int(matches[0],16)
    base=symbols['lk_anitab1']-local('lk_anitab1')
    values={name:base+local(name) for name in LABELS}
    assert all(0xff800000<=address<0x100000000 and address%8==0 for address in values.values())
    return values
