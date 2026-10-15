"""Specialize the frozen read-only RAM raster callback to the stock reference."""
import ast
from pathlib import Path

path=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_anchor_ui_remote.py')
source=path.read_text()
before="{'delayed':27800,'standard':12004}"
assert source.count(before)==1
source=source.replace(before,"{'stock':38904}",1)
ast.parse(source)
exec(compile(source,str(path)+'::stock_reference_host_binding','exec'),{})
