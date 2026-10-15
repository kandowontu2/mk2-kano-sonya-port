"""Original-art and emitted native effect/action source qualification only.

Does not launch a game, accept rendering/audio/cleanup, or enable a player
input. Actual C++ initializer emits into RAM; no ROM/media copies retained.
The constructor unit model uses native process-field contracts checked from
the original program. Full in-game earned-action verification remains next.
"""
import gzip
import hashlib
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_secondary_finisher_motion as motion

visual=motion.visual
ROOT=motion.ROOT
STAGE=ROOT/'source_native_secondary_finisher_effects'
OUT=ROOT/'audit_native_secondary_finisher_effects_source'
BEGIN,END='// SECONDARY_FINISHER_EFFECTS_BEGIN','// SECONDARY_FINISHER_EFFECTS_END'
FIRST,LAST=0xadc00,0xaf340
need,sha,address,u32=motion.need,motion.sha,motion.address,motion.u32
MOTION_PIN='7C8225153F428956BADDDF3116D5DD0E9B962D85B47A0FC28DE7E1EFF7CC8E3E'
PAYLOAD=ROOT/'diagnostic_native_cpu_finisher_spacing/roms/mk2ks/mk2ks.mdata'
PART_STREAMS=(0xffa98680,0xffa98860,0xffa98ec0,0xffa99080,0xffa993e0)
PART_PALETTES=(0xffcd6c80,0xffcd7090,0xffcd74a0)
PALETTE_INDEX=(0,0,1,2,1)
COUNTS=(4,4,20,2,2)


