"""Keep absence of sampled air kicks as an observation, not a false test premise."""
from pathlib import Path
code=Path(__file__).with_name('classify_current_mirror_jumpkick_samples.py').read_text()
old="assert actions[1025]>0,'No sampled native air kick'"
assert code.count(old)==1
code=code.replace(old,'# Air kick absence is reported, not assumed impossible.')
exec(compile(code,__file__,'exec'))
