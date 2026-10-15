"""Native laser palette helper, from continuously verified original ramp.

Rebuild whole initializer in RAM. Exactly five native ABI/address operands
are adapted; no host actor substitution, hidden forced finish, game build,
input binding or public promotion. Complete laser integration remains.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import traceback
from pathlib import Path
import qualify_native_sonya_orb_worker_lifetime as prior
import review_native_kano_laser_palette_reference as reference

ROOT=prior.ROOT
STAGE=ROOT/'source_native_kano_laser_palette'
OUT=ROOT/'audit_native_kano_laser_palette_source'
need,sha,address=prior.need,prior.sha,prior.address
BEGIN,END='// KANO_LASER_PALETTE_BEGIN','// KANO_LASER_PALETTE_END'
FIRST,LAST=0xaf700,0xaf800
REMAP={0x08:(0xff92b990,address(FIRST+0x20)),0x0e:(0xff926f20,0xff80e280),
       0x48:(0xff925320,0xff80c6b0),0x50:(0xff926960,0xff80dcc0),0x5a:(0xff926ac0,0xff80de20)}

def compile_probe(code,base,payload):
    probe=OUT/'initializer_probe.exe'
    compiled=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
        '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/'compiler.log').write_text(compiled.stdout+compiled.stderr)
    need(compiled.returncode==0,'Actual whole successor initializer compiles warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=result.returncode,stdoutBytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base) and not result.stderr,'Complete actual initialized program reconstructed in RAM')
    return result.stdout,probe

def helper_contract(guest,donor):
    original_at=(0xff92b890-0xff800000)//8
    expected=bytearray(donor[original_at:original_at+0xac])
    for offset,(old,new) in REMAP.items():
        need(struct.unpack_from('<I',expected,offset)[0]==old,'Actual original kernel operand '+hex(offset))
        struct.pack_into('<I',expected,offset,new)
    need(guest[FIRST:FIRST+0xac]==expected,'Every helper opcode/data byte conserved except five exact native ABI/address operands')
    levels=struct.unpack_from('<12H',donor,(0xff9b6200-0xff800000)//8)
    need(guest[0xaf7b0:0xaf7c8]==struct.pack('<12H',*levels) and
         levels==(1,2,4,6,8,10,12,14,16,18,20,0xffff),'Exact finite original intensity table with terminal negative word')
    need(struct.unpack_from('<H',guest,FIRST+2)[0]==0x09c1 and
         struct.unpack_from('<H',guest,FIRST+4)[0]==0x119,'Native palette auxiliary119process, not unsafe winner-deleted100')
    need((0x119&0xffffffff)!=0x100,'Native exact winner deletion cannot kill finite119palette helper')
    need(struct.unpack_from('<H',guest,FIRST+0x0c)[0]==0x0d5f,'Constructor is an ordinary native short CALLA')
    # Native A7..A12 process layout is identical. A9 saves encoded bank,
    # A8 deliberately holds a low-word cadence, A10 method, A11 table.
    need(struct.unpack_from('<6H',guest,FIRST+0x12)==(0xb2c0,0xa0,0xb0a0,0xc0,0xb140,0x80),
         'Native constructor saves only bank/cadence/method in actual A9/A8/A10 slots')
    need(0x100+16+65*16<0x6f0,'Largest converted65color palette fits native private task scratch without stack/body overlap')
    return dict(nativeConstructor=f'{address(FIRST):08X}',nativeWorker=f'{address(FIRST+0x20):08X}',
        nativeArithmetic=f'{address(FIRST+0x5e):08X}',nativeIntensityTable=f'{address(0xaf7b0):08X}',
        nativeTaskCategory='0119',nativeAllocate='FF80E280',nativeQueue='FF80C6B0',nativeSleep='FF80DCC0',nativeRetire='FF80DE20',
        fieldsPerLevel=6,levels=list(levels),maximumNativeColorCount=65,maximumScratchEndBitOffset='520',
        currentPaletteLookup='0105BB30 + bank*40bits',sourceOpcodeBytesConserved=0xac-20,
        callerContract='A0 true victim encoded bank; A5=6; A10=1; A11=native intensity table; call at real contact; retain actual bank ownership through helper retirement')

def decode(program,start,bits):
    return subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(program),'-arch','tms34010','-basepc',hex(start),
        '-skip',hex((start-0xff800000)//8),'-count',str(bits),'-norawbytes'],text=True,capture_output=True,check=True).stdout

def main():
    need(not OUT.exists(),'Fresh source helper qualification; preserve any executed failures as successors')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text())
        runtime=ROOT/'audit_native_sonya_orb_worker_allocation_epoch_review/report.json'
        review=json.loads(runtime.read_text());original_review=json.loads((reference.OUT/'report.json').read_text())
        need(receipt['passed'] and review['passed'] and review['nativeOrbWorkerCleanupAccepted'] and
             original_review['passed'] and original_review['originalLaserVictimRampReferenceAccepted'] and
             all(sha(p)==h for record in (receipt,review,original_review) for p,h in record['inputHashes'].items()),
             'Actual full source, earned orb cleanup and continuous original laser reference conserved')
        old=(prior.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        need(new.count(BEGIN)==new.count(END)==1,'One appended native palette helper')
        start=new.index('\n\t'+BEGIN);end=new.index(END)+len(END)
        block=new[start:end]
        need(new[:start-1]+new[end:]==old,'Only appended palette helper; all existing native gameplay and Sonya fixes untouched')
        for leaf in ('midtunit.cpp','midtunit.h'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'No host/platform/audio/identity changes')
        old_harness=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// SONYA_ORB_PALETTE_END'
        need(old_harness.count(anchor)==1,'Exact frozen whole initializer append boundary')
        harness=old_harness.replace(anchor,anchor+'\n'+block)
        base=prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=compile_probe(harness,base,payload)
        donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();contract=helper_contract(guest,donor)
        expected_prior=bytearray(guest);expected_prior[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        need(hashlib.sha256(expected_prior).hexdigest().upper()==receipt['proposedGuestSHA256'],
             'Every previous initialized gameplay byte exact; only unused reserved palette helper range changes')
        faults=[]
        for name,at in [('wrong_worker_entry',FIRST+8),('wrong_native_allocate',FIRST+0xe),
            ('wrong_native_queue',FIRST+0x48),('wrong_native_sleep',FIRST+0x50),
            ('wrong_native_retire',FIRST+0x5a),('wrong_task_class',FIRST+4),('wrong_palette_math',FIRST+0x80),
            ('wrong_intensity',0xaf7b0)]:
            wrong=bytearray(guest);wrong[at]^=1
            try:helper_contract(bytes(wrong),donor)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Wrong source helper admitted: '+name)
        mk2=ROOT/'mk2/mk2-maincpu.bin'
        kernels=dict(allocator=decode(mk2,0xff80e280,608),clock=decode(mk2,0xff80dcc0,352),queue=decode(mk2,0xff80c6b0,320),hardware=decode(mk2,0xff80c7f0,720))
        need('MMTM   A0,A2,A7-A12' in kernels['allocator'] and 'MOVE   A1,*A0(20h),0' in kernels['allocator'] and
             'MOVE   A0,-*A1,0' in kernels['clock'] and 'MOVE   A0,*A3+,1' in kernels['queue'] and
             'MOVE   A1,*A3+,0' in kernels['queue'] and 'MOVE   A2,*A3+,0' in kernels['queue'] and
             'MOVI   1800000h,A5' in kernels['hardware'],
             'Actual native task context, word-cadence, queue record and MKII hardware palette contract')
        # Native converted costumes include one additional explicit transparent
        # palette entry; observe its legitimate65word scratch/queue capacity.
        cases=[]
        for record_at in (0xfda00,0xfdb00,0xf1500,0xf1600):
            count=struct.unpack_from('<H',guest,record_at)[0];need(count==65,'True native primary/alternate converted costume header')
            colors=struct.unpack_from('<65H',guest,record_at+2)
            cases.append(dict(nativePalette=f'{address(record_at):08X}',count=count,
                allLevels=[dict(level=k,sha256=hashlib.sha256(struct.pack('<65H',*(reference.ramp(c,k) for c in colors))).hexdigest().upper()) for k in contract['levels'][:-1]]))
        paths=[Path(__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',runtime,reference.OUT/'report.json',
            ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'mame-mkp/unidasm.exe',
            ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
            *(STAGE/f for f in ('midtunit.cpp','midtunit.h','midtunit_m.cpp'))]
        result=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),nativeHelperContract=contract,
            exactNativeOperandRemaps={hex(k):dict(original=f'{v[0]:08X}',native=f'{v[1]:08X}') for k,v in REMAP.items()},
            convertedPrimaryAlternatePaletteCases=cases,actualSourceFaultsRejected=faults,actualNativeKernelDisassembly=kernels,
            originalNaturalIntegrationRequirements=review['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=review['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Unbound internal native helper only; no new playable build or port laser runtime acceptance.',
                'Caller must launch at contact and retain real victim palette allocation through finite native helper lifetime.',
                'True victim body streams/offsets/camera, smoke/bone effects, original sound/priority, human/CPU bindings and broader integration/release remain.'])
        (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as f:json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block),f)
        need(probe.parent.resolve()==OUT.resolve(),'Only exact terminal temporary source probe removed');probe.unlink()
        print(json.dumps(dict(passed=True,guest=result['proposedGuestSHA256'],faults=len(faults),nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as f:json.dump(dict(actualInitializerHarness=harness),f)
        raise

if __name__=='__main__':main()
