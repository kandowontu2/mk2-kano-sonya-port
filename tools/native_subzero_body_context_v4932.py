"""Exact compiled own-body candidate and independent initialized ROM expectation."""
import hashlib,json
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as old
import build_native_subzero_bodies_v4927 as encoder
import qualify_native_subzero_bodies_v4930 as qualified

ROOT,need,sha=old.ROOT,old.need,old.sha
NAME='diagnostic_v4926_native_subzero_bodies'
EXE_SHA='D037A629F6ACC3D8B549C1272526A8BC25AA6D864247DBC1DF24DB1D7D02D08B'
GUEST_SHA='F025FC75F2C61A08EED34E660E09F225D6B5D144FEDADD80C79103C702F11889'

def expected():
 base=old.expected();asset=json.loads((encoder.OUT/'report.json').read_text())
 payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(hashlib.sha256(payload).hexdigest().upper()=='08D87AC46142687CEE2A13A81F4C7B78268C8AA99D3020F3AF21693058F00C08','Actual new immutable payload')
 need(qualified.data_gate(base,(ROOT/old.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),payload,asset)==GUEST_SHA,
      'Independent native whole guest/data qualification')
 qualified.source_gate(qualified.SOURCE.read_text(),qualified.BASE.read_text())
 guest=encoder.expected_guest(base,payload)
 need(hashlib.sha256(guest).hexdigest().upper()==GUEST_SHA,'Whole independently qualified expected guest')
 restored=json.loads((ROOT/NAME/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restored['passed']and all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),
      'Actual dirty checkout/historical installed executable restored')
 return guest

def expected_gfx():
 payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 lengths=(int.from_bytes(payload[0x1f6408:0x1f640c],'little'),int.from_bytes(payload[0x1f6410:0x1f6414],'little'))
 return payload[0x1d0800:0x1d0800+lengths[0]]+payload[0x1e0800:0x1e0800+lengths[1]]
