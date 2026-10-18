"""Reuse our bounded clean-build folder, refusing modified staged inputs."""
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import prepare_game_candidate as prepare

PORT=Path(__file__).resolve().parent;CLEAN=prepare.BASE.parent/'clean_program'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
assert sys.argv[1:] in (['--check'],['--refresh'])
receipt=PORT/'CLEAN_PROGRAM_INPUTS.json'
old=json.loads(receipt.read_text())
assert sha(prepare.ZIP.read_bytes())==old['originalZIP_SHA256']
for name,digest in old['sourceSHA256'].items():
    assert Path(name).name==name
    assert sha((CLEAN/'srcp'/name).read_bytes())==digest,f'Modified staged source: {name}'
for name,digest in old['inputs'].items():assert sha((CLEAN/name).read_bytes())==digest
batch=(prepare.BASE/'PBUILD.BAT').read_text().replace('goto fail\n','goto failed\n')
batch=batch.replace('\r\n','\n')
legacy=batch.replace('gspa KSICEPAL -h -l -v10 > C:\\PICEPAL.LOG\nif errorlevel 1 goto failed\n','')
if 'buildScriptSHA256' in old:
    assert sha((CLEAN/'PBUILD.BAT').read_bytes())==old['buildScriptSHA256'],'Modified staged build script'
else:
    assert (CLEAN/'PBUILD.BAT').read_text() in (legacy,batch),'Unexpected staged build script'
generated=prepare.main(audit=True)
assert set(old['sourceSHA256'])<=set(generated),'Refusing source removal'
objects=re.findall(r'(?im)^\s*([\w]+\.obj)\b',(CLEAN/'srcp/MK2NEWW.CMD').read_text())
assert len(objects)==len(set(name.upper() for name in objects))
targets=[CLEAN/'srcp'/name for name in objects]+[CLEAN/'srcp/MK2P.OUT']
targets += [CLEAN/f'srcp/rom/P12{part}.{lane}' for part in ('F8','FC') for lane in range(2)]
if sys.argv[1]=='--check':
    previous=json.loads((PORT/'CLEAN_PROGRAM_QUALIFICATION.json').read_text())
    for item in previous['programROMs']:
        assert sha((CLEAN/'srcp/rom'/item['file']).read_bytes())==item['SHA256']
    assert {path.name.upper() for path in (CLEAN/'srcp').glob('*.OBJ')}=={name.upper() for name in objects}
    plan=dict(root=str(CLEAN.resolve()),targets=[dict(path=str(path.resolve()),SHA256=sha(path.read_bytes())) for path in targets],
        previousInputReceiptSHA256=sha(receipt.read_bytes()),sourceInputsVerified=True)
    (PORT/'CLEAN_PROGRAM_REFRESH_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps(dict(verifiedSources=len(old['sourceSHA256']),generatedOutputsToRemove=len(targets),newSources=len(generated))))
else:
    plan=json.loads((PORT/'CLEAN_PROGRAM_REFRESH_PLAN.json').read_text())
    assert sha(receipt.read_bytes())==plan['previousInputReceiptSHA256']
    assert all(not Path(item['path']).exists() for item in plan['targets'])
    assert not list((CLEAN/'srcp').glob('*.OBJ'))
    changed=[]
    for name,data in generated.items():
        assert Path(name).name==name
        path=CLEAN/'srcp'/name
        if not path.exists() or path.read_bytes()!=data:path.write_bytes(data);changed.append(name)
    (CLEAN/'PBUILD.BAT').write_bytes(batch.replace('\n','\r\n').encode('ascii'))
    old.update(generatedFiles=len(generated),sourceSHA256={name:sha(data) for name,data in generated.items()},
        existingObjectsImported=False,existingProgramOutputsImported=False,
        refreshedExistingCleanDirectory=True,oldGeneratedOutputsRemoved=len(plan['targets']),
        freshBuildNotBeforeEpoch=time.time(),buildScriptSHA256=sha((CLEAN/'PBUILD.BAT').read_bytes()))
    receipt.write_text(json.dumps(old,indent=2)+'\n')
    print(json.dumps(dict(changedGeneratedSources=changed,existingObjectsImported=False,awaitingCleanBuild=True)))
