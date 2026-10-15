"""Private Sonya second-finisher input/CPU binding, source-only qualification.

Compiles actual old/new initializers into RAM, independently assembles the
typed parser/action guard and cursor save, and executes the emitted parser
against physical-port/history kernel contracts. Never writes guest memory
or starts a game. Native match/art/audio/cleanup acceptance is still required.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_secondary_finisher_contracts as prior

ROOT=prior.ROOT
STAGE=ROOT/'source_native_sonya_orb_dispatch'
OUT=ROOT/'audit_native_sonya_orb_dispatch_source'
BEGIN,END='// SONYA_ORB_DISPATCH_BEGIN','// SONYA_ORB_DISPATCH_END'
RECORD,PARSER,ENTRY,LAST=0xaf340,0xaf380,0xaf600,0xaf680
FALLBACK=0xfff9a000
PIN='409853F6E5CCF1EE432CD2B3CF24692B5294240574C12AAFDCECA33A9759E31E'
VICTIM_PIN='2EFFF1B3BDD4880189F3B50F2CE17B8A8CCD59C41C3725EAD0A2E97CF04EAD6F'
OLD_HANDOFF='\tleg_movi(7,native_address(secondary_victim_spin)); leg_call(0xff842710);'
NEW_HANDOFF='\tleg_code({0xa32f}); // victim handoff may reuse A9: retain the owned orb cursor on this non-yielding short call\n'+OLD_HANDOFF+'\n\tleg_code({0x09af,0x0200});'
need,sha,address=prior.need,prior.sha,prior.address


def model(old):
    g=bytearray(old)
    need(all(b==255 for b in old[RECORD:LAST]), 'Whole new input/guard allocation unused')
    # Re-encode this worker independently; all schedule/effect ownership stays
    # the same, with only a balanced A9 save around the synchronous handoff.
    g[0xaf090:0xaf190]=b'\xff'*0x100
    a=prior.motion.Assembler(g,0xaf090,0xaf190)
    def cooperate(target):a.words(0x0147,0x0b07,0x60,0xa2ec,0xc080,target,target>>16)
    a.movi(9,address(0xad284));a.movi(11,address(0xad640));cooperate(address(0xad500))
    cooperate(address(0xad840));a.words(0xa32f);a.movi(7,address(0xaf190));a.call(0xff842710);a.words(0x09af,0x200)
    cooperate(address(0xadb40));a.movi(7,address(0xaf1d0));a.call(0xff842710)
    cooperate(address(0xad4c0));a.call(address(0xaf290));a.branch(0xc080,0xff80de20)
    struct.pack_into('<13H',g,RECORD,48,6,7,5,5,0,0,6,8,5,5,0,0)
    a=prior.motion.Assembler(g,PARSER,ENTRY)
    a.words(0x05a4,0x1b00,0x0106,0x0b44,0xfffc);a.branch(0xcb80,FALLBACK)
    for p1,p2,branch in ((0x13,0x100c,0xcb80),(0x40,0x4000,0xca80)):
        a.movi(0,p1);a.movi(1,p2);a.call(0xff877d80);a.branch(branch,FALLBACK)
    a.movi(0,0x20);a.movi(1,0x2000);a.call(0xff877d80);block=a.branch(0xcb80)
    a.words(0x05a2,0x20,0x160,0x03e2,0x4904);p2=a.branch(0xcb80)
    a.words(0x1fa2);done=a.branch(0xc080);a.here(p2);a.words(0x1f22);a.here(done)
    a.branch(0xca80,FALLBACK);a.here(block)
    a.movi(0,0x13);a.movi(1,0x100c);a.movi(11,address(RECORD));a.call(0xff8775d0);a.branch(0xc980,FALLBACK)
    a.call(0xff834cc0);a.words(0x0b43,(~208)&0xffff);a.branch(0xc480,FALLBACK)
    a.movi(1,320);a.movi(7,address(ENTRY));a.branch(0xc080,0xff876f70)
    a=prior.motion.Assembler(g,ENTRY,LAST)
    a.words(0xb7a0,0x140,0xb404,0x1f0,0x0b44,(~12)&0xffff);a.branch(0xca80,0xffa14860)
    a.words(0x0b44,(~13)&0xffff);a.branch(0xca80,0xffa14860);a.branch(0xc080,address(0xaf000))
    for at,value in ((0xff270+18*4,address(PARSER)),(0xf436c+18*4,address(ENTRY)),(0xf395c+18*4,0x01000080)):
        struct.pack_into('<I',g,at,value)
    return bytes(g)


def parser_unit(g,side,facing,primary_block,alternate_block,gap,flag=3,hk=True,extra=0,history=True,age=20):
    regs=[0]*16;regs[8]=0x1000 if side==1 else 0x3000;pc=address(PARSER)
    zero=lt=carry=False;calls=[]
    held=(0x40 if side==1 else 0x4000) if hk else 0
    if primary_block:held|=0x20 if side==1 else 0x2000
    held|=extra
    low_pressed=(1<<(2 if side==1 else 6)) if alternate_block else 0
    for step in range(1000):
        if pc==FALLBACK:return dict(result='fallback',calls=calls)
        if pc==0xff876f70:
            need(regs[1]==320 and regs[7]==address(ENTRY), 'Actual emitted parser reaches native common gate with correct max and separate own action')
            return dict(result='native_gate' if gap<=regs[1] else 'native_max_rejection',calls=calls)
        op=struct.unpack_from('<H',g,(pc-0xff800000)//8)[0];pc+=16
        def word():
            nonlocal pc
            v=struct.unpack_from('<H',g,(pc-0xff800000)//8)[0];pc+=16;return v
        def longword():return word()|(word()<<16)
        if 0x09e0<=op<=0x09ef:regs[op&15]=longword();zero=regs[op&15]==0
        elif op==0x05a4:
            need(longword()==0x1061b00,'Only existing native finish flag read');regs[4]=flag;zero=flag==0
        elif op==0x05a2:
            need(longword()==0x1600020,'Only existing redundant physical Block port read');regs[2]=(~low_pressed)&0xffffffff;zero=regs[2]==0
        elif op in (0x0b44,0x0b43):
            immediate=(~word())&0xffff;reg=op&15;zero=(regs[reg]&0xffff)==immediate;lt=(regs[reg]&0xffff)<immediate
        elif op in (0xc080,0xca80,0xcb80,0xc980,0xc480):
            target=longword()
            if op==0xc080 or (op==0xca80 and zero) or (op==0xcb80 and not zero) or (op==0xc980 and not carry) or (op==0xc480 and lt):pc=target
        elif op==0x03e2:regs[2]=(~regs[2])&0xffffffff;zero=regs[2]==0
        elif op==0x4904:zero=regs[8]==regs[4]
        elif op in (0x1fa2,0x1f22):zero=not bool(regs[2]&(1<<((~(op>>5))&31)))
        elif op==0x0d5f:
            target=longword();calls.append(f'{target:08X}')
            if target==0xff877d80:
                regs[2]=held&(regs[0] if side==1 else regs[1]);regs[4]=0x1000;zero=regs[2]==0
            elif target==0xff8775d0:
                need((regs[0],regs[1],regs[11])==(0x13,0x100c,address(RECORD)), 'Actual history call does not accidentally forbid the required Block/HK chord')
                expected=(6,7 if facing==0 else 8,5,5,0,0)
                actual=struct.unpack_from('<6H',g,RECORD+2+facing*12)
                timeout=struct.unpack_from('<H',g,RECORD)[0]
                carry=history and actual==expected and age<=timeout and not (held&(0x13 if side==1 else 0x100c))
            elif target==0xff834cc0:regs[3]=gap;regs[10]=0x6000
            else:raise ValueError('Unexpected parser native kernel '+hex(target))
        else:raise ValueError(f'Unexpected real parser opcode {op:04X}')
    raise ValueError('Emitted input parser does not terminate')


def unit_cases(g):
    cases=[]
    for side in (1,2):
        for facing in (0,1):
            for alternate in (False,True):
                for gap in (207,208,256,320,321):
                    got=parser_unit(g,side,facing,not alternate,alternate,gap)
                    wanted='fallback' if gap<208 else 'native_max_rejection' if gap>320 else 'native_gate'
                    need(got['result']==wanted, 'Actual emitted both-slot/mirror/Block-port parser preserves original distance limits')
                    cases.append(dict(side=side,facing=facing,alternateBlock=alternate,gap=gap,result=got['result']))
            for name,kwargs in (('no_block',dict(primary_block=False)),('no_hk',dict(hk=False)),
                                ('wrong_history',dict(history=False)),('history_expired',dict(age=49)),
                                ('outside_finish_mode',dict(flag=0)),('other_LP',dict(extra=1 if side==1 else 4)),
                                ('other_HP',dict(extra=2 if side==1 else 8)),('other_LK',dict(extra=16 if side==1 else 0x1000))):
                args=dict(side=side,facing=facing,primary_block=True,alternate_block=False,gap=256);args.update(kwargs)
                got=parser_unit(g,**args)
                need(got['result']=='fallback', 'Rejected chord/history/state preserves exact original HK fallback')
                cases.append(dict(side=side,facing=facing,rejection=name,result=got['result']))
    return cases


def source_contract():
    run=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(ROOT/'mk2/mk2-maincpu.bin'),'-arch','tms34010',
                        '-basepc','0xff800000','-norawbytes'],text=True,capture_output=True,check=True)
    lines={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in run.stdout.splitlines()}
    facts={0xff842830:'MOVE   *A13(140h),A8,1',0xff842850:'MOVE   *A13(170h),A13,1',
           0xff842980:'MMFM   SP,A7',0xff8429a0:'MOVE   *A13(170h),A0,1',0xff8429c0:'JA     FF83F930h',
           0xff83f9f0:'MOVE   A7,*A0,1',0xff83fa00:'MMFM   SP,A0,A2',0xff83fa20:'RETS',
           0xff877f90:'AND    A0,A2',0xff877fb0:'AND    A1,A2',
           0xff876f70:'CALLA  FF834CC0h',0xff876fa0:'CMP    A1,A3',0xff876fb0:'JRHI   FF877420h',
           0xff9b4350:'SRL    10h,A0',0xff9b4470:'JA     FF876B80h',0xff9b44a0:'ZEXT   A0,0',
           0xff9b45c0:'JA     FF876B40h'}
    need(all(lines.get(p)==s for p,s in facts.items()), 'Actual original native handoff/short return/physical masks/common range/CPU halves agree with binding')
    return facts


def compile_probe(code,base,payload,label):
    path=OUT/(label+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                           '-x','c++','-','-o',str(path)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Actual '+label+' initializer compiled warning-free')
    result=subprocess.run([str(path)],input=base+payload,capture_output=True)
    (OUT/(label+'_native_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,stdoutBytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    (OUT/(label+'_initializer.stderr')).write_bytes(result.stderr)
    need(result.returncode==0 and len(result.stdout)==len(base),'Actual '+label+' initializer emitted complete guest in RAM')
    return result.stdout,path


def main():
    need(not OUT.exists() and not prior.visual.native.census(),'Fresh private binding evidence; no game live')
    OUT.mkdir();old_code=new_code=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text())
        victims=ROOT/'audit_native_secondary_victim_ownership/report.json'
        victim_receipt=json.loads(victims.read_text())
        need(sha(prior.OUT/'report.json')==PIN and sha(victims)==VICTIM_PIN and
             receipt['passed'] and victim_receipt['passed'] and
             all(sha(p)==h for r in (receipt,victim_receipt) for p,h in r['inputHashes'].items()), 'Both prior semantic and true-victim ownership proofs unchanged')
        old_source=(prior.STAGE/'midtunit_m.cpp').read_text();new_source=(STAGE/'midtunit_m.cpp').read_text()
        need(new_source.count(BEGIN)==new_source.count(END)==1 and old_source.count(OLD_HANDOFF)==1,'Exact new input block and prior victim handoff')
        first,last=new_source.index('\t'+BEGIN),new_source.index(END)+len(END)
        block=new_source[first:last]
        need(new_source[:first-1]+new_source[last+1:]==old_source.replace(OLD_HANDOFF,NEW_HANDOFF), 'Only balanced cursor preservation and appended own dispatch change staged source')
        for leaf in ('midtunit.h','midtunit.cpp'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Native host/platform/audio code unchanged')
        old_code=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(old_code.count(OLD_HANDOFF)==old_code.count('// SECONDARY_FINISHER_EFFECTS_END')==1,'Exact actually executed initializer boundaries')
        new_code=old_code.replace(OLD_HANDOFF,NEW_HANDOFF).replace('// SECONDARY_FINISHER_EFFECTS_END','// SECONDARY_FINISHER_EFFECTS_END\n'+block)
        extra='''constexpr unsigned sonya_finish_action=0xf5640;
    auto read32=[&](unsigned at) { return uint32_t(rom[at])|(uint32_t(rom[at+1])<<8)|(uint32_t(rom[at+2])<<16)|(uint32_t(rom[at+3])<<24); };
    auto emit=[&](unsigned at,std::initializer_list<uint16_t> words) { for(uint16_t value:words) { write16(at,value);at+=2; } };
'''
        needle='constexpr unsigned sonya_finish_poses=0xf5740;'
        need(new_code.count(needle)==1,'Unique actual standalone initializer helper insertion')
        new_code=new_code.replace(needle,needle+'\n'+extra)
        base=prior.visual.prior.expected();payload=prior.effects.PAYLOAD.read_bytes()
        old,old_probe=compile_probe(old_code,base,payload,'prior')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['expectedGuestSHA256'],'Actual complete prior corrected guest conserved')
        guest,probe=compile_probe(new_code,base,payload,'dispatch')
        expected=model(old);need(guest==expected,'Whole actual initializer equals independent exact input/worker/CPU model')
        native_facts=source_contract();cases=unit_cases(guest)
        motion_units,factory=prior.corrected_units();motion_cases=motion_units(guest)
        factories=[factory(guest,e) for e in (0xae900,0xaed00)]
        # Verify native boss guard and real action route through actual words.
        guard=guest[ENTRY:ENTRY+40]
        need(guard==expected[ENTRY:ENTRY+40] and struct.unpack_from('<I',guest,0xf4320+18*4)[0]==0xfffab200 and
             struct.unpack_from('<I',guest,0xf436c+18*4)[0]==address(ENTRY) and
             struct.unpack_from('<I',guest,0xf395c+18*4)[0]==0x01000080,
             'Independent second CPU action/256 target; first fire kiss and128 target unchanged')
        faults=[]
        for name,at in (('history_timeout',RECORD),('right_history',RECORD+4),('left_history',RECORD+16),
                        ('required_HK',PARSER+42),('primary_Block',PARSER+74),('minimum_gap',PARSER+176),
                        ('native_max_gap',PARSER+184),('boss_immunity',ENTRY+8),
                        ('second_CPU_action',0xf436c+72),('second_CPU_distance',0xf395c+74),
                        ('first_CPU_action',0xf4320+72),('stock_input',0xff270),('victim_cursor_save',0xaf0b8)):
            wrong=bytearray(guest);wrong[at]^=1
            try:need(bytes(wrong)==expected,'Whole emitted parser/worker/CPU/conservation model rejects changed byte')
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Dispatch/conservation fault admitted: '+name)
        binary=OUT/'generated_dispatch.bin';binary.write_bytes(guest[0xaf090:LAST])
        run=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010','-basepc',hex(address(0xaf090)),'-norawbytes'],text=True,capture_output=True,check=True)
        lines={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in run.stdout.splitlines()}
        worker=[s for p,s in lines.items() if address(0xaf090)<=p<address(0xaf190)]
        need('MOVE   A9,-*SP,1' in worker and 'MMFM   SP,A9' in worker and worker.count('CALLA  FF842710h')==2,'Actual decoded worker saves/restores its own cursor around victim handoff')
        need(lines[address(ENTRY)]=='MOVE   *A13(140h),A0,1','Actual boss guard reads real victim, never performer/other character/global')
        sources={leaf:sha(STAGE/leaf) for leaf in prior.visual.SOURCE_PINS}
        paths=[Path(__file__),prior.OUT/'report.json',victims,ROOT/'mk2/mk2-maincpu.bin',ROOT/'mame-mkp/unidasm.exe',
               ROOT/'audit_native_sonya_secondary_input/report.json',*(STAGE/leaf for leaf in sources)]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
                    stagedSourceHashes=sources,proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                    initializedGuestByteDelta=sum(a!=b for a,b in zip(base,guest)),initializedByteDeltaFromPrior=sum(a!=b for a,b in zip(old,guest)),
                    command=dict(hold='Block',chronological=['Up','Up','Back','Down','HK'],minimumGap=208,maximumGap=320,timeoutTicks=48),
                    cpuFirstAction='FFFAB200',cpuSecondAction=f'{address(ENTRY):08X}',cpuFirstDistance=128,cpuSecondDistance=256,
                    parserUnitCases=cases,motionUnitCases=motion_cases,constructorUnitCases=factories,actualFaultsRejected=faults,
                    nativeContractInstructions={f'{p:08X}':s for p,s in native_facts.items()},
                    actualNativeDisassembly={f'{p:08X}':s for p,s in lines.items() if s!='DW     FFFFh'},
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    previousGoalTurnClassification='progress: six real pointer-copy opcodes repaired;34 true-ID victim streams source-qualified',
                    thisGoalTurnClassification='progress: adapted Sonya second finisher command/CPU variant, native boss immunity and owned cursor preservation implemented/source-qualified',
                    originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
                    gameBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
                    limitations=['Actual initialized native guest/parser units only: no current in-game second-finisher, allocation/render/cleanup or audio acceptance.',
                                 'New original finisher sound samples not yet imported; Kano laser victim/action still unbound.',
                                 'Full original14requirements/6remaininggroups and finished ZIP remain.'],
                    nextAction='Build one compressed private candidate; physically earn and activate Sonya orb from both slots/mirrors; review actual full native rendering/32bones/3smoke/victim/cleanup and sound, then complete Kano and all remaining scope.')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        for temporary in (old_probe,probe,binary):
            need(temporary.parent.resolve()==OUT.resolve(),'Only exact generated temporary test artifacts')
            temporary.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,
                              parserCases=len(cases),faultRejections=len(faults),guest=report['proposedGuestSHA256'])))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False,failure=traceback.format_exc(),nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(files={str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in (Path(__file__),*(STAGE/leaf for leaf in prior.visual.SOURCE_PINS))},
                           actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code),stream)


if __name__=='__main__':main()
