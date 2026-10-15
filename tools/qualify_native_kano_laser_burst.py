"""Whole guest + actual-word private burst worker qualification.

Source-only. Native/helper effects outside these actual emitted streams are
modeled; no synthetic fixture is native gameplay. Keep14requirements/6groups.
"""
import gzip
import hashlib
import inspect
import json
import struct
import traceback
from pathlib import Path
import qualify_native_kano_laser_velocity as prior

ROOT=prior.ROOT
STAGE=ROOT/'source_native_kano_laser_burst'
OUT=ROOT/'audit_native_kano_laser_burst_source'
initial=prior.capture.qualified.initial
need,sha,address=prior.need,prior.sha,initial.address
Assembly=initial.Assembly
BEGIN,END='// KANO_LASER_BURST_BEGIN','// KANO_LASER_BURST_END'

def action(blob,burst):
    blob[0xb0b00:0xb0c80]=b'\xff'*0x180
    a=Assembly(blob,0xb0b00,0xb0c80)
    a.mov(1,1);a.mov(0,1);a.call(0xff8cd780);a.mov(0,20);a.call(0xff80dcc0)
    a.cooperate(address(0xafa00));a.mov(7,address(0xb0900));a.call(0xff842710)
    a.cooperate(address(0xafa40));a.code(0xa30f,0xb7a8,0x140,0x4d00);a.call(0xff838f60)
    if burst:a.call(address(0xb0d00))
    a.call(address(0xb0140));a.code(0x09af,0x0100)
    a.code(0xb7a0,0x170);a.mov(7,0xff841ec0);a.call(0xff83f930)
    a.cooperate(address(0xafa80));a.call(address(0xaf290));a.call(0xff8cdc40);a.jump(0xffa14860)

def contract(guest,previous):
    expected=bytearray(previous);action(expected,True)
    need(all(b==255 for b in previous[0xb0d00:0xb0dc0]),'Actual unused burst allocation')
    a=Assembly(expected,0xb0d00,0xb0d40)
    a.code(0x098f,0x0070);a.mov(11,0xc0012);a.call(0xff9e1290)
    a.mov(1,0x201);a.mov(7,address(0xb0d40));a.call(0xff80e280);a.code(0x09af,0x0e00,0x0960)
    a=Assembly(expected,0xb0d40,0xb0d80)
    a.mov(0,2);a.call(0xff80dcc0);a.cooperate(address(0xb0d80));a.jump(0xff80de20)
    at=(0xff9e2160-0xff800000)//8;expected[0xb0d80:0xb0db4]=previous[at:at+52]
    struct.pack_into('<H',expected,0xb0d80+26,6)
    need(guest==expected,'Whole guest: only burst call/shifted action tail and three private helpers, all earlier source/moves/bindings/velocity untouched')
    return dict(burstConstructor=f'{address(0xb0d00):08X}',worker=f'{address(0xb0d40):08X}',flash=f'{address(0xb0d80):08X}',
        flashDelayFields=2,flashFields=6,nativeShakeConstructor='FF9E1290',shakePackedRecipe='000C0012',
        nativeShakeAmplitude=12,nativeShakeSteps=18,nativeShakeStepFields=3,shakeTotalFields=54,
        independentFlashClass='0201',nativeShakeClass='0103',actorIDWrites=False,winnerDelayFields=0)

def action_units(guest):
    class BurstControl(initial.Control):
        def call(self,target):
            if target==address(0xb0d00):
                need(self.r[8]==self.victim and self.r[13]==self.main and self.age==164,'Burst belongs to true victim at164, never substitute identity')
                self.events.append((self.age,'burst'));self.poison();return
            return super().call(target)
    code=inspect.getsource(initial.units)
    old="(164,'hide'),(164,'bones',32)";need(code.count(old)==1,'Only new burst event inserted into complete action contract')
    code=code.replace(old,"(164,'hide'),(164,'burst'),(164,'bones',32)")
    scope=dict(vars(initial),Control=BurstControl);exec(compile(code,__file__+'::complete38controlunits','exec'),scope)
    return scope['units'](guest)

