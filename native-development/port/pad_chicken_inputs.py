"""Explicit verified regeneration of staged clucks for HENRY frame alignment."""
import json
from pathlib import Path
from prepare_chicken_pcm import encode,ROOT
from prepare_dcs_candidate import DEST,OUT,sha

receipt=OUT/'DCS_CHICKEN_INPUTS.json'
old=json.loads(receipt.read_text())
assert sha((DEST/'MK2.PLS').read_bytes())==old['stagedPlaylistSHA256']
changes=[]
for clip in old['clips']:
    path=DEST/f'SNDS/{clip["region"]}.SND'
    before=path.read_bytes();assert sha(before)==clip['pcmSHA256']
    assert 'paddingSamples' not in clip,'Already regenerated'
    pcm,metadata=encode(Path(clip['source']))
    assert metadata['sourceSHA256']==clip['sourceSHA256']
    assert pcm[:len(before)]==before and not any(pcm[len(before):])
    changes.append((path,pcm,metadata))
for clip,(path,pcm,metadata) in zip(old['clips'],changes):
    path.write_bytes(pcm);clip.update(metadata)
old.update(codecFramePaddingApplied=True,runtimeVerified=False,soundROMsBuilt=False)
receipt.write_text(json.dumps(old,indent=2)+'\n')
print(json.dumps(dict(paddedClips=[dict(region=c['region'],samples=c['samples'],padding=c['paddingSamples']) for c in old['clips']],
                     playlistUnchanged=True,awaitingSoundRebuild=True),indent=2))
