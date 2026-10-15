"""Fresh syntax correction of4920; preserve previously executed source."""
from pathlib import Path
prior=Path(__file__).with_name('build_native_subzero_bodies_v4920.py')
text=prior.read_text()
assert text.count('identity<=18 else11')==1
text=text.replace('identity<=18 else11','identity<=18 else 11',1)
text=text.replace('asset_v4921_native_subzero_bodies','asset_v4928_native_subzero_bodies',1)
text=text.replace('Path(__file__).resolve(),Path(codec.__file__)','Path(__file__).resolve(),prior,Path(codec.__file__)',1)
exec(compile(text,str(Path(__file__).resolve())+'::corrected_encoder4920','exec'),globals())