def check_sources():
    report=json.loads((motion.OUT/'report.json').read_text())
    need(sha(motion.OUT/'report.json')==MOTION_PIN and report['passed'] and report['sourceOnlyAccepted'] and
         not report['nativeRuntimeAccepted'] and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Whole qualified motion source and every accepted proof input conserved')
    _,_,old_block,spacing=motion.source_check()
    old=(motion.STAGE/'midtunit_m.cpp').read_text()
    new=(STAGE/'midtunit_m.cpp').read_text()
    need(new.count(BEGIN)==new.count(END)==1,'Unique effect/action source block')
    a,b=new.index('\t'+BEGIN),new.index(END)+len(END)
    need(new[:a-1]+new[b+1:]==old,'Only one appended effect/action initializer block; previous game code unchanged')
    for leaf in ('midtunit.h','midtunit.cpp'):
        need(sha(STAGE/leaf)==sha(motion.STAGE/leaf),'Native platform/host code unchanged')
    return report,old_block,new[a:b],spacing


def compile_probe(code, base, payload, name):
    path=OUT/(name+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                           '-x','c++','-','-o',str(path)],input=code,text=True,capture_output=True)
    (OUT/(name+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Actual '+name+' C++ initializer compiled warning-free')
    run=subprocess.run([str(path)],input=base+payload,capture_output=True)
    (OUT/(name+'_initializer.stderr')).write_bytes(run.stderr)
    (OUT/(name+'_native_exit.json')).write_text(json.dumps(dict(nativeExit=run.returncode,
        stdoutBytes=len(run.stdout),stderrBytes=len(run.stderr)),indent=2)+'\n')
    need(run.returncode==0 and len(run.stdout)==len(base),'Actual '+name+' initializer emitted complete guest in RAM')
    return run.stdout,path


def model_assets(old, original, payload):
    expected=bytearray(old)
    need(all(b==255 for b in old[FIRST:LAST]) and
         all(b==255 for b in (ROOT/'mk2/mk2-maincpu.bin').read_bytes()[FIRST:LAST]),
         'Exact whole new storage range unused in actual prior/original guests')
    def read(pointer):
        return (pointer-0xff800000)//8
    def palette(pointer, target, count):
        at=read(pointer)
        need(struct.unpack_from('<H',original,at)[0]==count and
             original[at:at+2+count*2]==payload[at:at+2+count*2],
             'Actual original colors unchanged in frozen appended-data payload')
        expected[target:target+2+count*2]=original[at:at+2+count*2]
    def frame(pointer,target,pal):
        at=read(pointer)
        need(original[at:at+14]==payload[at:at+14],'Actual generic descriptor bytes remain original in payload')
        record=bytearray(original[at:at+14])
        width,height,x,y,gfx,command=struct.unpack('<HHhhIH',record)
        need(0<width<=180 and 0<height<=180 and gfx<0x08000000,'Source effect dimensions/graphics bounds')
        # Existing renderer translates (original+10000000)-0A000000. This
        # places the complete source at the already appended byte C00000.
        need((gfx+0x06000000)//8<0x2000000,'Existing native video source translation fits real 32-MiB region')
        struct.pack_into('<I',record,8,gfx+0x10000000)
        expected[target:target+20]=record+struct.pack('<IH',address(pal),0)
        return dict(originalFrame=f'{pointer:08X}',nativeFrame=f'{address(target):08X}',
                    width=width,height=height,xOrigin=x,yOrigin=y,dma=f'{command:04X}')
    palette(0xffcd7cc0,0xadf40,14)
    descriptors=[]
    for pose in range(13):
        group=0xffaa3080+pose*0x60
        a=read(group)
        first=0xffc8e4b0+(pose-1)*0xe0 if pose else 0xffc8e3b0
        second=first+0x70 if pose else 0xffc8e440
        need(struct.unpack_from('<III',original,a)==(first,second,0) and
             original[a:a+12]==payload[a:a+12],'Original two-component cloud and terminator')
        for c,pointer in enumerate((first,second)):
            target=0xadc00+(pose*2+c)*20
            descriptors.append(frame(pointer,target,0xadf40))
            struct.pack_into('<I',expected,0xade40+pose*12+c*4,address(target))
        struct.pack_into('<I',expected,0xade40+pose*12+8,0)
        struct.pack_into('<I',expected,0xadf00+pose*4,address(0xade40+pose*12))
    struct.pack_into('<I',expected,0xadf00+13*4,0)
    for index,pointer in enumerate(PART_PALETTES):
        palette(pointer,0xae680+index*130,64)
    for part,pointer in enumerate(PART_STREAMS):
        a=read(pointer)
        values=struct.unpack_from('<14I',original,a)
        need(values[12:]==(1,pointer),'Original twelve-frame rotating bone loop and native-compatible loop grammar')
        for pose,frame_pointer in enumerate(values[:12]):
            target=0xae000+(part*12+pose)*20
            descriptors.append(frame(frame_pointer,target,0xae680+PALETTE_INDEX[part]*130))
            struct.pack_into('<I',expected,0xae500+part*56+pose*4,address(target))
        struct.pack_into('<II',expected,0xae500+part*56+48,1,address(0xae500+part*56))
    return bytes(expected),descriptors


def model_code(old):
    """Independent fixed layouts for typed factories and cooperative action."""
    guest=bytearray(old)
    Assembler=motion.Assembler
    a=Assembler(guest,0xae900,0xaec00)
    for part,count in enumerate(COUNTS):
        a.movi(9,address(0xae500+part*56));a.movi(11,(2 if part else 1)*0x10000)
        for _ in range(count):a.call(address(0xaec00))
    a.words(0x0960)
    a=Assembler(guest,0xaec00,0xaed00)
    a.words(0x098f,0xf0);a.movi(10,0x4000);a.words(0x4d0b)
    a.movi(1,0x10c);a.movi(7,0xff9f2e40);a.call(0xff80e280)
    a.words(0x09af,0xf00,0xb320,0x250,0xb360,0x290)
    for value,offset in ((0,0x270),(0x80000,0x2b0),(0x40000,0x2d0),(0x4000,0x80),(0xff9ecdb0,0x100)):
        a.movi(2,value);a.words(0xb240,offset)
    a.movi(2,3);a.words(0xb040,0x230,0xb502,0x90,0xb040,0x2f0,
                            0xb502,0xb0,0x0b02,0x90,0xb040,0x310,0x0960)
    a=Assembler(guest,0xaed00,0xaee00)
    for offset in (64,32,0):a.movi(11,offset);a.call(address(0xaee00))
    a.words(0x0960)
    a=Assembler(guest,0xaee00,0xaef00)
    a.words(0x098f,0xf0);a.movi(9,address(0xadf00));a.call(0xff83ae20);a.call(0xff83f610)
    a.words(0x4d00,0x09af,0xf00,0x4d01,0xbb20,0x80,0x80,0xbb20,0xa0,0xa0,
            0xb403,0xb0,0x4163,0xb060,0xb0,0xb405,0xf0,0x0b85,0x10,0,0xb0a0,0xf0)
    a.movi(2,0x51);a.words(0xb240,0xc0);a.movi(2,0x64)
    a.words(0xb040,0xd0,0x4c0a,0x098f,0xf0,0x4d48)
    a.movi(1,0x100);a.movi(7,address(0xaef00));a.call(0xff80e280)
    a.words(0x09af,0xf00,0xb340,0x60,0x0960)
    def cooperate(a,target):a.words(0x0147,0x0b07,0x60,0xa2ec,0xc080,target,target>>16)
    a=Assembler(guest,0xaef00,0xaf000)
    a.movi(9,address(0xadf00));a.movi(0,5);cooperate(a,0xff83c340)
    a.words(0xb700,0x1a0,0x0be0,0xfeff,0xa20f,0x4d00)
    a.call(0xff840450);a.words(0x09af,1);a.call(0xff80e0e0);a.branch(0xc080,0xff80de20)
    a=Assembler(guest,0xaf000,0xaf090)
    a.movi(1,1);a.movi(0,1);a.call(0xff8cd780);a.movi(0,20);a.call(0xff80dcc0)
    a.movi(9,address(0xf5740));a.movi(0,3);cooperate(a,0xff83c340);a.call(address(0xad640))
    a.movi(1,0x100);a.movi(7,address(0xaf090));a.call(0xff80e280)
    a.words(0xbba0,0x140,0x140,0xbba0,0x170,0x170,0xbba0,0x190,0x190)
    a.movi(1,0);a.words(0xb22d,0x190);a.movi(0,144);a.call(0xff80dcc0)
    a.call(0xff8cdc40);a.branch(0xc080,0xffa14860)
    a=Assembler(guest,0xaf090,0xaf190)
    a.movi(9,address(0xad200+11*12));a.movi(11,address(0xad640));cooperate(a,address(0xad500))
    cooperate(a,address(0xad840));a.movi(7,address(0xaf190));a.call(0xff842710)
    cooperate(a,address(0xadb40));a.movi(7,address(0xaf1d0));a.call(0xff842710)
    cooperate(a,address(0xad4c0));a.call(address(0xaf290));a.branch(0xc080,0xff80de20)
    a=Assembler(guest,0xaf190,0xaf1d0);loop=address(a.at)
    a.movi(9,35);a.call(0xff906090);a.movi(0,4);cooperate(a,0xff83c340);a.branch(0xc080,loop)
    a=Assembler(guest,0xaf1d0,0xaf290)
    a.call(address(0xae900));a.call(address(0xaed00));a.movi(9,5);a.call(0xff906090)
    a.movi(0,4);cooperate(a,0xff83c340);a.words(0x4d00);a.call(0xff838f60);a.branch(0xc080,0xff841ec0)
    a=Assembler(guest,0xaf290,LAST)
    a.words(0xb7a0,0x190,0xb600,0x1a0,0x0be0,0xfeff,0xa20f)
    a.call(0xff83efd0);a.words(0x09af,1);a.call(0xff80e0e0);a.words(0x0960)
    return bytes(guest)


def factory_unit(guest,entry):
    """Execute actual emitted short factory words with native-kernel stubs.

    This is not an emulator or gameplay trace. Shared kernels are contracts;
    their real allocation/render/scheduler behavior remains a runtime gate.
    """
    mem={};regs=[0]*16;regs[8]=0x1000;regs[13]=0x2000
    stack=[('pc',0x12345678)];jobs=[];clouds=[];pc=address(entry)
    def put(at,value,field=1):
        for bit in range(0,32 if field else 16,8):mem[at+bit]=(value>>bit)&255
    def get(at,field=1):
        if at>=0xff800000:return u32(guest,(at-0xff800000)//8)
        return sum(mem.get(at+bit,0)<<bit for bit in range(0,32 if field else 16,8))
    put(0x1080,315*65536+32768);put(0x10a0,102*65536+16384)
    put(0x10f0,0x10,0);put(0x11f0,17,0);put(0x1140,0x0700,0)
    original=mem.copy()
    for step in range(20000):
        need(pc&15==0,'Exact emitted factory instruction alignment')
        op=struct.unpack_from('<H',guest,(pc-0xff800000)//8)[0];pc+=16
        def word():
            nonlocal pc
            value=struct.unpack_from('<H',guest,(pc-0xff800000)//8)[0];pc+=16;return value
        def longword():return word()|(word()<<16)
        if 0x09e0<=op<=0x09ef:regs[op-0x09e0]=longword()
        elif op==0x0d5f:
            target=longword()
            if target==0xff80e280:
                job=0x8000+len(jobs)*0x1000
                # Actual MMTM scans A7..A12 ascending, predecrementing
                # from +100 by 20 bits: IP A7 at E0; A8 C0; A9 A0;
                # A10 80; A11 60; native new A12 stack at 40.
                for reg in range(7,13):
                    put(job+0x100-(reg-6)*0x20,job+0x6f0 if reg==12 else regs[reg])
                put(job+0x20,regs[1],0);put(job+0x30,1,0)
                jobs.append(job);regs[0]=job
            elif target==0xff83ae20:
                child=0x70000+len(clouds)*0x1000
                need(regs[9]==address(0xadf00),'Actual cloud allocation consumes its own typed composite stream')
                put(child+0x1a0,0x90000+len(clouds)*0x1000+0x100)
                put(child+0xf0,0x20,0);put(child+0x140,0x0800+len(clouds)*0x100,0)
                clouds.append(child);regs[8]=child;regs[0]=0xeeee0000
            elif target==0xff83f610:
                need(regs[8] in clouds,'Native render-list registration applies only to the new cloud')
            else:
                need(address(0xae900)<=target<address(0xaef00),'Only defined non-yielding private factory call')
                stack.append(('pc',pc));pc=target
        elif op==0x0960:
            need(stack and stack[-1][0]=='pc','Balanced native short return')
            pc=stack.pop()[1]
            if pc==0x12345678:break
        elif op==0x098f:
            mask=word()
            need(mask==0xf0,'Exactly the four caller-owned factory registers saved')
            for reg in range(8,12):stack.append(('reg',regs[reg]))
        elif op==0x09af:
            mask=word();need(mask==0xf00,'Exactly the four native saved registers restored')
            for reg in reversed(range(8,12)):
                need(stack and stack[-1][0]=='reg','Typed native register save/restore')
                regs[reg]=stack.pop()[1]
        elif op in (0x4d00,0x4d01,0x4c0a,0x4d48,0x4d0b):
            src,dst={0x4d00:(8,0),0x4d01:(8,1),0x4c0a:(0,10),0x4d48:(10,8),0x4d0b:(8,11)}[op]
            regs[dst]=regs[src]
        elif op in (0xb320,0xb360,0xb240,0xb040,0xb060,0xb0a0,0xb340):
            src,field={0xb320:(9,1),0xb360:(11,1),0xb240:(2,1),0xb040:(2,0),
                       0xb060:(3,0),0xb0a0:(5,0),0xb340:(10,1)}[op]
            put(regs[0]+word(),regs[src],field)
        elif op in (0xb502,0xb403,0xb405):
            src,dst={0xb502:(8,2),0xb403:(0,3),0xb405:(0,5)}[op]
            regs[dst]=get(regs[src]+word(),0)
        elif op==0xbb20:
            source,destination=word(),word();put(regs[0]+destination,get(regs[1]+source))
        elif op==0x4163:regs[3]=(regs[3]+regs[11])&0xffffffff
        elif op==0x0b02:regs[2]=(regs[2]+word())&0xffffffff
        elif op==0x0b85:regs[5]&=(~longword())&0xffffffff
        else:raise ValueError(f'Unexpected factory opcode {op:04X} at {pc-16:08X}')
    else:raise ValueError('Native factory does not return')
    need(not stack and regs[8]==0x1000 and all(mem.get(at)==value for at,value in original.items()),
         'Factory returns with real victim identity, palette, world coordinates and stack unchanged')
    if entry==0xae900:
        expected_types=[part for part,count in enumerate(COUNTS) for _ in range(count)]
        need(len(jobs)==32 and not clouds,'Exactly the 32 original typed bone pieces, no player/cloud allocation')
        for job,part in zip(jobs,expected_types):
            fields={0x20:0x10c,0xe0:0xff9f2e40,0xc0:0x1000,0x60:0x1000,0x80:0x4000,
                    0x40:job+0x6f0,0x100:0xff9ecdb0,
                    0x230:3,0x250:address(0xae500+part*56),0x270:0,
                    0x290:(2 if part else 1)*65536,0x2b0:8*65536,0x2d0:4*65536,
                    0x2f0:315,0x310:246}
            for offset,value in fields.items():
                need(get(job+offset,0 if offset in (0x20,0x230,0x2f0,0x310) else 1)==value,
                     f'Every actual bone process field initialized correctly: +{offset:X}')
    else:
        need(len(jobs)==len(clouds)==3,'Exactly three separately owned native cloud animation/cache objects')
        for job,child,offset in zip(jobs,clouds,(64,32,0)):
            need(get(job+0x20,0)==0x100 and get(job+0xe0)==address(0xaef00) and
                 get(job+0xc0)==child and get(job+0x60)==child and get(job+0x40)==job+0x6f0,
                 'Cloud job owns its new effect actor, never the actual victim')
            need(get(child+0x80)==315*65536+32768 and get(child+0xa0)==(102+offset)*65536+16384 and
                 get(child+0xc0,0)==0x51 and get(child+0xd0,0)==0x64 and
                 get(child+0xc0)==0x00640051 and get(child+0xf0,0)==0x20,
                 'Actual emitted cloud position, fraction, native layer and non-player flags')
    return dict(entry=f'{address(entry):08X}',boneTasks=len(jobs) if entry==0xae900 else 0,
                cloudTasks=len(clouds),trueVictimUnchanged=True,callerStackBalanced=True)


def inspect(guest,old,model):
    need(guest==model,'Whole actual C++ guest matches original-data and independent typed native opcode model')
    need(guest[:FIRST]==old[:FIRST] and guest[LAST:]==old[LAST:],
         'Every stock/input/CPU/audio/identity and previously qualified byte conserved')
    return [factory_unit(guest,entry) for entry in (0xae900,0xaed00)]


def main():
    need(not OUT.exists() and not visual.native.census(),'Fresh effects evidence; no native game live')
    OUT.mkdir();old_code=new_code=''
    try:
        receipt,old_block,effect_block,spacing=check_sources()
        original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();payload=PAYLOAD.read_bytes()
        need(sha(ROOT/'mk3/mk3-maincpu.bin')=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651' and
             sha(PAYLOAD)=='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3',
             'Exact original source and actual immutable playable descriptor/graphics payload')
        base=visual.prior.expected()
        old_code=visual.harness_code(old_block,spacing)
        old,old_probe=compile_probe(old_code,base,b'','motion')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['expectedGuestSHA256'],'Re-executed whole qualified motion guest')
        extra=r'''
    static uint8_t donor_memory[0x200000]; uint8_t *donor=donor_memory;
    std::cin.read(reinterpret_cast<char *>(donor),sizeof(donor_memory));
    if (std::cin.gcount()!=sizeof(donor_memory)) return 4;
    auto rom_offset=[](uint32_t a) { return (a-0xff800000U)>>3; };
    auto donor32=[&](unsigned a) { return uint32_t(donor[a])|(uint32_t(donor[a+1])<<8)|(uint32_t(donor[a+2])<<16)|(uint32_t(donor[a+3])<<24); };
    constexpr unsigned sonya_finish_poses=0xf5740;
'''
        new_code='#include <algorithm>\n'+visual.harness_code(old_block+'\n'+effect_block,spacing)
        need(new_code.count(visual.HARNESS_HEADER)==1,'Unique actual initializer harness insertion')
        new_code=new_code.replace(visual.HARNESS_HEADER,visual.HARNESS_HEADER+extra)
        guest,new_probe=compile_probe(new_code,base,payload,'effects')
        asset_model,descriptors=model_assets(old,original,payload)
        model=model_code(asset_model);unit=inspect(guest,old,model)
        faults=[]
        for label,at in (('Cloud_gfx',0xadc08),('Cloud_component',0xade40),('Cloud_terminator',0xade48),
                         ('Cloud_palette',0xadf42),('Bone_gfx',0xae008),('Bone_palette',0xae682),
                         ('Bone_loop',0xae530),('Bone_velocity',0xaec36),('Bone_job_entry',0xaec0c),
                         ('Cloud_job_actor',0xaee72),('Cloud_cache_cleanup',0xaef1e),
                         ('Main_effect_transfer',0xaf06a),('Own_victim_spin',0xaf190),
                         ('Own_victim_crouch',0xaf1dc),('Orb_cache_cleanup',0xaf2a8),
                         ('Unrelated_stock_input',0xff270)):
            wrong=bytearray(guest);wrong[at]^=1
            try:inspect(bytes(wrong),old,model)
            except ValueError as error:faults.append(dict(name=label,rejected=str(error)))
            else:raise ValueError('Effects fault admitted: '+label)
        binary=OUT/'generated_effect_helpers.bin';binary.write_bytes(guest[0xae900:LAST])
        run=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                            '-basepc',hex(address(0xae900)),'-norawbytes'],text=True,capture_output=True,check=True)
        lines={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in run.stdout.splitlines()}
        need(lines[address(0xaf190)]=='MOVI   23h,A9','Decoded real victim selects native main35, not roundhouse32')
        scope=json.loads((ROOT/'audit_native_secondary_finisher_reference_progress/report.json').read_text())
        paths=[Path(__file__),motion.OUT/'report.json',ROOT/'tools/qualify_native_secondary_finisher_motion.py',
               PAYLOAD,ROOT/'mk3/mk3-maincpu.bin',ROOT/'audit_native_secondary_finisher_reference_progress/report.json',
               *(STAGE/leaf for leaf in visual.SOURCE_PINS)]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,
                    completeSecondFatalitiesAccepted=False,fullPortAcceptance=False,
                    previousGoalTurnClassification='no progress: user-requested status inspection/restatement only',
                    thisGoalTurnClassification='progress: original effect assets, 32 native bone tasks, three smoke tasks, independent Sonya action/worker/victim/cache cleanup implemented and source-qualified',
                    expectedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                    initializedByteDeltaFromMotion=sum(a!=b for a,b in zip(old,guest)),
                    initializedByteDeltaFromPlayable=sum(a!=b for a,b in zip(base,guest)),
                    originalDescriptorCount=len(descriptors),sourceDescriptors=descriptors,
                    constructorUnitCases=unit,faultRejections=faults,
                    actualNativeDisassembly={f'{pc:08X}':text for pc,text in lines.items() if text!='DW     FFFFh'},
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                    gameBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active',
                    limitations=['Actual C++ initialized buffers, exact original data and scoped emitted-word constructor units only.',
                                 'Native game allocation capacity/render/palettes/physics/shadows/sound/cleanup not accepted by these units.',
                                 'New Sonya action is deliberately unbound to inputs and CPU dispatch.',
                                 'Original new finisher sound samples and complete runtime/after-win/next-match verification remain required.',
                                 'Kano victim red-fade/skeleton-burst action still needs connecting.',
                                 'No finished release; full original integration/campaign/audio/ZIP scope remains.'],
                    nextAction='Qualify true-victim native35/5 mappings and shared effect runtime, bind adapted Sonya second input/CPU choice in a private built game, physically earn it and review complete native action/cleanup; then finish Kano laser victim/audio and full remaining integration.')
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        for temporary in (old_probe,new_probe,binary):
            need(temporary.parent.resolve()==OUT.resolve(),'Exact generated temporary source-test artifacts')
            temporary.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,originalDescriptors=len(descriptors),
                              constructorUnitCases=unit,rejectedFaults=len(faults),nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False,failure=traceback.format_exc(),nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        paths=[Path(__file__),*(STAGE/leaf for leaf in visual.SOURCE_PINS)]
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(files={str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in paths},
                           actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),stream)


if __name__=='__main__':main()