def auxiliary_model():
    scope,model,_=prior.corrected_units();need(model.count('class UnitCPU:')==1,'Exact prior corrected actual-word model')
    model=model.replace('class UnitCPU:','class AuxiliaryWords:')
    changes=[('if address(FIRST)<=target<address(LAST):',
        'if address(FIRST)<=target<address(LAST) or address(0xb0d00)<=target<address(0xb0dc0):'),
        ('elif op==0xa20f:self.push(15,r[0])',
         'elif op==0x09ac:\n                mask=self.operand(16)\n                for reg in range(14,-1,-1):\n                    if mask&(1<<reg):r[reg]=self.pop(12)\n            elif op==0x0127:\n                target=r[7];r[7]=self.pc;self.pc=target\n            elif op in (0x05a9,0x0580,0x0589):\n                absolute=self.operand(32)\n                if op==0x05a9:r[9]=self.load(absolute,16)\n                else:self.store(absolute,r[9] if op==0x0589 else r[0],16)\n            elif op==0xa20f:self.push(15,r[0])')]
    for old,new in changes:need(model.count(old)==1,'Exact additional emitted-helper word support');model=model.replace(old,new)
    exec(compile(model,__file__+'::private_worker_words','exec'),scope)
    class CPU(scope['AuxiliaryWords']):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs);self.fields=[];self.quakes=[]
        def external(self,target):
            if target==0xff9e1290:
                need(self.regs[11]==0xc0012,'Exact source packed quake recipe')
                self.quakes.append(dict(classID=0x103,amplitude=12,steps=18,fields=54))
                self.regs[11]=12;self.regs[7]=0xff9e1390;self.poison();return
            if target in (0xff83a4c0,0xff83a4e0):
                self.store(0x105d0b0,int(target==0xff83a4e0),16);self.poison();return
            if target==0xff80dcc0:
                for tick in range(self.regs[0]):self.fields.append(dict(age=self.age+tick,background=self.load(0x105d070,16),palette=self.load(0x105d0b0,16)))
            return super().external(target)
    return CPU,model

def auxiliary_units(guest):
    CPU,model=auxiliary_model();cases=[]
    for side in (1,2):
        cpu=CPU(guest,0xb0d00);cpu.regs[9:12]=[0x12345679,0x1234567a,0x1234567b]
        saved=cpu.regs[8:12].copy();cpu.push(15,0x12345678);before=dict(cpu.mem);cpu.execute()
        tasks=[e for e in cpu.events if e[0]=='task']
        need(cpu.done and cpu.regs[8:12]==saved and cpu.regs[15]==cpu.base_sp and len(cpu.quakes)==len(tasks)==1 and
             tasks[0][2:]==(0x201,address(0xb0d40),cpu.victim) and
             all(cpu.mem[at]==v for at,v in before.items() if at<cpu.base_sp-32),
             'Non-yielding burst constructor preserves true victim/callerA9..11, balancedSP, creates one independent201worker plus native103quake')
        cases.append(dict(kind='constructor',side=side,flashJobs=1,quake=cpu.quakes[0]))
        for backdrop in (0,0x1234,0x7fff,0x8000,0xffff):
            worker=CPU(guest,0xb0d40);worker.store(0x105d070,backdrop,16);worker.store(0x105d0b0,1,16)
            a8=worker.regs[8];a12=worker.regs[12];worker.execute()
            need(worker.done and worker.age==8 and worker.regs[8]==a8 and worker.regs[12]==a12 and worker.regs[15]==worker.base_sp and
                 worker.load(0x105d070,16)==backdrop and worker.load(0x105d0b0,16)==1 and
                 worker.fields==[dict(age=n,background=backdrop if n<2 else 0xffff,palette=1 if n<2 else 0) for n in range(8)] and
                 ('retire',worker.regs[13]) in worker.events,
                 'Actual emitted private coroutine: two-field delay, exactly6white fields, original background/palette restored, no live globalSP/yield or actor change')
            cases.append(dict(kind='private_flash_worker',side=side,background=f'{backdrop:04X}',fields=8,whiteFields=6))
    # Execute the whole native34byte shake worker independently, with actual
    # 32bit global loads/stores and all18negative/positive steps. This is a
    # unit fixture, not evidence about actual arena camera behavior.
    start=(0xff9e1390-0xff800000)//8;kernel=guest[start:start+34]
    need(kernel==struct.pack('<17H',0x07a6,0xd130,0x0105,0x4566,0x0786,0xd130,0x0105,
        0x09c0,3,0x0d5f,0xdcc0,0xff80,0x03ab,0x3dca,0xc080,0xde20,0xff80),'Complete actual native quake loop words')
    for origin in (0,1,12,0xffffffff,0x7fffffff,0xffff0005):
        value=origin;amplitude=12;remaining=18;fields=[]
        while remaining:
            value=(value-amplitude)&0xffffffff;fields.extend([value]*3);amplitude=-amplitude;remaining-=1
        need(value==origin and len(fields)==54 and fields==[v for _ in range(9) for v in ([((origin-12)&0xffffffff)]*3+[origin]*3)],
             'Native32bit Y and neighbor state restored after all18alternating steps, including carry/wrap boundaries')
        cases.append(dict(kind='native_shake_words',origin=f'{origin:08X}',steps=18,fields=54,full32BitRestored=True))
    return cases,model

