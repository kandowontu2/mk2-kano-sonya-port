"""Entire qualified Ring renderer, explicitly two real Sonya physical IDs.

Only the admitted identity tuple changes. All native palette, CPU/DMA/shift,
scanout, one-base and no-target-reseed kernels remain identical to6376.
"""
import hashlib
import current_cpu_ring_render_model_v6376 as prior
original=prior.original
need,digest,parse,Transport=prior.need,prior.digest,prior.parse,prior.Transport
source=prior.source
before='len(self.ids)==2 and set(self.ids)=={17,18}'
need(source.count(before)==1,'Only explicit genuine physical mirror identity admission changes')
source=source.replace(before,'self.ids==(18,18)',1)
scope=dict(prior.scope)
exec(compile(source,__file__+'::whole_original_renderer_true_Sonya_mirror','exec'),scope)
Model=scope['Model'];MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
