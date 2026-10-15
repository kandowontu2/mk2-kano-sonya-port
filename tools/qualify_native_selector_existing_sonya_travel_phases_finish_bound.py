"""Correct metadata substitution ordering, keep all phase/source checks.

Original finish_boundary rejection occurred before bicycle qualification.
No new game or changed native data; preserve that rejection and loaded source.
"""
from pathlib import Path
import qualify_native_selector_existing_sonya_travel_phases_finish_boundary as boundary

path=Path(boundary.__file__)
source=path.read_text()
changes=(
    ("audit_native_selector_existing_sonya_travel_phases_finish_boundary_checked",
     "audit_native_selector_existing_sonya_travel_phases_finish_bound_checked"),
    ('    source=replace(source,"directNativeFallTapAccepted=False", "directNativeFallTapAccepted=False,adjacentFinisherOperandSourceQualified=True")\n',''),
    ("timing.OUT/'failure.json',PARENT,",
     "timing.OUT/'failure.json',Path(boundary.__file__),boundary.OUT/'failure.json',PARENT,"),
)
for before,after in changes:
    assert source.count(before)==1,'Only exact metadata ordering/receipt pin boundaries'
    source=source.replace(before,after,1)
exec(compile(source,str(path)+'::whole_original_without_premature_metadata_replace','exec'))
