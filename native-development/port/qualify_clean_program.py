"""Compare independently compiled native program ROMs; no gameplay claims."""
import hashlib
import json
from pathlib import Path
import re

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
CLEAN=BASE/'clean_program'
CURRENT=BASE/'mk2-rebuild-main'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
inputs=json.loads((PORT/'CLEAN_PROGRAM_INPUTS.json').read_text())
assert not inputs['existingObjectsImported'] and not inputs['existingProgramOutputsImported']
assert (CLEAN/'POK.TXT').read_text().strip()=='DONE'
assert not (CLEAN/'PFAIL.TXT').exists()
for name,digest in inputs['sourceSHA256'].items():
    assert sha((CLEAN/'srcp'/name).read_bytes())==digest
for name,digest in inputs['inputs'].items():
    assert sha((CLEAN/name).read_bytes())==digest
if 'buildScriptSHA256' in inputs:
    assert sha((CLEAN/'PBUILD.BAT').read_bytes())==inputs['buildScriptSHA256']
objects=re.findall(r'(?im)^\s*([\w]+\.obj)\b',(CLEAN/'srcp/MK2NEWW.CMD').read_text())
assert len(objects)==len(set(name.upper() for name in objects))
assert all((CLEAN/'srcp'/name).exists() for name in objects)
fresh_after=inputs.get('freshBuildNotBeforeEpoch')
if fresh_after is not None:
    assert inputs['oldGeneratedOutputsRemoved']>0
    for path in [CLEAN/'srcp'/name for name in objects]+[CLEAN/'srcp/MK2P.OUT',CLEAN/'POK.TXT']:
        assert path.stat().st_mtime>=fresh_after-2,f'Stale compiler output: {path}'
results=[]
for part in ('F8','FC'):
    for lane in range(2):
        name=f'P12{part}.{lane}'
        clean=(CLEAN/'srcp/rom'/name).read_bytes()
        current=(CURRENT/'srcp/rom'/name).read_bytes()
        if fresh_after is not None:assert (CLEAN/'srcp/rom'/name).stat().st_mtime>=fresh_after-2
        assert len(clean)==len(current)==262144
        results.append(dict(file=name,SHA256=sha(clean),currentSHA256=sha(current),identical=clean==current))
report=dict(scope='Independent program assembly/link/ROM split from regenerated sources',
    inputReceiptSHA256=sha((PORT/'CLEAN_PROGRAM_INPUTS.json').read_bytes()),
    linkedObjectCount=len(objects),existingObjectsImported=False,programROMs=results,
    generatedOutputsFreshAfterStaging=fresh_after is not None,
    cleanProgramRebuildByteIdentical=all(result['identical'] for result in results),
    graphicsCleanRebuildVerified=False,soundCleanRebuildVerified=False,
    fullRebuildVerified=False,gameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'CLEAN_PROGRAM_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['cleanProgramRebuildByteIdentical'],'Investigate ROM mismatch before promoting regenerated sources'
