"""Source-only owned orb palette successor; preserves failed native evidence.

The CPU metadata guard suppresses genuine FE83F6F0 requests when A5 still
names an imported frame. Use an owned native 32-color record and ordinary
palette replace/free, clearing A5 only during the typed synchronous request.
No broad CPU guard changes, new art, gameplay acceptance or public promotion.
"""
import gzip
import hashlib
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_sonya_orb_cursor as prior

ROOT=prior.ROOT
STAGE=ROOT/'source_native_sonya_orb_palette'
OUT=ROOT/'audit_native_sonya_orb_palette_source'
BEGIN,END='// SONYA_ORB_PALETTE_BEGIN','// SONYA_ORB_PALETTE_END'
OLD='\t\tif (fighter) leg_call(native_address(orb_visual_position));'
NEW='''\t\tif (fighter)
\t\t{
\t\t\tleg_call(native_address(orb_visual_position));
\t\t\t// This real 32-color orb record is not Wolf body-frame metadata.
\t\t\t// Use an owned native palette and a non-yielding typed request;
\t\t\t// clear only A5 during allocation, restoring it and the performer.
\t\t\tleg_code({0x098f,0x0480,0xb7a8,0x0190});
\t\t\tleg_movi(0,native_address(0xaf680)); leg_movi(5,0);
\t\t\tleg_call(0xff841090); leg_code({0x09af,0x0120});
\t\t}'''
need,sha,address=prior.need,prior.sha,prior.address


def compile_probe(code,base,payload,label):
    probe=OUT/(label+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                           '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Actual '+label+' initialized source compiled warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/(label+'_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,bytes=len(result.stdout)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base),'Whole actual '+label+' guest retained in RAM')
    return result.stdout,probe


