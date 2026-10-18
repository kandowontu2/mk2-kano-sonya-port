"""Refresh generated-art provenance after TI symbol normalization/integration."""
import hashlib
import json
from pathlib import Path
PORT=Path(__file__).resolve().parent
p=PORT/'generated_throw/THROW_DATA.json'
report=json.loads(p.read_text())
report['sourceSHA256']=hashlib.sha256((p.parent/'KSTHANI.ASM').read_bytes()).hexdigest().upper()
report['enabledInCandidate']=True
report['controllerSource']='asm/KSTHROW.ASM'
report['kanoFacingControlPending']=False
report['facingImplementation']='Explicit native flip_multi after victim release, then face_opponent after recovery'
p.write_text(json.dumps(report,indent=2)+'\n')
