"""Whole4645/3642 one-base replay with actual operation-timed indexed surface.

Every original CPU/DMA/shift/source/pre/flip/held VRAM gate is retained. The
actual indexed display surface is sampled before writes, at source-bound
native partial-update times, then converted with the current native palette.
No special field/identity/pixel fallback, image search or comparison reanchor.
"""
import hashlib,re
import numpy as np
import ending_display_ram_model_v4645 as previous
need,Transport,digest,visible_start=previous.need,previous.Transport,previous.digest,previous.visible_start
FLOAT={'seconds','next_vblank','scan_period','frame_period'}
HEX={'start','dpyadr','control','tap'}
STR={'fighter','assistance','reason'}
KEYS={'frame','human_slot','fighter','writes','assistance','epoch','sequence','next_event','reason',
      'start','dpyadr','control','tap','vcount','vsblnk','veblnk','vtotal'}|FLOAT

def parse(line):
    if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_CLOCK '):return previous.parse(line)
    pairs=re.findall(r'(\w+)=([^\s]+)',line);row=dict(pairs)
    need(len(row)==len(pairs)and set(row)==KEYS,'Exact complete actual operation raster clock schema')
    need(row['reason']in('begin','field','before','finish'),'Only actual observer clock phases')
    return 'FLOOR_RASTER_CLOCK',{k:v if k in STR else float(v)if k in FLOAT else int(v,16 if k in HEX else 10)for k,v in row.items()}

