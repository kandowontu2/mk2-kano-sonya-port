"""Source-checked native MKII identities; do not infer IDs from selection layout."""
import hashlib
from pathlib import Path
import re

PORT=Path(__file__).resolve().parent
SOURCE=PORT.parent/'baseline/mk2-rebuild-main/srcp/MAINEQU.ASM'
ORIGINAL=(('ft_hathead',0,'KUNG LAO'),('ft_kang',1,'LIU KANG'),
    ('ft_cage',2,'JOHNNY CAGE'),('ft_sa',3,'BARAKA'),('ft_fn1',4,'KITANA'),
    ('ft_fn2',5,'MILEENA'),('ft_st',6,'SHANG TSUNG'),('ft_raiden',7,'RAIDEN'),
    ('ft_subzero',8,'SUB-ZERO'),('ft_reptile',9,'REPTILE'),
    ('ft_scorpion',10,'SCORPION'),('ft_jax',11,'JAX'))

OWN=(('ft_kano',17,'KANO'),('ft_sonya',18,'SONYA'))
NONSELECTABLE=(('ft_goro',12,'KINTARO'),('ft_final_boss',13,'SHAO KAHN'),
    ('ft_smoke',14,'SMOKE'),('ft_noob',15,'NOOB SAIBOT'),('ft_jade',16,'JADE'))

def verified_names(include_nonselectable=False):
    source=SOURCE.read_text()
    names={}
    for symbol,identity,name in ORIGINAL+OWN+(NONSELECTABLE if include_nonselectable else ()):
        match=re.search(r'^'+symbol+r'\s+\.set\s+(\d+)[ \t]*(?:;[^\n]*)?$',source,re.M)
        assert match and int(match[1])==identity,(symbol,match[1] if match else None)
        names[identity]=name
    return names

def provenance():
    return dict(source=str(SOURCE),SHA256=hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper())
