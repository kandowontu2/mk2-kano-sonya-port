"""Entire qualified continuous renderer; explicit Sonya charge/child palettes."""
import hashlib,inspect
import current_tomb_ram_model_v3642 as original
import current_cpu_effect_render_model_v6347 as effects
import verify_ring_glow_source_v1310 as charge
need,digest,parse,Transport=original.need,original.digest,original.parse,original.Transport


def owned_palette(scene,q,colors):
 if q['slot']==2 and q['pose']in charge.CHARGE_POSES:
  need(q['id']==q['roster']==18 and q['actor']==q['owner'],'Actual true Sonya charging body owner')
  charge.check_charge_palette(q,colors);return
 if q['slot']in(1,2):
  original.check_owned_body_palette(q,colors,scene.guest,scene.ids,q['slot']);return
 # Keep the complete originally qualified knife/ring64-pen routine. The only
 # effect identity admission differs; this observer has no blade slot4.
 source=inspect.getsource(effects.owned_palette)
 need(source.count("q['roster']==17")==1 and source.count("q['id']==17")==1,'Only true native effect identity differs')
 source=source.replace("q['roster']==17","q['roster']==18",1).replace("q['id']==17","q['id']==18",1)
 scope=dict(effects.owned_palette.__globals__)
 exec(compile(source,__file__+'::whole_original64pen_ring_effect_palette','exec'),scope)
 need(q['slot']==3,'Only the actual ring child uses effect colors')
 scope['owned_palette'](scene,q,colors)


source=inspect.getsource(original.Model)
changes={"check_owned_body_palette(q,colors,self.guest,self.ids,q['slot'])":'owned_palette(self,q,colors)',
         'for n in(1,2)})':'for n in(1,2,3)})'}
for before,after in changes.items():
 need(source.count(before)==1,'Only native charge/effect palette and visible role inventory changes')
 source=source.replace(before,after,1)
scope=dict(original.__dict__,owned_palette=owned_palette)
exec(compile(source,__file__+'::whole_original_continuous_native_ring_renderer','exec'),scope)
Model=scope['Model'];MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
