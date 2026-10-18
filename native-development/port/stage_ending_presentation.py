"""Stage only the regenerated ending/link artifacts; preserve unrelated sources."""
import hashlib
import json
from pathlib import Path
from prepare_game_candidate import main,DEST

PORT=Path(__file__).resolve().parent
generated=main(audit=True)
names=('MKEND.ASM','UNZIP.ASM','KSENDART.ASM','MK2NEWW.CMD')
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
before={path.name:sha(path.read_bytes()) for path in DEST.iterdir() if path.is_file()}
changes=[]
for name in names:
    data=generated[name]
    (DEST/name).write_bytes(data)
    changes.append(dict(file=name,beforeSHA256=before.get(name),afterSHA256=sha(data)))
for name,digest in before.items():
    if name not in names: assert sha((DEST/name).read_bytes())==digest,name
report=dict(changes=changes,unrelatedFilesPreserved=len(before)-sum(name in before for name in names),
    compiled=False,runtimeVerified=False,releaseReady=False)
(PORT/'ENDING_PRESENTATION_STAGING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
