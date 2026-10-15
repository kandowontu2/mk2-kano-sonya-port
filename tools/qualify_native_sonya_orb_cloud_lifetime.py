"""Source-only native201 independent cloud lifetime successor.

The actual FF8204B0 exact100 delete killed all three cloud allocations at
age198 before their65field sequence could run its owned cleanup. Preserve
that runtime evidence and all compiled predecessors. No winner timing,
shortened art, broad scheduler changes, public promotion or guest writes.
"""
import gzip
import hashlib
import inspect
import json
import struct
import subprocess
import traceback
from pathlib import Path
import qualify_native_sonya_orb_palette as prior
import review_native_sonya_orb_palette_runtime as runtime

ROOT=prior.ROOT
STAGE=ROOT/'source_native_sonya_orb_cloud_lifetime'
OUT=ROOT/'audit_native_sonya_orb_cloud_lifetime_source'
need,sha,address=prior.need,prior.sha,prior.address
OLD='\tleg_movi(1,0x100); leg_movi(7,native_address(secondary_ash_task)); leg_call(0xff80e280);'
NEW='''\t// Native independent effect201 must finish its own13x5 sequence and
\t// object/palette/cache cleanup after winner deletes exact100 UI tasks.
\tleg_movi(1,0x201); leg_movi(7,native_address(secondary_ash_task)); leg_call(0xff80e280);'''

def compile_probe(code,base,payload,label):
    probe=OUT/(label+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
        '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Actual whole '+label+' initializer compiles warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/(label+'_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,bytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base) and not result.stderr,'Whole actual initialized '+label+' guest')
    return result.stdout,probe

def factory_model():
    effects=prior.prior.prior.prior.effects
    code=inspect.getsource(effects.factory_unit)
    old='''        elif op==0xbb20:
            source,destination=word(),word();put(regs[0]+destination,get(regs[1]+source))
'''
    new='''        elif op&0xfe00 in (0xb800,0xba00):
            source,destination=word(),word()
            src,dst,field=(op>>5)&15,op&15,(op>>9)&1
            put(regs[dst]+destination,get(regs[src]+source,field),field)
'''
    need(code.count(old)==code.count('get(job+0x20,0)==0x100')==1,'Preserved original factory and known corrected opcode boundary')
    namespace=dict(vars(effects))
    exec(compile(code.replace(old,new).replace('get(job+0x20,0)==0x100','get(job+0x20,0)==0x201'),
                 '<independent effect201 constructor successor>','exec'),namespace)
    return namespace['factory_unit']

