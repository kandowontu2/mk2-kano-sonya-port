"""Entire3642 continuous native raster model with explicitly declared mirror IDs.

Only the allowed exact two-slot ID tuples change. All original CPU, integer
DMA decoding, shift/register erase, palette, one-base/continuous VRAM and exact
visible RGB checks are preserved. No comparison target initializes the model.
"""
import hashlib,inspect
import current_tomb_ram_model_v3642 as original
need=original.need
source=inspect.getsource(original.Model)
old='len(self.ids)==2 and set(self.ids)=={17,18}'
new='self.ids in ((17,18),(18,17),(17,17),(18,18))'
need(source.count(old)==1,'Exact original explicit physical-slot ID admission')
source=source.replace(old,new)
scope=dict(original.__dict__)
exec(compile(source,'<entire3642_continuous_raster_explicit_native_mirror_slots>','exec'),scope)
Model=scope['Model']
Transport=original.Transport
parse=original.parse
digest=original.digest
erase=original.erase
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
