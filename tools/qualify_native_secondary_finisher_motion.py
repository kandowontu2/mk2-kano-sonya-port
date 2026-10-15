"""Finite native-orb source/CPU-unit qualification, explicitly not gameplay.

Compiles actual old/new initializer blocks through stdin; whole ROMs remain
in RAM. Independently encodes the intended new TMS instructions and runs
the emitted words in a clobbering unit model. Original passive observations
constrain source timing/geometry. Never launches or writes to an emulator.
"""
import gzip
import hashlib
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_secondary_finisher_visuals as visual

ROOT = visual.ROOT
STAGE = ROOT/'source_native_secondary_finisher_motion'
OUT = ROOT/'audit_native_secondary_finisher_motion_source'
BEGIN, END = '// SECONDARY_FINISHER_MOTION_BEGIN', '// SECONDARY_FINISHER_MOTION_END'
FIRST, LAST = 0xad800, 0xadc00
FLIGHT, TICK, ADVANCE, POSITION, WRAP = 0xad840, 0xad9c0, 0xad9e0, 0xada40, 0xadb40
need, sha, address, u32 = visual.need, visual.sha, visual.address, visual.u32
VISUAL_RECEIPT_SHA = '229F53A21AF466B84D5981F261DFEBC332589592E023D87BB9155D94A5D1604F'
OLD_COORDS = '\t\t0xb820,0x0090,0x0090,0xb820,0x00b0,0x00b0,\n'
NEW_COORDS = '\t\t0xbb20,0x0080,0x0080,0xbb20,0x00a0,0x00a0,\n'


def source_check():
    receipt = json.loads((visual.OUT/'report.json').read_text())
    need(sha(visual.OUT/'report.json') == VISUAL_RECEIPT_SHA and receipt['passed'] and
         receipt['sourceOnlyAccepted'] and not receipt['nativeRuntimeAccepted'] and
         all(sha(p) == h for p, h in receipt['inputHashes'].items()),
         'Whole qualified visual-stage source and finite proof unchanged')
    old_block, spacing_source = visual.source_block()
    old = (visual.STAGE/'midtunit_m.cpp').read_text()
    source = (STAGE/'midtunit_m.cpp').read_text()
    need(source.count(BEGIN) == source.count(END) == 1, 'Unique appended native motion block')
    start, end = source.index('\t'+BEGIN), source.index(END)+len(END)
    removed = source[:start-1]+source[end+1:]
    visual_start,visual_end=old.index(visual.BEGIN),old.index(visual.END)+len(visual.END)
    old_visual=old[visual_start:visual_end]
    need(old_visual.count(OLD_COORDS) == 1 and old_visual.count(NEW_COORDS) == 0 and
         removed == old[:visual_start]+old_visual.replace(OLD_COORDS,NEW_COORDS)+old[visual_end:],
         'Only reviewed fixed-point allocator repair and one native motion block added')
    for leaf in ('midtunit.h', 'midtunit.cpp'):
        need(sha(STAGE/leaf) == sha(visual.STAGE/leaf), 'Platform/host state unchanged')
    new_visual = source[source.index('\t'+visual.BEGIN):source.index(visual.END)+len(visual.END)]
    return receipt, old_block, new_visual+'\n'+source[start:end], spacing_source


def compile_probe(code, base, label):
    probe = OUT/(label+'_initializer_probe.exe')
    result = subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                             '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode == 0, 'Actual '+label+' C++ initializer compiled warning-free')
    result = subprocess.run([str(probe)],input=base,capture_output=True)
    (OUT/(label+'_initializer.stderr')).write_bytes(result.stderr)
    need(result.returncode == 0 and len(result.stdout) == len(base), 'Actual '+label+' initializer emitted full RAM buffer')
    return result.stdout, probe


