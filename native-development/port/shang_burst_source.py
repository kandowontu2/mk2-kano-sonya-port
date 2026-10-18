"""Own-ID body-entry offsets; preserve all original distance-table entries."""
from arm_rip_source import lookup

OLD, NEW = lookup('burst_distance_offset','get_his_char_long',
                  '00010005fH','0000d0058H','st_burst',other=True)


def integrate(text):
    assert text.count(OLD)==1
    return text.replace(OLD,NEW)
