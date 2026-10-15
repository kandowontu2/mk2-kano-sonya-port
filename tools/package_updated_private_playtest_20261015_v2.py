"""Preserve v1 failure; correct only the existing repository license location."""
from pathlib import Path
source = Path(__file__).with_name('package_updated_private_playtest_20261015.py')
text = source.read_text()
old = "if name=='PLAY.cmd':return R/'PLAY_CURRENT_NATIVE_CHECKED.cmd'"
assert text.count(old) == 1
text = text.replace(old, old + "\n    if name=='COPYING':return R/'mame-mkp/COPYING'")
exec(compile(text, str(source), 'exec'))
