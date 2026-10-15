"""Entire continuous raster model; exact true stock/added physical palette owners.

Only explicit physical-ID admission changes. All CPU/DMA/shift/FIFO/graphics/
VRAM/RGB and original compressed-shadow contracts retained. Pipeline equality
does not by itself prove aesthetic reference fidelity, all arenas or audio.
"""
import hashlib,inspect
import current_tomb_ram_model_v3642 as original
import run_jax_arms_native_scene_v4074 as assets
need,Transport,parse,digest=original.need,original.Transport,original.parse,original.digest
text=inspect.getsource(original.Model)
before='len(self.ids)==2 and set(self.ids)=={17,18}'
after='len(self.ids)==2 and 10 in self.ids and any(i in (1,4,17,18) for i in self.ids) and len(set(self.ids))==2'
need(text.count(before)==1,'Only explicit true native Scorpion/victim roster admission')
text=text.replace(before,after,1)
palette=inspect.getsource(assets.native_palette)
before='hero in(11,17,18)'
need(palette.count(before)==1,'Only exact original source palette identity admission')
palette=palette.replace(before,'hero in(1,4,10,17,18)',1)
scope=dict(vars(assets));exec(compile(palette,__file__+'::original4074_palette_owner_only','exec'),scope)
PALETTES,PALETTE_ROUTES,QUEUE_ROUTES=assets.PALETTES,assets.PALETTE_ROUTES,assets.QUEUE_ROUTES
native_palette=scope['native_palette'];palette_trace=assets.palette_trace;sources=assets.sources
namespace=dict(vars(original),check_owned_body_palette=native_palette)
exec(compile(text,__file__+'::whole3642_continuous_raster_true_stock_victim_ids','exec'),namespace)
Model=namespace['Model']
MODEL_SOURCE_SHA256=hashlib.sha256((text+palette).encode()).hexdigest().upper()
