"""Preserve the preflight syntax rejection; qualify unchanged native data."""
from pathlib import Path


def verify(ram):
    source_path=Path(__file__).with_name('qualify_native_selector_held.py')
    source=source_path.read_text()
    for before,after in (('else44','else 44'),('else0x52','else 0x52'),('else2','else 2'),
                         ('else323','else 323'),('else17','else 17'),
                         ('Path(__file__),Path(capture.__file__)','Path(__file__),original_source_path,Path(capture.__file__)')):
        assert source.count(before)==1,(before,source.count(before))
        source=source.replace(before,after,1)
    scope=dict(__file__=__file__,original_source_path=source_path)
    exec(compile(source,str(source_path)+'::syntax_only_spacing_correction','exec'),scope)
    return scope['verify'](ram)
