"""Exact guest stub plus real pre/post registers and first FIFO publications."""
import struct
from pathlib import Path
from verify_native_pit_scene_v680_v1 import need, rows, number, hexnum

BASE=0xfffc9c00
WORDS=(0x098f,0xff00,0xb500,0x01f0,0x0b40,0xffee,
       0xca80,0x9d40,0xfffc,0x0b40,0xffed,0xcb80,0x9da0,0xfffc,
       0x09e0,0x2180,0xff18,0xc080,0x9d70,0xfffc,
       0x09e0,0x2000,0xff18,0x0d5f,0x8790,0xff83,
       0x09af,0x00ff,0x09e0,0x0c00,0xff18,0x0960)

def guest_bytes(raw):
    # This observer used read_range(width=8,step=1) on a bit-addressed space.
    # Each byte is repeated eight times. Validate every copy, not just a slice.
    need(len(raw)%8==0,'Complete bit-addressed read-range capture')
    need(all(len(set(raw[i:i+8]))==1 for i in range(0,len(raw),8)),
         'Every redundant guest byte read agrees')
    return raw[::8]

def stub(code,hook):
    need(len(code)==128 and struct.unpack_from('<32H',code)==WORDS and code[64:]==b'\xff'*64,
         'Exact bounded synchronous added-ID initializer with intact unused tail')
    need(hook==struct.pack('<HI',0x0d5f,BASE),'Actual constructor CALL at original MOVI site')
    return True

def execute(identity):
    """Small independent instruction model for every branch and register mask.
    Native copy is synchronous and deliberately clobbers all permitted A0..A7;
    the wrapper must restore them before the displaced MOVI/return."""
    regs=[0x12340000+i*137 for i in range(16)]
    initial=regs.copy();pc=0;stack=[];zero=False;copies=[];steps=0
    while True:
        steps+=1;need(steps<30,'Bounded synchronous initializer')
        op=WORDS[pc];pc+=1
        if op==0x098f:
            mask=WORDS[pc];pc+=1
            for i in range(16):
                if mask&(0x8000>>i):stack.append(regs[i])
        elif op==0xb500:
            need(WORDS[pc]==0x1f0,'Actual actor ID offset');pc+=1;regs[0]=identity
        elif op==0x0b40:
            immediate=(~WORDS[pc])&65535;pc+=1;zero=regs[0]==immediate
        elif op in (0xca80,0xcb80,0xc080):
            target=WORDS[pc]|WORDS[pc+1]<<16;pc+=2
            if op==0xc080 or (zero if op==0xca80 else not zero):
                need(BASE<=target<BASE+len(WORDS)*16 and (target-BASE)%16==0,'Branch is aligned inside initializer')
                pc=(target-BASE)//16
        elif op==0x09e0:
            regs[0]=WORDS[pc]|WORDS[pc+1]<<16;pc+=2
        elif op==0x0d5f:
            target=WORDS[pc]|WORDS[pc+1]<<16;pc+=2
            need(target==0xff838790,'Only original synchronous component copier called')
            copies.append(regs[0])
            for i in range(8):regs[i]=0xfedc0000+i
        elif op==0x09af:
            mask=WORDS[pc];pc+=1
            for i in range(15,-1,-1):
                if mask&(1<<i):regs[i]=stack.pop()
        elif op==0x0960:break
        else:raise ValueError('Unsupported initializer instruction')
    need(not stack and regs[0]==0xff180c00 and regs[1:]==initial[1:],
         'Exact stack balance/all other registers preserved/displaced MOVI result')
    need(copies==([0xff182000]if identity==17 else[0xff182180]if identity==18 else[]),
         'Only real added IDs initialize their own cache; every stock ID bypasses copier')
    return dict(id=identity,copies=copies,steps=steps)

def verify(folder,proof):
    folder=Path(folder)
    stub(guest_bytes((folder/'pit_initial_guest_code.bin').read_bytes()),
         guest_bytes((folder/'pit_initial_guest_hook.bin').read_bytes()))
    branches=[execute(i)for i in range(19)]
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    initial=rows(log,'PIT_INITIAL')
    need(len(initial)==2*len(proof['episodes']),'Exactly one actual synchronous call/return pair per real episode')
    identity=proof['actual_id'];group=0xff182000+(identity-17)*384
    for index,episode in enumerate(proof['episodes']):
        pair=initial[index*2:index*2+2];enter,leave=pair
        need(tuple(hexnum(r,'entry')for r in pair)==(BASE,BASE+31*16) and
             tuple(hexnum(r,'pc')for r in pair)==(BASE+16,BASE+32*16),'Actual guest call and return opcode fetches')
        need(all(number(r,'id')==identity and number(r,'mode')==9 and number(r,'frame')==episode['pit_enter'] and
                 hexnum(r,'a8')==episode['actor'] and hexnum(r,'a13')==episode['main']for r in pair),
             'Real unchanged cinematic identity and synchronous same-field preload')
        for key in ('sp','a8','a13','cache','a1','a2','a3','a4','a5','a6','a7'):
            need(enter[key]==leave[key],'Actual native register/owner/cache preservation: '+key)
        need(hexnum(enter,'pose')==0 and hexnum(leave,'pose')==group and hexnum(leave,'a0')==0xff180c00,
             'Own first composite installed before registration, coordinate MOVI executes')
    enter=initial[0]
    queues=[q for q in rows(log,'FLOOR_QUEUE')if hexnum(q,'actor')==hexnum(enter,'a8')]
    need(queues and all(hexnum(q,'pose') in {group+i*64 for i in range(6)}for q in queues),
         'Every actual cinematic FIFO publication owns a valid fall/impact group; no stale pose0')
    first=min(number(q,'frame')for q in queues)
    need(first==proof['pit_enter']+1 and all(hexnum(q,'pose')==group and number(q,'part')==0
         for q in queues if number(q,'frame')==first),'First original FIFO draw is own first fall, never previous KO cache')
    return dict(passed=True,initial_frame=proof['pit_enter'],actual_preloads=len(proof['episodes']),first_body_queue=first,
                actual_registers_preserved=11,static_all_19_id_branches=branches,
                scope='actual own constructor/cache/first publication plus independently modeled exact stock bypass; not stock scene raster coverage')
