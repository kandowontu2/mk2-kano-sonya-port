"""Read-only native raster callback bound to the original successor UI host."""
from pathlib import Path
path=Path('C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port/tools/read_native_anchor_ui_remote.py')
source=path.read_text()
before="{'delayed':27800,'standard':12004}"
assert source.count(before)==1
source=source.replace(before,"{'layers':39892}",1)
exec(compile(source,str(path)+'::same_terminal_layers_case_rasters','exec'),{})
