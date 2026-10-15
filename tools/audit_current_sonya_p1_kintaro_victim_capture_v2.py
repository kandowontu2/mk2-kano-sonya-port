"""Correct counted capture total; preserve failed five-pair expectation."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_kintaro_victim_capture.py').read_text()
source=source.replace("out=root/'audit_current_sonya_p1_kintaro_victim_capture_checked'","out=root/'audit_current_sonya_p1_kintaro_victim_capture_v2_checked'").replace('assert len(pairs)==5','assert len(pairs)==6')
exec(compile(source,__file__,'exec'))
