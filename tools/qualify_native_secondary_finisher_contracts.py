"""Supersede the earlier coordinate-copy semantic checks, not their evidence.

The original emitted BB20 reads A9, not A1. Compile the real successor
initializer, decode all six replacements with the native disassembler and
execute them with source/destination/field extracted from the actual opcode.
Source-only: no gameplay, player input, audio or release acceptance.
"""
import gzip
import hashlib
import inspect
import json
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_secondary_finisher_effects as effects

motion, visual = effects.motion, effects.visual
ROOT = effects.ROOT
STAGE = ROOT/'source_native_secondary_finisher_contracts'
OUT = ROOT/'audit_native_secondary_finisher_contracts_source'
EFFECTS_PIN = '404B033DE792EA55C0B8AE4651981BEB349883C1637F5CF6403920CE4A4C68B9'
OLD = '0xbb20,0x0080,0x0080,0xbb20,0x00a0,0x00a0'
NEW = '0xba20,0x0080,0x0080,0xba20,0x00a0,0x00a0'
need, sha, address = effects.need, effects.sha, effects.address


def corrected_units():
    """Local successors; never rewrite or monkeypatch frozen accepted units."""
    old_cpu = '''            elif op==0xbb20:
                source_offset,destination_offset=word(),word()
                self.store(self.reg[0]+destination_offset,self.load(self.reg[1]+source_offset,1),1)
'''
    new_cpu = '''            elif op&0xfe00 in (0xb800,0xba00):
                source_offset,destination_offset=word(),word()
                src,dst,field=(op>>5)&15,op&15,(op>>9)&1
                self.store(self.reg[dst]+destination_offset,self.load(self.reg[src]+source_offset,field),field)
'''
    code = inspect.getsource(motion.CPU)
    need(code.count(old_cpu)==1, 'Exact preserved earlier motion-unit defect identified')
    namespace = dict(vars(motion))
    exec(compile(code.replace(old_cpu,new_cpu), '<corrected native coordinate CPU>', 'exec'), namespace)
    exec(compile(inspect.getsource(motion.unit_cases), '<unchanged motion cases>', 'exec'), namespace)
    old_factory = '''        elif op==0xbb20:
            source,destination=word(),word();put(regs[0]+destination,get(regs[1]+source))
'''
    new_factory = '''        elif op&0xfe00 in (0xb800,0xba00):
            source,destination=word(),word()
            src,dst,field=(op>>5)&15,op&15,(op>>9)&1
            put(regs[dst]+destination,get(regs[src]+source,field),field)
'''
    code = inspect.getsource(effects.factory_unit)
    need(code.count(old_factory)==1, 'Exact preserved earlier factory-unit defect identified')
    factory_namespace = dict(vars(effects))
    exec(compile(code.replace(old_factory,new_factory), '<corrected native factory CPU>', 'exec'), factory_namespace)
    return namespace['unit_cases'], factory_namespace['factory_unit']


def opcode_contract():
    source_root = ROOT/'mame-mkp/src/devices/cpu/tms34010'
    files = [source_root/leaf for leaf in ('tms34010.cpp','34010ops.hxx','34010dsm.cpp')]
    cpu, ops, decoder = [p.read_text() for p in files]
    need('#define SRCREG(O)       (((O) >> 5) & 0x0f)' in cpu and
         '#define DSTREG(O)       ((O) & 0x0f)' in cpu and
         'int32_t data = RFIELD##F(R##REG(SRCREG(op))+o1);' in ops and
         'WFIELD##F(R##REG(DSTREG(op))+o2,data);' in ops and
         "(op & 0x200) ? '1' : '0'" in decoder,
         'Real native CPU and disassembler specify source, destination, offset and field')
    need(((0xbb20>>5)&15)==9 and ((0xba20>>5)&15)==1 and
         (0xbb20&15)==(0xba20&15)==0 and ((0xba20>>9)&1)==1,
         'Old BB20 uses A9; corrected BA20 uses A1; both use A0 and 32-bit field1')
    return files


