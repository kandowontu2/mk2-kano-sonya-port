"""Whole one-base VRAM replay and native scanline/register state machine.

Ordinary notifier clocks occur at screen VBLANK, with prior CPU VCOUNT273.
The next deadline is one full native field later. Explicit original CPU I/O
stores and every native scanline decrement are replayed before sampling. Scheduler timestamps during CPU taps use cycle-quantized local time; one
source-defined TMS34010 cycle can precede the already-dispatched beam timer.
No same-field DPYSTRT/latch assumption, fixed field exception or target reanchor.
"""
import hashlib,re
import numpy as np
import ending_raster_clock_model_v4709 as previous
need,Transport,digest,visible_start=previous.need,previous.Transport,previous.digest,previous.visible_start
CPU_CYCLE_SECONDS=8/50000000
IO_KEYS={'frame','human_slot','fighter','writes','assistance','epoch','event','at','register','before','value','mask','pc'}
REGISTERS={0xc0000080:'control',0xc00001b0:'tap',0xc00001e0:'dpyadr'}

def parse(line):
    if not line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RASTER_IO '):return previous.parse(line)
    pairs=re.findall(r'(\w+)=([^\s]+)',line);fields=dict(pairs)
    need(len(pairs)==len(fields)and set(fields)==IO_KEYS,'Entire actual display-register store schema')
    strings={'fighter','assistance','register'};hexadecimal={'at','before','value','mask','pc'}
    return 'FLOOR_RASTER_IO',{k:v if k in strings else int(v,16 if k in hexadecimal else 10)for k,v in fields.items()}

