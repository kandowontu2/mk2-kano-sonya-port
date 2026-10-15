"""Correct two lexical spaces; preserve the uncompiled6686 attempt exactly."""
from pathlib import Path
source_path=Path(__file__).with_name('launch_interruption_model_v6686.py')
source=source_path.read_text()
for before,after in(('else45512','else 45512'),('else40720','else 40720')):
 if source.count(before)!=1:raise ValueError('Only the two original lexical missing spaces')
 source=source.replace(before,after,1)
exec(compile(source,str(source_path)+'::two_lexical_spaces_corrected','exec'),globals())
