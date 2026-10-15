"""Include original tail branch beyond first truncated disassembly window."""
from pathlib import Path
source=Path(__file__).with_name('audit_original_shao_taunt_path.py').read_text()
source=source.replace("'-count','1536'","'-count','1600'").replace("out=root/'audit_original_shao_taunt_path_checked'","out=root/'audit_original_shao_taunt_path_v2_checked'")
exec(compile(source,__file__+'::complete_original_window','exec'))
