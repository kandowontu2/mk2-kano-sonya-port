"""Exact compiled native AI repair, independent of gameplay acceptance."""
import hashlib
import json
from pathlib import Path
import qualify_native_ai_response as repair
ROOT,need,sha=repair.ROOT,repair.need,repair.sha
NAME='diagnostic_native_ai_response'
ROSTER=repair.prior.repair.ROSTER

def expected():
    before=repair.prior.expected()
    guest=repair.expected_guest(before)
    repair.guest_gate(guest,before)
    sources=repair.source_check()
    guard=json.loads((repair.OUT/'report.json').read_text())
    meta=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeFixAccepted'] and
         guard['stagedSourceHashes']==sources and all(sha(k)==v for k,v in guard['inputHashes'].items()),
         'Every reviewed AI source and actual original diagnosis still frozen')
    need(meta['expected_guest_sha256']==guard['proposedGuestSHA256']==hashlib.sha256(guest).hexdigest().upper(),
         'Independently derived whole native guest identity')
    need(meta['initialized_guest_byte_delta']==448 and
         sha(ROOT/NAME/'mkport_candidate.exe')==meta['executable_sha256'] and
         all(sha(k)==v for k,v in meta['input_hashes'].items()),'Actual whole compiled input and executable identity')
    old=json.loads((ROOT/repair.prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    a={str(Path(k).resolve()):v for k,v in old['canonical_source_hashes_at_compile'].items()}
    b={str(Path(k).resolve()):v for k,v in meta['canonical_source_hashes_at_compile'].items()}
    need(a.keys()==b.keys(),'Entire native platform compile-input set conserved')
    delta={k:v for k,v in b.items() if a[k]!=v}
    need(delta=={str((ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').resolve()):sources['midtunit_m.cpp']},
         'Only reviewed native AI table extension compiled; header, host audio and machine unchanged')
    for leaf in ('restoration.json','cache_retirement.json'):
        receipt=json.loads((ROOT/NAME/leaf).read_text(encoding='utf-8-sig'))
        need(receipt['passed'],'Actual original working files restored and temporary cache retired')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'No retained generated compiler cache')
    return guest
