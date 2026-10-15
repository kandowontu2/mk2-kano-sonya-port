"""Preserve unexecuted v1 artifact; fix numeric Lua keyword token boundaries."""
from pathlib import Path
source=Path(__file__).with_name('prepare_current_kano_ending_sonya_crossjoin.py').read_text()
source=source.replace('audit_current_kano_ending_sonya_crossjoin_preparation','audit_current_kano_ending_sonya_crossjoin_v2_preparation').replace('audit_current_kano_ending_sonya_crossjoin_source_checked','audit_current_kano_ending_sonya_crossjoin_v2_source_checked').replace('audit_current_kano_ending_sonya_crossjoin_runtime','audit_current_kano_ending_sonya_crossjoin_v2_runtime').replace('and18or identity','and 18 or identity')
exec(compile(source,__file__,'exec'))
