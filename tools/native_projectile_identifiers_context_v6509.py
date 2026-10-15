"""Isolated compiled packed-ID repair; independently expected full game memory.

This context identifies test artifacts, not runtime acceptance or promotion.
"""
import hashlib,json
from pathlib import Path
import current_payload_metadata_context_v5229 as old
import qualify_projectile_identifiers_v6503 as repair
ROOT,need,sha=old.ROOT,old.need,old.sha
NAME='diagnostic_v6508_native_projectile_identifiers'
EXE_SHA='2FBD8BECEC0E4F673647B936976343D1CE47A8B5D5206C26C12355E9D7874334'
GUEST_SHA='BD65848028298C9D6AD92C64CD2384447CAFAD3BE5019C9EB0BD5D819F1BE8BE'
PAYLOAD_SHA=old.PAYLOAD_SHA

def expected():
 base=old.expected();guest=repair.expected_guest(base)
 p=ROOT/NAME;meta=json.loads((p/'build-info.json').read_text(encoding='utf-8-sig'))
 prior=json.loads((ROOT/old.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 guard=json.loads((ROOT/'audit_v6504_projectile_identifiers_source_checked/report.json').read_text())
 need(guard['passed'] and not guard['nativeFixAccepted'] and guard['expectedGuestChangedBytes']==158 and
      all(sha(k)==v for k,v in guard['inputHashes'].items()),'Entire actual source-only diagnosis unchanged')
 repair.check((ROOT/'source_v6502_native_projectile_identifiers/midtunit_m.cpp').read_text())
 need(EXE_SHA!='UNBUILT' and sha(p/'mkport_candidate.exe')==meta['executable_sha256']==EXE_SHA and
      sha(p/'roms/mk2ks/mk2ks.mdata')==meta['payload_sha256']==PAYLOAD_SHA and
      hashlib.sha256(guest).hexdigest().upper()==meta['expected_guest_sha256']==GUEST_SHA,
      'Actual newly compiled executable and independently expected whole memory')
 delta={k:(prior['canonical_source_hashes_at_compile'][k],v) for k,v in meta['canonical_source_hashes_at_compile'].items()
        if prior['canonical_source_hashes_at_compile'][k]!=v}
 need(len(delta)==1 and next(iter(delta)).endswith('/midtunit_m.cpp') and list(delta.values())==
      [('37E02771B1F20CF17D0D619F83033F5FE37FE5B62DCD9519F60872763BE0E57A',guard['stagedSourceSHA256'])],
      'Exactly one reviewed source delta; no other native/platform/audio/art source change')
 need(all(sha(k)==v for k,v in meta['input_hashes'].items()),'Every actual compiled input unchanged')
 restore=json.loads((p/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restore['passed'] and all(sha(k)==v for k,v in restore['restored_actual_preexisting_files'].items()),
      'Dirty preexisting canonical sources and installed executable restored exactly')
 need(sum(a!=b for a,b in zip(base,guest))==158,'Exactly two data tables/two operands,158 initialized bytes changed')
 return guest

def expected_gfx():
 expected()
 return old.expected_gfx()
