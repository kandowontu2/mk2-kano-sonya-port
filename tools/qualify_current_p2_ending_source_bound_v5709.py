"""Preserve5705's failed preflight; complete the inverse typed address map.

The actual Lua5701 already has both inverse entries. Retain every original
source/model/control gate and bind the corrected full collector before boot.
"""
from pathlib import Path
import qualify_current_p2_ending_source_v5705 as previous

source=Path(previous.__file__).read_text()
changes=[
 ("OUT=ROOT/'audit_v5706_current_p2_ending_source_checked'",
  "OUT=ROOT/'audit_v5710_current_p2_ending_source_checked'"),
 ('addresses=dict(parent.parent.ADDRESSES)',
  "addresses=dict(parent.parent.ADDRESSES)\n addresses.update({'0x01060ecf':'0x010602ff','0x010601f0':'0x01060dc0'})"),
 ('import run_current_p2_ending_pixels_v5707 as host',
  'import run_current_p2_ending_pixels_bound_v5711 as host'),
 ('pins={}',
  "failure=ROOT/'audit_v5706_current_p2_ending_source_checked/report.json'\n failed=json.loads(failure.read_text())\n need(not failed['passed']and 'Every original P2 admission' in failed['error'],'Actual failed source adapter retained, not native game failure')\n pins={str(Path(previous.__file__).resolve()):sha(previous.__file__),str(failure):sha(failure)}")]
for before,after in changes:
 previous.need(source.count(before)==1,'Unique full source preflight correction '+before)
 source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_corrected_inverse_map_preflight','exec'),globals())
