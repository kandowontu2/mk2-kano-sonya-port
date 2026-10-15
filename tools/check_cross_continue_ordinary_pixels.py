"""Own selected-player icon and original additional image faults, current RAM."""
import inspect
from pathlib import Path
import check_continue_extra_pixels_v6617 as previous
import cross_continue_ordinary_contract as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=inspect.getsource(previous.check)
source=source.replace('audit_v6615_continue_viewport_checked_','audit_cross_continue_ordinary_checked_',1)
source=source.replace('audit_v6618_continue_extra_pixels_','audit_cross_continue_ordinary_pixels_',1)
before="top=old['actualUIPixels']['continuedViewport']['objects']['18']['projectedTop']"
after="visible=old['actualUIPixels']['continuedViewport']['visibleSourceRasterIDs'][0];top=old['actualUIPixels']['continuedViewport']['objects'][str(visible)]['projectedTop']"
need(source.count(before)==1,'Actually visible schedule source, no erasure of offscreen raster')
source=source.replace(before,after,1)
source=source.replace('contract.model.shadow(ui,18,side)',"contract.model.shadow(ui,17 if target=='kano'else 18,side)",1)
source=source.replace('proof,Path(__file__),*contract.DEPENDENCIES','proof,Path(__file__),Path(previous.__file__),*contract.DEPENDENCIES',1)
scope=dict(vars(previous),__file__=__file__,previous=previous,contract=contract)
exec(compile(source,__file__+'::whole_original_selected_player_icon_and_actual_raster_faults','exec'),scope)
check=scope['check']
