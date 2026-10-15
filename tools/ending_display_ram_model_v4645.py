"""Whole hardware-bound ending replay with actual native log context schema.

The original2062 logger adds human_slot/fighter/writes/assistance to every
record. Admit precisely those real fields and validate their physical scope.
Keep every4612/4519/3642 hardware/CPU/DMA/shift/VRAM/RGB/fault gate unchanged.
"""
import hashlib,re
import ending_display_ram_model_v4612 as previous
need,Transport,digest,visible_start=previous.need,previous.Transport,previous.digest,previous.visible_start

def parse(line):
    if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT '):return previous.parse(line)
    pairs=re.findall(r'(\w+)=([^\s]+)',line);fields=dict(pairs)
    need(len(pairs)==len(fields)and set(fields)=={'frame','human_slot','fighter','writes','assistance','epoch','start','dpyadr','control','tap','vcount','vsblnk','veblnk'},
         'Complete actual native hardware and original logger context schema; no inferred or dropped fields')
    need(fields['human_slot']=='2'and fields['fighter']in ('kano','sonya')and fields['writes']=='0'and fields['assistance']=='none',
         'Actual unchanged physical P2 ending context, no guest writes or assistance')
    strings={'fighter','assistance'};hexadecimal={'start','dpyadr','control','tap'}
    return 'FLOOR_SCANOUT',{k:v if k in strings else int(v,16 if k in hexadecimal else 10)for k,v in fields.items()}

def validate_context(scan,ids):
    need(ids in ((13,17),(13,18))and
         (scan['fighter'],scan['human_slot'],scan['writes'],scan['assistance'])==
         ('kano'if ids==(13,17)else'sonya',2,0,'none'),
         'Every actual hardware field bound to the true own model and original physical context')

source=previous.source
before="scan=self.groups['FLOOR_SCANOUT'][-1]; visible=visible_start(scan,display,frame)"
need(source.count(before)==1,'Only actual per-field true model/context binding added')
source=source.replace(before,"scan=self.groups['FLOOR_SCANOUT'][-1]; validate_context(scan,self.ids); visible=visible_start(scan,display,frame)")
scope=dict(vars(previous.previous.original),parse=parse,visible_start=visible_start,validate_context=validate_context)
exec(compile(source,__file__+'::entire_hardware_bound_ending_with_native_context_schema','exec'),scope)
Model=scope['Model'];MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
