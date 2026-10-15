"""Keep whole6686 model; correct lexical spaces and shadowed floor-module name.

The inherited physical gate locally names a fighter victim. Use a distinct
module alias for the original ROM-derived stock floor calculation.
"""
from pathlib import Path
source_path=Path(__file__).with_name('launch_interruption_model_v6686.py')
source=source_path.read_text()
for before,after in(('else45512','else 45512'),('else40720','else 40720'),
                    ('import verify_current_projectile_repeat_v5295 as victim','import verify_current_projectile_repeat_v5295 as floor_source'),
                    ('victim.subzero_floor(guest)','floor_source.subzero_floor(guest)'),
                    ('native=current,victim=victim','native=current,floor_source=floor_source')):
 if source.count(before)!=1:raise ValueError('Exact lexical or original-gate module binding correction: '+before)
 source=source.replace(before,after,1)
exec(compile(source,str(source_path)+'::lexical_spaces_and_unshadowed_floor_module','exec'),globals())
