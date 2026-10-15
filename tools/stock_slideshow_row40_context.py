"""Whole source-bound identity of the isolated stock picture-table repair.

Artifact identity only. Runtime/visual/gameplay/release acceptance is separate.
"""
import hashlib
import json
from pathlib import Path
import kano_ball_launch_context_v6642 as prior
import qualify_stock_slideshow_row40 as repair

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
NAME='diagnostic_stock_slideshow_row40'
EXE_SHA='CB8396BAEEEB182E8D50F1C543CB3F13711A0E9454A5B6D7C0D99AA31E9B8E93'
GUEST_SHA='D4E6A2FB587CD2768476EC5662981BF884EE441C00585DECF3D20F6F4C13D2AD'
PAYLOAD_SHA=prior.PAYLOAD_SHA


def expected():
    base=prior.expected()
    guest=repair.expected_guest(base)
    sources=repair.check_sources()
    guard=json.loads((repair.OUT/'report.json').read_text())
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeFixAccepted'] and
         guard['expectedGuestChangedBytes']==4 and len(guard['actualRecordFaultsRejected'])==4 and
         guard['stagedSourceHashes']==sources and all(sha(k)==v for k,v in guard['inputHashes'].items()),
         'Complete actual failure/source conservation guard intact; never inherited runtime acceptance')
    build=ROOT/NAME
    meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
    old=json.loads((ROOT/prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(EXE_SHA!='UNBUILT' and sha(build/'mkport_candidate.exe')==meta['executable_sha256']==EXE_SHA and
         sha(build/'roms/mk2ks/mk2ks.mdata')==meta['payload_sha256']==PAYLOAD_SHA and
         hashlib.sha256(guest).hexdigest().upper()==meta['expected_guest_sha256']==GUEST_SHA,
         'Actual compiled executable/shared payload and independently reconstructed entire guest')
    normalize=lambda entries:{str(Path(k).resolve()):v for k,v in entries.items()}
    before=normalize(old['canonical_source_hashes_at_compile'])
    after=normalize(meta['canonical_source_hashes_at_compile'])
    need(before.keys()==after.keys(), 'All actual native/platform compiled source inputs retained')
    delta={k:(before[k],v) for k,v in after.items() if before[k]!=v}
    cpp=str((ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').resolve())
    need(delta=={cpp:(before[cpp],sources['midtunit_m.cpp'])},
         'Exactly one reviewed source delta; no audio/art/CPU/renderer/control/platform source changes')
    need(all(sha(k)==v for k,v in meta['input_hashes'].items()), 'Every actual frozen compiled input unchanged')
    need(sha(build/'samples/mk2ks/kano_ball_launch.wav')==prior.ASSET_SHA,
         'Seventeenth original launch waveform unchanged; all earlier assets retained in input pins')
    restore=json.loads((build/'restoration.json').read_text(encoding='utf-8-sig'))
    cache=json.loads((build/'cache_retirement.json').read_text(encoding='utf-8-sig'))
    need(restore['passed'] and restore['native_build_exit']==0 and
         all(sha(k)==v for k,v in restore['restored_actual_preexisting_files'].items()),
         'Actual dirty preexisting sources and installed executable restored after compiler exit')
    need(cache['passed'] and cache['nativeCompilerExit']==0 and cache['preexistingFilesRestored'] and
         cache['cacheAbsent'] and not Path(cache['removedGeneratedCache']).exists(),
         'Generated cache actually retired after all native compiler processes terminated')
    need(meta['initialized_guest_byte_delta']==4 and sum(a!=b for a,b in zip(base,guest))==4 and
         not meta['public_build_promoted'] and not meta['native_runtime_accepted'] and not meta['full_port_accepted'],
         'Only one original picture pointer restored; no automatic full-port or public promotion')
    return guest


def expected_gfx():
    expected()
    return prior.expected_gfx()
