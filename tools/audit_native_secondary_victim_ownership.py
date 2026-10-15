"""Structural ownership of second-finisher victim streams, not gameplay.

Re-execute the actual qualified initializer into RAM, follow the native
true-ID selector and every crouch/stumble component, then compare native
stock descriptors or the correct original Kano/Sonya art. Bosses are
reported separately: their main35 cells are not normal victim streams.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import traceback
from pathlib import Path

import qualify_native_secondary_finisher_contracts as contracts
import build_mk2ks_mk3 as art

ROOT = contracts.ROOT
OUT = ROOT/'audit_native_secondary_victim_ownership'
PIN = '409853F6E5CCF1EE432CD2B3CF24692B5294240574C12AAFDCECA33A9759E31E'
need, sha = contracts.need, contracts.sha


def inspect_streams(guest, payload, original, donor):
    def data(pointer, size):
        need(pointer&15==0, 'Actual native victim pointer is word-aligned')
        if pointer>=0xff800000:
            source,at = guest,(pointer-0xff800000)//8
        elif 0xfe800000<=pointer<0xff800000:
            source,at = payload,(pointer-0xfe800000)//8
        else:raise ValueError(f'Invalid native victim address {pointer:08X}')
        need(at>=0 and at+size<=len(source), 'Entire native victim record fits real ROM region')
        return source[at:at+size]
    def word(pointer):return struct.unpack('<I',data(pointer,4))[0]
    def stream(pointer):
        groups=[]
        for step in range(32):
            value=word(pointer+step*32)
            if not value:
                need(groups, 'Nonempty native victim animation before its own phase terminator')
                return groups
            need(value>=0xfe800000, 'Victim crouch/stumble is a genuine group stream, not executable/token data')
            frames=[]
            for component in range(8):
                frame=word(value+component*32)
                if not frame:break
                record=data(frame,14)
                width,height=struct.unpack_from('<HH',record)
                need(0<width<200 and 0<height<220, 'Every native victim component has valid body dimensions')
                frames.append((frame,record))
            else:raise ValueError('Native victim composite lacks component terminator')
            need(frames, 'Native victim composite is not empty/hidden proxy')
            groups.append((value,frames))
        raise ValueError('Native victim phase lacks finite native terminator')
    table=word(0xff9060a0)
    need(table==0xfffe4000, 'Actual native true-ID main selector points to the complete 19-row table')
    rows=[]
    for ident in range(19):
        root=word(table+ident*32)
        if ident in (12,13):
            rows.append(dict(identity=ident,mainRoot=f'{root:08X}',normalVictimStreamsAccepted=False,
                             reason='Original bosses have no ordinary main35 victim phase; preserve native boss finish-mode immunity before activation.'))
            continue
        if ident<17:
            native_root=struct.unpack_from('<I',original,art.MK2_MAIN_TABLE+ident*4)[0]
            need(root==native_root, 'Stock/secret victim keeps its exact original character main root')
        for index,donor_index in ((5,4),(35,32)):
            pointer=word(root+index*32)
            groups=stream(pointer)
            if ident<17:
                expected=struct.unpack_from('<I',original,art.stock_file(root)+index*4)[0]
                need(pointer==expected, 'Actual stock/secret victim uses its own original animation, never another ID')
                for group,frames in groups:
                    expected_frames=[]
                    for component in range(8):
                        frame=struct.unpack_from('<I',original,art.stock_file(group)+component*4)[0]
                        if not frame:break
                        expected_frames.append((frame,original[art.stock_file(frame):art.stock_file(frame)+14]))
                    need(frames==expected_frames, 'Every native stock victim component and descriptor remains exact original data')
            else:
                donor_root,block=(art.KANO_MAIN,art.KANO_BLOCK) if ident==17 else (art.SONYA_MAIN,art.SONYA_BLOCK)
                spans=art.sequence_spans(donor,donor_root,block,(donor_root,art.KANO_SPECIAL if ident==17 else art.SONYA_SPECIAL))
                start,end=spans[donor_index]
                references=art.group_references(donor,start,end,*block)
                expected_groups=[]
                for _,group,frames in references:
                    records=[]
                    for frame in frames:
                        record=bytearray(donor[art.stock_file(frame):art.stock_file(frame)+14])
                        struct.pack_into('<I',record,8,struct.unpack_from('<I',record,8)[0]+art.GFX_REBASE)
                        records.append(bytes(record))
                    expected_groups.append(records)
                need(expected_groups, 'Correct added victim has original character-owned crouch/stumble groups')
                for _,frames in groups:
                    need([record for _,record in frames] in expected_groups,
                         'Added victim composite exactly matches its own original art, including DMA/shape/origin, with only existing graphics rebase')
                other=word(word(table+(18 if ident==17 else 17)*32)+index*32)
                need(pointer!=other, 'Kano and Sonya own separate native victim streams')
            rows.append(dict(identity=ident,animation=index,nativeStream=f'{pointer:08X}',
                             semantic='crouch' if index==5 else 'stumble',groups=len(groups),
                             components=sum(len(frames) for _,frames in groups),originalOwnedArt=True))
    return rows


def main():
    need(not OUT.exists() and not contracts.visual.native.census(), 'Fresh victim evidence; no native game live')
    OUT.mkdir();harness=''
    try:
        receipt=json.loads((contracts.OUT/'report.json').read_text())
        need(sha(contracts.OUT/'report.json')==PIN and receipt['passed'] and receipt['sourceOnlyAccepted'] and
             not receipt['nativeRuntimeAccepted'] and all(sha(p)==h for p,h in receipt['inputHashes'].items()),
             'Actual corrected guest/source/CPU semantic proof unchanged')
        harness=json.loads(gzip.open(contracts.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        probe=OUT/'victim_initializer_probe.exe'
        compiled=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                                 '-x','c++','-','-o',str(probe)],input=harness,text=True,capture_output=True)
        (OUT/'compiler.log').write_text(compiled.stdout+compiled.stderr)
        need(compiled.returncode==0, 'Actual qualified C++ initializer compiles warning-free')
        base=contracts.visual.prior.expected();payload=contracts.effects.PAYLOAD.read_bytes()
        run=subprocess.run([str(probe)],input=base+payload,capture_output=True)
        (OUT/'native_exit.json').write_text(json.dumps(dict(nativeExit=run.returncode,stdoutBytes=len(run.stdout),stderrBytes=len(run.stderr)),indent=2)+'\n')
        (OUT/'initializer.stderr').write_bytes(run.stderr)
        guest=run.stdout
        need(run.returncode==0 and len(guest)==len(base) and hashlib.sha256(guest).hexdigest().upper()==receipt['expectedGuestSHA256'],
             'Actual whole successor guest re-executed in RAM with exact accepted hash')
        original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        rows=inspect_streams(guest,payload,original,donor)
        accepted=[row for row in rows if row.get('originalOwnedArt')]
        need(len(accepted)==34, 'Both own victim phases qualified for all 17 ordinary/secret/added identities; bosses not misrepresented')
        selector=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(ROOT/'mk2/mk2-maincpu.bin'),'-arch','tms34010',
                                 '-basepc','0xff800000','-norawbytes'],text=True,capture_output=True,check=True)
        lines={int(l.split(':',1)[0],16):l.split(':',1)[1].strip() for l in selector.stdout.splitlines()}
        facts={0xff9060c0:'MOVE   *A8(1F0h),A0,0',0xff9060e0:'SLL    5h,A0',
               0xff9060f0:'ADD    A14,A0',0xff906100:'MOVE   *A0,A0,1',
               0xff906110:'SLL    5h,A9',0xff906120:'ADD    A0,A9',0xff906130:'MOVE   *A9,A9,1'}
        need(all(lines.get(pc)==text for pc,text in facts.items()), 'Actual shared native selector consumes true A8 actor identity, never a proxy global')
        faults=[]
        for ident,index in ((0,5),(8,35),(17,5),(17,35),(18,5),(18,35)):
            wrong=bytearray(guest);root=struct.unpack_from('<I',guest,0xfc800+ident*4)[0]
            data,at=(wrong,art.stock_file(root)+index*4) if root>=0xff800000 else (bytearray(payload),(root-0xfe800000)//8+index*4)
            struct.pack_into('<I',data,at,0)
            try:inspect_streams(bytes(wrong),bytes(data) if data is not wrong else payload,original,donor)
            except ValueError as error:faults.append(dict(identity=ident,animation=index,rejected=str(error)))
            else:raise ValueError('Invalid actual victim stream pointer admitted')
        paths=[Path(__file__),contracts.OUT/'report.json',contracts.OUT/'executed_sources.json.gz',
               ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',contracts.effects.PAYLOAD,
               ROOT/'tools/build_mk2ks_mk3.py',ROOT/'mame-mkp/unidasm.exe']
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
                    expectedGuestSHA256=receipt['expectedGuestSHA256'],trueIdentityVictimRows=rows,
                    acceptedOrdinarySecretAddedStreams=len(accepted),unacceptedBossVictimIDs=[12,13],
                    originalNativeSelectorFacts={f'{p:08X}':s for p,s in facts.items()},faultRejections=faults,
                    inputHashes={str(p.resolve()):sha(p) for p in paths},
                    originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
                    originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],goalStatus='active',
                    gameBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
                    limitations=['Structural real-actor selector and complete first native animation phases only; no rendered or live reaction acceptance.',
                                 'Original bosses have no ordinary stumble phase; native immunity/finish-mode routing must be preserved and tested.',
                                 'Input/CPU binding, new sounds, real native effects/cleanup and all full-goal work remain.'],
                    nextAction='Qualify native worker handoff and finish-mode/boss rejection; bind adapted Sonya second command/CPU distance in a private successor and physically earn/test the action.')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        need(probe.parent.resolve()==OUT.resolve(), 'Only this exact generated initializer probe is temporary')
        probe.unlink()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,
                              ownVictimStreams=len(accepted),bossIDsNotClaimedAccepted=[12,13],faultRejections=len(faults))))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False,failure=traceback.format_exc(),nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(checker=dict(sha256=sha(Path(__file__)),text=Path(__file__).read_text()),actualInitializerHarness=harness),stream)


if __name__=='__main__':main()
