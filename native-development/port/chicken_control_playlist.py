"""Diagnostic cluck-volume controls; preserve all play/priority/routing data."""
import re

def verify_location_map(source,generated):
    before=source.splitlines(keepends=True);after=generated.splitlines(keepends=True)
    assert len(before)>1 and len(after)>1
    pattern=rb"; \.LOC file for MK2\.DEF, \d+/\d+/\d+, \d+:\d+:\d+"
    assert re.fullmatch(pattern,before[0].rstrip(b'\r\n'))
    assert re.fullmatch(pattern,after[0].rstrip(b'\r\n'))
    assert b''.join(before[1:])==b''.join(after[1:]),'Generated sound region map changed beyond its timestamp'

def verify_sample_rom(source,generated,chip):
    assert chip in (3,4,5) and len(source)==len(generated)==1048576
    pattern=f'U{chip} '.encode()+rb'\d{2}/\d{2}/\d{3}\x00'
    assert re.fullmatch(pattern,source[:13]) and re.fullmatch(pattern,generated[:13])
    # LOC maps place the first compressed region at0x0e. Date+checksum
    # precede that payload; no compressed/sample byte may differ.
    assert source[14:]==generated[14:]
    assert sum(source[:14])%256==sum(generated[:14])%256

def control_playlist(original,keep_track=0):
    assert keep_track in (0,1,2,3)
    seen=[];changed=[]
    pattern=rb"playlist\s+(203[6-9]|204[0-7]), ([123]), 'Sonya Friendship [0-3]'\s+0\s+setvol\s+([123]), 100"
    def mute(match):
        number,track,volume_track=map(int,match.groups())
        assert track==volume_track==(number-2036)%3+1
        seen.append(number)
        if track==keep_track:return match[0]
        changed.append(number)
        return match[0].replace(b', 100',b', 0',1)
    modified=re.sub(pattern,mute,original)
    assert seen==list(range(2036,2048))
    assert len(changed)==(12 if keep_track==0 else 8)
    return modified,changed
