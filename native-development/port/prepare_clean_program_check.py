"""Prepare small source-only clean build, never importing any existing objects."""
import hashlib
import json
import os
from pathlib import Path
import prepare_game_candidate as prepare

PORT=Path(__file__).resolve().parent
BUILD=prepare.BASE
OUT=BUILD.parent/'clean_program'
assert not OUT.exists(),'Never overwrite a clean-build investigation'
generated=prepare.main(audit=True)
OUT.mkdir();(OUT/'srcp').mkdir();(OUT/'srcp/rom').mkdir();(OUT/'ti').mkdir();(OUT/'data').mkdir()
for name,data in generated.items():
    assert Path(name).name==name
    (OUT/'srcp'/name).write_bytes(data)
inputs={}
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
for name in ('GSPA.EXE','GMAKE.EXE','GSPLNK.EXE','BIGSREC.EXE'):
    source=BUILD/'ti'/name
    os.link(source,OUT/'ti'/name)
    inputs['ti/'+name]=sha(source.read_bytes())
for relative in ('data/MK8MIL.IRW','srcp/rom/P.LRN'):
    source=BUILD/relative
    (OUT/relative).write_bytes(source.read_bytes())
    inputs[relative]=sha(source.read_bytes())
batch=(BUILD/'PBUILD.BAT').read_text().replace('goto fail\n','goto failed\n')
(OUT/'PBUILD.BAT').write_bytes(batch.replace('\r\n','\n').replace('\n','\r\n').encode('ascii'))
assert not list((OUT/'srcp').glob('*.OBJ'))
report=dict(scope='Clean program source preparation only, not full graphics/sound rebuild',
    originalZIP_SHA256=sha(prepare.ZIP.read_bytes()),generatedFiles=len(generated),
    existingObjectsImported=False,existingProgramOutputsImported=False,
    inputs=inputs,sourceSHA256={name:sha(data) for name,data in generated.items()},
    liveSourceChanged=False,cleanRebuildVerified=False,releaseReady=False)
(PORT/'CLEAN_PROGRAM_INPUTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(directory=str(OUT),sourceFiles=len(generated),existingObjectsImported=False,
    generatedSourceBytes=sum(map(len,generated.values()))),indent=2))
