"""Whole source-byte and emitted-control qualification for private laser.

Source/unit evidence only, never native gameplay acceptance. All graphics,
palette/effect lifetimes and position ABI remain pinned to preceding proofs.
Actual sound/flash/roster alignment and scene cleanup require earned runs.
"""
import gzip
import hashlib
import inspect
import json
import struct
import traceback
from pathlib import Path

import qualify_native_kano_laser_button_gate as gate
import qualify_native_kano_laser_button_gate_bound as accepted
import audit_native_kano_laser_victim_position_complete as position

ROOT=gate.ROOT
STAGE=ROOT/'source_native_kano_laser_action'
OUT=ROOT/'audit_native_kano_laser_action_source'
FIRST,LAST=0xb0800,0xb0d00
BEGIN,END='// KANO_LASER_ACTION_BEGIN','// KANO_LASER_ACTION_END'
need,sha,address=gate.need,gate.sha,gate.address
u32=lambda b,a:struct.unpack_from('<I',b,a)[0]


class Assembly:
    def __init__(self,guest,start,limit):self.guest=guest;self.at=start;self.limit=limit
    def code(self,*words):
        need(self.at+2*len(words)<=self.limit,'Independent expected-code allocation')
        struct.pack_into('<'+'H'*len(words),self.guest,self.at,*words);self.at+=2*len(words)
    def mov(self,reg,value):value&=0xffffffff;self.code(0x09e0+reg,value&65535,value>>16)
    def call(self,target):self.code(0x0d5f,target&65535,target>>16)
    def jump(self,target,op=0xc080):self.code(op,target&65535,target>>16)
    def cooperate(self,target):self.code(0x0147,0x0b07,0x60,0xa2ec);self.jump(target)


