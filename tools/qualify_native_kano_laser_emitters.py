"""Actual emitted native particle/paired-bone code; source-only qualification.

Execute generated TMS words in a bounded unit model. Native external helper
calls are modeled, not emulator evidence. Preserve full native reference,
all earlier source and whole guest; no action/input binding or public build.
"""
import gzip
import hashlib
import inspect
import json
import struct
import traceback
from pathlib import Path

import qualify_native_kano_laser_effect_assets_camera as accepted
import review_native_kano_laser_effect_lifetime as reference

assets=accepted.prior
phases=assets.prior
ROOT=assets.ROOT
STAGE=ROOT/'source_native_kano_laser_emitters'
OUT=ROOT/'audit_native_kano_laser_emitters_source'
FIRST,LAST=0xafdc0,0xb0690
BEGIN,END='// KANO_LASER_EMITTERS_BEGIN','// KANO_LASER_EMITTERS_END'
need,sha,address,u32=phases.need,phases.sha,phases.address,phases.u32


class UnitCPU:
    """Bounded actual-word unit model; volatile registers/stack exercised."""
    def __init__(self,guest,entry,xy=(748,102),face=0,roll='low',task=None):
        self.guest=guest;self.regs=[0]*16;self.mem={};self.events=[];self.age=0;self.roll=roll
        self.base_sp=0x80000;self.regs[15]=self.base_sp
        self.victim=0x30000;self.parent=0x10000;self.regs[8]=self.victim;self.regs[13]=self.parent
        self.regs[12]=self.parent+0x6f0;self.regs[9]=0xdead0009;self.regs[10]=2;self.regs[11]=3
        self.next_job=0x20000;self.next_actor=0x40000
        self.regs[0]=2;self.regs[1]=0xfeed0001
        self.pc=address(entry);self.zero=False;self.negative=False;self.done=False
        self.store(self.victim+0x80,xy[0]*65536+1234,32);self.store(self.victim+0xa0,xy[1]*65536+5678,32)
        self.store(self.victim+0xf0,face|0x200,16);self.store(self.victim+0x1f0,18,16)
        self.store(self.parent+0x190,0x50000,32);self.store(self.parent+0x140,0x50100,32)
        self.original_victim=dict(self.mem)
        if task:
            self.regs[13]=task
            for r in range(7,13):self.regs[r]=self.load(task+0x100-(r-6)*0x20,32)
        if entry in (0xafdc0,0xafe80,0xb0140,0xb0440):self.push(15,0x12345678)

    def store(self,at,value,width):
        self.mem[at]=value&0xffff
        if width==32:self.mem[at+16]=(value>>16)&0xffff

    def load(self,at,width):
        if at>=0xff800000:
            byte=(at-0xff800000)//8
            return struct.unpack_from('<H' if width==16 else '<I',self.guest,byte)[0]
        value=self.mem.get(at,0)
        return value if width==16 else value|(self.mem.get(at+16,0)<<16)

    def push(self,r,value):self.regs[r]-=32;self.store(self.regs[r],value,32)
    def pop(self,r):
        value=self.load(self.regs[r],32);self.regs[r]+=32;return value
    def flags(self,value):
        self.zero=(value&0xffffffff)==0;self.negative=bool(value&0x80000000)
    def operand(self,width):
        value=self.load(self.pc,width);self.pc+=width;return value
    def poison(self):
        for r in range(7):self.regs[r]=0xfade0000+r
    def create_actor(self,composite):
        actor=self.next_actor;self.next_actor+=0x1000
        self.regs[8]=actor;self.store(actor+0xf0,0x8002,16)
        if composite:
            cache=self.next_job;self.next_job+=0x1000
            self.store(actor+0x1a0,cache+0x100,32);self.events.append(('cache',cache,actor,self.regs[9]))
            self.poison();self.regs[0]=cache
        else:self.events.append(('single',actor,self.regs[5]))

    def external(self,target):
        r=self.regs
        if target==0xff83ae20:self.create_actor(True)
        elif target==0xff83f610:self.events.append(('insert',r[8]));self.poison()
        elif target in (0xff80eae0,0xff80eb70):
            bound=r[0]*(2 if target==0xff80eb70 else 1)
            need(bound>0,'Actual native RNG range positive')
            result=1 if self.roll=='low' else bound if self.roll=='high' else bound//2
            r[0]=(result-(bound//2 if target==0xff80eb70 else 0))&0xffffffff
            self.events.append(('rng',target,bound));self.flags(r[0])
        elif target==0xff80e280:
            job=self.next_job;self.next_job+=0x1000
            self.store(job+0x20,r[1],16);self.store(job+0x30,1,16)
            for reg in range(7,13):self.store(job+0x100-(reg-6)*0x20,job+0x6f0 if reg==12 else r[reg],32)
            self.events.append(('task',job,r[1],r[7],r[8]));r[0]=job
        elif target==0xff83c870:
            self.store(r[13]+0x1d0,r[0],16);self.store(r[13]+0x1e0,1,16);r[0]=1
        elif target==0xff83ada0:self.create_actor(False)
        elif target==0xff840450:self.events.append(('object_free',r[0]));self.poison()
        elif target==0xff80e0e0:self.events.append(('cache_free',r[0]));self.poison()
        elif target==0xff80dcc0:
            need(r[15]==self.base_sp,'No global SP live across native sleep')
            self.events.append(('sleep',self.age,r[0]));self.age+=r[0];self.poison()
        else:raise ValueError(f'Unexpected native short helper {target:08X}')

    def execute(self,max_steps=10000,stop_fields=None):
        r=self.regs
        for _ in range(max_steps):
            if stop_fields is not None and self.age>=stop_fields:break
            op=self.operand(16);src=(op>>5)&15;dst=op&15
            if 0x09e0<=op<=0x09ef:r[dst]=self.operand(32);self.flags(r[dst])
            elif 0x09c0<=op<=0x09cf:r[dst]=self.operand(16);self.flags(r[dst])
            elif 0x4c00<=op<=0x4dff:r[dst]=r[src];self.flags(r[dst])
            elif op in (0x098f,0x09af):
                mask=self.operand(16)
                if op==0x098f:
                    for reg in range(15):
                        if mask&(1<<(15-reg)):self.push(15,r[reg])
                else:
                    for reg in range(14,-1,-1):
                        if mask&(1<<reg):r[reg]=self.pop(15)
            elif op==0x0960:
                target=self.pop(15)
                if target==0x12345678:self.done=True;break
                self.pc=target
            elif op==0x0d5f:
                target=self.operand(32)
                if address(FIRST)<=target<address(LAST):self.push(15,self.pc);self.pc=target
                else:self.external(target)
            elif op in (0xc080,0xca80,0xcb80):
                target=self.operand(32)
                take=op==0xc080 or op==0xca80 and self.zero or op==0xcb80 and not self.zero
                if take:
                    if target==0xff80de20:self.events.append(('retire',r[13]));self.done=True;break
                    elif target==0xff9f31e0:self.events.append(('native_debris_continuation',target));self.done=True;break
                    elif target==0xff83c340:
                        need(r[15]==self.base_sp,'Animation continuation lives only on private A12 stack')
                        fields=r[0];cursor=r[9];poses=0
                        while self.load(cursor,32):
                            self.events.append(('pose',self.age,r[8],self.load(cursor,32)))
                            self.age+=fields;cursor+=32;poses+=1
                            need(poses<=5,'Finite original five-frame particle only')
                        r[9]=cursor;self.pc=self.pop(12);self.poison()
                    else:self.pc=target
            elif op in (0xce01,0xcf01):
                if (op==0xce01 and self.negative)or(op==0xcf01 and not self.negative):self.pc+=16
            elif op==0x0147:r[7]=self.pc
            elif op==0x0b07:r[7]=(r[7]+self.operand(16))&0xffffffff
            elif op==0xa2ec:self.push(12,r[7])
            elif 0x1420<=op<=0x142f:r[dst]=(r[dst]-1)&0xffffffff;self.flags(r[dst])
            elif op==0x03a0:r[0]=(-r[0])&0xffffffff;self.flags(r[0])
            elif 0x0b80<=op<=0x0b8f:r[dst]&=self.operand(32);self.flags(r[dst])
            elif op==0x0b00:r[0]=(r[0]+self.operand(32))&0xffffffff;self.flags(r[0])
            elif 0x4000<=op<=0x41ff:r[dst]=(r[dst]+r[src])&0xffffffff;self.flags(r[dst])
            elif op==0x54a4:r[4]|=r[5];self.flags(r[4])
            elif op==0x0be0:
                immediate=(~self.operand(16))&0xffff;r[0]=(r[0]-immediate)&0xffffffff;self.flags(r[0])
            elif 0xb400<=op<=0xb7ff:
                width=32 if op&0x200 else 16;at=r[src]+self.operand(16)
                r[dst]=self.load(at,width)
                if width==16 and r[dst]&0x8000:r[dst]|=0xffff0000
                self.flags(r[dst])
            elif 0xb000<=op<=0xb3ff:
                width=32 if op&0x200 else 16;self.store(r[dst]+self.operand(16),r[src],width)
            elif 0xb800<=op<=0xbbff:
                width=32 if op&0x200 else 16;source=self.operand(16);destination=self.operand(16)
                self.store(r[dst]+destination,self.load(r[src]+source,width),width)
            elif op==0x8725:r[5]=self.load(r[9],32)
            elif op==0x1820:r[0]=1;self.flags(1)
            else:raise ValueError(f'Unknown emitted word {op:04X} at {self.pc-16:08X}')
        else:raise ValueError('Unit execution exceeds finite step bound')
        return self


def inspect_units(guest,previous,native):
    need(guest[:FIRST]==previous[:FIRST] and guest[LAST:]==previous[LAST:],
         'Entire previous native gameplay/dispatch/audio unchanged outside exact unused emitter allocation')
    offset=(0xff9f2e40-0xff800000)//8
    kernel=bytearray(native[offset:offset+0x74])
    first=struct.pack('<HHHI',0xb5a0,0x230,0x0d5f,0xff83c870)+struct.pack('<5H',*([0x4c00]*5))
    need(len(first)==20,'Exact native cadence replacement boundary')
    kernel[:20]=first;struct.pack_into('<4H',kernel,0x3e,0xb7a1,0x330,0x4c21,0xcf01)
    need(guest[0xb0600:0xb0674]==kernel and guest[0xb0674:0xb067a]==struct.pack('<HI',0xc080,0xff9f31e0),
         'Whole native debris kernel conserved except source cadence/direction and ordinary native continuation')
    cases=[]
    for count in (2,3):
        cpu=UnitCPU(guest,0xafdc0);cpu.regs[0]=count;before=cpu.regs[10];cpu.execute()
        task=[e for e in cpu.events if e[0]=='task']
        need(cpu.done and len(task)==1 and task[0][2:]==(0x201,address(0xafe00),cpu.victim) and
             cpu.load(task[0][1]+0x80,32)==count and cpu.regs[10]==before and cpu.regs[15]==cpu.base_sp,
             'True victim/saved count native201 emitter birth and balanced non-yielding constructor')
        cpu.pc=address(0xafe00);cpu.regs[13]=task[0][1]
        for reg in range(7,13):cpu.regs[reg]=cpu.load(task[0][1]+0x100-(reg-6)*0x20,32)
        cpu.execute(stop_fields=12)
        children=[e for e in cpu.events if e[0]=='task' and e[3]==address(0xb00c0)]
        need(len(children)==count*3 and cpu.regs[8]==cpu.victim and cpu.regs[10]==count and cpu.regs[15]==cpu.base_sp,
             'All three4fieldticks spawn exact2/3independent particles; victim/count/stack stay intact')
        cases.append(dict(kind='emitter',count=count,ticks=3,particles=len(children)))
    for face in (0,16):
        for xy in ((748,102),(400,130)):
            for roll in ('low','mid','high'):
                cpu=UnitCPU(guest,0xafe80,xy,face,roll);original=cpu.regs[8:12].copy();cpu.execute()
                jobs=[e for e in cpu.events if e[0]=='task'];caches=[e for e in cpu.events if e[0]=='cache']
                need(cpu.done and len(jobs)==len(caches)==1 and caches[0][3]==address(0xafc40) and jobs[0][2:4]==(0x201,address(0xb00c0)) and
                     cpu.regs[8:12]==original and cpu.regs[15]==cpu.base_sp and
                     all(cpu.mem[at]==value for at,value in cpu.original_victim.items()),
                     'Sole native particle/cache ownership; every true victim/main field and live caller register conserved')
                actor=jobs[0][4];x_offset=-31 if roll=='low' else 32 if roll=='high' else 0
                if face:x_offset=-x_offset
                y_offset=0 if roll=='low' else 111 if roll=='high' else 55
                vx=-0x1ffff if roll=='low' else 0x20000 if roll=='high' else 0
                vy=-0x10000 if roll=='low' else -0x3ffff if roll=='high' else -(0x30000//2+0xffff)
                need(cpu.load(actor+0x90,16)==xy[0]+x_offset and cpu.load(actor+0xb0,16)==xy[1]+y_offset and
                     cpu.load(actor+0x40,32)==vx&0xffffffff and cpu.load(actor+0x60,32)==vy&0xffffffff and
                     cpu.load(actor+0xf0,16)==0x8002|face and cpu.load(actor+0xc0,32)==0x51,
                     'Exact facing-relative source position, full32bitXY fractions, signedX and negative1..4pxY velocities')
                job=jobs[0][1];cpu.regs[13]=job
                for reg in range(7,13):cpu.regs[reg]=cpu.load(job+0x100-(reg-6)*0x20,32)
                cpu.pc=address(0xb00c0);cpu.done=False;cpu.age=0;cpu.execute()
                events=cpu.events
                need(cpu.age==20 and len([e for e in events if e[0]=='pose'])==5 and
                     ('object_free',actor) in events and ('cache_free',caches[0][1]) in events and ('retire',job) in events and
                     cpu.regs[15]==cpu.base_sp and cpu.regs[12]==job+0x6f0,
                     'Full5x4particle lifetime followed by sole object/palette/cache/task retirement with both stacks balanced')
                cases.append(dict(kind='particle',face=face,xy=xy,roll=roll,fields=20))
    for face in (0,16):
        for roll in ('low','high'):
            cpu=UnitCPU(guest,0xb0140,(748,102),face,roll);original=cpu.regs[8:12].copy();cpu.execute()
            jobs=[e for e in cpu.events if e[0]=='task']
            need(cpu.done and len(jobs)==32 and cpu.regs[8:12]==original and cpu.regs[15]==cpu.base_sp,
                 'Entire own five-part32bone emitter preserves caller and balanced native stack')
            by_part=[4,4,20,2,2];cursor=0
            for part,count in enumerate(by_part):
                recipe=struct.unpack_from('<12I',guest,0xafca0+part*48)
                for index,event in enumerate(jobs[cursor:cursor+count]):
                    job=event[1]
                    need(event[2:]==(0x10c,address(0xb0600),cpu.victim) and
                         cpu.load(job+0x250,32)==recipe[11] and cpu.load(job+0x330,32)==(0xffffffff if index%2 else 0) and
                         all(cpu.load(job+offset,32)==value for offset,value in
                             ((0x290,recipe[5]),(0x270,recipe[6]),(0x2b0,recipe[7]),(0x2d0,recipe[8]),(0x80,recipe[4]))) and
                         cpu.load(job+0x230,16)==recipe[9] and cpu.load(job+0x2f0,16)==748 and
                         cpu.load(job+0x310,16)==102+recipe[3] and cpu.load(job+0x100,32)==0xff9ecdb0,
                         'Every real emitted bone task uses own typed ranges/anchors/gravity/cadence and alternating source pair directions')
                    child=UnitCPU(guest,0xb0600,roll=roll)
                    child.mem=dict(cpu.mem);child.regs[13]=job
                    for reg in range(7,13):child.regs[reg]=child.load(job+0x100-(reg-6)*0x20,32)
                    child.execute();actor=child.regs[8]
                    magnitude=1 if roll=='low' else recipe[5]
                    expected_vx=-magnitude if index%2 else magnitude
                    expected_vy=-(recipe[8]+(1 if roll=='low' else recipe[7]))
                    need(child.done and child.load(actor+0x40,32)==expected_vx&0xffffffff and
                         child.load(actor+0x60,32)==expected_vy&0xffffffff and
                         child.load(actor+0x90,16)==748 and child.load(actor+0xb0,16)==102+recipe[3] and
                         child.load(job+0x1d0,16)==3 and child.load(job+0x1e0,16)==1 and
                         child.regs[10]==0x4000 and child.regs[15]==child.base_sp and
                         ('native_debris_continuation',0xff9f31e0) in child.events,
                         'Actual copied native initializer has correct pair sign, independent RNG, exact cadence3 and original native physics continuation')
                cursor+=count
            cases.append(dict(kind='paired_bones',face=face,roll=roll,particles=32))
    return cases


def main():
    need(not OUT.exists() and not phases.visual.native.census(),'Fresh immutable source qualification; no native games live')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((accepted.OUT/'report.json').read_text());original=json.loads((reference.OUT/'report.json').read_text())
        need(receipt['passed'] and original['passed'] and original['originalSmokeLifecycleReferenceAccepted'] and
             all(sha(p)==h for record in (receipt,original) for p,h in record['inputHashes'].items()),
             'Actual current source and real477epoch smoke reference conserved')
        old=(assets.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        need(new.count(BEGIN)==new.count(END)==1,'Unique actual source block')
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END);block=new[first:last]
        need(new[:first-1]+new[last:]==old,'Only appended native emitters; every preceding source/gameplay byte unchanged')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(assets.STAGE/leaf),'Host/audio/identity/platform source untouched')
        old_harness=json.loads(gzip.open(accepted.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_EFFECT_ASSETS_END';need(old_harness.count(anchor)==1,'Exact preserved initializer append boundary')
        harness=old_harness.replace(anchor,anchor+'\n'+block)
        scope=dict(vars(phases),OUT=OUT)
        exec(compile(inspect.getsource(phases.compile_probe),__file__+'::isolated_compile','exec'),scope)
        base=phases.palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=phases.palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=scope['compile_probe'](harness,base,payload)
        previous=bytearray(guest);previous[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole prior initialized guest conserved exactly')
        native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();cases=inspect_units(guest,bytes(previous),native)
        faults=[]
        for name,at in (('emitter_count',0xafdc4),('emitter_type',0xafdc8),('emitter_target',0xafdce),
            ('smoke_stream',0xafe86),('smoke_palette_object_free',0xb00e8),('bone_pair_branch',0xb0644),
            ('native_cadence',0xb0602),('native_bone_kernel',0xb0628),('previous_dispatch',0xf436c)):
            wrong=bytearray(guest);wrong[at]^=1
            try:inspect_units(bytes(wrong),bytes(previous),native)
            except (ValueError,KeyError,IndexError,struct.error) as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Actual emitted fault admitted: '+name)
        paths=[Path(__file__),accepted.OUT/'report.json',accepted.OUT/'executed_sources.json.gz',reference.OUT/'report.json',
            ROOT/'mk2/mk2-maincpu.bin',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),previousGoalTurnClassification='progress: actual source phases/grey assets/native camera qualified',
            emittedWordUnitCases=cases,negativeFaultsRejected=faults,nativeSmokeTaskCategory='0201',nativeBoneTaskCategory='010C',
            sourceSmokeFields=20,sourceEmitterCadence=4,sourceEmitterCounts=[2,3],sourcePairedBones=32,
            emittersPersistUntilNativeSceneTeardown=True,winnerDelayed=False,trueIdentitySubstitution=False,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            latestPlayableChanged=False,limitations=['Unit external native helpers are modeled, not actual port gameplay evidence.',
                'Native particles use exact source ranges/positions/lifetimes; scene transition must still prove actual object/cache/palette clearance.',
                'Native bone kernel keeps native three-arc physics/cleanup/impact-audio; broad source art/sound fidelity still needs runtime acceptance.',
                'Full victim/action/input/CPU/audio integration and all14requirements/sixremainingworkgroups remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original natural-game scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Exact terminal generated source probe only');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],unitCases=len(cases),faults=len(faults),nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise


if __name__=='__main__':main()
