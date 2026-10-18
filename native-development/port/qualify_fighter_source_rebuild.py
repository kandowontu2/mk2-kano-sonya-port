"""Reimport stock fighter artwork using only standalone native art readers."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import import_character_art as art

PORT=Path(__file__).resolve().parent
OUT=PORT.parent/'baseline/clean_program/graphics_fighters'
assert not OUT.exists()
with contextlib.redirect_stdout(io.StringIO()):
    art.main(output=OUT)
assert 'legacy_art_parser' not in sys.modules
metadata=json.loads((OUT/'ART_IMPORT.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
files=['KANOART.ASM','SONYAART.ASM','fighter_graphics.bin',*metadata['graphicsPacking']['sockets']]
results=[]
for name in files:
    generated=(OUT/name).read_bytes();current=(PORT/'generated_packed'/name).read_bytes()
    results.append(dict(file=name,SHA256=sha(generated),identical=generated==current))
report=dict(scope='Original MK3 art data to native typed fighter ASM and graphics bank',
    inputProgramSHA256=metadata['inputProgramSHA256'],files=results,
    legacyDriverBuildScriptImported=False,executableCodeImported=False,
    nativeDataByteIdentical=all(result['identical'] for result in results),
    completeGraphicsRebuildVerified=False,visualGameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'FIGHTER_SOURCE_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['nativeDataByteIdentical']
