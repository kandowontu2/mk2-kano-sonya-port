"""Entire5707 renderer, bound to the complete inverse-map preflight5709."""
from pathlib import Path
import run_current_p2_ending_pixels_v5707 as previous_host

source=Path(previous_host.__file__).read_text()
for before,after in [
 ('qualify_current_p2_ending_source_v5705','qualify_current_p2_ending_source_bound_v5709'),
 ('audit_v5708_','audit_v5712_')]:
 previous_host.need(source.count(before)>=1,'Actual complete collector source binding '+before)
 source=source.replace(before,after)
exec(compile(source,__file__+'::entire_original_P2_RAM_collector','exec'),globals())
