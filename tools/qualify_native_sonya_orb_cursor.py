"""Correct the runtime-proven orb cursor overrun; source-only acceptance.

Conserves the failed private candidate and its native tests. Executes the
actual whole C++ initializer, decodes the new helper, and applies native
CMPI.W/CMPI.L semantics rather than the old incorrect low-word-only mock.
No emulator, public launcher, guest write, ROM copy or release promotion.
"""
import gzip
import hashlib
import inspect
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_sonya_orb_dispatch as prior

ROOT=prior.ROOT
STAGE=ROOT/'source_native_sonya_orb_cursor'
OUT=ROOT/'audit_native_sonya_orb_cursor_source'
need,sha,address=prior.need,prior.sha,prior.address
OLD='\tleg_code({0x09af,0x0100,0x0b49,uint16_t(~native_address(orb_motion_groups_end))});'
NEW='''\t// A9 is a full 32-bit ROM address. CMPI.W sign-extends its complemented
\t// 16-bit operand; comparing only C080h never matches FFD6C080h and lets
\t// the next draw consume FFFFFFFF filler as a composite. Use CMPI.L.
\tleg_code({0x09af,0x0100,0x0b69,uint16_t(~native_address(orb_motion_groups_end)),
\t\tuint16_t((~native_address(orb_motion_groups_end))>>16)});'''
PIN='2BC5A604BF8F1CA9BFCAB31B6CB9ACEB3CFA8F3276D4E50BE1BCDF1866FCB139'


def native_motion_units():
    motion=prior.prior.motion
    code=inspect.getsource(motion.CPU)
    old_coords='''            elif op==0xbb20:
                source_offset,destination_offset=word(),word()
                self.store(self.reg[0]+destination_offset,self.load(self.reg[1]+source_offset,1),1)
'''
    new_coords='''            elif op&0xfe00 in (0xb800,0xba00):
                source_offset,destination_offset=word(),word()
                src,dst,field=(op>>5)&15,op&15,(op>>9)&1
                self.store(self.reg[dst]+destination_offset,self.load(self.reg[src]+source_offset,field),field)
'''
    old_cmp='''            elif op in (0x0b45,0x0b44,0x0b42,0x0b49):
                reg=op&15; expected=(~word())&0xffff
                self.zero=(self.reg[reg]&0xffff)==expected
                self.hi=(self.reg[reg]&0xffff)>expected
'''
    new_cmp='''            elif op&0xfff0 in (0x0b40,0x0b60):
                reg=op&15
                if op&0xfff0==0x0b40:
                    value=(~word())&0xffff
                    expected=(value|0xffff0000) if value&0x8000 else value
                else:
                    expected=(~longword())&0xffffffff
                self.zero=self.reg[reg]==expected
                self.hi=self.reg[reg]>expected
'''
    need(code.count(old_coords)==code.count(old_cmp)==1,'Both frozen unit-model defects identified exactly')
    namespace=dict(vars(motion))
    exec(compile(code.replace(old_coords,new_coords).replace(old_cmp,new_cmp),'<native motion compare successor>','exec'),namespace)
    exec(compile(inspect.getsource(motion.unit_cases),'<preserved motion cases>','exec'),namespace)
    return namespace['unit_cases'],code.replace(old_coords,new_coords).replace(old_cmp,new_cmp)


