"""Whole ending pipeline with independently hardware-derived native scanout.

Keep the entire4519/3642 integer CPU/DMA/shift/source/pre/flip/held replay.
Only RGB crop binding uses actual DPYADR/beam timing instead of requested
DPYSTRT. No matching-buffer search, comparison reanchor, or game mutation.
"""
import hashlib,re
import ending_display_ram_model_v4519 as previous

need,Transport,digest=previous.need,previous.Transport,previous.digest

def parse(line):
    if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SCANOUT '):
        return previous.parse(line)
    fields=dict(re.findall(r'(\w+)=([^\s]+)',line))
    need(set(fields)=={'frame','epoch','start','dpyadr','control','tap','vcount','vsblnk','veblnk'},
         'Complete actual native hardware scanout metadata, no inferred fields')
    return 'FLOOR_SCANOUT',{k:int(v,16 if k in {'start','dpyadr','control','tap'} else 10)
                            for k,v in fields.items()}

def visible_start(scan,display,frame):
    need(scan['frame']==display['frame']==frame and scan['epoch']==display['epoch']==1,
         'Actual hardware/palette/RGB field and original epoch binding')
    need(all(scan[k]==display[k]for k in ('start','control','tap')),
         'Actual hardware scanout retains all original requested-display registers')
    need(scan['vcount']==scan['vsblnk']-1 and scan['vsblnk']-scan['veblnk']==254 and
         scan['control']&0x8000 and scan['start']&3==scan['dpyadr']&3==0 and
         scan['control']&0x03fc==16,
         'Actual end-of-visible enabled nonzoom native DUDATE scope; never guess a row')
    return (scan['dpyadr']+(scan['vcount']-scan['veblnk']+1)*(scan['control']&0x03fc))&0xffff

source=previous.source
changes=[
    ("palettes=self.raw.pop(display['palette_file']); rgb=self.rgb.pop(snap['file'])",
     "need(len(self.groups['FLOOR_SCANOUT'])==len(self.records)+1, 'Exactly one actual hardware row per continuous field')\n"
     "        scan=self.groups['FLOOR_SCANOUT'][-1]; visible=visible_start(scan,display,frame)\n"
     "        palettes=self.raw.pop(display['palette_file']); rgb=self.rgb.pop(snap['file'])"),
    ("record=dict(frame=frame,event=target['event'],modeledFlip=modeled,",
     "record=dict(frame=frame,event=target['event'],modeledFlip=modeled,\n"
     "                    requestedStart=scan['start'],nativeDPYADR=scan['dpyadr'],hardwareDerivedVisibleStart=visible,")]
for before,after in changes:
    need(source.count(before)==1,'One declared complete native model boundary: '+before)
    source=source.replace(before,after)
before="raw,palettes,target['start'],target['control'],target['tap']"
need(source.count(before)==3,'Original positive RGB, actual bit fault, and positive restoration all retained')
source=source.replace(before,"raw,palettes,visible,target['control'],target['tap']")
scope=dict(vars(previous.original),parse=parse,visible_start=visible_start)
exec(compile(source,__file__+'::entire3642_hardware_bound_ending_pipeline','exec'),scope)
Model=scope['Model']
MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
