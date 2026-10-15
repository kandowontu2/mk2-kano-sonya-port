"""Read the existing stock capture's root RAM schema, with no native writes."""
from pathlib import Path
path=Path('C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port/tools/read_native_anchor_ui_remote.py')
source=path.read_text()
for before,after in (("{'delayed':27800,'standard':12004}","{'classic':37792}"),
                     ("captured=ram['cases'][case]","captured=ram")):
    assert source.count(before)==1
    source=source.replace(before,after,1)
exec(compile(source,str(path)+'::original_stock_root_capture','exec'),{})