class Scanline:
    def __init__(self,ids):
        self.ids=ids;self.sequence=0;self.frame=None;self.clock=None;self.finished=False
        self.surface=None;self.blank=None;self.completed=0;self.records=0;self.current_count=0
        self.state=None;self.phase=-1;self.seed=None;self.blank_time=None;self.io_count=0

    def advance(self,words,row):
        previous.previous.validate_context(row,self.ids)
        need(row['epoch']==1 and row['sequence']==self.sequence+1,'Every actual clock once, no missing or duplicate actual phase')
        need(row['vsblnk']==274 and row['veblnk']==20 and row['vtotal']==288 and
             row['control']&0x03fc==16 and row['start']&3==row['dpyadr']&3==0 and row['tap']<0x4000 and
             all(np.isfinite(row[k])for k in previous.FLOAT)and row['scan_period']>0 and
             abs(row['frame_period']-289*row['scan_period'])<1e-9,
             'Actual native nonzoom fixed geometry, complete finite native periods and DUDATE')
        if row['reason']in('begin','field'):
            need((self.frame is None and row['reason']=='begin')or
                 (self.finished and row['reason']=='field'and row['frame']==self.frame+1),
                 'One actual ordinary-notifier seed per consecutive complete native renderer field')
            need(row['vcount']==273 and abs(row['next_vblank']-row['seconds']-row['frame_period'])<1e-9,
                 'Actual source-order VBLANK notifier retains prior CPU273; next screen blank is one native field later')
            fields={k:row[k]for k in('start','dpyadr','control','tap')}
            if self.state is None:self.state=fields
            else:need(fields==self.state,'All later hardware seeds compare with continuous register replay, never reanchor')
            self.frame=row['frame'];self.finished=False;self.completed=0;self.phase=-1;self.seed=row
            self.blank_time=row['next_vblank']-row['frame_period'];self.current_count=0
            self.surface=np.empty((254,400),dtype=np.uint16);self.blank=np.zeros((254,400),dtype=bool)
        else:
            need(self.seed is not None and not self.finished and row['frame']==self.frame and
                 row['seconds']>=self.clock['seconds']and row['next_event']>=self.clock['next_event'],
                 'Every actual pre-operation/finish clock remains in current real ordered field')
            need(all(row[k]==self.seed[k]for k in('vsblnk','veblnk','vtotal'))and
                 abs(row['scan_period']-self.seed['scan_period'])<1e-12 and
                 abs(row['frame_period']-self.seed['frame_period'])<1e-12,
                 'Actual fixed geometry and native scanline/frame periods retained')
            phase=(row['vcount']-274)%289
            first=self.blank_time+phase*row['scan_period']
            need(phase>=self.phase and first-CPU_CYCLE_SECONDS-1e-9<=row['seconds']<first+row['scan_period']+1e-9,
                 'Actual CPU beam follows source-scheduled native scanline; no field skipped or chosen by image')
            wanted_deadline=self.seed['next_vblank']+(row['frame_period']if row['reason']=='finish'else 0)
            need(abs(row['next_vblank']-wanted_deadline)<1e-9,'Every actual operation/finish future screen deadline bound to native cycle')
            columns=np.arange(400)
            for index in range(self.phase+1,phase+1):
                beam=(274+index)%289
                if beam==274:self.state['dpyadr']=self.state['start']
                if 20<=beam<274:
                    y=beam-20
                    need(self.completed==y,'Every indexed scanline sampled exactly once in original order')
                    before=self.state['dpyadr']
                    actual=before if self.state['control']&0x0400 else before^0xfffc
                    source_row=(actual>>4)&511
                    column=((((actual&0x7c)<<4)|(self.state['tap']&0x3fff))*2)&511
                    self.surface[y]=words[source_row,(column+columns)&511]&0x7fff
                    if not self.state['control']&0x8000:self.blank[y]=True
                    self.completed+=1
                    self.state['dpyadr']=(self.state['dpyadr']-16)&0xffff
            self.phase=phase
            need(all(row[k]==self.state[k]for k in('start','dpyadr','control','tap')),
                 'Every actual hardware register matches original explicit CPU stores and native line/latch replay')
            if row['reason']=='finish':
                need(row['vcount']==273 and self.completed==254,'All254 actual indexed rows complete before renderer frame_done')
                self.finished=True;self.records+=1
        self.clock=row;self.sequence=row['sequence'];self.current_count+=1

    def bind(self,kind,row):
        need(self.clock is not None and self.clock['frame']==row['frame']and row['event']>=self.clock['next_event']and
             not self.finished and row['epoch']==1,'Every original native operation inherits its actual preceding clock')
        if kind=='FLOOR_FLIP':
            need(row['at']==0xc0000090 and row['mask']==0xffff and row['value']&3==0,
                 'Actual original full native nonzoom DPYSTRT store, not simultaneous-latch assumption')
            self.state['start']=row['value']
        elif kind=='FLOOR_RASTER_IO':
            previous.previous.validate_context(row,self.ids)
            register=REGISTERS.get(row['at'])
            need(register is not None and row['register']==register and row['mask']==0xffff and
                 row['before']==self.state[register],
                 'Every actual explicit CPU display-register store compares with continuous prior hardware state')
            if register=='dpyadr':need(row['value']&3==0,'Original explicit DPYADR store remains nonzoom')
            elif register=='control':need(row['value']&0x03fc==16,'Original control stores retain actual DUDATE')
            else:need(row['value']<0x4000,'Native DPYTAP geometry')
            self.state[register]=row['value'];self.io_count+=1

    def compare(self,rgb,palettes,visible,control,tap):
        need(self.finished and self.completed==254 and rgb.shape==(254,400,3)and len(palettes)==131072 and
             control==self.state['control']and tap==self.state['tap']and
             visible==(self.state['dpyadr']+254*16)&0xffff,
             'Every current native scanout register independently agrees with completed continuous hardware replay')
        colors=np.frombuffer(palettes,dtype='<u4')
        expected=np.stack([(colors[self.surface]>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
        # The original disabled IND16 callback blanks to the native palette's
        # permanently black pen; this is not a matching-image/palette search.
        expected[self.blank]=0
        mismatch=np.any(expected!=rgb,axis=2)
        if mismatch.any():
            first=np.argwhere(mismatch)[0].tolist()
            raise ValueError(f'Every original source-timed native indexed pixel exact: {int(mismatch.sum())} mismatches; first {first}')
        actual=visible if control&0x0400 else visible^0xfffc
        return dict(row=(actual>>4)&511,column=((((actual&0x7c)<<4)|(tap&0x3fff))*2)&511,pixels=101600)

source=previous.source
before="'FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT','FLOOR_RASTER_CLOCK'}"
need(source.count(before)==1,'Whole original model operations plus explicit display IO only')
source=source.replace(before,before[:-1]+",'FLOOR_RASTER_IO'}",1)
before="actualRasterClocks=self.scanline.current_count,sourceTimedIndexedSHA256=digest(self.scanline.surface.astype('<u2').tobytes()),"
need(source.count(before)==1,'Original complete indexed digest plus explicit native blank/IO inventory')
source=source.replace(before,before+"\n                    sourceTimedBlankPixels=int(self.scanline.blank.sum()),actualDisplayIOStoresAtSnapshot=self.scanline.io_count,",1)
scope=dict(previous.Model.__init__.__globals__,parse=parse,Scanline=Scanline)
exec(compile(source,__file__+'::whole4709_one_base_VRAM_and_actual_IO_scanline_replay','exec'),scope)
Model=scope['Model'];MODEL_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
