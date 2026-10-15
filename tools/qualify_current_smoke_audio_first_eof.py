"""Bind to the first inactive record; later EOF cannot hide a corrupted first."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_smoke_audio.py').read_text()
source=source.replace("out=sync.ROOT/'audit_current_smoke_audio_checked'","out=sync.ROOT/'audit_current_smoke_audio_first_eof_checked'")
old="eof=next(r for r in channels if int(r['frame'])>begin and float(r['pos'])==length and r['sample']=='4294967295')"
assert source.count(old)==1
source=source.replace(old,"""eof=next(r for r in channels if int(r['frame'])>begin and r['sample']=='4294967295')
    assert float(eof['pos'])==length""")
exec(compile(source,__file__+'::first_actual_inactive_record_gate','exec'))
