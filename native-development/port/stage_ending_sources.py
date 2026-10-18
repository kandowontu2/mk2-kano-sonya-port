"""Generate only the two ending inputs after confirming the working tree pins."""
import hashlib
import json
from pathlib import Path
from ending_source import winner,story
import prepare_game_candidate as prepare

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
generated=prepare.main(audit=True)
changes={}
for name,transform in (('MKEND.ASM',winner),('UNZIP.ASM',story)):
    path=SRC/name
    before=path.read_bytes()
    text=before.decode('cp437').replace('\r\n','\n')
    after=transform(text).replace('\n','\r\n').encode('cp437')
    assert after==generated[name],f'Generator/source mismatch: {name}'
    changes[name]=(before,after)
# Historical working sources have comment/ref-placement differences from the
# generator. Preserve them byte-for-byte; this operation touches only two files.
other_hashes={name:sha((SRC/name).read_bytes()) for name in generated if name not in changes}
for name,(before,after) in changes.items():
    assert (SRC/name).read_bytes()==before
    (SRC/name).write_bytes(after)
assert all(sha((SRC/name).read_bytes())==digest for name,digest in other_hashes.items())
report=dict(generatedSources={name:dict(beforeSHA256=sha(before),afterSHA256=sha(after))
                             for name,(before,after) in changes.items()},
            otherGeneratedSourcesUnchanged=True,compiled=False,runtimeVerified=False,
            endingArtworkFinal=False,releaseReady=False)
(PORT/'ENDING_SOURCE_STAGING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
