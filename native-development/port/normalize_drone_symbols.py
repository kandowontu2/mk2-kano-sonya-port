"""Mechanical symbol-only normalization; does not change instructions/data."""
from pathlib import Path
from drone_source import DISPATCH_TABLES
p=Path(__file__).resolve().parent.parent/'baseline/mk2-rebuild-main/srcp/MKDRONE.ASM'
s=p.read_text()
for old,new in [('ks_drone_reverse_zap_jump_sonya','ks_ai_zrev_s'),('ks_drone_reverse_zap_jump_original','ks_ai_zrev_o'),('ks_drone_zap_jsrp_sonya','ks_ai_zap_s'),('ks_drone_zap_jsrp_original','ks_ai_zap_o')]:
    assert s.count(old)==2,old
    s=s.replace(old,new)
p.write_text(''.join('\t.def '+name+'\n' for name in DISPATCH_TABLES)+s)
