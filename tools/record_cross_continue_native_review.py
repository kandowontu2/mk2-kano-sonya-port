"""Record only what these actual inspected screens display, not every move."""
import inspect
from pathlib import Path
import review_cross_continue_ram as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=inspect.getsource(previous.record_review)
before='The continued match displays the newly selected real fighter jumping, with its correct shadowed lifebar name.'
need(source.count(before)==1,'Finite first-match appearance review, no unsupported jump-raster claim')
source=source.replace(before,'The continued match displays the newly selected real fighter and its correct shadowed lifebar name. A pre-task jump marker is not itself evidence of a rendered airborne pose.',1)
source=source.replace('str(Path(__file__)):sha(__file__)','str(Path(__file__)):sha(__file__),str(Path(previous.__file__)):sha(previous.__file__)')
scope=dict(vars(previous),__file__=__file__,previous=previous)
exec(compile(source,__file__+'::actual_reviewed_selection_ladder_fighter_names','exec'),scope)
record_review=scope['record_review']
