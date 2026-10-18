"""Apply the native action dispatch generator to the hash-audited working input."""
import json
from pathlib import Path
from cpu_action_source import integrate
from build_arm_rip_assets import sha

PORT=Path(__file__).resolve().parent
source=PORT.parent/'baseline/mk2-rebuild-main/srcp/MKDRONE.ASM'
audit=json.loads((PORT/'CPU_ACTION_LOOKUP_AUDIT.json').read_text())
before=source.read_bytes();assert sha(before)==audit['sourceSHA256']
after=integrate(before.decode('cp437').replace('\r\n','\n')).replace('\n','\r\n').encode('cp437')
source.write_bytes(after)
report=dict(source=str(source),beforeSHA256=sha(before),afterSHA256=sha(after),
            compiled=False,runtimeVerified=False,releaseReady=False)
(PORT/'CPU_ACTION_STAGING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
