"""Whole original continuous renderer; true knife and single-frame blade roles.

Pixel/CPU/DMA/shift/VRAM/RGB kernels unchanged. Only explicit mirror tuple,
effect palette dispatch and visible ownership inventory extend the model.
One initial base only; no tested later target ever initializes rendering.
"""
import hashlib,inspect,struct
import numpy as np
import current_tomb_ram_model_v3642 as original
import verify_human_projectile_display_v1352 as art
need,digest,parse,Transport=original.need,original.digest,original.parse,original.Transport


def owned_palette(scene,q,colors):
 if q['slot']in(1,2):
  original.check_owned_body_palette(q,colors,scene.guest,scene.ids,q['slot']);return
 need(q['slot']in(3,4)and q['parent']!=q['actor']and q['roster']==17,
      'Only actual separate native knife/blade effects use effect palettes')
 if q['slot']==3:
  need(q['kind']==1 and q['multipart']==1 and q['owner']==q['actor']and q['id']==17,'True owned native knife child')
  descriptor=art.read(scene.payload,q['pose'],'<I',0xfe800000)[0]
  palette=art.read(scene.payload,descriptor+112,'<I',0xfe800000)[0]
 else:
  need(q['kind']==2 and q['multipart']==0 and q['owner']==q['parent']and q['pose']==0 and
       0xfff8f800<=q['cache']<=0xfff8fda0 and(q['cache']-0xfff8f800)%160==0,
       'Actual single-frame blade descriptor, source-owned parent Main, no fake fighter ID')
  palette=art.read(scene.guest,q['cache']+112,'<I',0xff800000)[0]
  need(palette==0xfe800000+0x1d0100*8,'Dedicated original blade palette, not a body bank alias')
 raw,base=(scene.payload,0xfe800000)if 0xfe800000<=palette<0xff800000 else(scene.guest,0xff800000)
 need(art.read(raw,palette,'<H',base)[0]==64,'Whole64pen original effect palette')
 words=art.read(raw,palette+16,'<64H',base)
 expected=np.array([sum(((((c>>shift)&31)<<3)|(((c>>shift)&31)>>2))<<dest
                       for shift,dest in((10,16),(5,8),(0,0)))for c in words],dtype=np.uint32)
 bank=q['bank']&0x7f00
 need(np.array_equal(colors[bank:bank+64],expected),'Whole source-bound native effect palette reaches scanout')


source=inspect.getsource(original.Model)
changes={
 'len(self.ids)==2 and set(self.ids)=={17,18}':'self.ids==(17,17)',
 "check_owned_body_palette(q,colors,self.guest,self.ids,q['slot'])":'owned_palette(self,q,colors)',
 'for n in(1,2)})':'for n in(1,2,3,4)})',
}
for before,after in changes.items():
 need(source.count(before)==1,'Only declared role/palette/inventory extension');source=source.replace(before,after,1)
scope=dict(original.__dict__,owned_palette=owned_palette)
exec(compile(source,__file__+'::whole_original_continuous_native_renderer','exec'),scope)
Model=scope['Model']
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