def contract(guest,previous,payload):
    expected=bytearray(previous);need(all(x==255 for x in previous[FIRST:LAST]),'Actual previous unused action range')
    groups=[]
    for ident in range(19):
        if ident in (12,13):groups.append(None);struct.pack_into('<I',expected,0xb0800+ident*4,0);continue
        if ident>=17:
            root=0x4794 if ident==17 else 0x6370
            stream=u32(payload,root+64*4);need(stream==(0xfe831b00 if ident==17 else 0xfe83ecc0),'Actual own original laser-hit stream')
            group=u32(payload,(stream-0xfe800000)//8)
            need(group==(0xfe831b40 if ident==17 else 0xfe83ed00),'Actual own original laser-hit group')
        else:
            root=u32(previous,0xfc800+ident*4)
            pain=u32(previous,(root-0xff800000)//8+16*4)
            group=u32(previous,(pain-0xff800000)//8+4)
            need(0xff800000<=group<0xfffffff0,'Actual own native recoil composite, never null64')
        stream=0xb0860+ident*8
        struct.pack_into('<II',expected,stream,group,0)
        struct.pack_into('<I',expected,0xb0800+ident*4,address(stream))
        groups.append(dict(id=ident,group=f'{group:08X}',stream=f'{address(stream):08X}',
            source='Own original MK3 laser-hit64' if ident>=17 else 'Own native MKII high-hit16 second composite'))
    a=Assembly(expected,0xb0900,0xb0b00)
    a.code(0xb500,0x140);a.mov(10,1);a.mov(5,6);a.mov(11,address(0xaf7b0));a.call(address(0xaf700))
    a.mov(0,address(0xb0800));a.code(0xb501,0x1f0,0x24a1,0x4020,0x8609)
    a.code(0x098f,0x8080,0xb7a0,0x140,0x5608,0x5700,0x5608);a.call(0xff83ce60);a.code(0x09af,0x0101)
    a.call(0xff83b470);a.mov(0,-184);a.mov(1,0);a.call(0xff83cc20)
    a.mov(0,4);a.cooperate(0xff83c340);a.call(address(0xafda0))
    a.mov(0,0x30000);a.mov(1,3);a.mov(2,5);a.cooperate(address(0xafb00))
    a.mov(0,2);a.call(address(0xafdc0))
    a.mov(0,0x50000);a.mov(1,3);a.mov(2,10);a.cooperate(address(0xafb00))
    a.mov(0,3);a.call(address(0xafdc0));loop=address(a.at)
    a.mov(0,0x50000);a.mov(1,3);a.mov(2,40);a.cooperate(address(0xafb00));a.jump(loop)
    a=Assembly(expected,0xb0b00,0xb0c80)
    a.mov(1,1);a.mov(0,1);a.call(0xff8cd780);a.mov(0,20);a.call(0xff80dcc0)
    a.cooperate(address(0xafa00));a.mov(7,address(0xb0900));a.call(0xff842710)
    a.cooperate(address(0xafa40));a.code(0xa30f,0xb7a8,0x140,0x4d00);a.call(0xff838f60)
    a.call(address(0xb0140));a.code(0x09af,0x0100)
    a.code(0xb7a0,0x170);a.mov(7,0xff841ec0);a.call(0xff83f930)
    a.cooperate(address(0xafa80));a.call(address(0xaf290));a.call(0xff8cdc40);a.jump(0xffa14860)
    a=Assembly(expected,0xb0c80,0xb0cc0)
    a.call(address(0xb06c0));a.jump(address(0xf5500),0xc980)
    a.mov(1,176);a.mov(7,address(0xb0cc0));a.jump(0xff876f70)
    a=Assembly(expected,0xb0cc0,LAST)
    a.code(0xb7a0,0x140,0xb404,0x1f0,0x0b44,0xfff3);a.jump(0xffa14860,0xca80)
    a.code(0x0b44,0xfff2);a.jump(0xffa14860,0xca80);a.jump(address(0xb0b00))
    changes=((0xff270+17*4,address(0xb0c80)),(0xf436c+17*4,address(0xb0cc0)),(0xf395c+17*4,0x00960050))
    for at,value in changes:struct.pack_into('<I',expected,at,value)
    need(guest==expected,'Entire guest exact: own victim/actions plus only three real Kano bindings')
    need(u32(guest,0xf4320+17*4)==address(0xf55c0) and u32(guest,0xff270+18*4)==u32(previous,0xff270+18*4),
         'First Kano finisher and every Sonya route unchanged')
    return dict(ownVictimComposites=groups,logicalBoundaries=dict(setup=20,contact=68,burst=164,returnAndCleanup=196),
        humanHKParser=f'{address(0xb0c80):08X}',cpuSecondAction=f'{address(0xb0cc0):08X}',cpuFirstSpacing=80,cpuSecondSpacing=150,
        trueVictimHandoff='FF842710',trueVictimPark='FF83F930 -> FF841EC0',normalFinishGate='FF876F70',winner='FF8CDC40 -> FFA14860',
        originalOpaqueFlag400NotTransferred=True,identitySubstitution=False)


class Control:
    """Execute emitted entry/control words; dependent/native helpers modeled.

The independently proved helper streams are read from actual emitted guest.
Volatile registers are poisoned across sleep/short helpers. No emulator is
used and these synthetic unit fixtures are never called gameplay evidence.
"""
    def __init__(self,guest,side,ident,victim_mode=False):
        self.guest=guest;self.r=[0]*16;self.mem={};self.sp=[];self.private=[];self.events=[];self.age=68 if victim_mode else 0
        self.side=side;self.ident=ident;self.performer=0x30000;self.victim=0x40000;self.main=0x10000;self.vm=0x20000
        self.r[8]=self.victim if victim_mode else self.performer;self.r[13]=self.vm if victim_mode else self.main
        self.r[12]=self.r[13]+0x6f0;self.r[15]=0x80000
        self.mem.update({self.performer+0x1f0:17,self.victim+0x1f0:ident,self.main+0x140:self.victim,
            self.main+0x170:self.vm,self.vm+0x140:self.performer,self.vm+0x170:self.main,
            self.main+0x190:0,self.victim+0x140:0x500,self.victim+0xf0:0 if side==2 else 16})
        self.pc=address(0xb0900 if victim_mode else 0xb0cc0);self.z=False;self.c=False;self.n=False;self.v=False
        self.original=dict(self.mem)
    def word(self):v=struct.unpack_from('<H',self.guest,(self.pc-0xff800000)//8)[0];self.pc+=16;return v
    def long(self):v=u32(self.guest,(self.pc-0xff800000)//8);self.pc+=32;return v
    def read(self,at):return u32(self.guest,(at-0xff800000)//8) if at>=0xff800000 else self.mem.get(at,0)
    def poison(self):
        for reg in range(7):self.r[reg]=0xdead0000+reg
    def yield_fields(self,count):
        need(not self.sp and self.r[8] in (self.performer,self.victim),'No live global stack/changed actor across native yield')
        self.age+=count;self.poison()
    def coroutine(self,target):
        need(len(self.private)==1,'Exactly one current native private continuation')
        if target in (address(0xafa00),address(0xafa40),address(0xafa80)):
            phase=(target-address(0xafa00))//0x200;table=(0xaf800,0xaf8a0,0xaf970)[phase]
            duration=0;rows=0
            while True:
                own,effect,ticks=struct.unpack_from('<3I',self.guest,table+rows*12)
                if not own and not effect:break
                duration+=ticks;rows+=1
            need((duration,rows)==((48,12),(96,16),(32,8))[phase] and self.r[8]==self.performer,'Whole actual phase duration/owner')
            if phase==0:self.mem[self.main+0x190]=0x50000
            else:need(self.mem[self.main+0x190]==0x50000,'One own beam persists through all phases')
            self.events.append((self.age,'phase',phase,duration));self.yield_fields(duration)
        elif target==0xff83c340:
            group=self.read(self.r[9]);need(group>=0xfe800000 and self.read(self.r[9]+32)==0,'One real own laser-hit composite and terminator')
            need(self.r[8]==self.victim and self.r[0]==4,'True victim receives four-field contact pose')
            self.events.append((self.age,'pose',group));self.yield_fields(4)
        elif target==address(0xafb00):
            packed,cadence,cycles=self.r[:3]
            need(self.r[8]==self.victim and (packed,cadence,cycles) in ((0x30000,3,5),(0x50000,3,10),(0x50000,3,40)),'Exact victim shake arguments')
            self.events.append((self.age,'shake',packed,cadence,cycles));self.yield_fields(cadence*cycles*2)
        else:raise ValueError(f'Unexpected cooperative helper {target:08X}')
        self.pc=self.private.pop();self.r[12]+=32
    def call(self,target):
        r=self.r
        if target==0xff8cd780:
            need(r[8]==self.performer and r[0]==r[1]==1,'Normal native fatality initialization');self.events.append((self.age,'init'))
        elif target==0xff80dcc0:self.yield_fields(r[0]);return
        elif target==0xff842710:
            need(r[8]==self.performer and r[13]==self.main and r[7]==address(0xb0900),'Handoff true native victim entry')
            self.events.append((self.age,'contact',self.victim,self.vm));r[9]=0xbad90000;r[10]=0xbada0000;r[11]=0xbadb0000
        elif target==0xff838f60:
            need(r[0]==self.victim and r[8]==self.victim,'Hide actual victim body only');self.events.append((self.age,'hide'))
        elif target==address(0xb0140):
            need(r[8]==self.victim and r[13]==self.main,'Own 32 bones constructed from true hidden victim');self.events.append((self.age,'bones',32))
        elif target==0xff83f930:
            need(r[0]==self.vm and r[7]==0xff841ec0 and r[8]==self.performer,'Park actual victim without re-showing hidden body');self.events.append((self.age,'park'))
        elif target==address(0xaf290):
            need(r[8]==self.performer and self.mem[self.main+0x190]==0x50000,'Only own beam object/cache cleanup')
            self.mem[self.main+0x190]=0;self.events.append((self.age,'cleanup'))
        elif target==0xff8cdc40:self.events.append((self.age,'winner'))
        elif target==address(0xaf700):
            need(r[8]==self.victim and (r[0],r[5],r[10],r[11])==(0x500,6,1,address(0xaf7b0)),'Actual victim encoded bank; six-field source red ramp')
            self.events.append((self.age,'palette',self.victim));r[9]=0xbad90000
        elif target==0xff83ce60:
            need(r[8]==self.performer and r[0]==self.victim,'Complete native copy helper true source/destination; no ID swap');self.events.append((self.age,'copy_position'))
        elif target==0xff83b470:
            need(r[8]==self.victim,'Flip/redraw actual victim own current body');self.events.append((self.age,'flip'))
        elif target==0xff83cc20:
            need(r[8]==self.victim and (r[0],r[1])==(0xffffff48,0),'Source184pixel facing-relative actual victim offset');self.events.append((self.age,'offset'))
        elif target==address(0xafda0):
            need(r[8]==self.victim,'Native tracking camera true victim');self.events.append((self.age,'camera'))
        elif target==address(0xafdc0):
            need(r[8]==self.victim and r[0] in (2,3),'Independent smoke201 true-victim emitter');self.events.append((self.age,'smoke',r[0]))
        else:raise ValueError(f'Unexpected native/control helper {target:08X}')
        self.poison()
    def run(self,stop=200):
        for _ in range(1000):
            if self.pc==0xffa14860 or self.age>=stop:
                need(not self.sp and not self.private,'Both native control stacks balanced at handoff boundary')
                need(self.mem[self.performer+0x1f0]==17 and self.mem[self.victim+0x1f0]==self.ident and
                     all(self.mem[at]==v for at,v in self.original.items() if at!=self.main+0x190),'Every real actor ID/main/opponent reference conserved')
                return self.events
            op=self.word();r=self.r;dst=op&15;src=(op>>5)&15
            if op&0xfff0==0x09e0:r[dst]=self.long();self.z=r[dst]==0
            elif op==0x0d5f:self.call(self.long())
            elif op==0x0147:r[7]=self.pc
            elif op==0x0b07:r[7]+=self.word()
            elif op==0xa2ec:self.private.append(r[7]);r[12]-=32
            elif op==0x098f:
                mask=self.word()
                for reg in range(16):
                    if mask&(0x8000>>reg):self.sp.append(r[reg])
            elif op==0x09af:
                mask=self.word()
                for reg in reversed(range(16)):
                    if mask&(1<<reg):r[reg]=self.sp.pop()
            elif op==0xa30f:self.sp.append(r[8])
            elif op&0xfe10==0xb600:
                displacement=self.word();r[dst]=self.read(r[src]+displacement);self.z=r[dst]==0
            elif op&0xfe10==0xb400:
                displacement=self.word();r[dst]=self.read(r[src]+displacement)&65535;self.z=r[dst]==0
            elif op&0xfc10==0x2400:r[dst]=(r[dst]<<(((op>>5)&31) or 32))&0xffffffff;self.z=r[dst]==0
            elif op&0xfe10==0x4000:r[dst]=(r[dst]+r[src])&0xffffffff;self.z=r[dst]==0
            elif op&0xfe10==0x8600:r[dst]=self.read(r[src]);self.z=r[dst]==0
            elif op&0xfe10==0x5600:r[dst]^=r[src];self.z=r[dst]==0
            elif op&0xfe10==0x4c00:r[dst]=r[src];self.z=r[dst]==0
            elif op&0xfff0==0x0b40:
                v=(self.word()^65535);v=v-65536 if v&32768 else v;self.z=r[dst]==(v&0xffffffff)
            elif op&0xf000==0xc000:
                need(op&255==128,'Only independently expected absolute entry/control branches')
                target=self.long();take={0:True,10:self.z,9:not self.c}.get((op>>8)&15)
                need(take is not None,'Expected control branch condition')
                if take:
                    if target in (address(0xafa00),address(0xafa40),address(0xafa80),address(0xafb00),0xff83c340):self.coroutine(target)
                    else:self.pc=target
            else:raise ValueError(f'Unsupported emitted control {op:04X} at {self.pc-16:08X}')
        raise ValueError('Control unit instruction budget exceeded')


def units(guest):
    cases=[]
    for side in (1,2):
        for ident in range(19):
            own=Control(guest,side,ident);events=own.run()
            if ident in (12,13):need(events==[],'Actual boss immunity before native init')
            else:
                need(events==[(0,'init'),(20,'phase',0,48),(68,'contact',own.victim,own.vm),(68,'phase',1,96),
                    (164,'hide'),(164,'bones',32),(164,'park'),(164,'phase',2,32),(196,'cleanup'),(196,'winner')],
                    'Whole emitted action: exact contact/burst/return, own cleanup and native winner without added delay')
                victim=Control(guest,side,ident,True);v=victim.run(stop=162)
                need(v[0:4]==[(68,'palette',victim.victim),(68,'copy_position'),(68,'flip'),(68,'offset')],
                    'True victim bank/position/facing/offset before native pose')
                need([(e[0],e[1],e[2:] if len(e)>2 else ()) for e in v if e[1] in ('camera','smoke')]==
                     [(72,'camera',()),(102,'smoke',(2,))], 'Native camera72, first independent emitter102')
                # Continue through emitter3 and its first full repeat without
                # treating the source's deliberate long victim loop as done.
                v=victim.run(stop=400)
                need((162,'smoke',3) in v and (162,'shake',0x50000,3,40) in v,'Second smoke162 and full240field repeat')
            cases.append(dict(side=side,victimID=ident,bossImmune=ident in (12,13)))
    return cases


def main():
    need(not OUT.exists() and not gate.prior.phases.visual.native.census(),'Fresh source qualification and no native games live')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((accepted.OUT/'report.json').read_text());abi=json.loads((position.OUT/'report.json').read_text())
        need(all(r['passed'] and all(sha(p)==h for p,h in r['inputHashes'].items()) for r in (receipt,abi)),
             'Whole latest source, complete native position helpers and all inputs conserved')
        old=(gate.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END);block=new[first:last]
        need(new.count(BEGIN)==new.count(END)==1 and new[:first-1]+new[last:]==old,'One new action source block only')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(gate.STAGE/leaf),'Host/audio/platform source conserved')
        old_harness=json.loads(gzip.open(accepted.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_BUTTON_GATE_END';need(old_harness.count(anchor)==1,'Exact prior initializer boundary')
        harness=old_harness.replace(anchor,anchor+'\n'+block)
        scope=dict(vars(gate.prior.phases),OUT=OUT)
        exec(compile(inspect.getsource(gate.prior.phases.compile_probe),__file__+'::isolated_compile','exec'),scope)
        base=gate.prior.phases.palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=gate.prior.phases.palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=scope['compile_probe'](harness,base,payload)
        previous=bytearray(guest);previous[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        for at,value in ((0xff270+17*4,address(0xf5500)),(0xf436c+17*4,address(0xf55c0)),(0xf395c+17*4,0x00500050)):
            struct.pack_into('<I',previous,at,value)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole prior guest including all previous bindings exact')
        result=contract(guest,bytes(previous),payload);cases=units(guest);faults=[]
        for name,at in (('own_Kano_pose',0xb0860+17*8),('own_stock_pose',0xb0860),('victim_palette_bank',0xb0902),
            ('full_position_helper',0xb094e),('contact_pose_ticks',0xb0970),('setup_ticks',0xb0b14),
            ('handoff',0xb0b28),('bone_burst',0xb0b40),('native_victim_park',0xb0b54),
            ('human_HK_binding',0xff270+17*4),('CPU_second_binding',0xf436c+17*4),('first_spacing',0xf395c+17*4)):
            wrong=bytearray(guest);wrong[at]^=1
            try:contract(bytes(wrong),bytes(previous),payload)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Actual source fault admitted: '+name)
        paths=[Path(__file__),accepted.OUT/'report.json',accepted.OUT/'executed_sources.json.gz',position.OUT/'report.json',
            ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedGuestByteDelta=sum(a!=b for a,b in zip(guest,previous)),
            previousGoalTurnClassification='progress: real button-history gate implemented/qualified and complete victim position helpers verified',
            sourceContract=result,controlUnitCases=cases,negativeFaultsRejected=faults,latestPlayableChanged=False,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            limitations=['Dependent native/component helpers modeled in control units; these are not gameplay.',
                'Actual first/second physical activation, CPU distance and every true victim pose/beam alignment require earned tests.',
                'Original audio cues/priority, white-flash fidelity and opaque source400 semantics remain unaccepted.',
                'Actual smoke/object/cache/palette clearance across winner/scene and full14+6 final acceptance remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope intact')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Only exact terminal temporary source probe retired');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],controlCases=len(cases),faults=len(faults),nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise


if __name__=='__main__':main()
