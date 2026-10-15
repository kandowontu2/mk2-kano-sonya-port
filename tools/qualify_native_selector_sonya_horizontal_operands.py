"""Every actual Bicycle x/vx write bound to full native source operands.

Whole32 pre-values/ordered low-high masked replay retained. Decode original
MOVE register/offset and MMTM register-list writes using complete A registers
and field-width status, rather than accepting data/address alone. No replay.
"""
import json
import re
import struct
import traceback
from pathlib import Path
import capture_native_selector_sonya_horizontal_operands as capture
import qualify_native_selector_sonya_shadow_geometry as geometry
import qualify_native_selector_sonya_shadow_bound_faults_words as prior

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_checked'


def replay_binding():
    return prior.complete_before(geometry.coverage_bindings())


def gate(text,guest):
    geometry.coverage.original.phases.original.phase_source.source_gate(text,guest)
    result=replay_binding()(text,guest)
    rows=[r for r in capture.base.choices.native_state.rows(text,'MK2_SONYA_HORIZONTAL_STORE')
          if r['slot']=='2'and 3191<=int(r['frame'])<=3252]
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    ranges=((0xff804000,0xff804110),(0xff8054e0,0xff805680),(0xff83cc20,0xff83cd50),
            (0xff80f6b0,0xff80f740),(0xff828570,0xff8285d0))
    for lo,hi in ranges:
        a,b=((v-0xff800000)//8 for v in (lo,hi))
        need(guest[a:b]==stock[a:b],'Complete original native motion/store/clamp routines unchanged')
    sites={0xff805630:(0xb062,0x90,16),0xff805580:(0xb282,0x40,32),
           0xff83ccd0:(0xb048,0x90,16),0xff80f700:(0xb228,0x40,32),
           0xff8285b0:(0xb2e9,0x40,32)}
    counted={};records=[]
    for r in rows:
        pc=int(r['pc'],16);at=int(r['at'],16);data=int(r['data'],16)
        regs={n:int(r['a'+str(n)],16)for n in range(15)}
        status=int(r['status'],16)
        if pc==0xff8040b0:
            need(struct.unpack_from('<HH',guest,(pc-32-0xff800000)//8)==(0x0983,0x00c0),
                 'Original actual MMTM A3,A8,A9 source instruction/list')
            # MMTM decrements A3 by32 before WLONG(A3,A9). A3 is therefore
            # already the real target at each of the two memory callbacks.
            need(r['kind']=='x'and regs[3]==0x01035120 and at in (regs[3],regs[3]+16),
                 'Actual updated MMTM A3 pointer and both native x target words')
            bit=at-regs[3];value=regs[9];src=9;dst=3;width=32
        else:
            need(pc in sites,'Every real Bicycle horizontal store source site inventoried')
            op,offset,width=sites[pc]
            need(struct.unpack_from('<HH',guest,(pc-32-0xff800000)//8)==(op,offset)and not(op&16),
                 'Original actual MOVE register-to-offset source and A-register bank')
            src=(op>>5)&15;dst=op&15;target=(regs[dst]+offset)&0xffffffff
            field=1 if op&0x200 else 0
            actual_width=(status>>(6 if field else 0))&31
            actual_width=actual_width or 32
            need(actual_width==width,'Actual CPU field-width status agrees with original16/32-bit store')
            bit=at-target
            need(bit in ((0,16)if width==32 else(0,))and
                 target==0x010350a0+(0x80 if r['kind']=='x'else 0x40)+(16 if width==16 else 0),
                 'Actual destination register/offset and low/high native write address')
            value=regs[src]
        need(int(r['mask'],16)==65535 and data==((value>>bit)&65535),
             'Every actual native data word comes from its independently captured source register')
        counted[r['pc']]=counted.get(r['pc'],0)+1
        records.append(dict(frame=int(r['frame']),pc=r['pc'],kind=r['kind'],at=r['at'],
            sourceRegister=src,destinationRegister=dst,sourceValue=f'{value:08X}',
            destinationValue=f'{regs[dst]:08X}',status=r['status'],
            actualWordBit=bit,fieldWidth=width,data=r['data']))
    index=0
    while index<len(records):
        a=records[index]
        if a['fieldWidth']==32:
            need(index+1<len(records),'No missing high half of actual32-bit instruction')
            b=records[index+1]
            need(a['actualWordBit']==0 and b['actualWordBit']==16 and
                 int(b['at'],16)==int(a['at'],16)+16 and
                 all(a[k]==b[k]for k in ('frame','pc','kind','sourceRegister','destinationRegister',
                     'sourceValue','destinationValue','status','fieldWidth')),
                 'Both native halves of one instruction retain the entire independently observed operand values')
            index+=2
        else:index+=1
    need(len(rows)==310 and sum(counted.values())==310 and len(counted)==6,
         'Every original native horizontal write and all six source sites covered')
    return dict(passed=True,wholeOrderedMaskedWordReplay=result,sourceOperandSites=counted,
        everyActualSourceRegisterAndDestinationExact=True,completeSourceBoundOperandStores=records,
        completeHorizontalNativeWritesAccepted=True,allContactsArenasAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh complete native operand qualification')
    path=capture.OUT/'report.json';receipt=json.loads(path.read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(receipt['passed']and held['process'].poll()==receipt['nativeExit']==0 and
         held['identity']==receipt['actualNativeIdentity'],'Same actual new native original terminal0 capture')
    pins=dict(receipt['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every complete source/native input pin unchanged')
    _,text,_=capture.RAM_CASES[capture.KEY];positive=gate(text,state['guest']);faults=[]
    def change(key,value,**where):
        line=next(l for l in text.splitlines()if l.startswith('MK2_SONYA_HORIZONTAL_STORE ')and
            all(dict(re.findall(r'(\w+)=([^\s]+)',l)).get(k)==str(v)for k,v in where.items()))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Actual effective previously missing native operand corruption')
        return text.replace(line,changed,1)
    trials=[]
    for pc,key,value in (('FF8040B0','a9','00000000'),('FF8040B0','a3','01000000'),
                         ('FF805630','a3','0000003D'),('FF805630','a2','01000000'),
                         ('FF805580','a4','00000001'),('FF805580','a2','01000000'),
                         ('FF83CCD0','a2','00000000'),('FF83CCD0','a8','01000000'),
                         ('FF80F700','a1','00000001'),('FF80F700','a8','01000000'),
                         ('FF8285B0','a7','00000000'),('FF8285B0','a9','01000000'),
                         ('FF805630','status','00000000'),('FF8285B0','status','00000400')):
        trials.append((pc+'_'+key,change(key,value,slot=2,pc=pc,
                        frame=3232 if pc in ('FF8040B0','FF805630','FF805580','FF8285B0')else3191)))
    for label,bad in trials:
        try:gate(bad,state['guest'])
        except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual previously missing source operand corruption admitted: '+label)
    need(gate(text,state['guest'])==positive,'Whole untouched310-write positive restored')
    for p in (Path(__file__),path,Path(prior.__file__),Path(geometry.__file__),
              ROOT/'mk2/mk2-maincpu.bin',ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx',
              ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Executed source/native evidence never overwritten');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All original source/evidence pins after effective full-operand faults')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeCurrentBicycleHorizontalOperands=positive,effectiveOperandFaultsRejected=faults,inputHashes=pins,
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        wholeBicycleLifecycleAccepted=False,wholeSavedDisplayAccepted=False,wholeSourceAudioAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS310 actual Bicycle x/vx writes, full source/destination operands and14 effective faults',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual complete operand qualification rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
