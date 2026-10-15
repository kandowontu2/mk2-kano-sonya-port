"""Actual final native body palette FFB06AE0, not normal costume colors."""
from pathlib import Path
prior=Path(__file__).with_name('prepare_native_subzero_shatter_references_v4860.py')
text=prior.read_text()
before="palette_address=struct.unpack_from('<I',program,native.off(0xff907910)+identity*4)[0]"
after="palette_address=0xffb06ae0  # Actual original MOVI atFF8C2710, CALLA palette atFF8C2740"
assert text.count(before)==1
text=text.replace(before,after,1)
text=text.replace('art_reference_subzero_shatter_v4861','art_reference_subzero_shatter_v4865',1)
before="rows.append(dict(identity=identity,group=f'{group:08X}',descriptors="
after="rows.append(dict(identity=identity,group=f'{group:08X}',palette=f'{palette_address:08X}',descriptors="
assert text.count(before)==1
text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::actual_native_body_palette_reference','exec'),globals())
