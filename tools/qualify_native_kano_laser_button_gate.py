"""Qualify the actual MKII button-history laser predicate, not gameplay.

Compile the whole successor initializer in RAM. Execute its emitted words
and the unchanged native held-mask/history/ring writer instructions in a
bounded unit model. Only body separation is modeled externally. Preserve
full scope, frozen source/checkers, public build and storage constraints.
"""
import gzip
import hashlib
import inspect
import json
import struct
import traceback
from pathlib import Path

import qualify_native_kano_laser_emitters as prior
import qualify_native_kano_laser_emitters_disjoint as accepted

ROOT=prior.ROOT
STAGE=ROOT/'source_native_kano_laser_button_gate'
OUT=ROOT/'audit_native_kano_laser_button_gate_source'
FIRST,LAST=0xb0690,0xb0800
BEGIN,END='// KANO_LASER_BUTTON_GATE_BEGIN','// KANO_LASER_BUTTON_GATE_END'
need,sha,address=prior.need,prior.sha,prior.address


def contract(guest,previous,native):
    expected=bytearray(previous)
    need(all(v==255 for v in previous[FIRST:LAST]),'Actual prior allocation wholly unused')
    struct.pack_into('<7H',expected,FIRST,40,3,2,2,1,0,0)
    words=[];fixups=[]
    def dword(value):words.extend((value&65535,value>>16))
    def mov(reg,value):words.append(0x09e0+reg);dword(value)
    def call(value):words.append(0x0d5f);dword(value)
    def fail(op):words.append(op);fixups.append(len(words));dword(0)
    words.extend((0x05a4,0x1b00,0x0106,0x0b44,0xfffc));fail(0xcb80)
    mov(0,0x33);mov(1,0x300c);call(0xff877d80);fail(0xcb80)
    mov(0,0x40);mov(1,0x4000);call(0xff877d80);fail(0xca80)
    mov(11,address(FIRST));call(0xff877580);fail(0xc980)
    call(0xff834cc0)
    words.extend((0x0b43,0xff7f));fail(0xc480)
    words.extend((0x0b43,0xff4f));fail(0xc380)
    words.extend((0x0de0,0x0960))
    target=address(0xb06c0+len(words)*2)
    words.extend((0x0320,0x0960))
    for at in fixups:words[at:at+2]=[target&65535,target>>16]
    struct.pack_into('<'+'H'*len(words),expected,0xb06c0,*words)
    need(guest==expected,'Whole actual guest exact: one record and callable gate only; every binding conserved')
    for start,end in ((0xff877580,0xff877a90),(0xff877d80,0xff877fd0),(0xff814b70,0xff814c90)):
        first=(start-0xff800000)//8;last=(end-0xff800000)//8
        need(guest[first:last]==native[first:last],'Entire actual native history/held-mask/ring producer unchanged')
    return dict(record=f'{address(FIRST):08X}',predicate=f'{address(0xb06c0):08X}',
        buttonParser='FF877580',directionParserNotUsed='FF8775D0',
        historyNewestFirst=[3,2,2,1],timeoutTicks=40,separation=[128,176],
        allowedFinalButtons=['High Kick'],groundAndOpponentGateStillRequiredAtBinding=True)


