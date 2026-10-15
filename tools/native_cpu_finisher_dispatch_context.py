"""Independent whole-guest/source oracle; no runtime acceptance is inherited."""
import hashlib,json
from pathlib import Path
import qualify_native_cpu_finisher_dispatch_source as repair
ROOT,need,sha=repair.ROOT,repair.need,repair.sha
NAME='diagnostic_native_cpu_finisher_dispatch'
ROSTER=repair.prior.ROSTER
meta=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
EXE_SHA=meta['executable_sha256'];GUEST_SHA=meta['expected_guest_sha256'];PAYLOAD_SHA=meta['payload_sha256']
def expected():
    base=repair.prior.expected();guest=repair.expected_guest(base);repair.gate(guest,base)
    source=repair.source_check()
    guard=json.loads((repair.OUT/'report.json').read_text())
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeRepairAccepted'] and
         guard['stagedSourceHashes']==source and all(sha(p)==h for p,h in guard['inputHashes'].items()),
         'All source-only diagnosis/correction inputs frozen')
    need(meta['initialized_guest_byte_delta']==122 and GUEST_SHA==guard['proposedGuestSHA256']==hashlib.sha256(guest).hexdigest().upper(),
         'Independent whole compiled guest equals only reviewed two-table data repair')
    need(sha(ROOT/NAME/'mkport_candidate.exe')==EXE_SHA and
         all(sha(p)==h for p,h in meta['input_hashes'].items()),'Actual executable and entire compile input set unchanged')
    previous=json.loads((ROOT/repair.prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    a={str(Path(p).resolve()):h for p,h in previous['canonical_source_hashes_at_compile'].items()}
    b={str(Path(p).resolve()):h for p,h in meta['canonical_source_hashes_at_compile'].items()}
    need(a.keys()==b.keys() and {p:h for p,h in b.items()if a[p]!=h}==
         {str((ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').resolve()):source['midtunit_m.cpp']},
         'Only reviewed native initialized finisher dispatch compiled; all other platform inputs conserved')
    need(PAYLOAD_SHA==previous['payload_sha256'] and sha(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==PAYLOAD_SHA,
         'Entire immutable character/portrait/ending payload unchanged')
    for leaf in ('restoration.json','cache_retirement.json'):
        need(json.loads((ROOT/NAME/leaf).read_text(encoding='utf-8-sig'))['passed'],
             'Actual working sources/executable restored and generated compiler cache retired')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'No retained temporary compiler cache')
    return guest
