"""Fix actual earned-test velocity failure, not its acceptance threshold.

Actual TMS opcode table:0B00=ADDI.W(sign-extended16),0B20=ADDI.L(32).
Original FF9590D0 is RNG,DEC,ADD A1. Keep the exact source1..4px range;
change one emitted opcode byte, strengthen the prior synthetic model.
No new game build, ROM copy, raw media or public launcher change.
"""
import gzip
import hashlib
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
import capture_native_kano_laser_action as capture
import qualify_native_kano_laser_emitters as emitters

ROOT=capture.ROOT
STAGE=ROOT/'source_native_kano_laser_velocity'
OUT=ROOT/'audit_native_kano_laser_velocity_source'
need,sha=capture.need,capture.sha

def corrected_units():
    model=inspect.getsource(emitters.UnitCPU)
    replacements=[('elif op==0xa2ec:self.push(12,r[7])','elif op==0xa20f:self.push(15,r[0])\n            elif op==0xa2ec:self.push(12,r[7])'),
        ('self.next_job=0x20000;self.next_actor=0x40000',"self.next_job=0x90000;self.next_actor=0x40000\n        need(self.next_job>self.base_sp and self.victim<self.next_actor<self.base_sp,'Disjoint synthetic pools')"),
        ('elif op==0x0b00:r[0]=(r[0]+self.operand(32))&0xffffffff;self.flags(r[0])',
         'elif op==0x0b20:r[0]=(r[0]+self.operand(32))&0xffffffff;self.flags(r[0])\n            elif op==0x0b00:\n                immediate=self.operand(16);immediate=immediate-0x10000 if immediate&0x8000 else immediate\n                r[0]=(r[0]+immediate)&0xffffffff;self.flags(r[0])')]
    for old,new in replacements:need(model.count(old)==1,'Exact actual unit-model fix');model=model.replace(old,new)
    units=inspect.getsource(emitters.inspect_units)
    old='cpu.load(actor+0xc0,32)==0x51';need(units.count(old)==1,'Keep native class WORD/depth WORD fix')
    units=units.replace(old,'cpu.load(actor+0xc0,16)==0x51 and cpu.load(actor+0xd0,16)==1')
    scope=dict(vars(emitters));exec(compile(model,__file__+'::actual_tms_immediate_widths','exec'),scope)
    exec(compile(units,__file__+'::all_particle_bone_units','exec'),scope)
    return scope,model,units

