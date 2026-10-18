"""Add one zero guard block, preserving verified already padded PCM bytes."""
import json
from pathlib import Path
from prepare_chicken_pcm import encode
from prepare_dcs_candidate import DEST,OUT,sha

receipt=OUT/'DCS_CHICKEN_INPUTS.json';report=json.loads(receipt.read_text())
assert report['codecFramePaddingApplied'] and not report.get('silentGuardBlockApplied')
assert sha((DEST/'MK2.PLS').read_bytes())==report['stagedPlaylistSHA256']
changes=[]
for clip in report['clips']:
    path=DEST/f'SNDS/{clip["region"]}.SND';old=path.read_bytes()
    assert sha(old)==clip['pcmSHA256']
    new,metadata=encode(Path(clip['source']))
    assert metadata['sourceSHA256']==clip['sourceSHA256']
    assert new==old+b'\0'*480
    changes.append((path,new,metadata))
for clip,(path,new,metadata) in zip(report['clips'],changes):
    path.write_bytes(new);clip.update(metadata)
report.update(silentGuardBlockApplied=True,soundROMsBuilt=False,runtimeVerified=False)
receipt.write_text(json.dumps(report,indent=2)+'\n')
print('Added240 zero guard samples per clip; original PCM bytes unchanged. Awaiting rebuild/decode.')
