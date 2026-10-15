"""Actual isolated semantic-leg candidate; independent full guest/GFX expectation."""
import json,hashlib
from pathlib import Path
import native_subzero_body_context_v4932 as old
import qualify_native_subzero_legs_v4987 as qualified
import build_native_subzero_legs_v4983 as encoder

ROOT,need,sha=old.ROOT,old.need,old.sha
NAME='diagnostic_v4992_native_subzero_legs'
EXE_SHA='3B6005F7D4A37690F63D00D9C5137A059C698128C60469FFB4A691679933EDE7'
GUEST_SHA='5255F3D3870BF9E10999DF79BFD1E15AC892533F38BA1922E981060D2E84ED30'
PAYLOAD_SHA='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3'

def expected():
 base=old.expected();asset=json.loads((encoder.OUT/'report.json').read_text())
 payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(hashlib.sha256(payload).hexdigest().upper()==PAYLOAD_SHA,'Actual immutable semantic leg payload')
 qualified.source_gate(qualified.SOURCE.read_text(),qualified.BASE.read_text())
 prior=(ROOT/old.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(qualified.data_gate(base,prior,payload,asset)==GUEST_SHA,'Independent entire guest and decoded data')
 g=encoder.expected_guest(base,payload);need(hashlib.sha256(g).hexdigest().upper()==GUEST_SHA,'Entire guest reconstruction')
 info=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(info['executable_sha256']==EXE_SHA and info['expected_guest_sha256']==GUEST_SHA
      and sha(ROOT/NAME/'mkport_candidate.exe')==EXE_SHA,'Actual compiled executable bound')
 restored=json.loads((ROOT/NAME/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restored['passed']and all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),
      'Actual dirty source/historical installed binary restored')
 return g

def expected_gfx():
 payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 return old.expected_gfx()+payload[0x1d2800:0x1d2800+3720]+payload[0x1e2800:0x1e2800+3312]
