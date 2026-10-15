"""Full original laser phases and exact victim-local coroutine, source only.

No playable build/guest-state assistance. Reconstruct the actual whole
initializer in RAM, preserve previous accepted evidence, model emitted
instructions with volatile registers poisoned, and reject negative faults.
Full victim/effects/audio/input/CPU/runtime acceptance is still required.
"""
import gzip
import hashlib
import inspect
import json
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_kano_laser_palette as palette
import qualify_native_secondary_finisher_visuals as visual

ROOT=palette.ROOT
PRIOR_STAGE=ROOT/'source_native_kano_laser_palette'
PRIOR_OUT=ROOT/'audit_native_kano_laser_palette_isolated_source'
STAGE=ROOT/'source_native_kano_laser_phases'
OUT=ROOT/'audit_native_kano_laser_phases_source'
BEGIN,END='// KANO_LASER_PHASES_BEGIN','// KANO_LASER_PHASES_END'
FIRST,LAST=0xaf800,0xafb80
TABLES=(0xaf800,0xaf8a0,0xaf970)
ENTRIES=(0xafa00,0xafa40,0xafa80)
COUNTS=(12,16,8)
need,sha,address=palette.need,palette.sha,palette.address
u32=visual.u32


def compile_probe(code,base,payload):
    probe=OUT/'initializer_probe.exe'
    run=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
        '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/'compiler.log').write_text(run.stdout+run.stderr)
    need(run.returncode==0,'Actual whole successor initializer compiles warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=result.returncode,
        bytes=len(result.stdout),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base) and not result.stderr,
         'Whole actual initialized guest reconstructed in RAM')
    return result.stdout,probe


def phase_model():
    # Extend the preserved emitted-word unit model only with entry-time and
    # already-owned child arguments, so phase calls share one real child.
    code=inspect.getsource(visual.pair_cpu_model)
    swaps=[('def pair_cpu_model(guest, entry):','def pair_cpu_model(guest, entry, start, existing_child):'),
           ('False, 21, 0','False, start, existing_child'),
           ('memory = {}','memory = {0x2000+0x190:existing_child}')]
    for old,new in swaps:
        need(code.count(old)==1,'Exact preserved visual model boundary')
        code=code.replace(old,new)
    scope=dict(vars(visual))
    exec(compile(code,__file__+'::phase_model','exec'),scope)
    return scope['pair_cpu_model'],code