def native_mapping(native):
    read=lambda a:struct.unpack_from('<I',native,(a-0xff800000)//8)[0]
    table=0xff812090
    expected={5:0xff813ae0,6:0xff813bb0,13:0xff813f00,14:0xff813fd0,
              64:0xff813a90,68:0xff813eb0}
    for event,handler in expected.items():
        need(read(table+event*48+16)==handler,'Actual physical press dispatch for both players')
    # Entry words establish the true token and separate press-ring pointer.
    for handler,token,ring in ((0xff813a90,1,0x1060340),(0xff813eb0,1,0x1060f10),
        (0xff813b60,2,0x1060340),(0xff813f80,2,0x1060f10),
        (0xff813bb0,3,0x1060340),(0xff813fd0,3,0x1060f10)):
        at=(handler-0xff800000)//8
        need(struct.unpack_from('<HHI',native,at)==(0x1800+token*32,0x09e1,ring),
             'Actual native LP/Block/HK press tokens and true player ring')
    return dict(physicalPressTable=f'{table:08X}',handlers={str(k):f'{v:08X}' for k,v in expected.items()},
                buttonRings=['01060340','01060F10'],tokens=dict(LP=1,Block=2,HK=3),
                releaseRingsNotUsed=['01060880','01061450'])


class CPU:
    """Unit-only TMS words; actual port runtime acceptance stays false."""
    def __init__(self,guest,side=1,gap=150,finish=3,in0=None,in2=0xffff):
        self.guest=guest;self.r=[0x12340000+i for i in range(16)];self.mem={}
        self.z=False;self.c=False;self.pc=0;self.calls=[];self.gap=gap;self.writes=[]
        self.r[8]=0x30000 if side==1 else 0x40000;self.r[13]=0x10000;self.r[15]=0x80000
        self.store(0x1060220,0x30000,32);self.store(0x1061b00,finish,16)
        self.store(0x1600000,in0 if in0 is not None else (0xffffffff^(0x40 if side==1 else 0x4000)),32)
        self.store(0x1600020,in2,32)
        self.ring=0x1060340 if side==1 else 0x1060f10
        self.store(self.ring,self.ring+32,32)
        self.writes.clear()

    def load(self,at,bits):
        if at>=0xff800000:return int.from_bytes(self.guest[(at-0xff800000)//8:(at-0xff800000)//8+bits//8],'little')
        return sum(self.mem.get(at+i,0)<<(i) for i in range(0,bits,16))

    def store(self,at,value,bits):
        for i in range(0,bits,16):self.mem[at+i]=(value>>i)&65535
        self.writes.append((at,bits))

    def push(self,value):self.r[15]-=32;self.store(self.r[15],value,32)
    def pop(self):
        value=self.load(self.r[15],32);self.r[15]+=32;return value
    def nz(self,value):self.z=(value&0xffffffff)==0;return value&0xffffffff
    def cmp(self,left,right):self.z=(left&0xffffffff)==(right&0xffffffff);self.c=(left&0xffffffff)<(right&0xffffffff)
    def word(self):value=self.load(self.pc,16);self.pc+=16;return value
    def long(self):value=self.load(self.pc,32);self.pc+=32;return value
    def signed(self,value):return value-65536 if value&32768 else value

    def run(self,start):
        sentinel=0x76543210;self.push(sentinel);self.pc=start
        for _ in range(3000):
            if self.pc==sentinel:
                need(self.r[15]==0x80000,'All real native CALL/RETS and A8 save slots balanced');return self.c
            at=self.pc;op=self.word();dst=op&15;src=(op>>5)&15;r=self.r
            if op&0xfff0==0x09e0:r[dst]=self.nz(self.long())
            elif op&0xfff0==0x09c0:r[dst]=self.nz(self.signed(self.word()))
            elif op&0xfc10==0x1800:r[dst]=self.nz(((op>>5)&31) or 32)
            elif op&0xfff0 in (0x05a0,0x07a0):
                bits=16 if op&0xfff0==0x05a0 else 32;v=self.load(self.long(),bits)
                r[dst]=self.nz(self.signed(v) if bits==16 else v)
            elif op&0xfff0==0x0b40:self.cmp(r[dst],self.signed(self.word()^65535)&0xffffffff)
            elif op&0xfff0==0x0b00:r[dst]=self.nz(r[dst]+self.signed(self.word()))
            elif op&0xfff0==0x0be0:r[dst]=self.nz(r[dst]-self.signed(self.word()^65535))
            elif op&0xfff0==0x03e0:r[dst]=self.nz(~r[dst])
            elif op&0xfff0==0x0b80:r[dst]=self.nz(r[dst]&(self.long()^0xffffffff))
            elif op&0xfff0==0x0ba0:r[dst]|=self.long()
            elif op&0xfe10==0x4800:self.cmp(r[dst],r[src])
            elif op&0xfe10==0x4c00:r[dst]=self.nz(r[src])
            elif op&0xfe10==0x5000:r[dst]=self.nz(r[dst]&r[src])
            elif op&0xfe10==0x5400:r[dst]=self.nz(r[dst]|r[src])
            elif op&0xfe10==0x4400:r[dst]=self.nz(r[dst]-r[src])
            elif op&0xfc10==0x1c00:self.z=not bool(r[dst]&(1<<(31-((op>>5)&31))))
            elif op&0xfe10==0x2400:r[dst]=self.nz(r[dst]<<(((op>>5)&31) or 32))
            elif op==0x0520:r[0]=self.nz(r[0]&65535)
            elif op==0xe500:
                # CMPXY Z compares the high signed Y word (button token),
                # not the low clock word. Actual 34010ops.hxx contract.
                delta=((r[0]>>16)-(r[8]>>16))&65535;self.z=delta==0;self.c=bool(delta&32768)
            elif op==0xa30f:self.push(r[8])
            elif op==0xa20f:self.push(r[0])
            elif op==0x09af:
                mask=self.word()
                for reg in reversed(range(16)):
                    if mask&(1<<reg):r[reg]=self.pop()
            elif op==0x9569 or op==0x9568:
                r[dst]=self.nz(self.signed(self.load(r[11],16)));r[11]+=16
            elif op&0xfe10==0x8600:r[dst]=self.nz(self.load(r[src],32))
            elif op==0x92e0:self.store(r[0],r[7],32);r[0]+=32
            elif op==0x8201:self.store(r[1],r[0],32)
            elif op==0x0d5f:
                target=self.long();self.calls.append(target)
                if target==0xff834cc0:
                    for reg in range(7):r[reg]=0xfeed0000+reg
                    r[3]=self.gap;self.z=False;self.c=True
                else:self.push(self.pc);self.pc=target
            elif op==0x0d3f:
                displacement=self.signed(self.word())*16;self.push(self.pc);self.pc+=displacement
            elif op==0x0960:self.pc=self.pop()
            elif op==0x0320:self.c=False
            elif op==0x0de0:self.c=True
            elif op&0xf000==0xc000:
                cond=(op>>8)&15
                take={0:True,3:not self.c and not self.z,4:self.c,8:self.c,9:not self.c,10:self.z,11:not self.z}.get(cond)
                need(take is not None,f'Unit branch condition {op:04X}')
                target=self.long() if op&255==128 else self.pc+self.signed((op&255)| (0xff00 if op&128 else 0))*16
                if take:self.pc=target
            else:raise ValueError(f'Unsupported actual word {op:04X} at {at:08X}')
        raise ValueError('Actual emitted/native word unit budget exceeded')

    def history(self,tokens=(1,2,2,3),first=970,position=0):
        self.store(self.ring,self.ring+32+position*32,32)
        for index,token in enumerate(tokens):
            self.r[0]=token;self.r[1]=self.ring
            self.store(0x105d090,first+(1000-first)*index//3,16)
            self.run(0xff814b70)
        self.store(0x105d090,1000,16)


def units(guest):
    cases=[]
    for side in (1,2):
        for position in range(20):
            for gap in (127,128,150,176,177):
                cpu=CPU(guest,side,gap);cpu.history(position=position);actor=cpu.r[8];main=cpu.r[13]
                before=dict(cpu.mem);cpu.writes.clear();result=cpu.run(address(0xb06c0))
                need(result==(128<=gap<=176),'Native unit exact128..176 inclusive body-gap gate')
                need(cpu.r[8]==actor and cpu.r[13]==main and all(at>=0x7ff00 for at,bits in cpu.writes),
                     'True actor/main, both history rings, physical ports and all non-stack guest fields unchanged')
                need(all(cpu.mem[at]==value for at,value in before.items() if at<0x7ff00), 'No identity/history/gameplay state mutation')
                need(0xff877580 in cpu.calls and 0xff8775d0 not in cpu.calls,'Actual button routine, never directional/facing routine')
                cases.append(dict(side=side,ringStart=position,gap=gap,accepted=result))
        for first in (960,959):
            cpu=CPU(guest,side);cpu.history(first=first)
            need(cpu.run(address(0xb06c0))==(first==960),'Native actual history timeout boundary40/41')
        for tokens in ((1,2,3,3),(1,2,2,4),(4,2,2,3),(1,2,1,3)):
            cpu=CPU(guest,side);cpu.history(tokens=tokens)
            need(not cpu.run(address(0xb06c0)),'Wrong native button chronology cannot activate')
        for finish in (0,1,2,4):
            cpu=CPU(guest,side,finish=finish);cpu.history()
            need(not cpu.run(address(0xb06c0)),'Only actual finish-window3')
        for attack in (0,0x10 if side==1 else 0x1000,0x20 if side==1 else 0x2000):
            hk=0x40 if side==1 else 0x4000
            cpu=CPU(guest,side,in0=0xffffffff^(hk|attack) if attack else 0xffffffff);cpu.history()
            need(not cpu.run(address(0xb06c0)),'Final HK mandatory; held HP/Block rejected')
        for bit in ((0,1) if side==1 else (4,5)):
            cpu=CPU(guest,side,in2=0xffffffff^(1<<bit));cpu.history()
            need(not cpu.run(address(0xb06c0)),'Actual separate-port LP/LK normalization rejected')
    return dict(gapAndRingWrapCases=cases,timeoutCases=4,wrongHistoryCases=8,finishWindowCases=8,
                finalHeldButtonCases=10,actualNativeRingWriterExecuted=True,actualNativeConsumerWordsExecuted=True,
                nativeGameplayEvidence=False,externalBodyGapHelperModeled=True)


def main():
    need(not OUT.exists() and not prior.phases.visual.native.census(),'Fresh immutable source qualification; no native games live')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((accepted.OUT/'report.json').read_text())
        need(receipt['passed'] and all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Whole latest source/evidence conserved')
        old=(prior.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END);block=new[first:last]
        need(new.count(BEGIN)==new.count(END)==1 and new[:first-1]+new[last:]==old,'Only one new source block')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Host/platform/audio untouched')
        old_harness=json.loads(gzip.open(accepted.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_EMITTERS_END';need(old_harness.count(anchor)==1,'Exact latest initializer boundary')
        harness=old_harness.replace(anchor,anchor+'\n'+block)
        scope=dict(vars(prior.phases),OUT=OUT)
        exec(compile(inspect.getsource(prior.phases.compile_probe),__file__+'::isolated_compile','exec'),scope)
        base=prior.phases.palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=prior.phases.palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=scope['compile_probe'](harness,base,payload)
        previous=bytearray(guest);previous[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole prior initialized guest exact')
        native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
        mapping=native_mapping(native);details=contract(guest,bytes(previous),native);tests=units(guest)
        faults=[]
        for name,at in (('timeout',FIRST),('HK_token',FIRST+2),('LP_token',FIRST+8),
            ('finish_window',0xb06c8),('forbidden_buttons',0xb06d2),('history_parser',0xb070e),
            ('near_distance',0xb0724),('prior_CPU_binding',0xf436c)):
            wrong=bytearray(guest);wrong[at]^=1
            try:contract(bytes(wrong),bytes(previous),native)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Actual emitted fault admitted: '+name)
        paths=[Path(__file__),accepted.OUT/'report.json',accepted.OUT/'executed_sources.json.gz',
            ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',
            ROOT/'audit_native_kano_secondary_input/report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
            ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            previousGoalTurnClassification='no progress: status restatement only; latest receipts revalidated before successor work',
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),nativeMapping=mapping,contract=details,
            emittedWordUnits=tests,negativeFaultsRejected=faults,latestPlayableChanged=False,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            limitations=['Callable gate unbound until complete action/victim choreography exists.',
                'Unit synthetic inputs are not physical native gameplay evidence.',
                'Normal native ground/opponent gate, CPU second dispatch, actual move/audio and all14+6 scope remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Only exact terminal temporary probe retired');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],ringGapCases=len(tests['gapAndRingWrapCases']),nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise


if __name__=='__main__':main()