def main():
    need(not OUT.exists() and not prior.prior.prior.prior.visual.native.census(),'Fresh evidence; native games actually terminal')
    OUT.mkdir();old_code=new_code=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text());review=json.loads((runtime.OUT/'report.json').read_text())
        need(receipt['passed'] and receipt['sourceOnlyAccepted'] and review['passed'] and review['evidenceReviewAccepted'] and
             not review['finisherAccepted'] and all(sha(p)==h for r in (receipt,review) for p,h in r['inputHashes'].items()),
             'Actual preserved palette/cursor source and earned mass-unlink failure evidence unchanged')
        old_source=(prior.STAGE/'midtunit_m.cpp').read_text();new_source=(STAGE/'midtunit_m.cpp').read_text()
        need(old_source.count(OLD)==1 and new_source==old_source.replace(OLD,NEW),'Only cloud process category changes; all timing/cleanup/art/cursors/winner/identity code conserved')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Host/platform/audio source byte-exact')
        old_code=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(old_code.count(OLD)==1,'Exactly the actual previously compiled initializer cloud constructor')
        new_code=old_code.replace(OLD,NEW)
        base=prior.prior.prior.prior.visual.prior.expected();payload=prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        old,old_probe=compile_probe(old_code,base,payload,'preserved_palette')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole prior built guest reconstructed unchanged')
        guest,probe=compile_probe(new_code,base,payload,'native_effect201')
        pattern=struct.pack('<HIHI',0x09e1,0x100,0x09e7,address(0xaef00))
        at=old.find(pattern,0xaee00,0xaef00)
        need(at>=0xaee00 and old.find(pattern,at+1,0xaef00)==-1,'Single exact cloud category/entry pair inside allocated constructor')
        modeled=bytearray(old);struct.pack_into('<I',modeled,at+2,0x201)
        need(guest==bytes(modeled) and sum(a!=b for a,b in zip(old,guest))==2,
             'Whole actual initialized guest differs by precisely two category-immediate bytes; every other opcode, data and art byte identical')
        factory=factory_model();factories=[factory(guest,e) for e in (0xae900,0xaed00)]
        try:factory(old,0xaed00)
        except ValueError as error:old_rejected=str(error)
        else:raise ValueError('Actually observed unsafe100 cloud guest admitted')
        motion,_=prior.prior.native_motion_units();motion_cases=motion(guest)
        parser=prior.prior.prior.unit_cases(guest);typed=prior.typed_unit(guest)
        streams=struct.unpack_from('<14I',guest,0xadf00)
        need(streams[-1]==0 and streams[:-1]==tuple(address(0xade40+i*12) for i in range(13)),
             'Original full13group cloud stream and terminator intact; no shortened animation')
        faults=[]
        for name,value in [('unsafe_ui100',0x100),('unsafe_ui101',0x101),('wrong_effect200',0x200)]:
            wrong=bytearray(guest);struct.pack_into('<I',wrong,at+2,value)
            try:factory(bytes(wrong),0xaed00)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Incorrect cloud category admitted: '+name)
        mk2=ROOT/'mk2/mk2-maincpu.bin';mk3=ROOT/'mk3/mk3-maincpu.bin'
        native=dict(dispatcher=runtime.decode(mk2,0xff9a5b00,0x180),compoundEffect=runtime.decode(mk2,0xff9ad600,0x180),
                    originalSonya=runtime.decode(mk3,0xff9aeec0,0x90))
        need(all('MOVI   201h,A1' in t for t in native.values()),'Same actual original and native MKII independent effect category')
        binary=OUT/'constructor.bin';binary.write_bytes(guest[0xaee00:0xaf090])
        decoded=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010','-basepc',hex(address(0xaee00)),'-norawbytes'],text=True,capture_output=True,check=True).stdout
        need('MOVI   201h,A1' in decoded and 'MOVI   FFD77800h,A7' in decoded and
             'CALLA  FF80E280h' in decoded and 'CALLA  FF840450h' in decoded and
             'CALLA  FF80E0E0h' in decoded,'Actual native decoder agrees on category, own entry and complete object/palette/cache cleanup')
        paths=[Path(__file__),Path(runtime.__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',runtime.OUT/'report.json',
            mk2,mk3,ROOT/'mame-mkp/unidasm.exe',*(STAGE/f for f in ('midtunit.cpp','midtunit.h','midtunit_m.cpp'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedByteDeltaFromPalette=2,
            initializedGuestByteDelta=sum(a!=b for a,b in zip(base,guest)),changedImmediateByteOffset=f'{at+2:X}',
            actualPriorGuestRejected=old_rejected,actualTypedFaultsRejected=faults,
            constructorUnitCases=factories,motionUnitCases=motion_cases,parserUnitCases=parser,typedPaletteUnit=typed,
            fullOriginalCloudGroups=13,fieldsPerGroup=5,cloudFields=65,independentNativeEffectCategory='0201',
            nativeEffectReferences=native,actualNativeDisassembly=decoded,
            originalNaturalIntegrationRequirements=review['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=review['originalRemainingWorkGroups'],goalStatus='active',
            previousGoalTurnClassification='no progress: status restatement only',
            thisGoalTurnClassification='progress: actual native deletion trace proves premature100 cloud kill; only cloud201 immediate corrected and independently whole-guest qualified',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Private new native build and physically earned P1/P2 animation/object/palette/cache lifetime checks still required.',
                'Runtime mask proof at gap256 does not accept long-distance worker lifetime, victim flash, audio, other victims or CPU.',
                'Kano laser and all remaining original integration/release requirements stay active.'])
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as f:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),f)
        for p in (old_probe,probe,binary):
            need(p.parent.resolve()==OUT.resolve(),'Only exact terminal generated probes/slice retired');p.unlink()
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],changedBytes=2,cloudFields=65,faults=len(faults))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as f:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),f)
        raise

if __name__=='__main__':main()
