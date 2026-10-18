"""Rebuild dedicated portrait data from explicit sources, not old release ZIP."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import import_selector_art as selector

PORT=Path(__file__).resolve().parent
CURRENT=PORT/'generated_ui_packed'
OUT=PORT.parent/'baseline/clean_program/graphics_ui'
reuse=OUT.exists()
if reuse:
    # Resume only our incomplete check, and only if every existing generated
    # file still exactly matches the corresponding accepted portrait output.
    assert not (OUT/'UI_IMPORT.json').exists(),'Completed check is immutable'
    assert all(path.is_file() and (CURRENT/path.name).is_file()
        and path.read_bytes()==(CURRENT/path.name).read_bytes() for path in OUT.iterdir())
selector.OUT=OUT
with contextlib.redirect_stdout(io.StringIO()):
    selector.main(reuse_generated=reuse)
metadata=json.loads((OUT/'UI_IMPORT.json').read_text())
assert not metadata['requiresLegacyReleaseZIP']
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
files=['KSUI.ASM','fighter_and_ui_graphics.bin',*metadata['sockets']]
results=[]
for name in files:
    generated=(OUT/name).read_bytes();current=(CURRENT/name).read_bytes()
    results.append(dict(file=name,SHA256=sha(generated),identical=generated==current))
report=dict(scope='Dedicated portrait source-to-native-data reproduction only',
    files=results,requiresLegacyReleaseZIP=False,sourcePixelsMigratedLosslessly=True,
    sourceManifestSHA256=sha((PORT/'assets/selector_source/SOURCE.json').read_bytes()),
    fighterPrefixReused=True,completeGraphicsRebuildVerified=False,
    portraitsNativeDataByteIdentical=all(result['identical'] for result in results),
    visualGameplayAcceptanceImplied=False,releaseReady=False)
(PORT/'SELECTOR_SOURCE_REBUILD.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['portraitsNativeDataByteIdentical']
