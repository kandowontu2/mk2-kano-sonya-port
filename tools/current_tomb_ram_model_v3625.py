"""Exact continuous native Tomb CPU/DMA/shift/scanout model, RAM targets only.

Reuse the existing integer decoders and transfer contracts unchanged. Only
the first actual base initializes the model. All later VRAM is a comparison
target, including held scanouts. Transport delta bases never seed the replay.
"""
import hashlib
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import inspect_current_cpu_knife_raster_v1975 as raster
import inspect_ball_register_erase_v1843 as erase
from verify_native_floor_display_v602 import check_latch
from verify_finish_display_v798 import check_owned_body_palette

raster.base.STR |= {'seconds'}
raster.base.HEX |= {'gravity','vx','vy','flags','trail','io0'}


def need(ok, message):
    if not ok: raise ValueError(message)


def digest(raw): return hashlib.sha256(raw).hexdigest().upper()


def parse(line):
    match = re.match(r'MK2_NAT_CAMPAIGN_(FLOOR_\w+|SHADOW_\w+) ', line)
    if not match: return None
    row = dict(re.findall(r'(\w+)=([^\s]+)', line))
    hexadecimal = raster.base.HEX | {'dest','native_offset','pitch','shape','status',
        'raster_control','psize','convdp_io','world','camera','display','clipLow','clipHigh'}
    strings = raster.base.STR | {'register','words','reason'}
    for key, value in row.items():
        if key not in strings: row[key] = int(value,16 if key in hexadecimal else 10)
    return match[1],row


