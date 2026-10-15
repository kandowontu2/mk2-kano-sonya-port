"""Use the actual retained module ledger, not an interactive __main__ guess."""
from pathlib import Path
root=Path('C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port')
source=(root/'tools/read_native_selector_ground_anchor_remote.py').read_text()
old="fields=sys.modules['__main__'].control_fields"
assert source.count(old)==1
source=source.replace(old,"fields=sys.modules['qualify_native_selector_fresh_lowkick_controls'].ledger.original.pair.rows(prepared.RAM_CASES[prepared.SCOPE['KEY']][1],'FIELD')",1)
exec(compile(source,__file__+'::actual_retained_field_ledger','exec'))
