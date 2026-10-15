"""Source-derived whole-memory identity of the isolated Kano startup build.

This is artifact identity, not gameplay/audio acceptance or public promotion.
The checked old build and all three reviewed source deltas remain bound.
"""
import hashlib,json
from pathlib import Path
import native_projectile_identifiers_context_v6509 as prior
import qualify_kano_launch_source_v6637 as repair
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
NAME='diagnostic_v6640_kano_ball_launch'
EXE_SHA='081598B54D6E2611ACFCACBADCFE4955FCEBAAD3B01A89662157EBFF09D0B5FF'
GUEST_SHA='4B8A8BB5917D25474CFE840BD3B20BC18636B44E3ABB6552D8EFA5873FA26D67'
PAYLOAD_SHA=prior.PAYLOAD_SHA
ASSET_SHA='3D2FB8BD79C818AA2079B10E869D3F1CF444B914582DB560CA64D4408EE57BD7'

def expected():
 base=prior.expected();guest=repair.expected_guest(base);repair.check_source()
 p=ROOT/NAME;meta=json.loads((p/'build-info.json').read_text(encoding='utf-8-sig'))
 old=json.loads((ROOT/prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 guard=json.loads((ROOT/'audit_v6638_kano_ball_launch_source_checked/report.json').read_text())
 need(guard['passed']and guard['sourceOnlyAccepted']and not guard['nativeFixAccepted']and
      len(guard['sourceNegativeFaults'])==7 and all(sha(k)==v for k,v in guard['inputHashes'].items()),
      'Whole exact reviewed source/original donor waveform guard intact')
 need(EXE_SHA!='UNBUILT'and sha(p/'mkport_candidate.exe')==meta['executable_sha256']==EXE_SHA and
      sha(p/'roms/mk2ks/mk2ks.mdata')==meta['payload_sha256']==PAYLOAD_SHA and
      hashlib.sha256(guest).hexdigest().upper()==meta['expected_guest_sha256']==GUEST_SHA,
      'Actual compiled executable/shared payload and independently reconstructed complete guest')
 normalized=lambda entries:{str(Path(k).resolve()):v for k,v in entries.items()}
 before=normalized(old['canonical_source_hashes_at_compile']);after=normalized(meta['canonical_source_hashes_at_compile'])
 need(before.keys()==after.keys(),'All original native/platform compiled inputs retained')
 delta={k:(before[k],v)for k,v in after.items()if before[k]!=v}
 reviewed={str((ROOT/'mame-mkp/src/mame/midway'/name).resolve()):
           (before[str((ROOT/'mame-mkp/src/mame/midway'/name).resolve())],digest)
           for name,digest in guard['stagedSourceHashes'].items()}
 need(delta==reviewed and len(delta)==3,'Exactly the three reviewed Kano launch/ownership/sample-registration deltas')
 need(all(sha(k)==v for k,v in meta['input_hashes'].items()),'Every actual compiled input unchanged')
 need(sha(p/'samples/mk2ks/kano_ball_launch.wav')==ASSET_SHA==guard['donorAssetSHA256'],
      'Actual registered seventeenth asset equals complete original donor waveform')
 restore=json.loads((p/'restoration.json').read_text(encoding='utf-8-sig'))
 cache=json.loads((p/'cache_retirement.json').read_text(encoding='utf-8-sig'))
 need(restore['passed']and restore['native_build_exit']==0 and
      all(sha(k)==v for k,v in restore['restored_actual_preexisting_files'].items()),
      'Exact dirty preexisting sources/installed executable restored after successful compile')
 need(cache['passed']and cache['nativeCompilerExit']==0 and cache['preexistingFilesRestored']and
      cache['cacheAbsent']and not Path(cache['removedGeneratedCache']).exists(),
      'New generated compiler cache actually retired after native termination')
 need(sum(a!=b for a,b in zip(base,guest))==246==meta['initialized_guest_byte_delta']and
      not meta['public_build_promoted']and not meta['native_runtime_accepted']and not meta['full_port_accepted'],
      'One reviewed marker/four branches only; no inherited runtime or public acceptance')
 return guest

def expected_gfx():
 expected()
 return prior.expected_gfx()
