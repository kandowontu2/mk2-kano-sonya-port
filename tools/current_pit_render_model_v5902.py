"""Entire3642 continuous renderer; explicit native cinematic slot4 palette.

No ID proxies, physical-slot remapping or target anchors. The whole original
CPU/DMA/shift/one-base/VRAM/RGB/palette gates remain. Cinematic Main+140 owner,
true victim and normal65color source palette are checked independently.
"""
import hashlib,inspect,struct
import numpy as np
import current_tomb_ram_model_v3642 as original
import verify_current_native_pit_matrix_v2107 as pit
need,digest,parse,Transport,erase=original.need,original.digest,original.parse,original.Transport,original.erase

def owned_palette(scene,q,colors):
 if q['slot'] in (1,2):
  original.check_owned_body_palette(q,colors,scene.guest,scene.ids,q['slot'])
  return
 need(q['slot']==4 and len(scene.groups['FLOOR_PIT_CONSTRUCTED'])==1,
      'Only source-qualified native cinematic slot4 has a nonphysical palette')
 cine=scene.groups['FLOOR_PIT_CONSTRUCTED'][0]
 need(q['actor']==q['owner']==cine['actor']==cine['owner'] and q['main']==cine['main'] and
      q['parent']==cine['original'] and q['id']==q['roster']==cine['id'] and
      q['id'] in scene.ids and q['kind']==2 and not q['body']&64,
      'Actual cinematic Main+140 owner, original victim ancestry and true normal palette')
 pointer=0xfda00 if q['id']==17 else 0xfdb00
 raw=struct.unpack_from('<65H',scene.guest,pointer+2)
 expected=np.array([sum(((((c>>shift)&31)<<3)|(((c>>shift)&31)>>2))<<dest
                       for shift,dest in ((10,16),(5,8),(0,0)))for c in raw],dtype=np.uint32)
 bank=q['bank']&0x7f00
 need(np.array_equal(colors[bank:bank+65],expected),
      'All65source-bound cinematic palette entries reach actual scanout unchanged')

source=inspect.getsource(original.Model)
before="check_owned_body_palette(q,colors,self.guest,self.ids,q['slot'])"
need(source.count(before)==1,'One original physical palette dispatch')
source=source.replace(before,'owned_palette(self,q,colors)',1)
before='for n in(1,2)})'
need(source.count(before)==1,'One original visible-body record inventory')
source=source.replace(before,'for n in(1,2,4)})',1)
scope=dict(vars(original),owned_palette=owned_palette)
exec(compile(source,__file__+'::entire3642_native_Pit_cinematic_palette','exec'),scope)
Model=scope['Model']
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
