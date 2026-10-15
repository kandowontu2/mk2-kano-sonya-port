"""Current compiled guest plus independently reconstructed full source graphics.

The graphics oracle comes from the original immutable payload/stock/donor
decoders. Each new native cold boot must match every actual graphics byte;
this interface does not transfer any old runtime acceptance.
"""
import json
from pathlib import Path
import native_ai_response_context as current
import kano_ball_launch_context_v6642 as graphics
ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
meta=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
EXE_SHA=meta['executable_sha256']
GUEST_SHA=meta['expected_guest_sha256']
PAYLOAD_SHA=meta['payload_sha256']

def expected():
    return current.expected()

def expected_gfx():
    expected()
    need(sha(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==graphics.PAYLOAD_SHA==PAYLOAD_SHA,
         'Entire original current character/portrait/ending graphics payload unchanged')
    return graphics.expected_gfx()