def compile_probe(code, base, payload, label):
    probe = OUT/(label+'_probe.exe')
    result = subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                             '-x','c++','-','-o',str(probe)], input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0, 'Actual '+label+' initializer compiled warning-free')
    result = subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/(label+'_native_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,
        stdoutBytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    (OUT/(label+'_initializer.stderr')).write_bytes(result.stderr)
    need(result.returncode==0 and len(result.stdout)==len(base), 'Actual '+label+' initializer emitted whole guest in RAM')
    return result.stdout, probe


def copy_cases(guest, offsets):
    cases = []
    for at in offsets:
        for x,y in ((315*65536+32768,102*65536+16384),
                    (-27*65536+12345,-9*65536+54321),
                    (485*65536+65535,150*65536+1), (0,0)):
            regs = [0]*16
            regs[0],regs[1],regs[9] = 0x4000,0x6000,0x9000
            memory = {regs[1]+0x80:x&0xffffffff,regs[1]+0xa0:y&0xffffffff,
                      regs[1]+0x140:0x0700,regs[1]+0x1f0:17,
                      regs[0]+0x80:0xcafef00d,regs[0]+0xa0:0xfacecafe,
                      regs[0]+0x140:0x0900,regs[0]+0x1f0:0x51,
                      regs[9]+0x80:0xbad00001,regs[9]+0xa0:0xbad00002}
            before = memory.copy()
            for offset in (at,at+6):
                op,source,destination = struct.unpack_from('<3H',guest,offset)
                need(op&0xfe00==0xba00, 'Real coordinate instruction is memory-to-memory field1')
                src,dst = (op>>5)&15,op&15
                memory[regs[dst]+destination] = memory[regs[src]+source]
            need(memory[regs[0]+0x80]==x&0xffffffff and memory[regs[0]+0xa0]==y&0xffffffff and
                 all(memory[p]==v for p,v in before.items() if p not in (0x4080,0x40a0)),
                 'Both full signed/fractional coordinates come from the true actor; every identity/palette/unrelated word conserved')
            cases.append(dict(byteOffset=f'{at:X}',x=x,y=y,sourceRegister=1,destinationRegister=0,
                              fractionalCoordinatesConserved=True,identityAndPaletteConserved=True))
    return cases


def main():
    need(not OUT.exists() and not visual.native.census(), 'Fresh contract evidence; no native game live')
    OUT.mkdir()
    old_harness = new_harness = ''
    try:
        receipt = json.loads((effects.OUT/'report.json').read_text())
        need(sha(effects.OUT/'report.json')==EFFECTS_PIN and receipt['passed'] and
             receipt['sourceOnlyAccepted'] and not receipt['nativeRuntimeAccepted'] and
             all(sha(p)==h for p,h in receipt['inputHashes'].items()), 'Every frozen effects proof/source input unchanged')
        old_source = (effects.STAGE/'midtunit_m.cpp').read_text()
        new_source = (STAGE/'midtunit_m.cpp').read_text()
        need(old_source.count(OLD)==new_source.count(NEW)==3 and
             new_source==old_source.replace(OLD,NEW), 'Only six reviewed coordinate-copy opcodes change')
        for leaf in ('midtunit.h','midtunit.cpp'):
            need(sha(STAGE/leaf)==sha(effects.STAGE/leaf), 'Platform/host code unchanged')
        native_sources = opcode_contract()
        executed = json.loads(gzip.open(effects.OUT/'executed_sources.json.gz','rt').read())
        old_harness = executed['actualNewInitializerHarness']
        need(old_harness.count(OLD)==3, 'Actual executed old initializer contains exactly the six defective instructions')
        new_harness = old_harness.replace(OLD,NEW)
        base = visual.prior.expected()
        payload = effects.PAYLOAD.read_bytes()
        old,old_probe = compile_probe(old_harness,base,payload,'preserved')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['expectedGuestSHA256'], 'Re-executed exact preserved effects guest')
        guest,new_probe = compile_probe(new_harness,base,payload,'corrected')
        expected = bytearray(old)
        offsets = []
        pattern = struct.pack('<6H',0xbb20,0x80,0x80,0xbb20,0xa0,0xa0)
        for first,last in ((0xad680,0xad780),(0xada40,0xadb40),(0xaee00,0xaef00)):
            at = old.find(pattern,first,last)
            need(at>=first and old.find(pattern,at+1,last)==-1, 'Exactly one complete coordinate pair in each native helper')
            offsets.append(at)
            for delta in (0,6):struct.pack_into('<H',expected,at+delta,0xba20)
        need(guest==bytes(expected) and sum(a!=b for a,b in zip(old,guest))==6,
             'Whole actual successor differs by exactly six source-register bytes; all other program/data conserved')
        motion_units,factory_unit = corrected_units()
        old_failures = []
        for name,call in (('old_motion',lambda:motion_units(old)),
                          ('old_cloud_factory',lambda:factory_unit(old,0xaed00)),
                          ('old_coordinate_copies',lambda:copy_cases(old,offsets))):
            try:call()
            except (ValueError,KeyError) as error:old_failures.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Earlier incorrect source unexpectedly admitted by corrected CPU semantics: '+name)
        motion_cases = motion_units(guest)
        factories = [factory_unit(guest,entry) for entry in (0xae900,0xaed00)]
        coordinates = copy_cases(guest,offsets)
        faults = []
        for at in offsets:
            for delta in (0,6):
                wrong = bytearray(guest)
                struct.pack_into('<H',wrong,at+delta,0xbb20)
                try:copy_cases(bytes(wrong),offsets)
                except ValueError as error:faults.append(dict(byteOffset=f'{at+delta:X}',rejected=str(error)))
                else:raise ValueError('Wrong actual source-register opcode admitted')
        binary = OUT/'decoded_coordinate_helpers.bin'
        binary.write_bytes(guest[0xad680:effects.LAST])
        result = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                                 '-basepc',hex(address(0xad680)),'-norawbytes'],text=True,capture_output=True,check=True)
        lines = {int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in result.stdout.splitlines()}
        decoded = {}
        for at in offsets:
            for delta,field in ((0,0x80),(6,0xa0)):
                pc = address(at+delta)
                need(lines[pc]==f'MOVE   *A1({field:X}h),*A0({field:X}h),1', 'Actual native disassembler agrees on every repaired register/field')
                decoded[f'{pc:08X}'] = lines[pc]
        scope = receipt
        paths = [Path(__file__),effects.OUT/'report.json',effects.OUT/'executed_sources.json.gz',
                 ROOT/'tools/qualify_native_secondary_finisher_effects.py',
                 ROOT/'tools/qualify_native_secondary_finisher_motion.py',ROOT/'mame-mkp/unidasm.exe',
                 *native_sources,*(STAGE/leaf for leaf in visual.SOURCE_PINS)]
        report = dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            expectedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
            initializedByteDeltaFromEffects=6,initializedByteDeltaFromPlayable=sum(a!=b for a,b in zip(base,guest)),
            defect='Earlier BB20 unit handlers incorrectly modeled source A1; actual native CPU uses A9.',
            supersededSemanticAcceptance=[str(motion.OUT/'report.json'),str(effects.OUT/'report.json')],
            knownIncorrectPriorGuestsRejected=old_failures,decodedCoordinateCopies=decoded,
            coordinateUnitCases=coordinates,motionUnitCases=motion_cases,constructorUnitCases=factories,
            faultRejections=faults,inputHashes={str(p.resolve()):sha(p) for p in paths},
            previousGoalTurnClassification='no progress: user-requested status inspection/restatement only',
            thisGoalTurnClassification='progress: corrected six actual pointer-copy opcodes; actual native decoder/CPU semantics reject previous bad motion/cloud guests; source-only successor passes',
            originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],goalStatus='active',
            gameBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Native allocation/render/physics/sound/cleanup still require actual earned-action game tests.',
                         'No new input/CPU activation or audio; no second-fatality runtime acceptance.',
                         'True victim animation35/5 ownership must still be qualified for the whole roster.',
                         'Full original integration, campaign/stage/audio regression and finished ZIP remain.'],
            nextAction='Qualify true-victim animation streams and worker handoff, bind the distinct Sonya action in a private successor, build and physically earn/test it; finish Kano laser and the full original scope.')
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6, 'Full goal scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        for temporary in (old_probe,new_probe,binary):
            need(temporary.parent.resolve()==OUT.resolve(), 'Exact generated test artifacts only')
            temporary.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,
                              repairedOpcodeBytes=6,rejectedIncorrectPriorGuests=len(old_failures),
                              coordinateCases=len(coordinates),motionCases=len(motion_cases),
                              constructorCases=len(factories),faults=len(faults))))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False,failure=traceback.format_exc(),nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(files={str(p.resolve()):dict(sha256=sha(p),text=p.read_text())
                                 for p in (Path(__file__),*(STAGE/leaf for leaf in visual.SOURCE_PINS))},
                           actualOldInitializerHarness=old_harness,actualNewInitializerHarness=new_harness),stream)


if __name__=='__main__':main()
