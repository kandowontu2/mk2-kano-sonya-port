"""Regenerate one verified original boss source; never import compiled bytes."""
import json
from pathlib import Path
import zipfile
from boss_category_source import integrate
from prepare_game_candidate import ZIP
from build_arm_rip_assets import sha

PORT=Path(__file__).resolve().parent
path=PORT.parent/'baseline/mk2-rebuild-main/srcp/MKBOSS.ASM'
before=path.read_bytes()
with zipfile.ZipFile(ZIP) as archive:
    original=archive.read('mk2-rebuild-main/src/MKBOSS.ASM').decode('cp437').replace('\r\n','\n')
assert before.decode('cp437').replace('\r\n','\n').rstrip()==original.rstrip()
after=integrate(original).replace('\n','\r\n').encode('cp437')
path.write_bytes(after)
report=dict(source=str(path),beforeSHA256=sha(before),afterSHA256=sha(after),
            compiled=False,runtimeVerified=False,releaseReady=False)
(PORT/'BOSS_CATEGORY_STAGING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