class Assembler:
    def __init__(self, guest, start, limit):
        self.guest, self.at, self.limit = guest, start, limit

    def words(self, *values):
        need(self.at+2*len(values)<=self.limit, 'Independent native code allocation bound')
        for value in values:
            struct.pack_into('<H',self.guest,self.at,value & 0xffff)
            self.at += 2

    def movi(self, reg, value):
        self.words(0x09e0+reg,value,value >> 16)

    def call(self, target):
        self.words(0x0d5f,target,target >> 16)

    def branch(self, op, target=0):
        at = self.at+2
        self.words(op,target,target >> 16)
        return at

    def here(self, operand):
        struct.pack_into('<I',self.guest,operand,address(self.at))


def expected(old_visual):
    guest = bytearray(old_visual)
    need(all(b == 255 for b in old_visual[FIRST:LAST]), 'Qualified old guest has unoccupied new program range')
    original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(all(b == 255 for b in original[FIRST:LAST]), 'Original stock program has unoccupied new program range')
    # Same encoded size, but copy the complete native fixed-point X/Y words.
    need(old_visual[0xad69a:0xad6a6] == struct.pack('<6H',0xb820,0x90,0x90,0xb820,0xb0,0xb0),
         'Exact old independent effect allocation copy identified')
    struct.pack_into('<6H',guest,0xad69a,0xbb20,0x80,0x80,0xbb20,0xa0,0xa0)
    for n, group in enumerate((0xfe83ff60,0xfe83ffa0,0xfe83ffe0,0xfe840020)):
        struct.pack_into('<I',guest,FIRST+n*4,group)
    a = Assembler(guest,FLIGHT,TICK)
    a.movi(9,address(FIRST)); a.movi(10,1)
    a.words(0xb505,0xf0,0x0b85,0xffef,0xffff,0x0b45,0xffff)
    left = a.branch(0xcb80)
    a.movi(11,0x20000)
    done = a.branch(0xc080)
    a.here(left); a.movi(11,-0x20000); a.here(done)
    loop = address(a.at)
    a.movi(0,1); a.call(0xff80dcc0)
    a.words(0xb7a0,0x190,0xb601,0x80,0x4161,0xb220,0x80)
    a.call(address(TICK))
    a.words(0xb7a0,0x140,0xb401,0x90,0xb7a0,0x190,0xb402,0x90,0x4422,0x0382,0x0b42,0xff4e)
    a.branch(0xc380,loop); a.call(address(POSITION)); a.words(0x09ac,0x80,0x0127)
    a = Assembler(guest,TICK,ADVANCE)
    a.words(0x142a); no_frame = a.branch(0xcb80)
    a.movi(10,3); a.call(address(ADVANCE)); a.here(no_frame); a.words(0x0960)
    a = Assembler(guest,ADVANCE,POSITION)
    a.words(0x9720,0xa30f,0xb7a8,0x190); a.call(0xff838790)
    a.words(0x09af,0x100,0x0b49,~address(FIRST+16))
    not_end = a.branch(0xcb80); a.movi(9,address(FIRST)); a.here(not_end); a.words(0x0960)
    a = Assembler(guest,POSITION,WRAP)
    a.words(0xb7a0,0x190,0xb7a1,0x140,0xbb20,0x80,0x80,0xbb20,0xa0,0xa0,
            0xb424,0xf0,0x0b84,0xffef,0xffff,0xb405,0xf0,0x0b85,0x10,0,0x5485,0xb0a0,0xf0,0x0b44,0xffff)
    left = a.branch(0xcb80); a.movi(2,-177*0x10000)
    done = a.branch(0xc080); a.here(left); a.movi(2,177*0x10000); a.here(done)
    a.words(0xb603,0x80,0x4043,0xb260,0x80,0x0960)
    a = Assembler(guest,WRAP,LAST)
    a.words(0xa34c); a.movi(10,13); loop = address(a.at)
    a.call(address(ADVANCE)); a.movi(0,3); a.call(0xff80dcc0)
    a.words(0x142a); a.branch(0xcb80,loop); a.words(0x09ac,0x400,0x09ac,0x80,0x0127)
    return bytes(guest)