def compile_probe(code,base,payload,label):
    probe=OUT/(label+'_probe.exe')
    result=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                           '-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/(label+'_compiler.log')).write_text(result.stdout+result.stderr)
    need(result.returncode==0,'Actual '+label+' whole initializer compiled warning-free')
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (OUT/(label+'_exit.json')).write_text(json.dumps(dict(nativeExit=result.returncode,bytes=len(result.stdout)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base),'Actual '+label+' whole initialized guest retained in RAM')
    return result.stdout,probe


def fields(line):return dict(re.findall(r'(\w+)=([^\s]+)',line))


def failure_evidence():
    first=ROOT/'audit_native_sonya_orb_earned_p1'
    trace=ROOT/'audit_native_sonya_orb_cursor_trace_p1'
    receipts=[json.loads((folder/'report.json').read_text()) for folder in (first,trace)]
    need(all(r['nativeExit']==0 and r['transportOnlyAccepted'] and not r['finisherAccepted'] and
             not r['latestPlayableChanged'] and all(sha(p)==h for p,h in r['inputHashes'].items()) for r in receipts),
         'Both actual terminal failed-game receipts and every executed input conserved')
    text=[gzip.open(folder/'run.log.gz','rt').read() for folder in (first,trace)]
    frames=[[fields(l) for l in t.splitlines() if l.startswith('MK2_ORB_RGB_DIGEST ')] for t in text]
    need(len(frames[0])==len(frames[1])==15 and frames[0]==frames[1],
         'All fifteen actual trace rasters byte-digests match the fifteen visually inspected failed-game rasters')
    children=[fields(l) for l in text[1].splitlines() if l.startswith('MK2_ORB_CHILD ')]
    by_age={int(r['age']):r for r in children}
    need(by_age[84]['cursor']=='FFD6C080' and by_age[84]['pose']=='FE840020' and
         by_age[87]['pose']=='FFFFFFFF' and by_age[88]['cursor']=='FFD6C0A0',
         'Actual native cursor crosses its four-group limit and submits FF filler as a composite')
    compares=list(dict.fromkeys(l for l in text[1].splitlines() if l.startswith('MK2_ORB_TRACE ') and 'pc=FFD6CF90 ' in l))
    need(any('age=84 ' in l and 'a9=FFD6C080 ' in l and 'word=0B49 next=3F7F' in l for l in compares),
         'Actual executed narrow compare cannot equal the observed full address')
    need(all('completed=-1 bones=0 clouds=0' in t for t in text), 'Neither real game reaches winner/bone/ash continuation')
    return dict(nativeGameCount=2,actualFailedFrames=frames[0],
                actualNativeCursorEvidence=[by_age[n] for n in (75,78,81,84,87,88)],
                actualCompareEvidence=compares,
                failedVisualReview='First game: all15 actual rasters reviewed; normal intro, red orb, stripes at90, missing actors and stalled arena through750. Successor trace has identical15 raster digests.',
                passiveTraceLimitation='Read tap also reads its own opcode; repeated reentrant observations are deduplicated, not counted as distinct executions. No guest/register writes.',
                finisherAccepted=False),[folder/leaf for folder in (first,trace) for leaf in ('report.json','run.log.gz')]


def main():
    need(not OUT.exists() and not prior.prior.visual.native.census(),'Fresh evidence; no native game live')
    OUT.mkdir();old_code=new_code=unit_code=''
    try:
        receipt=json.loads((prior.OUT/'report.json').read_text())
        need(sha(prior.OUT/'report.json')==PIN and all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Exact frozen failed private source proof')
        old_source=(prior.STAGE/'midtunit_m.cpp').read_text();new_source=(STAGE/'midtunit_m.cpp').read_text()
        need(old_source.count(OLD)==new_source.count(NEW)==1 and new_source==old_source.replace(OLD,NEW),
             'Only actual 32-bit cursor comparison changes; all other source conserved')
        for leaf in ('midtunit.h','midtunit.cpp'):need(sha(STAGE/leaf)==sha(prior.STAGE/leaf),'Platform and audio unchanged')
        evidence,evidence_paths=failure_evidence()
        ops=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
        cpu_source=ops.read_text()
        need('int32_t t = (int16_t)~PARAM_WORD();' in cpu_source and 'int32_t t = ~PARAM_LONG();' in cpu_source,
             'Authoritative native CPU compares full destination against sign-extended word or complete long operand')
        old_code=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        need(old_code.count(OLD)==1,'Exactly one executed failed initializer compare')
        new_code=old_code.replace(OLD,NEW)
        base=prior.prior.visual.prior.expected();payload=prior.prior.effects.PAYLOAD.read_bytes()
        old,old_probe=compile_probe(old_code,base,payload,'failed')
        need(hashlib.sha256(old).hexdigest().upper()==receipt['proposedGuestSHA256'],'Actual failed initialized guest conserved')
        guest,probe=compile_probe(new_code,base,payload,'cursor')
        # Independent exact encoder for this non-yielding helper only.
        modeled=bytearray(old);modeled[0xad9e0:0xada40]=b'\xff'*0x60
        a=prior.prior.motion.Assembler(modeled,0xad9e0,0xada40)
        a.words(0x9720,0xa30f,0xb7a8,0x190);a.call(0xff838790);a.words(0x09af,0x100)
        end=address(0xad810);a.words(0x0b69,(~end)&0xffff,((~end)>>16)&0xffff)
        skip=a.branch(0xcb80);a.movi(9,address(0xad800));a.here(skip);a.words(0x0960)
        need(guest==bytes(modeled),'Whole actual guest equals independent long-compare model; every outside byte conserved')
        units,unit_code=native_motion_units()
        try:units(old)
        except ValueError as error:old_rejection=str(error)
        else:raise ValueError('Runtime-failed old guest admitted by real native compare semantics')
        cases=units(guest)
        _,factory=prior.prior.corrected_units();factories=[factory(guest,e) for e in (0xae900,0xaed00)]
        parser=prior.unit_cases(guest)
        faults=[]
        compare=0xad9f2
        need(struct.unpack_from('<H',guest,compare)[0]==0x0b69,'Exact generated full compare byte position')
        for name,offset in (('word_opcode',compare),('low_limit',compare+2),('high_limit',compare+4)):
            wrong=bytearray(guest);wrong[offset]^=0x20 if name=='word_opcode' else 1
            try:units(bytes(wrong))
            except (ValueError,IndexError,struct.error) as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Bad actual cursor bound accepted: '+name)
        binary=OUT/'helper.bin';binary.write_bytes(guest[0xad9e0:0xada40])
        decoded=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                                '-basepc',hex(address(0xad9e0)),'-norawbytes'],capture_output=True,text=True,check=True).stdout
        need('CMPI   FFD6C080h,A9' in decoded and 'CMPI   FFFFC080h,A9' not in decoded,'Native decoder confirms full real four-group limit')
        paths=[Path(__file__),prior.OUT/'report.json',ops,ROOT/'mame-mkp/unidasm.exe',*evidence_paths,
               *(STAGE/leaf for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
                    proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                    initializedByteDeltaFromFailed=sum(a!=b for a,b in zip(old,guest)),
                    initializedGuestByteDelta=sum(a!=b for a,b in zip(base,guest)),
                    actualFailureEvidence=evidence,oldGuestRejectedByCorrectNativeSemantics=old_rejection,
                    motionUnitCases=cases,constructorUnitCases=factories,parserUnitCases=parser,
                    actualCursorFaultsRejected=faults,actualNativeDisassembly=decoded,
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    previousGoalTurnClassification='no progress: status inspection/restatement only',
                    thisGoalTurnClassification='progress: real same-candidate passive trace proves four-frame pointer overrun; successor fixes full native compare and corrected units reject failed guest',
                    originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
                    newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
                    limitations=['New cursor fix still requires private native runtime acceptance.',
                                 'Orb color, victim explosion, audio, cleanup and broader final scope remain incomplete/unaccepted.'])
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        with gzip.open(OUT/'executed_sources.json.gz','wt') as stream:
            json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code,actualCorrectedMotionCPU=unit_code),stream)
        for path in (old_probe,probe,binary):
            need(path.parent.resolve()==OUT.resolve(),'Only own terminal generated probe/slice retired');path.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,oldGuestRejected=old_rejection,motionCases=len(cases),faults=len(faults),guest=report['proposedGuestSHA256'])))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt') as stream:
            json.dump(dict(actualOldInitializerHarness=old_code,actualNewInitializerHarness=new_code,actualCorrectedMotionCPU=unit_code),stream)
        raise


if __name__=='__main__':main()
