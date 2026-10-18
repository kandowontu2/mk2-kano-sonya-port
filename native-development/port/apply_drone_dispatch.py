"""Mechanical application of canonical native AI integration to live source."""
from pathlib import Path
import json
from drone_source import integrate_dispatch,audit
PORT=Path(__file__).resolve().parent
destination=PORT.parent/'baseline/mk2-rebuild-main/srcp/MKDRONE.ASM'
text=integrate_dispatch(destination.read_text())
destination.write_text(text)
(PORT/'DRONE_TABLE_AUDIT.json').write_text(json.dumps(audit(text),indent=2)+'\n')
print('Integrated own CPU dispatch; runtime qualification is pending.')