class Transport:
    def __init__(self):
        self.previous = {}
        self.records = []

    def decode(self, row, encoded):
        file, family = row['file'],row['family']
        size, prior, count = (int(row[k]) for k in ('bytes','prior','blocks'))
        need(row['encoding']=='u32le_numeric_hex_delta' and row['block_bytes']=='64'
             and size in (2048,131072,524288,1048576), 'Exact bounded RAM transport format')
        wanted = re.sub(r'^display_(pre|vram|palette)_\d+\.bin$',r'\1',file)
        need(family==wanted and prior in (0,1) and bool(prior)==(family in self.previous),
             'Exact declared transport family and predecessor')
        raw = bytearray(self.previous[family]) if prior else bytearray(size)
        need(len(raw)==size, 'Unchanged family byte size')
        entries = encoded.split(',') if encoded else []
        need(len(entries)==count, 'Exact declared transport block count')
        seen = []
        for entry in entries:
            index,hexadecimal = entry.split(':')
            index = int(index); first = index*64
            need(index>=0 and first<size and len(hexadecimal)==min(64,size-first)*2
                 and re.fullmatch('[0-9A-F]+',hexadecimal), 'Complete bounded native block')
            need(not seen or seen[-1]<index, 'Unique increasing native blocks')
            seen.append(index)
            words = np.frombuffer(bytes.fromhex(hexadecimal),dtype='>u4')
            block = words.astype('<u4').tobytes()
            if prior: need(block!=self.previous[family][first:first+64], 'Only exact changed transport blocks')
            raw[first:first+len(block)] = block
        if not prior: need(seen==list(range((size+63)//64)), 'Initial transport base has every block')
        raw = bytes(raw); self.previous[family] = raw
        self.records.append(dict(file=file,bytes=size,changedBlocks=count,rawSHA256=digest(raw)))
        return raw


class Model:
    OPERATIONS = {'FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP',
                  'FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT'}

    def __init__(self, guest, payload, graphics):
        self.guest,self.payload,self.graphics = guest,payload,graphics
        self.groups = defaultdict(list); self.buffers = {}; self.owners = defaultdict(list)
        self.raw = {}; self.rgb = {}; self.events = []; self.replay = None
        self.flips = {}; self.shift = None; self.shift_data = {}
        self.pre_count=self.flip_count=self.loads=self.fills=self.transfers=self.direct=0
        self.cpu_count=self.palette_checks=0; self.records=[]; self.counterexamples=[]

    def line(self, line):
        parsed = parse(line)
        if not parsed: return
        kind,row = parsed
        if kind=='FLOOR_CPU': self.cpu_count+=1
        else: self.groups[kind].append(row)
        if kind=='FLOOR_GFX':
            raw=bytes.fromhex(row['data'])
            need(0<=row['first']<row['first']+row['bytes']<=len(self.graphics)
                 and len(raw)==row['bytes'] and raw==self.graphics[row['first']:row['first']+row['bytes']],
                 'Every observed graphics stream equals independent ROM/payload/UI bytes')
            need(row['key'] not in self.buffers, 'Unique observed graphics stream')
            self.buffers[row['key']]=row
        if kind=='FLOOR_OWNER': self.owners[row['frame'],row['source'],row['slot']].append(row)
        if kind=='FLOOR_SHIFT_DATA': self.shift_data[row['ref']]=self.raw.pop(row['file'])
        if kind in self.OPERATIONS: self.events.append((kind,row))
        if kind=='FLOOR_SNAP': self.snapshot(row)

    def begin(self, epoch):
        need(self.replay is None and len(self.groups['FLOOR_BASE'])==1, 'One initial native base only')
        self.replay=raster.Replay(Path('.'),self.groups,self.buffers,self.owners)
        base=self.groups['FLOOR_BASE'][0]; raw=self.raw.pop(base['file'])
        need(base['epoch']==epoch==1 and len(raw)==512*512*2 and
             base['phase']=='before_first_observed_write', 'Original initial VRAM base scope')
        self.replay.words=np.frombuffer(raw,dtype='<u2').copy().reshape(512,512)
        self.replay.body=np.zeros((512,512),dtype=np.uint8)
        self.replay.shadow=np.zeros((512,512),dtype=bool)
        self.replay.projected=np.zeros((512,512),dtype=bool)
        self.replay.epoch=epoch; self.replay.last_event=base['event']

    @staticmethod
    def exact(words,raw,label):
        actual=np.frombuffer(raw,dtype='<u2').reshape(512,512)
        mismatch=words!=actual
        if mismatch.any():
            y,x=np.argwhere(mismatch)[0]
            raise ValueError(f'{label}: {int(mismatch.sum())} word mismatches; first ({x},{y}) '
                             f'model={int(words[y,x]):04X} actual={int(actual[y,x]):04X}')

    def replay_events(self):
        for kind,row in self.events:
            if self.replay is None: self.begin(row['epoch'])
            model=self.replay
            need(row['epoch']==1, 'No later epoch or comparison target as model anchor')
            if row['event']<=model.last_event:
                need(kind=='FLOOR_FLIP' and row['event']==model.last_event,
                     'Only the initial pre-base native flip may precede its base')
                continue
            model.last_event=row['event']
            if kind=='FLOOR_PRE_FRAME':
                need(row['phase']=='before_first_frame_dma', 'Exact original pre-pass target')
                raw=self.raw.pop(row['file']); self.exact(model.words,raw,'Continuous pre-pass')
                self.pre_count+=1
            elif kind=='FLOOR_FLIP':
                self.flips[row['event']] = (model.words.copy(),model.body.copy(),model.shadow.copy(),row)
            elif kind=='FLOOR_SHIFT_LOAD':
                need((row['at'],row['pc'],row['op'],row['mask'],row['address'])==
                     (0xff817080,0xff817090,0xfa52,65535,0x1fe000) and row['control']&0x0800
                     and row['index']==row['address']>>3, 'Original native shift template load')
                raw=self.shift_data[row['ref']]
                expected=model.words.ravel()[row['index']:row['index']+1024].astype('<u2').tobytes()
                need(raw==expected, 'Shift stream equals preceding continuously modeled VRAM')
                self.shift=raw; self.loads+=1
            elif kind in ('FLOOR_SHIFT_FILL','FLOOR_SHIFT'):
                need(self.shift is not None and self.shift_data[row['ref']]==self.shift,
                     'Exact preceding original shift load, not a guessed erase rectangle')
                if kind=='FLOOR_SHIFT_FILL': indices=erase.copies_for_fill(row); self.fills+=1
                else:
                    need((row['at'],row['pc'],row['op'],row['mask'])==
                         (0xff816380,0xff816390,0xf800,65535) and row['control']&0x0800 and
                         row['index']==row['address']>>3 and 0<=row['index']<=512*512-1024,
                         'Original precise native shift store')
                    indices=[row['index']]; self.direct+=1
                for index in indices:
                    model.words.ravel()[index:index+1024]=np.frombuffer(self.shift,dtype='<u2')
                    model.body.ravel()[index:index+1024]=0
                    model.shadow.ravel()[index:index+1024]=False
                self.transfers+=len(indices)
            elif kind=='FLOOR_DMA': model.dma(row)
            elif kind=='FLOOR_CPU': model.cpu(row)
        self.events.clear()

    def snapshot(self,snap):
        self.replay_events(); frame=snap['frame']
        display=self.groups['FLOOR_DISPLAY'][-1]
        need(display['frame']==frame, 'Actual palette and snapshot field binding')
        palettes=self.raw.pop(display['palette_file']); rgb=self.rgb.pop(snap['file'])
        latch=self.groups['FLOOR_LATCH'][-1] if self.groups['FLOOR_LATCH'] else None
        modeled=bool(latch and latch['snapshot']==frame)
        if modeled:
            need(latch['flip_frame']==frame and latch['event'] in self.flips, 'Actual current native flip')
            words,body,shadow,flip=self.flips[latch['event']]
            need(tuple(latch[k]for k in('start','control','tap'))==
                 (flip['value'],flip['control'],flip['tap'])==tuple(display[k]for k in('start','control','tap')),
                 'Exact CPU flip/current display/snapshot registers')
            target=latch; self.flip_count+=1
        else:
            target=self.groups['FLOOR_HELD'][-1]
            need(target['snapshot']==frame, 'Actual held native scanout field')
            words,body,shadow=(self.replay.words,self.replay.body,self.replay.shadow)
        raw=self.raw.pop(target['file']); self.exact(words,raw,'Continuous flip/held target')
        bound=check_latch(rgb,raw,palettes,target['start'],target['control'],target['tap'])
        row,col=bound['row'],bound['column']; crop=lambda a:a[row:row+254,col:col+400]
        colors=np.frombuffer(palettes,dtype='<u4'); need(colors[15]==0, 'Native shadow pen15 remains black')
        queues={(q['frame'],q['cursor']):q for q in self.groups['FLOOR_QUEUE'] if q['frame']==frame-1}
        for d in self.groups['FLOOR_QUEUE_DISPATCH']:
            if d['frame']!=frame-1: continue
            q=queues[d['queue_frame'],d['cursor']]
            check_owned_body_palette(q,colors,self.guest,(17,18),q['slot']); self.palette_checks+=1
        record=dict(frame=frame,event=target['event'],modeledFlip=modeled,
                    exactVRAMWords=512*512,exactRGBPixels=bound['pixels'],rgbSHA256=digest(rgb.tobytes()),
                    shadowPixels=int(crop(shadow).sum()),
                    body={str(n):dict(pixels=int((crop(body)==n).sum()),
                         sole=int(np.where(crop(body)==n)[0].max())if (crop(body)==n).any()else None) for n in(1,2)})
        self.records.append(record)
        if len(self.records)==1:
            damaged=bytearray(raw); damaged[0]^=1
            try: self.exact(words,bytes(damaged),'Mutated actual VRAM target')
            except ValueError as error: self.counterexamples.append(dict(kind='VRAM target bit',rejectedBy=str(error)))
            else: raise ValueError('Actual changed VRAM accepted')
            changed=rgb.copy(); changed[0,0,0]^=1
            try: check_latch(changed,raw,palettes,target['start'],target['control'],target['tap'])
            except ValueError as error: self.counterexamples.append(dict(kind='visible RGB bit',rejectedBy=str(error)))
            else: raise ValueError('Actual changed visible RGB accepted')
            self.exact(words,raw,'Positive restoration')
            check_latch(rgb,raw,palettes,target['start'],target['control'],target['tap'])
        self.flips.clear()
