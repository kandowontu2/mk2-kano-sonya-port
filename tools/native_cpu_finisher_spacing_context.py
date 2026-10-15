"""Independent whole compiled guest with two dedicated CPU approach profiles."""
import hashlib,json
from pathlib import Path
import qualify_native_cpu_finisher_spacing_source as repair
ROOT,need,sha=repair.ROOT,repair.need,repair.sha
NAME='diagnostic_native_cpu_finisher_spacing'
ROSTER=repair.prior.ROSTER
meta=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
EXE_SHA=meta['executable_sha256'];GUEST_SHA=meta['expected_guest_sha256'];PAYLOAD_SHA=meta['payload_sha256']
def expected():
    base=repair.prior.expected();guest=repair.expected_guest(base);repair.gate(guest,base)
    source=repair.source_check();guard=json.loads((repair.OUT/'report.json').read_text())
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeRepairAccepted'] and
         guard['stagedSourceHashes']==source and all(sha(p)==h for p,h in guard['inputHashes'].items()),
         'Actual finite diagnosis and independently qualified spacing source inputs frozen')
    need(meta['initialized_guest_byte_delta']==6 and GUEST_SHA==guard['proposedGuestSHA256']==
         hashlib.sha256(guest).hexdigest().upper(),'Whole actual compiled guest matches exact six-byte distance-only model')
    need(sha(ROOT/NAME/'mkport_candidate.exe')==EXE_SHA and all(sha(p)==h for p,h in meta['input_hashes'].items()),
         'Actual native executable and every compile input conserved')
    previous=repair.prior.meta
    a={str(Path(p).resolve()):h for p,h in previous['canonical_source_hashes_at_compile'].items()}
    b={str(Path(p).resolve()):h for p,h in meta['canonical_source_hashes_at_compile'].items()}
    need(a.keys()==b.keys() and {p:h for p,h in b.items() if a[p]!=h}==
         {str((ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').resolve()):source['midtunit_m.cpp']},
         'Only reviewed initialized own CPU distances compiled; all native platform and host audio source conserved')
    need(PAYLOAD_SHA==previous['payload_sha256'] and sha(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==PAYLOAD_SHA,
         'Entire immutable graphics/portrait/ending payload unchanged, shared not duplicated')
    for leaf in ('restoration.json','cache_retirement.json'):
        need(json.loads((ROOT/NAME/leaf).read_text(encoding='utf-8-sig'))['passed'],
             'Actual working-source/executable restoration and terminal compiler cache retirement')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'No retained generated compiler cache')
    return guest
