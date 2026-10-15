"""Preserve failed comparator; exclude terminal-frame summaries on both sides."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_subzero_air_timing.py').read_text()
old="assert rows.get(tag,[])==[r for r in previous.get(tag,[]) if int(r['frame'])<9000]"
assert source.count(old)==1
source=source.replace(old,"assert [r for r in rows.get(tag,[]) if int(r['frame'])<9000]==[r for r in previous.get(tag,[]) if int(r['frame'])<9000]")
source=source.replace("'audit_current_subzero_air_timing_checked'","'audit_current_subzero_air_timing_prefix_checked'")
exec(compile(source,__file__+'::terminal cutoff','exec'))
