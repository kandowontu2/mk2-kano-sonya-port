"""Whole continuous3642 native CPU/DMA/shift/RGB model for ending video.

No floor actor classifier is used in this window. Only that floor-specific
identity admission/palette assertion and first held-base initialization adapt;
every actual CPU/DMA/shift/graphics/pre-pass/flip/VRAM/RGB gate remains intact.
This is not an independent stock slideshow/cinematic/art/audio reference.
"""
import hashlib,inspect
import current_tomb_ram_model_v3642 as original
need,Transport,parse,digest=original.need,original.Transport,original.parse,original.digest
source=inspect.getsource(original.Model)
changes={
 "len(self.ids)==2 and set(self.ids)=={17,18}":"self.ids in ((13,17),(13,18))",
 "need(colors[15]==0, 'Native shadow pen15 remains black')":"need(len(colors)==32768, 'Complete actual native ending palette, not a floor shadow palette assertion')",
 "self.replay_events(); frame=snap['frame']":"self.replay_events(); frame=snap['frame']\n        if self.replay is None: self.begin(snap['epoch'])",
}
for before,after in changes.items():
    need(source.count(before)==1,'Only declared original continuous model adaptation: '+before)
    source=source.replace(before,after)
scope=dict(vars(original))
exec(compile(source,__file__+'::entire3642_native_ending_pipeline','exec'),scope)
Model=scope['Model']
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
