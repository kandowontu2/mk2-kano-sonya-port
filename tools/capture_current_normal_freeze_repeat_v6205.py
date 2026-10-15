"""Fresh identical current SonyaP1 repeat; preserve complete6199 collector."""
from pathlib import Path
adapter_source=Path(__file__).with_name('capture_current_normal_freeze_v6199.py')
source=adapter_source.read_text()
source=source.replace('audit_v6200_current_normal_subzero_','audit_v6203_current_normal_subzero_').replace('audit_v6201_current_normal_subzero_','audit_v6204_current_normal_subzero_')
before="'for p in[*controllers,prior_source,Path(__file__),Path(native.__file__),'"
assert source.count(before)==1,'Preserve executed entire collector source pin'
source=source.replace(before,"'for p in[*controllers,prior_source,adapter_source,Path(__file__),Path(native.__file__),'",1)
exec(compile(source,__file__+'::complete_current_normal_freeze_repeat','exec'),globals())
