"""Compiled attract artifact identity, independent of runtime acceptance."""
import hashlib
import json
from pathlib import Path
import qualify_native_attract_bios as repair
ROOT,need,sha=repair.ROOT,repair.need,repair.sha
NAME='diagnostic_native_attract_bios'

def expected():
    guest,assembly=repair.expected_guest()
    sources,_=repair.source_check()
    guard=json.loads((repair.OUT/'report.json').read_text())
    meta=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeFixAccepted'] and
         guard['stagedSourceHashes']==sources and all(sha(k)==v for k,v in guard['inputHashes'].items()),'Frozen entire reviewed attract sources')
    need(meta['expected_guest_sha256']==guard['proposedGuestSHA256']==hashlib.sha256(guest).hexdigest().upper(), 'Whole independent expected native guest')
    need(sha(ROOT/NAME/'mkport_candidate.exe')==meta['executable_sha256'] and
         all(sha(k)==v for k,v in meta['input_hashes'].items()), 'Entire actual compiled input identity')
    original=json.loads((ROOT/repair.prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before={str(Path(k).resolve()):v for k,v in original['canonical_source_hashes_at_compile'].items()}
    after={str(Path(k).resolve()):v for k,v in meta['canonical_source_hashes_at_compile'].items()}
    need(before.keys()==after.keys(),'Every compiled platform input conserved')
    delta={k:v for k,v in after.items() if before[k]!=v}
    need(delta=={str((ROOT/'mame-mkp/src/mame/midway'/n).resolve()):sources[n] for n in ('midtunit_m.cpp','midtunit.h')}, 'Only reviewed native-attract implementation and audio-mode member compiled')
    for leaf in ('restoration.json','cache_retirement.json'):
        need(json.loads((ROOT/NAME/leaf).read_text(encoding='utf-8-sig'))['passed'],'Actual preexisting files restored and transient cache retired')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'No retained compiler cache')
    return guest
