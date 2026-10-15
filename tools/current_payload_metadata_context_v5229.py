"""Exact metadata-only rebuilt candidate; identical independently reconstructed guest."""
import hashlib,json
from pathlib import Path
import native_subzero_legs_context_v4993 as old
ROOT,need,sha=old.ROOT,old.need,old.sha
NAME='diagnostic_v5219_current_payload_rom_metadata'
EXE_SHA='A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944'
GUEST_SHA,PAYLOAD_SHA=old.GUEST_SHA,old.PAYLOAD_SHA

def expected():
 guest=old.expected()
 p=ROOT/NAME;meta=json.loads((p/'build-info.json').read_text(encoding='utf-8-sig'))
 prior=json.loads((ROOT/old.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 proof=json.loads((ROOT/'audit_v5226_current_metadata_native_startup_checked/report.json').read_text())
 need(sha(p/'mkport_candidate.exe')==meta['executable_sha256']==EXE_SHA and
  sha(p/'roms/mk2ks/mk2ks.mdata')==meta['payload_sha256']==PAYLOAD_SHA and
  hashlib.sha256(guest).hexdigest().upper()==meta['expected_guest_sha256']==GUEST_SHA,
  'Actual corrected executable and exact unchanged payload/whole guest')
 delta={k:(prior['canonical_source_hashes_at_compile'][k],v)for k,v in meta['canonical_source_hashes_at_compile'].items()
  if prior['canonical_source_hashes_at_compile'][k]!=v}
 need(len(delta)==1 and next(iter(delta)).endswith('/midtunit.cpp')and list(delta.values())==
  [('0094EAE7DC9D3AF85474F720A16054BCFA5DF654751E8DA9C3D105588E674363',
   '17FCD9D7C5D862FEB03487828364AC4126D9B0C7AB437DAEBD94F760DA11C0DE')],
  'Only actual compiled ROM metadata source changed')
 need(proof['passed']and proof['metadataOnlyFixCompiledAndNativeStartupAccepted']and
  proof['actualNativeROMVerificationPassedWithoutWarnings']and all(sha(k)==v for k,v in proof['inputHashes'].items()),
  'Actual native no-warning ROM audit and both full-guest/exact-6000field startup contexts')
 need(all(sha(k)==v for k,v in meta['input_hashes'].items()),'Every compiled native input unchanged')
 restore=json.loads((p/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restore['passed']and all(sha(k)==v for k,v in restore['restored_actual_preexisting_files'].items()),
  'Dirty preexisting sources/installed binary exactly restored')
 return guest

def expected_gfx():
 expected()
 return old.expected_gfx()