class CPU:
    """Scoped emitted-word unit model; native game processes never touched."""
    OWNER, TASK, CHILD, VICTIM = 0x1000, 0x2000, 0x4000, 0x6000

    def __init__(self, guest, child_x, victim_x, flip, victim_flip, fraction=0, move_victim=0):
        self.guest, self.reg, self.memory = guest, [0]*16, {}
        self.reg[8], self.reg[13] = self.OWNER,self.TASK
        self.global_stack, self.task_stack = [], []
        self.age, self.events, self.states, self.sleeps = 75,[],[],[]
        self.zero = self.hi = False
        self.move_victim = move_victim
        self.store(self.TASK+0x190,self.CHILD,1)
        self.store(self.TASK+0x140,self.VICTIM,1)
        self.store(self.TASK+0x170,0x7000,1)
        for actor in (self.OWNER,self.CHILD,self.VICTIM):
            self.store(actor+0x1f0,18 if actor!=self.VICTIM else 17,0)
            self.store(actor+0x140,0x0808 if actor==self.CHILD else 0x0300,0)
            self.store(actor+0xf0,(victim_flip if actor==self.VICTIM else flip)|0x204,0)
        self.store(self.CHILD+0x80,child_x*0x10000+fraction,1)
        self.store(self.CHILD+0xa0,87*0x10000+0x4000,1)
        self.store(self.VICTIM+0x80,victim_x*0x10000+fraction,1)
        self.store(self.VICTIM+0xa0,102*0x10000+0x4000,1)
        self.store(self.OWNER+0x80,(child_x-(32 if flip else -32))*0x10000+fraction,1)
        self.original_id = {a:self.load(a+0x1f0,0) for a in (self.OWNER,self.CHILD,self.VICTIM)}
        self.original_bank = {a:self.load(a+0x140,0) for a in (self.OWNER,self.CHILD,self.VICTIM)}

    def store(self, at, value, field):
        width = 32 if field else 16
        for bit in range(0,width,8):
            self.memory[at+bit] = (value >> bit)&255

    def load(self, at, field):
        if at>=0xff800000:
            return u32(self.guest,(at-0xff800000)//8)
        width = 32 if field else 16
        value = sum(self.memory.get(at+bit,0) << bit for bit in range(0,width,8))
        if width==16 and value & 0x8000:
            value |= 0xffff0000
        return value

    @staticmethod
    def signed(value):
        value &= 0xffffffff
        return value-0x100000000 if value & 0x80000000 else value

    def state(self):
        return dict(age=self.age,x=self.signed(self.load(self.CHILD+0x80,1)),
                    y=self.signed(self.load(self.CHILD+0xa0,1)),
                    flip=self.load(self.CHILD+0xf0,0)&0x10,
                    pose=next((e[1] for e in reversed(self.events) if e[0]<=self.age),0xfe83ff20))

    def poison(self):
        for reg in range(7):
            self.reg[reg]=0xfade0000+reg

    def run(self, entry):
        need(not self.task_stack and not self.global_stack,'Empty stacks before separate native coroutine entry')
        self.task_stack = [0x12345678]
        pc = address(entry)
        for steps in range(50000):
            need(pc&15==0 and 0xff800000<=pc<=0xffffffff,'Exact word-aligned instruction address')
            at=(pc-0xff800000)//8
            op=struct.unpack_from('<H',self.guest,at)[0]
            pc+=16
            def word():
                nonlocal pc
                value=struct.unpack_from('<H',self.guest,(pc-0xff800000)//8)[0]
                pc+=16
                return value
            def longword():
                return word() | (word()<<16)
            def setreg(reg,value):
                self.reg[reg]=value&0xffffffff
                self.zero=self.reg[reg]==0
            if 0x09e0<=op<=0x09ef:
                setreg(op-0x09e0,longword())
            elif op in (0xc080,0xcb80,0xc380):
                target=longword()
                if op==0xc080 or (op==0xcb80 and not self.zero) or (op==0xc380 and self.hi):
                    pc=target
            elif op==0x0d5f:
                target=longword()
                if target==0xff80dcc0:
                    need(not self.global_stack and self.reg[8]==self.OWNER and self.reg[0] in (1,3),
                         'Every native sleep has no shared-stack return or substituted performer')
                    elapsed=self.reg[0]
                    self.sleeps.append((self.age,elapsed))
                    for _ in range(elapsed):
                        self.age+=1
                        if self.move_victim and entry==FLIGHT:
                            self.store(self.VICTIM+0x80,self.load(self.VICTIM+0x80,1)+self.move_victim,1)
                    self.poison()
                elif target==0xff838790:
                    need(self.reg[8]==self.CHILD and self.reg[0] in
                         (0xfe83ff60,0xfe83ffa0,0xfe83ffe0,0xfe840020),
                         'Only the owned distinct orb is rendered with its genuine composite')
                    self.events.append((self.age,self.reg[0]))
                    self.poison()
                else:
                    need(address(FIRST)<=target<address(LAST),'Only qualified native motion short calls')
                    self.global_stack.append(('pc',pc)); pc=target
            elif op==0x0960:
                need(self.global_stack and self.global_stack[-1][0]=='pc','Balanced native short-call return')
                pc=self.global_stack.pop()[1]
            elif op==0xa30f:
                self.global_stack.append(('reg',self.reg[8]))
            elif op==0xa34c:
                self.task_stack.append(self.reg[10])
            elif op in (0x09af,0x09ac):
                mask=word()
                if op==0x09af:
                    need(mask==0x100 and self.global_stack and self.global_stack[-1][0]=='reg','Restore actual performer from short renderer save')
                    self.reg[8]=self.global_stack.pop()[1]
                else:
                    need(mask in (0x80,0x400) and self.task_stack,'Exact coroutine task-stack pop')
                    self.reg[7 if mask==0x80 else 10]=self.task_stack.pop()
            elif op==0x0127:
                need(self.reg[7]==0x12345678 and not self.task_stack and not self.global_stack and
                     self.reg[8]==self.OWNER,'Native task continuation and both stacks restored')
                for actor in self.original_id:
                    need(self.load(actor+0x1f0,0)==self.original_id[actor] and
                         self.load(actor+0x140,0)==self.original_bank[actor],
                         'Performer/victim/effect identity and palette ownership unchanged')
                return self.age
            elif op==0x9720:
                setreg(0,self.load(self.reg[9],1)); self.reg[9]+=32
            elif op in (0x0b45,0x0b44,0x0b42,0x0b49):
                reg=op&15; expected=(~word())&0xffff
                self.zero=(self.reg[reg]&0xffff)==expected
                self.hi=(self.reg[reg]&0xffff)>expected
            elif op in (0x0b85,0x0b84):
                mask=(~longword())&0xffffffff
                setreg(op&15,self.reg[op&15]&mask)
            elif op==0x142a:
                setreg(10,self.reg[10]-1)
            elif op in (0x4161,0x4043):
                src,dst=(11,1) if op==0x4161 else (2,3)
                setreg(dst,self.reg[dst]+self.reg[src])
            elif op==0x4422:
                setreg(2,self.reg[2]-self.reg[1])
            elif op==0x0382:
                setreg(2,abs(self.signed(self.reg[2])))
            elif op==0x5485:
                setreg(5,self.reg[5]|self.reg[4])
            elif op==0xbb20:
                source_offset,destination_offset=word(),word()
                self.store(self.reg[0]+destination_offset,self.load(self.reg[1]+source_offset,1),1)
            elif op in (0xb7a0,0xb7a1,0xb7a8,0xb601,0xb603,0xb401,0xb402,0xb424,0xb405,0xb505):
                sources={0xb7a0:(13,0,1),0xb7a1:(13,1,1),0xb7a8:(13,8,1),
                         0xb601:(0,1,1),0xb603:(0,3,1),0xb401:(0,1,0),0xb402:(0,2,0),
                         0xb424:(1,4,0),0xb405:(0,5,0),0xb505:(8,5,0)}
                src,dst,field=sources[op]
                setreg(dst,self.load(self.reg[src]+word(),field))
            elif op in (0xb220,0xb260,0xb0a0):
                src,field={0xb220:(1,1),0xb260:(3,1),0xb0a0:(5,0)}[op]
                self.store(self.reg[0]+word(),self.reg[src],field)
                if op==0xb220:
                    self.states.append(self.state())
            else:
                raise ValueError(f'Unexpected emitted motion opcode {op:04X} at {pc-16:08X}')
        raise ValueError('Native motion coroutine never completes')


def source_contract():
    """Check donor instructions that supply the motion's actual constants."""
    original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()==
         '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651','Actual original source ROM')
    run=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(ROOT/'mk3/mk3-maincpu.bin'),'-arch','tms34010',
                        '-basepc','0xff800000','-norawbytes'],text=True,capture_output=True,check=True)
    lines={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in run.stdout.splitlines()}
    facts={0xff9ae6a0:'MOVI   20000h,A0',0xff9ae700:'MOVK   3h,A0',
           0xff9ae740:'MOVI   1h,A0',0xff9ae840:'CMPI   B1h,A2',
           0xff9ae930:'MOVI   FF4Fh,A0',0xff9aea00:'MOVI   3000Dh,A0',
           0xff964bb0:'MOVK   1h,A0',0xff965da0:'MOVE   *A8(80h),*A0(80h),1',
           0xff965dd0:'MOVE   *A8(A0h),*A0(A0h),1'}
    need(all(lines.get(at)==text for at,text in facts.items()),'All actual donor motion/timer/range/offset/wrap/fixed-coordinate facts')
    return facts


