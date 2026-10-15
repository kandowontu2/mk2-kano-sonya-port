"""Native stream block updates may repeat position for one screen field."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_smoke_audio_first_eof.py').read_text()
source=source.replace('audit_current_smoke_audio_first_eof_checked','audit_current_smoke_audio_stream_timing_checked')
old="exec(compile(source,__file__+'::first_actual_inactive_record_gate','exec'))"
assert source.count(old)==1
source=source.replace(old,"""source=source.replace('all(a<b for a,b in zip(positions,positions[1:]))', 'all(a<=b for a,b in zip(positions,positions[1:])) and positions[-1]>positions[0] and positions[3]>positions[2]')
exec(compile(source,__file__+'::native_stream_block_timing_gate','exec'))""")
exec(compile(source,__file__+'::same_first_eof_gate','exec'))
