"""Retain5494; restore complete HUD reference and native compact descriptors.

The actual ROM graphics digest proves the only missing reconstruction is the
own name at0F000000. Reuse the complete qualified original HUD constructor.
Original stock single sprites use HH,I,H (10bytes), not imported HH,hh,I,H.
No native game/code/art change, omitted pixels or tolerance relaxation.
"""
import json, traceback
from pathlib import Path
import verify_current_reptile_overlap_v5492 as original
import current_cpu_scene_ram_contract_v5363 as hud

ROOT,need,sha=original.ROOT,original.need,original.sha
FAILED=ROOT/'audit_v5494_current_reptile_overlap_progress/progress.json'
BASE=ROOT/'audit_v5496_current_reptile_overlap_ram'
OUT=ROOT/'audit_v5497_current_reptile_overlap_progress'
COMPLETED=[]
failure=json.loads(FAILED.read_text())
need(not failure['passed']and failure['error']=="ValueError('Every complete actual foreground/body/blood graphics stream equals independently reconstructed ROM')",
     'Exact preserved missing native HUD-reference failure')
source=Path(original.__file__).read_text()
changes={
 "BASE=ROOT/'audit_v5493_current_reptile_overlap_ram'":"BASE=ROOT/'audit_v5496_current_reptile_overlap_ram'",
 "OUT=ROOT/'audit_v5494_current_reptile_overlap_progress'":"OUT=ROOT/'audit_v5497_current_reptile_overlap_progress'",
 "image=graphics.reconstruct(pins)":"image=hud.patch_hud(graphics.reconstruct(pins),pins)",
 "bw,bh,bx,by,bsource,bcommand=struct.unpack_from('<HHhhIH',guest,at)":"bw,bh,bsource,bcommand=struct.unpack_from('<HHIH',guest,at)",
 "    image=source_graphics(pins,expected_gfx)":"    image=source_graphics(pins,expected_gfx)\n    for p in (Path(original.__file__),Path(hud.__file__),FAILED):pins[str(p.resolve())]=sha(p)\n    for p in original.BASE.rglob('*'):\n        if p.is_file():pins[str(p.resolve())]=sha(p)",
}
for before,after in changes.items():
    need(source.count(before)==1,'Exact whole existing native contract reference correction: '+before)
    source=source.replace(before,after,1)
# Keep original module aliases stable: the canonical module imports use 'art',
# not 'original'; the two accepted helpers above remain this wrapper's aliases.
exec(compile(source,__file__+'.whole5492_complete_HUD_and_stock_compact_sprite_reference','exec'),globals())