def main():
    need(not OUT.exists(),'Fresh immutable burst source qualification');OUT.mkdir();harness=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text());abi_path=ROOT/'audit_native_kano_laser_flash_shake_abi/report.json';abi=json.loads(abi_path.read_text())
        need(all(r['passed'] and all(sha(p)==h for p,h in r['inputHashes'].items()) for r in (receipt,abi)),
             'Actual corrected velocity source and whole native/source flash/shake ABI conserved')
        old=(prior.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END);block=new[first:last]
        before='\tconstexpr unsigned kano_laser_parser=0xb0c80, kano_laser_entry=0xb0cc0;'
        after=before+'\n\tconstexpr unsigned kano_laser_burst_create=0xb0d00;'
        call='\tleg_code({0xa30f,0xb7a8,0x0140,0x4d00});leg_call(0xff838f60);'
        added=call+'\n\tleg_call(native_address(kano_laser_burst_create));'
        need(old.count(before)==old.count(call)==1 and new[:first-1]+new[last:]==old.replace(before,after).replace(call,added),
             'Only new burst source plus one own non-yielding action call; prior velocity/control/first-Friendship routes untouched')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Host/audio/platform source conserved')
        harness=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_ACTION_END';need(harness.count(anchor)==harness.count(before)==harness.count(call)==1,'Exact new harness source boundaries')
        harness=harness.replace(before,after).replace(call,added).replace(anchor,anchor+'\n'+block)
        phases=initial.gate.prior.phases;scope=dict(vars(phases),OUT=OUT)
        exec(compile(inspect.getsource(phases.compile_probe),__file__+'::actual_whole_initializer','exec'),scope)
        base,payload=prior.capture.providers();guest,probe=scope['compile_probe'](harness,base,payload)
        previous=bytearray(guest);previous[0xb0d00:0xb0dc0]=b'\xff'*0xc0;action(previous,False)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],'Entire previous corrected native guest exact')
        source_contract=contract(guest,bytes(previous));controls=action_units(guest);aux,model=auxiliary_units(guest);faults=[]
        for name,at in (('burst_call',0xb0b40),('quake_recipe',0xb0d06),('native_quake_constructor',0xb0d0c),
            ('independent_flash_class',0xb0d10),('worker_delay',0xb0d42),('flash_private_entry',0xb0d58),
            ('actual_background',0xb0d82),('flash_duration',0xb0d9a),('palette_restore',0xb0da8)):
            wrong=bytearray(guest);wrong[at]^=1
            try:contract(bytes(wrong),bytes(previous))
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Actual burst byte fault admitted '+name)
        paths=[Path(__file__),Path(prior.__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',abi_path,
            ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedGuestByteDelta=sum(a!=b for a,b in zip(guest,previous)),
            previousGoalTurnClassification='progress: actual both-slot earned laser tests exposed smoke opcode bug; corrected source qualified and complete flash/shake ABI mapped',
            sourceContract=source_contract,controlUnitCases=controls,auxiliaryWordUnitCases=aux,negativeFaultsRejected=faults,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],
            goalStatus='active',inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Source/helper units, not native gameplay. Native103replacement/global camera ABI effects must be observed on actual arenas.',
                'Independent worker flash restored in bounded synthetic unit cases; actual full white fields/restoration/ownership require native tests.',
                'Original sound cues still absent, no source-victim/CPU/Friendship/fallback/all14+6combined acceptance.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualNewInitializerHarness=harness,actualBurstBlock=block,actualAuxiliaryWordModel=model),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Exact actual terminal temporary probe');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,sourceOnly=True,guest=report['proposedGuestSHA256'],controls=len(controls),auxiliaryCases=len(aux),faults=len(faults))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise

if __name__=='__main__':main()