def main():
    need(not OUT.exists(),'Fresh immutable velocity-source correction');OUT.mkdir();harness=''
    try:
        guard_path=capture.qualified.OUT/'report.json';guard=json.loads(guard_path.read_text())
        need(guard['passed'] and all(sha(p)==h for p,h in guard['inputHashes'].items()),'Entire actual prior source conserved')
        failure=ROOT/'audit_native_kano_laser_typed_epochs_review/failure.txt'
        need('Actual grey particle X/Y source velocity ranges' in failure.read_text(),'Actual stricter native runtime checker failure retained')
        old=(capture.qualified.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        before='\tleg_code({0x0b00,0xffff,0x0000,0x03a0,0xb20a,0x0060});'
        after='\t// ADDI.L is0B20.0B00 is ADDI.W: FFFF becomes-1 and the next\n\t// 0000 word is an illegal instruction, not the high half of an immediate.\n\t// The original range helper is random-1+10000h, hence add0000FFFFh.\n\tleg_code({0x0b20,0xffff,0x0000,0x03a0,0xb20a,0x0060});'
        need(old.count(before)==1 and old.replace(before,after)==new,'Only real incorrect smoke opcode plus its explanatory comment changed')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(capture.qualified.STAGE/leaf),'Host/audio/platform source untouched')
        evidence=[];failed_native=[]
        for side in (1,2):
            folder=ROOT/f'audit_native_kano_laser_typed_epochs_p{side}';report=json.loads((folder/'report.json').read_text())
            need(report['passed'] and report['transportOnlyAccepted'] and report['nativeExit']==0 and report['wholeGuestMatched'] and
                 all(sha(p)==h for p,h in report['inputHashes'].items()),'Same actual old native trial terminal and all source/input hashes conserved')
            text=gzip.open(folder/'run.log.gz','rt').read();fields=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
                if line.startswith('MK2_LASER_EFFECT_FIELD ') and 'kind=particle ' in line]
            signed=lambda value:int(value,16)-(0x100000000 if int(value,16)&0x80000000 else 0)
            bad=[r for r in fields if not -0x3ffff<=signed(r['vy'])<=-0x10000]
            need(bad and max(signed(r['vy']) for r in fields)>-0x10000,'Actual source velocity bug reproduced, not merely observer pointer reuse')
            failed_native.append(dict(side=side,outOfSourceRangeFields=len(bad),outOfSourceRangeEpochs=len({r['epoch'] for r in bad}),
                observedMinY=signed(min(fields,key=lambda r:signed(r['vy']))['vy']),observedMaxY=signed(max(fields,key=lambda r:signed(r['vy']))['vy']),firstActualBadField=bad[0]))
            evidence.extend([folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz'])
        table=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010tbl.hxx';ops=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
        t=table.read_text();o=ops.read_text()
        need('// 0x0b00\n\t&tms34010_device::addi_w_a,   &tms34010_device::addi_w_b,   &tms34010_device::addi_l_a' in t and
             'int32_t a = PARAM_WORD();' in o and 'int32_t a = PARAM_LONG();' in o,'Actual native CPU table/implementation independently distinguish short/long operands')
        native=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();at=(0xff9590d0-0xff800000)//8
        need(native[at:at+10]==struct.pack('<5H',0x0d5f,0x7780,0xff92,0x1420,0x4020),'Actual source range helper RNG,DEC,ADD A1 boundary')
        harness=json.loads(gzip.open(capture.qualified.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(harness.count(before)==1,'Exact actual initialized-guest harness correction');harness=harness.replace(before,after)
        phases=capture.qualified.initial.gate.prior.phases;scope=dict(vars(phases),OUT=OUT)
        exec(compile(inspect.getsource(phases.compile_probe),__file__+'::compile_whole_guest','exec'),scope)
        base,payload=capture.providers();guest,probe=scope['compile_probe'](harness,base,payload)
        pattern=struct.pack('<6H',0x0b20,0xffff,0,0x03a0,0xb20a,0x60);positions=[i for i in range(0xafe80,0xb00c0) if guest[i:i+len(pattern)]==pattern]
        need(len(positions)==1,'One real emitted legal long-immediate instruction');offset=positions[0]
        previous=bytearray(guest);previous[offset]^=0x20
        need(hashlib.sha256(previous).hexdigest().upper()==guard['proposedGuestSHA256'],
             'Every prior guest byte conserved except one actual incorrect immediate-width opcode byte')
        unit_scope,model,unit_source=corrected_units();prior_emitters=bytes(previous);cases=unit_scope['inspect_units'](guest,guest,(ROOT/'mk2/mk2-maincpu.bin').read_bytes())
        try:unit_scope['inspect_units'](prior_emitters,prior_emitters,(ROOT/'mk2/mk2-maincpu.bin').read_bytes())
        except ValueError as error:rejected=str(error)
        else:raise ValueError('Old actual incorrect short-immediate byte admitted by corrected unit model')
        boundary=[]
        for opcode,words,initial_value,want,consumed in ((0x0b00,(0xffff,),0x12345678,0x12345677,4),
            (0x0b20,(0xffff,0),0x12345678,0x12355677,6)):
            blob=bytearray(guest);blob[0xafe80:0xafe80+16]=struct.pack('<'+str(len(words)+2)+'H',opcode,*words,0x0960)+bytes(16-(len(words)+2)*2)
            cpu=unit_scope['UnitCPU'](bytes(blob),0xafe80);cpu.regs[0]=initial_value;cpu.execute()
            need(cpu.done and cpu.regs[0]==want and cpu.pc==emitters.address(0xafe80+consumed+2),'Actual ADDI.W signed16 versus ADDI.L full32 unit instruction boundaries')
            boundary.append(dict(opcode=f'{opcode:04X}',immediateWords=list(words),result=f'{cpu.regs[0]:08X}',instructionBytes=consumed))
        paths=[Path(__file__),Path(emitters.__file__),Path(capture.__file__),guard_path,failure,ROOT/'tools/review_native_kano_laser_typed_epochs.py',table,ops,
            ROOT/'mk3/mk3-maincpu.bin',ROOT/'mk2/mk2-maincpu.bin',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*evidence,*(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedGuestByteDelta=1,correctedOpcodeByteOffset=offset,
            correctInstruction='ADDI.L 0000FFFFh,A0',oldIncorrectInstruction='ADDI.W FFFFh,A0; illegal0000word',
            actualNativeVelocityFailures=failed_native,oldOpcodeRejected=rejected,emittedWordUnitCases=cases,actualImmediateWidthUnits=boundary,
            exactSourceYRange=[-0x3ffff,-0x10000],previousGoalTurnClassification='progress: first private native action built and physical trial captured',
            originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Corrected source is not yet a native game build; old private candidate still has the demonstrated velocity bug.',
                'All actual old native captures and failed stricter checker retained, never relabeled full gameplay acceptance.',
                'Source/helper units are not native gameplay; both slots, audio/flash/victim/CPU/scene/full14+6acceptance remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope intact')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualNewInitializerHarness=harness,correctedUnitModel=model,correctedUnitContract=unit_source),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Only exact terminal temporary compiler probe');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,sourceOnly=True,guest=report['proposedGuestSHA256'],guestDelta=1,units=len(cases),oldOpcodeRejected=True)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualInitializerHarness=harness),stream)
        raise

if __name__=='__main__':main()
