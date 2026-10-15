"""Complete previously qualified renderer, only explicit physical P1 context.

No pixel/timing/CPU/DMA/shift/VRAM tolerance, reanchor or field exception.
Clone function globals rather than changing the immutable P2 model modules.
"""
import hashlib,inspect,re
from types import SimpleNamespace
import ending_raster_cpu_cycle_model_v4740 as original
import ending_display_ram_model_v4645 as context
import ending_raster_clock_model_v4709 as clock
need,Transport,digest,visible_start=original.need,original.Transport,original.digest,original.visible_start
CPU_CYCLE_SECONDS=original.CPU_CYCLE_SECONDS

def validate_context(scan,ids):
 need(ids in ((17,13),(18,13))and
  (scan['fighter'],scan['human_slot'],scan['writes'],scan['assistance'])==
  ('kano'if ids==(17,13)else'sonya',1,0,'none'),
  'Every actual hardware field bound to the true own model and original physical context')

scan_source=inspect.getsource(context.parse)
before="fields['human_slot']=='2'"
need(scan_source.count(before)==1,'Only exact parser physical-slot admission changes')
scan_source=scan_source.replace(before,"fields['human_slot']=='1'",1).replace('physical P2 ending','physical P1 ending')
scan_scope=dict(context.parse.__globals__)
exec(compile(scan_source,__file__+'::entire_original_scanout_parser_P1','exec'),scan_scope)
scan_parse=scan_scope['parse']
clock_scope=dict(clock.parse.__globals__,previous=SimpleNamespace(parse=scan_parse))
exec(compile(inspect.getsource(clock.parse),__file__+'::entire_original_clock_parser','exec'),clock_scope)
clock_parse=clock_scope['parse']
io_scope=dict(original.parse.__globals__,previous=SimpleNamespace(parse=clock_parse))
exec(compile(inspect.getsource(original.parse),__file__+'::entire_original_IO_parser','exec'),io_scope)
parse=io_scope['parse']
scanline_source=inspect.getsource(original.Scanline)
scanline_scope=dict(original.Scanline.__init__.__globals__,
 previous=SimpleNamespace(previous=SimpleNamespace(validate_context=validate_context),FLOAT=clock.FLOAT))
exec(compile(scanline_source,__file__+'::entire_original_scanline_state_machine','exec'),scanline_scope)
Scanline=scanline_scope['Scanline']
source=original.source
before='self.ids in ((13,17),(13,18))'
need(source.count(before)==1,'Only complete renderer physical identity admission changes')
source=source.replace(before,'self.ids in ((17,13),(18,13))',1)
scope=dict(original.Model.__init__.__globals__,parse=parse,Scanline=Scanline,validate_context=validate_context)
exec(compile(source,__file__+'::entire_original_single_base_native_renderer_P1','exec'),scope)
Model=scope['Model']
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