def shake_model(guest,packed,cadence,cycles,xy):
    """Execute actual emitted words; this is NOT emulator evidence."""
    regs=[0]*16
    regs[0],regs[1],regs[2]=packed,cadence,cycles
    regs[8],regs[12],regs[13]=0x30000,0x20000-32,0x10000
    regs[9:12]=[0xabcdef09,0xabcdef0a,0xabcdef0b]
    before=regs[9:12].copy();return_pc=0x12345678
    mem={regs[12]:return_pc,regs[8]+0x90:xy[0]&0xffff,regs[8]+0xb0:xy[1]&0xffff,
         regs[13]+0x140:0x40000,0x40000+0x90:123,0x40000+0xb0:456}
    untouched={at:value for at,value in mem.items() if at in (0x10140,0x40090,0x400b0)}
    pc=address(0xafb00);age=0;samples=[];writes=[];stack_depth=0
    def push(value):
        nonlocal stack_depth
        regs[12]-=32;mem[regs[12]]=value;stack_depth+=1
    def pop():
        nonlocal stack_depth
        value=mem[regs[12]];regs[12]+=32;stack_depth-=1;return value
    for steps in range(10000):
        at=(pc-0xff800000)//8;op=struct.unpack_from('<H',guest,at)[0];pc+=16
        def word():
            nonlocal pc
            value=struct.unpack_from('<H',guest,(pc-0xff800000)//8)[0];pc+=16;return value
        if op==0x098c:
            need(word()==0x70,'Only A9..11 saved on private coroutine stack')
            for r in (9,10,11):push(regs[r])
        elif op==0xa22c:push(regs[1])
        elif op==0xb30d:
            need(word()==0x230,'Dedicated victim-local shake scratch')
            mem[regs[13]+0x230]=regs[8];writes.append(regs[13]+0x230)
        elif op in (0x4c4b,0x4c09,0x4c0a):
            src,dst=(op>>5)&15,op&15;regs[dst]=regs[src]
        elif op==0x0529:regs[9]&=0xffff
        elif op==0x2e0a:regs[10]=(regs[10]&0xffffffff)>>16
        elif op==0xb7a3:
            need(word()==0x230,'Self context, never opponent pointer')
            regs[3]=mem[regs[13]+0x230]
        elif op==0xb460:
            displacement=word();need(displacement in (0x90,0xb0),'Only actor coordinate loads')
            regs[0]=mem[regs[3]+displacement]
        elif op in (0x4120,0x4140,0x4520,0x4540):
            src=(op>>5)&15
            regs[0]=(regs[0]+(regs[src] if op<0x4500 else -regs[src]))&0xffffffff
        elif op==0xb003:
            displacement=word();need(displacement in (0x90,0xb0) and regs[3]==0x30000,
                                      'Shake writes only the true A8 victim')
            mem[regs[3]+displacement]=regs[0]&0xffff;writes.append(regs[3]+displacement)
        elif op==0x8780:regs[0]=mem[regs[12]]
        elif op==0x0d5f:
            target=word()|(word()<<16)
            need(target==0xff80dcc0 and regs[0]==cadence and stack_depth==4,
                 'Actual native scheduler cadence with private live state')
            samples.append((age,mem[0x30090],mem[0x300b0],regs[0]));age+=regs[0]
            for r in range(7):regs[r]=0xfade0000+r
        elif op==0x0d8b:
            delta=struct.unpack('<h',struct.pack('<H',word()))[0]
            regs[11]=(regs[11]-1)&0xffffffff
            if regs[11]:pc+=delta*16
        elif op==0x09ac:
            mask=word()
            if mask==2:regs[1]=pop()
            elif mask==0xe00:
                for r in (11,10,9):regs[r]=pop()
            elif mask==0x80:regs[7]=pop()
            else:raise ValueError('Unexpected private stack restore')
        elif op==0x0127:
            need(regs[7]==return_pc and regs[12]==0x20000 and stack_depth==-1 and
                 regs[9:12]==before and regs[1]==cadence and regs[8]==0x30000 and
                 all(mem[at]==value for at,value in untouched.items()),
                 'Exact continuation, preserved live registers, balanced private stack and unchanged opponent')
            dx,dy=packed&0xffff,(packed>>16)&0xffff
            expected=[(i*cadence,(xy[0]+(dx if i%2==0 else 0))&0xffff,
                       (xy[1]+(dy if i%2==0 else 0))&0xffff,cadence) for i in range(2*cycles)]
            need(samples==expected and age==2*cycles*cadence and
                 (mem[0x30090],mem[0x300b0])==(xy[0]&0xffff,xy[1]&0xffff),
                 'Every shake half-cycle and final true victim position match original')
            return dict(packedXY=f'{packed:08X}',halfCycleFields=cadence,cycles=cycles,
                fields=age,samples=samples,privateStackBalanced=True,opponentUntouched=True,
                coordinateWriteCount=len(writes)-1)
        else:raise ValueError(f'Unknown actual shake word {op:04X} at {pc-16:08X}')
    raise ValueError('Shake did not return')


def contract(guest,base,donor):
    expected=bytearray(base)
    need(all(b==255 for b in base[FIRST:LAST]),'Whole prior initialized phase allocation is unused')
    rows=visual.original_rows()[0];cursor=0
    for table,entry,count in zip(TABLES,ENTRIES,COUNTS):
        at=table
        for row in rows[cursor:cursor+count]+[(0,0,0)]:
            struct.pack_into('<III',expected,at,*row);at+=12
        cursor+=count
        struct.pack_into('<HIHIHI',expected,entry,0x09e9,address(table),0x09eb,address(0xad600),0xc080,address(0xad500))
    shake=bytearray(donor[(0xff961a20-0xff800000)//8:(0xff961d50-0xff800000)//8])
    need(len(shake)==0x66,'Exact original self-shake boundary')
    for offset in (0x30,0x50):
        need(u32(shake,offset)==0xff926960,'Original sleep operand')
        struct.pack_into('<I',shake,offset,0xff80dcc0)
    expected[0xafb00:0xafb66]=shake
    need(guest==expected,'Whole actual guest exact: original phases/wrappers/self-shake only; every previous byte conserved')
    model,_=phase_model();phase_results=[];start=20
    for index,(entry,count) in enumerate(zip(ENTRIES,COUNTS)):
        result=model(guest,entry,start,0 if index==0 else 0x4000)
        phase_rows=rows[sum(COUNTS[:index]):sum(COUNTS[:index])+count]
        events=[];sleeps=[];age=start
        for own,child,fields in phase_rows:
            if own:events.append((age,'own',own))
            if child:events.append((age,'child',child))
            sleeps.append((age,fields));age+=fields
        need(result['events']==events and result['sleeps']==sleeps and result['endpoint']==age and
             result['allocations']==(1 if index==0 else 0),'Full native field choreography and single shared child')
        phase_results.append(dict(phase=index,start=start,end=age,rows=count,**result));start=age
    need(start==196 and [r['end']-r['start'] for r in phase_results]==[48,96,32],
         'Original contact68/boneburst164/return196 without shortening any of176fields')
    cases=[shake_model(guest,p,3,n,xy) for p,n in ((0x30000,5),(0x50000,10),(0x50000,40))
           for xy in ((932,102),(400,102))]
    # Extra signed/overflow coordinate cases are unit-only, not original choreography.
    cases.extend(shake_model(guest,p,3,5,xy) for p,xy in ((0xfffefffd,(1,1)),(0x00030000,(65535,65534))))
    return dict(phases=phase_results,victimSelfShakeCases=cases,fullVisualFields=176,
        logicalActionBoundaries=dict(start=20,contact=68,boneBurst=164,armReturned=196))


def main():
    need(not OUT.exists() and not visual.native.census(),'Fresh immutable successor and no live native game process')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((PRIOR_OUT/'report.json').read_text())
        need(receipt['passed'] and receipt['sourceOnlyAccepted'] and not receipt['nativeRuntimeAccepted'] and
             all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Actual accepted previous source and all inputs conserved')
        old=(PRIOR_STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
        need(new.count(BEGIN)==new.count(END)==1,'Unique source append markers')
        first=new.index('\n\t'+BEGIN);last=new.index(END)+len(END)
        block=new[first:last]
        need(new[:first-1]+new[last:]==old,'Only one appended source block; no prior source/gameplay changes')
        for leaf in ('midtunit.cpp','midtunit.h'):
            need(sha(STAGE/leaf)==sha(PRIOR_STAGE/leaf),'Host/platform/audio source unchanged')
        prior_harness=json.loads(gzip.open(PRIOR_OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        anchor='\t// KANO_LASER_PALETTE_END'
        need(prior_harness.count(anchor)==1,'Exact preserved actual initializer boundary')
        harness=prior_harness.replace(anchor,anchor+'\n'+block)
        # Use the preserved original base/payload provider; no new ROM files.
        base=palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
        payload=palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
        guest,probe=compile_probe(harness,base,payload)
        previous=bytearray(guest);previous[FIRST:LAST]=b'\xff'*(LAST-FIRST)
        need(hashlib.sha256(previous).hexdigest().upper()==receipt['proposedGuestSHA256'],
             'Actual complete prior initialized guest conserved')
        donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        result=contract(guest,bytes(previous),donor)
        faults=[]
        for name,at in (('intro_pose',0xaf800),('intro_cadence',0xaf808),('sustain_composite',0xaf8a4),
            ('sustain_terminator',0xaf960),('retire_cadence',0xaf978),('phase_entry',0xafa02),
            ('allocator_callback',0xafa08),('pair_target',0xafa0e),('self_actor',0xafb08),
            ('first_native_sleep',0xafb30),('second_native_sleep',0xafb50),('shake_loop',0xafb58),
            ('private_return',0xafb62),('previous_dispatch',0xf436c)):
            wrong=bytearray(guest);wrong[at]^=1
            try:contract(bytes(wrong),bytes(previous),donor)
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Fault accepted: '+name)
        _,model_source=phase_model()
        paths=[Path(__file__),Path(palette.__file__),Path(visual.__file__),PRIOR_OUT/'report.json',
            PRIOR_OUT/'executed_sources.json.gz',ROOT/'mk3/mk3-maincpu.bin',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
            *(STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            previousGoalTurnClassification='no progress: status answer only; revalidated accepted evidence then implemented successor',
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),contract=result,negativeFaultsRejected=faults,
            originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
            latestPlayableChanged=False,limitations=['Internal unbound phase and self-shake helpers, not full laser acceptance.',
                'Unit emitted-word execution is not native runtime evidence.',
                'True victim pose/offset/camera, grey smoke/bones, sound/priority and human/CPU action still require full integration and earned tests.',
                'Full14requirements/sixremainingworkgroups and verified CMD/release remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
             'Full original natural-game scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:
            json.dump(dict(actualNewInitializerHarness=harness,actualAppendedBlock=block,actualPhaseModel=model_source),stream)
        need(probe.parent.resolve()==OUT.resolve(),'Exact terminal generated source probe only');probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,guest=report['proposedGuestSHA256'],faults=len(faults),
            fullVisualFields=176,nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:
            json.dump(dict(actualInitializerHarness=harness),stream)
        raise


if __name__=='__main__':main()