def typed_unit(g,entry=0xad640):
    regs=[0xa0000000+i for i in range(16)];regs[8]=0x01034e90;regs[13]=0x01069c80
    original=regs.copy();child=0x0102fc10;pc=address(entry);stack=[('pc',0x12345678)];events=[]
    for step in range(100):
        op=struct.unpack_from('<H',g,(pc-0xff800000)//8)[0];pc+=16
        def word():
            nonlocal pc
            value=struct.unpack_from('<H',g,(pc-0xff800000)//8)[0];pc+=16;return value
        def longword():return word()|(word()<<16)
        if op in (0x098f,0x09af):
            mask=word()
            if op==0x098f:
                for n in range(16):
                    if mask&(1<<(15-n)):stack.append(('reg',n,regs[n]))
            else:
                for n in range(15,-1,-1):
                    if mask&(1<<n):
                        row=stack.pop();need(row[:2]==('reg',n),'Real ascending-save/descending-restore ABI');regs[n]=row[2]
        elif 0x09e0<=op<=0x09ef:regs[op&15]=longword()
        elif op==0xb7a8:
            need(word()==0x190,'Only owned independent child switched for palette request');regs[8]=child
        elif op==0x0d5f:
            target=longword();events.append(hex(target))
            if target in (address(0xad680),address(0xad780)):
                need(regs[8]==original[8],'Allocation/position preserves true performer')
                for n in range(6):regs[n]=0xb0000000+n
            elif target==0xff841090:
                need(regs[8]==child and regs[0]==address(0xaf680) and regs[5]==0,
                     'Native palette replacement acts only on orb, with actual owned record and no imported-frame tag')
                for n in range(5):regs[n]=0xc0000000+n
            else:raise ValueError('Unexpected native helper '+hex(target))
        elif op==0x0960:
            need(stack==[('pc',0x12345678)] and all(regs[n]==original[n] for n in range(8,16)),
                 'All true ownership/cadence/cursor/private stack registers preserved; no yield')
            need(events==[hex(address(0xad680)),hex(address(0xad780)),'0xff841090'],'Exact allocation/position/one replacement sequence')
            return dict(child=f'{child:08X}',palette=f'{address(0xaf680):08X}',nativeReplaces=1,sharedStackBalanced=True,
                        performerAndSchedulerRegistersConserved=True,bodyAndVictimIdentityWrites=0)
        else:raise ValueError(f'Unexpected actual typed helper {op:04X}')
    raise ValueError('Typed orb palette helper does not return')


def main():
    need(not OUT.exists() and not prior.prior.prior.visual.native.census(),'Fresh source evidence; no native game live')
    OUT.mkdir();old_code=new_code=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text())
        need(receipt['passed'] and receipt['sourceOnlyAccepted'] and not receipt['nativeRuntimeAccepted'] and
             all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Frozen real cursor fix and failed native evidence preserved')
        test=ROOT/'audit_native_sonya_orb_palette_trace_p1';run=json.loads((test/'report.json').read_text())
        need(run['nativeExit']==0 and run['transportOnlyAccepted'] and not run['finisherAccepted'] and
             all(sha(p)==h for p,h in run['inputHashes'].items()),'Actual earned palette trace terminal with all executed inputs pinned')
        log=gzip.open(test/'run.log.gz','rt').read()
        observed=[prior.fields(l) for l in log.splitlines() if l.startswith('MK2_ORB_PALETTE ')]
        alloc=[prior.fields(l) for l in log.splitlines() if l.startswith('MK2_ORB_PALETTE_ALLOC ')]
        need(len(alloc)==1 and alloc[0]['source']=='FE83F6F0' and
             len(observed)==3 and all(r['source']!='FE83F6F0' for r in observed),
             'Actual native constructor requests genuine orb palette, but actual cached bank does not own it')
        frames=[prior.fields(l) for l in log.splitlines() if l.startswith('MK2_ORB_RGB_DIGEST ')]
        need(frames==receipt['actualFailureEvidence']['actualFailedFrames'],
             'All fifteen actual palette trace rasters equal the fifteen inspected failed rasters')
        old_source=(prior.STAGE/'midtunit_m.cpp').read_text();new_source=(STAGE/'midtunit_m.cpp').read_text()
        first,last=new_source.index('\t'+BEGIN),new_source.index(END)+len(END)
        block=new_source[first:last]
        need(new_source[:first-1]+new_source[last+1:]==old_source.replace(OLD,NEW) and old_source.count(OLD)==1,
             'Only typed own palette request and one bounded original-color record added')
        for leaf in ('midtunit.h','midtunit.cpp'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Host and audio source untouched')
        cpu=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp';cpu_text=cpu.read_text()
        need(cpu_text.count('mk2ks_imported_descriptor && !mk2ks_native_morph_palette &&')==2 and
             cpu_text.count('uint32_t(m_regs[5].reg) >= 0xfe800000')==2,
             'Both actual debug/normal CPU paths retain metadata protection; typed native palette and clear A5 bypass only false classification')
        old_code=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(old_code.count(OLD)==old_code.count('// SONYA_ORB_DISPATCH_END')==1,'Exact source initializer anchors')
        new_code=old_code.replace(OLD,NEW).replace('// SONYA_ORB_DISPATCH_END','// SONYA_ORB_DISPATCH_END\n'+block)
        base=prior.prior.prior.visual.prior.expected();payload=prior.prior.prior.effects.PAYLOAD.read_bytes()
        old,old_probe=compile_probe(old_code,base,payload,'cursor')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['proposedGuestSHA256'],'Whole previously qualified cursor guest unchanged')
        guest,probe=compile_probe(new_code,base,payload,'palette')
        original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();at=(0xff83f6f0-0xff800000)//8
        colors=original[at:at+66];need(struct.unpack_from('<HH',colors)==(32,0) and colors==payload[at:at+66],
                                     'Actual 16-bit32count/transparentzero effect palette copied byte-exact, not shifted or synthesized')
        modeled=bytearray(old);need(all(b==255 for b in old[0xaf680:0xaf700]),'Owned palette storage unused')
        modeled[0xaf680:0xaf680+66]=colors;modeled[0xad640:0xad680]=b'\xff'*64
        a=prior.prior.prior.motion.Assembler(modeled,0xad640,0xad680)
        a.words(0x098f,0x40);a.movi(9,address(0xad390));a.call(address(0xad680));a.words(0x09af,0x200)
        a.call(address(0xad780));a.words(0x098f,0x480,0xb7a8,0x190);a.movi(0,address(0xaf680));a.movi(5,0)
        a.call(0xff841090);a.words(0x09af,0x120,0x0960)
        need(guest==bytes(modeled),'Whole actual guest equals exact independently encoded typed helper/palette; every other byte conserved')
        typed=typed_unit(guest)
        units,_=prior.native_motion_units();cases=units(guest);parser=prior.prior.unit_cases(guest)
        _,factory=prior.prior.prior.corrected_units();factories=[factory(guest,e) for e in (0xae900,0xaed00)]
        faults=[]
        for name,offset in (('own_palette_address',0xad664),('clear_frame_tag',0xad66a),('restore_performer',0xad676)):
            wrong=bytearray(guest);wrong[offset]^=1
            try:typed_unit(bytes(wrong))
            except (ValueError,IndexError,struct.error) as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Faulty typed palette helper admitted: '+name)
        binary=OUT/'helper.bin';binary.write_bytes(guest[0xad640:0xad680])
        decoded=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                                '-basepc',hex(address(0xad640)),'-norawbytes'],text=True,capture_output=True,check=True).stdout
        need('MOVI   FFD7B400h,A0' in decoded and 'MOVI   0h,A5' in decoded and
             'CALLA  FF841090h' in decoded and 'MMFM   SP,A5,A8' in decoded,'Native decoder confirms typed palette request/restore')
        paths=[Path(__file__),prior.OUT/'report.json',test/'report.json',test/'run.log.gz',cpu,ROOT/'mk3/mk3-maincpu.bin',
               *(STAGE/leaf for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
                    proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                    initializedByteDeltaFromCursor=sum(a!=b for a,b in zip(old,guest)),
                    initializedGuestByteDelta=sum(a!=b for a,b in zip(base,guest)),
                    actualPaletteAllocation=alloc,actualPaletteFailure=observed,actualNativeDisassembly=decoded,
                    originalPaletteBytes=66,originalPaletteColors=32,originalColorRecordSHA256=hashlib.sha256(colors).hexdigest().upper(),
                    typedRequestUnit=typed,actualTypedFaultsRejected=faults,motionUnitCases=cases,
                    parserUnitCases=parser,constructorUnitCases=factories,
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    previousGoalTurnClassification='no progress: status inspection/restatement only',
                    thisGoalTurnClassification='progress: runtime proves original palette request suppressed by metadata guard; owned byte-exact native palette/typed request source-qualified together with runtime-proven cursor fix',
                    originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
                    newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
                    limitations=['Both repairs still require a new private native build and earned-round rendering/cleanup checks.',
                                 'Victim explosion, finisher sounds, remaining Kano laser and broader release gates unaccepted.'])
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),stream)
        for path in (old_probe,probe,binary):
            need(path.parent.resolve()==OUT.resolve(),'Own terminal generated probe/slice only');path.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,guest=report['proposedGuestSHA256'],faults=len(faults))))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),stream)
        raise


if __name__=='__main__':main()
