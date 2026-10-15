"""Only independent orb worker100->201, from actual304pixel failure.

Cloud native13x5 cleanup is already physically proven in both slots. The
longer orb must finish its own choreography, not force-hide or delay the
winner. Preserve actual native failure and every previous compiled input.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import traceback
from pathlib import Path
import qualify_native_sonya_orb_cloud_lifetime as prior
import review_native_sonya_orb_cloud_lifetime_runtime as runtime

ROOT=prior.ROOT
STAGE=ROOT/'source_native_sonya_orb_worker_lifetime'
OUT=ROOT/'audit_native_sonya_orb_worker_lifetime_source'
need,sha,address=prior.need,prior.sha,prior.address
OLD='\tleg_movi(1,0x100); leg_movi(7,native_address(secondary_sonya_worker)); leg_call(0xff80e280);'
NEW='''\t// At longer legal distances the orb outlives the native winner handoff.
\t// Preserve its complete travel/wrap/retire and sole owned cleanup as201.
\tleg_movi(1,0x201); leg_movi(7,native_address(secondary_sonya_worker)); leg_call(0xff80e280);'''

def compile_probe(code,base,payload,label):
    probe=OUT/(label+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
        '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Whole '+label+' initializer compiled warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/(label+'_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,bytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base) and not result.stderr,'Entire actual '+label+' guest')
    return result.stdout,probe

def birth_contract(guest,at):
    regs=[0]*16;regs[8]=0x01034e90;regs[13]=0x0106a370
    parent=regs[13];worker=0x01069c80
    original={0x140:0x010350a0,0x170:0x0106b150,0x190:0x0102fc10}
    memory={parent+k:v for k,v in original.items()};created=False;pc=at
    for step in range(12):
        op=struct.unpack_from('<H',guest,pc)[0];pc+=2
        def word():
            nonlocal pc
            v=struct.unpack_from('<H',guest,pc)[0];pc+=2;return v
        def longword():return word()|(word()<<16)
        if 0x09e0<=op<=0x09ef:regs[op&15]=longword()
        elif op==0x0d5f:
            need(longword()==0xff80e280 and not created and regs[1]==0x201 and regs[7]==address(0xaf090),
                 'One ordinary native independent201 worker birth, exact own entry')
            created=True;regs[0]=worker
            memory[worker+0x20]=regs[1];memory[worker+0x30]=1
            for r in range(7,13):memory[worker+0x100-(r-6)*0x20]=worker+0x6f0 if r==12 else regs[r]
        elif op==0xbba0:
            src,dst=word(),word();need(created and src==dst and src in original,'Only true victim/child process fields transferred')
            memory[regs[0]+dst]=memory[regs[13]+src]
        elif op==0xb22d:
            need(word()==0x190 and regs[1]==0 and created,'Only parent child ownership cleared after native transfer')
            memory[parent+0x190]=0;break
        else:raise ValueError(f'Unexpected actual worker birth opcode {op:04X}')
    need(created and memory[worker+0xc0]==regs[8] and memory[worker+0x40]==worker+0x6f0 and
         all(memory[worker+k]==v for k,v in original.items()) and
         all(memory[parent+k]==v for k,v in original.items() if k!=0x190) and memory[parent+0x190]==0,
         'Exact performer, native private stack and sole child/victim ownership; no identity/health/history writes')
    return dict(nativeCategory='0201',workerEntry=f'{address(0xaf090):08X}',newTask=f'{worker:08X}',
                truePerformer=f'{regs[8]:08X}',nativePrivateStack=f'{worker+0x6f0:08X}',
                victimAndChildTransferred={f'{k:X}':f'{v:08X}' for k,v in original.items()},soleChildOwnership=True)

def main():
    need(not OUT.exists() and not prior.prior.prior.prior.prior.visual.native.census(),'Fresh successor; all native game handles terminal')
    OUT.mkdir();old_code=new_code=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text());review=json.loads((runtime.OUT/'report.json').read_text())
        need(receipt['passed'] and review['passed'] and review['nativeFiniteCloudLifetimeAccepted'] and not review['finisherAccepted'] and
             all(sha(p)==h for r in (receipt,review) for p,h in r['inputHashes'].items()),'Actual cloud acceptance and physically earned304worker mass-delete failure conserved')
        old_source=(prior.STAGE/'midtunit_m.cpp').read_text();new_source=(STAGE/'midtunit_m.cpp').read_text()
        need(old_source.count(OLD)==1 and new_source==old_source.replace(OLD,NEW),'Only worker category changes, never shortened sequence, moved winner or narrowed range')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Host/platform/audio byte-exact')
        old_code=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(old_code.count(OLD)==1,'Exact actually compiled worker constructor anchor')
        new_code=old_code.replace(OLD,NEW)
        base=prior.prior.prior.prior.prior.visual.prior.expected();payload=prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        old,old_probe=compile_probe(old_code,base,payload,'preserved_cloud')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole prior native built cloud guest conserved')
        guest,probe=compile_probe(new_code,base,payload,'independent_worker201')
        pattern=struct.pack('<HIHI',0x09e1,0x100,0x09e7,address(0xaf090))
        at=old.find(pattern,0xaf000,0xaf090)
        need(at>=0xaf000 and old.find(pattern,at+1,0xaf090)==-1,'Unique own worker category/entry immediate pair')
        expected=bytearray(old);struct.pack_into('<I',expected,at+2,0x201)
        need(guest==bytes(expected) and sum(a!=b for a,b in zip(old,guest))==2,'Entire actual initialized guest changes only two worker-category bytes')
        birth=birth_contract(guest,at);faults=[]
        for name,offset in [('old_unsafe100',at+2),('wrong_worker_entry',at+8),('wrong_child_transfer',at+12+6+12+2)]:
            wrong=bytearray(guest);wrong[offset]^=1
            try:birth_contract(bytes(wrong),at)
            except (ValueError,KeyError,struct.error) as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Wrong actual worker constructor admitted: '+name)
        try:birth_contract(old,at)
        except ValueError as error:old_rejected=str(error)
        else:raise ValueError('Actual failing100worker guest admitted')
        factory=prior.factory_model();factories=[factory(guest,e) for e in (0xae900,0xaed00)]
        motion,_=prior.prior.prior.native_motion_units();motion_cases=motion(guest)
        parser=prior.prior.prior.prior.unit_cases(guest);typed=prior.prior.typed_unit(guest)
        binary=OUT/'worker_birth.bin';binary.write_bytes(guest[0xaf000:0xaf090])
        decoded=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010','-basepc',hex(address(0xaf000)),'-norawbytes'],text=True,capture_output=True,check=True).stdout
        need('MOVI   201h,A1' in decoded and 'MOVI   FFD78480h,A7' in decoded and
             'MOVE   *A13(190h),*A0(190h),1' in decoded and 'MOVI   90h,A0' in decoded and
             'CALLA  FF8CDC40h' in decoded and 'JA     FFA14860h' in decoded,
             'Native decoder confirms independent birth, sole ownership and identical144field normal winner continuation')
        paths=[Path(__file__),Path(runtime.__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',runtime.OUT/'report.json',
            ROOT/'audit_native_sonya_orb_victim_palette_role/report.json',*(STAGE/f for f in ('midtunit.cpp','midtunit.h','midtunit_m.cpp'))]
        result=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedByteDeltaFromCloudLifetime=2,
            initializedGuestByteDelta=sum(a!=b for a,b in zip(base,guest)),changedImmediateByteOffset=f'{at+2:X}',
            workerBirthUnit=birth,actualOldUnsafeGuestRejected=old_rejected,actualTypedFaultsRejected=faults,
            constructorUnitCases=factories,motionUnitCases=motion_cases,parserUnitCases=parser,typedPaletteUnit=typed,
            independentNativeWorkerCategory='0201',winnerTimingChanged=False,choreographyTruncated=False,
            actualNativeDisassembly=decoded,originalNaturalIntegrationRequirements=review['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=review['originalRemainingWorkGroups'],goalStatus='active',
            previousGoalTurnClassification='progress: native winner mass unlink and independent201cloud repair source-qualified/private build started',
            thisGoalTurnClassification='progress: actual nominal P1/P2 cloud13x5 cleanup verified;304pixel real worker prematurely unlinked/lingering orb proved; exact two-byte native201 worker successor whole-guest qualified',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['New private native build and earned both-slot long-distance object/cache/palette teardown still required.',
                'Original visible victim palette must stay unchanged until hidden; earlier flash inference was unsupported.',
                'Full native audio, CPU/other victims/arenas/320boundary, Kano laser and original remaining full release gates remain unaccepted.'])
        (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as f:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),f)
        for p in (old_probe,probe,binary):
            need(p.parent.resolve()==OUT.resolve(),'Exact terminal generated probe/slice only');p.unlink()
        print(json.dumps(dict(passed=True,guest=result['proposedGuestSHA256'],changedBytes=2,workerCategory='0201',faults=len(faults))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as f:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),f)
        raise

if __name__=='__main__':main()