class Scanline:
    def __init__(self,ids):
        self.ids=ids;self.sequence=0;self.frame=None;self.clock=None;self.finished=False
        self.surface=None;self.completed=0;self.records=0;self.current_count=0
        self.request=None;self.latched=None;self.seed=None;self.phase=-1

    def advance(self,words,row):
        previous.validate_context(row,self.ids)
        need(row['epoch']==1 and row['sequence']==self.sequence+1,'Every actual clock once in original sequential epoch')
        need(row['vsblnk']==274 and row['veblnk']==20 and row['vtotal']==288 and
             row['control']&0x8000 and row['control']&0x03fc==16 and
             row['start']&3==row['dpyadr']&3==0 and row['tap']<0x4000 and
             all(np.isfinite(row[k])for k in FLOAT)and row['scan_period']>0 and
             abs(row['frame_period']-289*row['scan_period'])<1e-9,
             'Actual enabled nonzoom native289scanline/254visible geometry and periods')
        if row['reason']in('begin','field'):
            need((self.frame is None and row['reason']=='begin')or
                 (self.finished and row['reason']=='field'and row['frame']==self.frame+1),
                 'One actual ordinary-notifier seed per consecutive completed renderer field')
            need(row['vcount']==273 and 0<row['next_vblank']-row['seconds']<=row['scan_period']+1e-9,
                 'Actual field starts after prior273partial update, before next274latch')
            self.frame=row['frame'];self.surface=np.empty((254,400),dtype=np.uint16)
            self.completed=0;self.finished=False;self.latched=None;self.seed=row
            self.request=row['start'];self.phase=-1;self.current_count=0
        else:
            need(self.seed is not None and row['frame']==self.frame and not self.finished,
                 'Every actual operation/finish clock belongs to current incomplete renderer field')
            need(row['seconds']>=self.clock['seconds']and row['next_event']>=self.clock['next_event'],
                 'Actual native time and operation cursor never reverse')
            need(all(row[k]==self.seed[k]for k in('control','tap','vsblnk','veblnk','vtotal'))and
                 abs(row['scan_period']-self.seed['scan_period'])<1e-12 and
                 abs(row['frame_period']-self.seed['frame_period'])<1e-12,
                 'No unobserved geometry/control/tap change within a field')
            need(row['start']==self.request,'Every native DPYSTRT request bound to original observed flip stores')
            if row['seconds']<self.seed['next_vblank']-1e-9:
                need(row['vcount']==273 and row['dpyadr']==self.seed['dpyadr']and row['reason']=='before',
                     'Initial post-partial prior-field writes are before actual274latch, not new visible pixels')
            else:
                if self.latched is None:self.latched=self.request
                phase=(row['vcount']-274)%289
                first=self.seed['next_vblank']+phase*row['scan_period']
                need(phase>=self.phase and first-1e-9<=row['seconds']<first+row['scan_period']+1e-9,
                     'Every real beam clock follows actual source-scheduled scanline, no skipped cycle')
                self.phase=phase
                visible=20<=row['vcount']<274
                count=row['vcount']-20+1 if visible else 0
                address=(self.latched-count*16)&0xffff
                need(row['dpyadr']==address,'Actual DPYADR from observed native274latch and original per-line DUDATE')
                if visible:
                    columns=np.arange(400)
                    for y in range(self.completed,count):
                        before=(self.latched-y*16)&0xffff
                        actual=before if row['control']&0x0400 else before^0xfffc
                        source_row=(actual>>4)&511
                        column=((((actual&0x7c)<<4)|(row['tap']&0x3fff))*2)&511
                        self.surface[y]=words[source_row,(column+columns)&511]&0x7fff
                    self.completed=count
            if row['reason']=='finish':
                need(row['vcount']==273 and self.completed==254,'All254 actual indexed rows completed before native frame_done')
                self.finished=True;self.records+=1
        self.clock=row;self.sequence=row['sequence'];self.current_count+=1

    def bind(self,kind,row):
        need(self.clock is not None and self.clock['frame']==row['frame']and
             row['event']>=self.clock['next_event']and not self.finished,
             'Every original operation inherits its actual immediately preceding native clock')
        if kind=='FLOOR_FLIP':self.request=row['value']

    def compare(self,rgb,palettes,visible,control,tap):
        need(self.finished and self.completed==254 and rgb.shape==(254,400,3)and len(palettes)==131072,
             'Complete native indexed surface/current palette/RGB, no omitted row or pixel')
        colors=np.frombuffer(palettes,dtype='<u4')
        expected=np.stack([(colors[self.surface]>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
        mismatch=np.any(expected!=rgb,axis=2)
        if mismatch.any():
            where=np.argwhere(mismatch)[0].tolist()
            raise ValueError(f'Every actual source-timed scanline pixel exact: {int(mismatch.sum())} mismatches; first {where}')
        actual=visible if control&0x0400 else visible^0xfffc
        return dict(row=(actual>>4)&511,column=((((actual&0x7c)<<4)|(tap&0x3fff))*2)&511,pixels=101600)

source=previous.source
changes=[
 ("self.cpu_count=self.palette_checks=0; self.records=[]; self.counterexamples=[]",
  "self.cpu_count=self.palette_checks=0; self.records=[]; self.counterexamples=[]\n        self.scanline=Scanline(self.ids)"),
 ("'FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT'}",
  "'FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT','FLOOR_RASTER_CLOCK'}"),
 ("        kind,row = parsed\n        if kind=='FLOOR_CPU':",
  "        kind,row = parsed\n        if kind=='FLOOR_RASTER_CLOCK':\n            self.events.append((kind,row));return\n        if kind=='FLOOR_CPU':"),
 ("            model=self.replay\n            need(row['epoch']==1,",
  "            model=self.replay\n            if kind=='FLOOR_RASTER_CLOCK':\n                self.scanline.advance(model.words,row);continue\n            need(row['epoch']==1,"),
 ("            model.last_event=row['event']\n            if kind=='FLOOR_PRE_FRAME':",
  "            self.scanline.bind(kind,row)\n            model.last_event=row['event']\n            if kind=='FLOOR_PRE_FRAME':"),
 ("bound=check_latch(rgb,raw,palettes,visible,target['control'],target['tap'])",
  "bound=self.scanline.compare(rgb,palettes,visible,target['control'],target['tap'])"),
 ("check_latch(changed,raw,palettes,visible,target['control'],target['tap'])",
  "self.scanline.compare(changed,palettes,visible,target['control'],target['tap'])"),
 ("check_latch(rgb,raw,palettes,visible,target['control'],target['tap'])",
  "self.scanline.compare(rgb,palettes,visible,target['control'],target['tap'])"),
 ("                    exactVRAMWords=512*512,exactRGBPixels=bound['pixels'],rgbSHA256=digest(rgb.tobytes()),",
  "                    exactVRAMWords=512*512,exactRGBPixels=bound['pixels'],rgbSHA256=digest(rgb.tobytes()),\n                    actualRasterClocks=self.scanline.current_count,sourceTimedIndexedSHA256=digest(self.scanline.surface.astype('<u2').tobytes()),"),
]
for before,after in changes:
    need(source.count(before)==1,'Only declared full pipeline scanline timing adaptation: '+before)
    source=source.replace(before,after,1)
scope=dict(vars(previous.previous.previous.original),parse=parse,visible_start=visible_start,
           validate_context=previous.validate_context,Scanline=Scanline)
exec(compile(source,__file__+'::whole4645_one_base_pipeline_actual_raster_clock','exec'),scope)
Model=scope['Model'];MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