def unit_cases(guest):
    results=[]
    cases=[('original_left',576,315,0x10,0,0,0),
           ('mirrored_right',224,485,0,0x10,0,0),
           ('left_half_pixel',576,315,0x10,0,0x8000,0),
           ('right_half_pixel',224,485,0,0x10,0x8000,0),
           ('left_close_177',492,315,0x10,0,0,0),
           ('right_close_177',308,485,0,0x10,0,0),
           ('left_far_320',635,315,0x10,0,0x8000,0),
           ('right_far_320',165,485,0,0x10,0x8000,0),
           ('left_moving_victim',576,315,0x10,0,0,0x8000),
           ('right_moving_victim',224,485,0,0x10,0,-0x8000)]
    for name,cx,vx,flip,vflip,fraction,move in cases:
        cpu=CPU(guest,cx,vx,flip,vflip,fraction,move)
        original_flags=cpu.load(cpu.CHILD+0xf0,0)
        original_y=cpu.load(cpu.CHILD+0xa0,1)
        endpoint=cpu.run(FLIGHT)
        velocity=-0x20000 if flip else 0x20000
        victim_x=vx*0x10000+fraction
        child_x=cx*0x10000+fraction
        expected_states=[]
        for tick in range(1,1000):
            victim_x+=move; child_x+=velocity
            expected_states.append(child_x)
            if abs((child_x>>16)-(victim_x>>16))<=177:
                break
        else:
            raise ValueError('Independent motion case never reaches source gate')
        need([r['x'] for r in cpu.states]==expected_states and endpoint==75+len(expected_states),
             'Actual emitted movement equals independently calculated per-field true-target distance')
        need(cpu.load(cpu.CHILD+0xa0,1)==cpu.load(cpu.VICTIM+0xa0,1) and
             cpu.signed(cpu.load(cpu.CHILD+0x80,1))==victim_x+(177 if vflip else -177)*0x10000 and
             (cpu.load(cpu.CHILD+0xf0,0)&0x10)==vflip and
             (cpu.load(cpu.CHILD+0xf0,0)&~0x10)==(original_flags&~0x10),
             'Full victim-relative wrap position, fractional Y and facing; unrelated flags preserved')
        need(all(r['y']==original_y and r['flip']==flip for r in cpu.states),
             'Travel preserves its own original Y/flip until target wrap')
        events=[(age,group) for age,group in cpu.events]
        expected_events=[(76+3*n,(0xfe83ff60,0xfe83ffa0,0xfe83ffe0,0xfe840020)[n%4])
                         for n in range((len(expected_states)+2)//3)]
        need(events==expected_events,'Actual emitted one-then-three cadence and four-frame travel cycle')
        cursor_before=cpu.reg[9]
        event_count=len(cpu.events)
        endpoint_wrap=cpu.run(WRAP)
        expected_wrap=[(endpoint+3*n,(0xfe83ff60,0xfe83ffa0,0xfe83ffe0,0xfe840020)
                       [((cursor_before-address(FIRST))//32+n)%4]) for n in range(13)]
        need(cpu.events[event_count:]==expected_wrap and endpoint_wrap==endpoint+39,
             'All thirteen actual wrap steps continue the flight cursor and hold exactly three fields')
        need(cpu.signed(cpu.load(cpu.CHILD+0x80,1))==victim_x+(177 if vflip else -177)*0x10000,
             'No post-wrap motion drift')
        if name=='original_left':
            text=gzip.open(ROOT/'audit_native_secondary_sonya_source_distance/run.log.gz','rt').read()
            observations=[dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in text.splitlines()
                          if l.startswith('MK3_SECONDARY_OBJECT') and 'actor=01034A70' in l]
            for r in observations:
                age=int(r['age'])
                if 76<=age<156:
                    pose=next(p for a,p in reversed(cpu.events) if a<=age)
                    x=(576-2*(age-75)) if age<endpoint else 138
                    need(pose==int(r['pose'],16)-0x01000000 and x==int(r['x']) and
                         int(r['y'])==(87 if age<endpoint else 102),
                         'Every actual original travel/wrap observation matches port unit-model phase and geometry')
            need(endpoint==117 and endpoint_wrap==156,'Actual original source-distance travel42 and wrap39 fields')
        results.append(dict(name=name,flightFields=len(expected_states),wrapFields=39,
                            wrapStartAge=endpoint,retireStartAge=endpoint_wrap,
                            fractionalPositionPreserved=bool(fraction),movingTarget=bool(move)))
    return results


def inspect(guest, old_visual, modeled):
    need(guest==modeled,'Whole actual C++ guest equals independent exact old visual/fixed-point repair/new-motion model')
    need(guest[:0xad69a]==old_visual[:0xad69a] and guest[0xad6a6:FIRST]==old_visual[0xad6a6:FIRST] and
         guest[LAST:]==old_visual[LAST:],'No changed input, CPU, identity, victim, audio, stock routine or outside-range byte')
    return unit_cases(guest)


def main():
    need(not OUT.exists() and not visual.native.census(),'Fresh motion evidence; no native game live')
    OUT.mkdir()
    old_code=new_code=''
    try:
        receipt,old_block,new_block,spacing=source_check()
        facts=source_contract()
        base=visual.prior.expected()
        old_code=visual.harness_code(old_block,spacing)
        new_code=visual.harness_code(new_block,spacing)
        old,old_probe=compile_probe(old_code,base,'old')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['emittedInitializedGuestSHA256'],
             'Re-executed qualified original visual initializer exactly matches frozen whole guest')
        guest,new_probe=compile_probe(new_code,base,'new')
        modeled=expected(old)
        cases=inspect(guest,old,modeled)
        faults=[]
        for label,at in (('Full_fixed_X_copy',0xad69c),('Full_fixed_Y_copy',0xad6a2),
                         ('Travel_group',FIRST),('Initial_cadence',FLIGHT+6),
                         ('Flight_facing',FLIGHT+12),('Per_field_yield',FLIGHT+44),
                         ('True_victim_pointer',FLIGHT+76),('Animation_timer',TICK),
                         ('Cursor_rollover',ADVANCE+18),('Victim_wrap_X_copy',POSITION+8),
                         ('Victim_wrap_facing',POSITION+22),('Thirteen_wrap_steps',WRAP+2),
                         ('Coroutine_return',WRAP+42),('Unrelated_stock_dispatch',0xf4320)):
            wrong=bytearray(guest);wrong[at]^=1
            try:
                inspect(bytes(wrong),old,modeled)
            except ValueError as error:
                faults.append(dict(name=label,rejected=str(error)))
            else:
                raise ValueError('Source motion fault admitted: '+label)
        # Tiny newly generated opcode slice, not a duplicated game/ROM.
        binary=OUT/'generated_motion_helpers.bin';binary.write_bytes(guest[FIRST:LAST])
        disasm=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                               '-basepc',hex(address(FIRST)),'-norawbytes'],
                              text=True,capture_output=True,check=True).stdout
        rows={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in disasm.splitlines()}
        need(rows[address(TICK)]=='DEC    A10' and rows[address(WRAP)]=='MOVE   A10,-*A12,1',
             'Actual native unit-model opcodes independently decoded')
        scope=json.loads((ROOT/'audit_native_secondary_finisher_reference_progress/report.json').read_text())
        paths=[Path(__file__),visual.OUT/'report.json',ROOT/'audit_native_secondary_sonya_source_distance/run.log.gz',
               ROOT/'audit_native_sonya_orb_reference_checked/report.json',ROOT/'mk3/mk3-maincpu.bin',
               ROOT/'tools/qualify_native_secondary_finisher_visuals.py',
               ROOT/'audit_native_secondary_finisher_reference_progress/report.json',
               *(STAGE/leaf for leaf in visual.SOURCE_PINS)]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,
                    completeSecondFatalitiesImplemented=False,fullPortAcceptance=False,
                    previousGoalTurnClassification='progress: native owned visual helpers staged and qualified',
                    thisGoalTurnClassification='progress: native Sonya orb fixed-point flight/wrap and shared exact child coordinates implemented and C++/emitted-word tested',
                    expectedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                    initializedByteDeltaFromVisual=sum(a!=b for a,b in zip(old,guest)),
                    initializedByteDeltaFromPlayable=sum(a!=b for a,b in zip(base,guest)),
                    actualOriginalSourceFacts={f'{a:08X}':t for a,t in facts.items()},
                    finiteUnitCases=cases,faultRejections=faults,
                    actualNativeDisassembly={f'{a:08X}':t for a,t in rows.items() if t!='DW     FFFFh'},
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                    gameBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
                    limitations=['Actual initialized C++ buffers and scoped emitted-TMS unit cases; not native game acceptance.',
                                 'Distinct finisher inputs/CPU tables remain unbound.',
                                 'Victim spin/palette/bone/ash effects, audio and complete cleanup must be integrated.',
                                 'Kano red-fade/skeleton-burst reaction still required.',
                                 'Whole native final visual/audio/campaign regression and finished ZIP remain required.'],
                    nextAction='Add real native own-victim reactions, imported generic debris/ash effects, original sounds and complete normal handoff; bind distinct human/CPU variants in a private compiled game and earn them physically.',
                    goalStatus='active')
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
             'Original full integration objective retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        for temporary in (old_probe,new_probe,binary):
            need(temporary.parent.resolve()==OUT.resolve(),'Exact generated temporary test artifact')
            temporary.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,finiteUnitCases=cases,
                              rejectedFaults=len(faults),completeSecondFatalitiesImplemented=False)))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False,failure=traceback.format_exc(),
                                                      nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        paths=[Path(__file__),*(STAGE/leaf for leaf in visual.SOURCE_PINS)]
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(files={str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in paths},
                           actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),stream)


if __name__=='__main__':
    main()
