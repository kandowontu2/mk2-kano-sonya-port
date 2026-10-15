"""Real invalid-callback trap and complete known live-ID AI consumer repair.

Source-only proof. Explicitly stopped diagnostic is never gameplay acceptance.
"""
import copy
import gzip
import hashlib
import json
import struct
from pathlib import Path
import native_attract_bios_context as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
STAGE=ROOT/'source_native_ai_response'
OUT=ROOT/'audit_native_ai_response_source'
RUN=ROOT/'audit_native_attract_error_checked_fetch'
TABLES=(
 (0xff9c3c90,0xf3910,0xff9b9ba0,(0xff9c2d10,0xff9c3c40)),
 (0xff9b4930,0xf395c,0x01100070,(0xff9b42c0,)),
 (0xff9bc980,0xf39a8,0xff9bfa80,(0xff9bc920,)),
 (0xff9bde50,0xf6830,0xff9be070,(0xff9bde00,)),
 (0xff9be7f0,0xf687c,0xff9bea10,(0xff9be7a0,)),
 (0xff9bf750,0xf6f60,0xff9bf320,(0xff9bf2d0,)),
 (0xff9c3310,0xf6fac,0,(0xff9c2e50,)))
def offset(bit):return (bit-0xff800000)//8
def address(byte):return 0xff800000+byte*8
def u32(raw,at):return struct.unpack_from('<I',raw,at)[0]

def failure_gate(snapshot,entry,base):
    need(snapshot['entry']=='FFA1E800' and snapshot['pc']==entry['pc']=='FFA1E810' and
         snapshot['A0']=='00000016' and snapshot['mode']=='1' and snapshot['counter']=='18',
         'Genuine executed illegal-instruction error16, not the earlier ROM self-read')
    need(snapshot['A1']=='FF9C3C90' and snapshot['A8']=='01036960' and snapshot['A13']=='0106F6B0' and
         snapshot['p1_actor_words'].endswith('0012') and snapshot['frame']==entry['frame']=='22631',
         'Actual P1 Sonya18 actor/Main and response-table base retained at the fault')
    words=[int(entry['stack'][i:i+4],16) for i in range(0,16,4)]
    saved_pc=words[2]|words[3]<<16
    callback=u32(base,offset(0xff9c3c90)+18*4)
    need(callback==0xed9a0d3f and saved_pc==(callback&~15)+16==0xed9a0d40,
         'Actual trap saves the next aligned fetch of Sonya18 table cell containing CALLR instructions')
    need(all(r['writes']=='0' and r['assistance']=='none' for r in (snapshot,entry)), 'Entire error provenance passive')
    # Read the complete original common lookup grammar directly, pinned below;
    # original unidasm confirms MOVE A0,A1; MOVE *A8(1F0h),A0,0;
    # SLL 5h,A0; ADD A1,A0; MOVE *A0,A0,1; RETS through FF83B850.
    words=struct.unpack_from('<7H',base,offset(0xff83b7f0))
    need(words==(0x4c01,0xb500,0x01f0,0x24a0,0x4020,0x8600,0x0960),
         'Whole original dispatcher reads actual A8 ID, scales32bits, dereferences pointer and returns')
    return dict(actualIllegalTarget=f'{callback:08X}',savedFaultPC=f'{saved_pc:08X}',trueActorID=18,actualResponseTableBase=snapshot['A1'])

def source_check():
    names=('midtunit_m.cpp','midtunit.h','midtunit.cpp')
    texts={n:(STAGE/n).read_text() for n in names}
    old={n:(ROOT/'source_native_attract_bios'/n).read_text() for n in names}
    marker='\n\n\t// The ordinary-human AI response dispatcher indexes the actual actor ID.\n'
    a=texts['midtunit_m.cpp'].index(marker)
    b=texts['midtunit_m.cpp'].index('\n}\n\n\nvoid midtunit_state::init_mk2ks_native_selector()',a)
    need(texts['midtunit_m.cpp'][:a]+texts['midtunit_m.cpp'][b:]==old['midtunit_m.cpp'],
         'Entire old host audio, movements, selector, portraits, bios, graphics and engine source unchanged')
    need(all(texts[n]==old[n] for n in ('midtunit.h','midtunit.cpp')), 'No host members, machine/DCS/channel/sample configuration changes')
    addition=texts['midtunit_m.cpp'][a:b]
    for original,destination,value,operands in TABLES:
        need(f'{{0x{original:x},0x{destination:x},' in addition, 'Every independently reviewed table is staged')
    return {n:sha(STAGE/n) for n in names}

def expected_guest(base=None):
    if base is None:base=prior.expected()
    guest=bytearray(base)
    for source,destination,value,operands in TABLES:
        need(base[destination:destination+76]==b'\xff'*76,'Each entire new nineteen-ID table uses genuinely erased, disjoint storage')
        guest[destination:destination+68]=base[offset(source):offset(source)+68]
        struct.pack_into('<II',guest,destination+68,value,value)
        for operand in operands:
            need(u32(base,offset(operand))==source,'Every original whole MOVI pointer operand matches actual reviewed consumer')
            struct.pack_into('<I',guest,offset(operand),address(destination))
    return bytes(guest)

def guest_gate(guest,base):
    expected=expected_guest(base)
    need(guest==expected,'Whole1MiB guest equals exact seven tables and eight pointer operands; no bypass/ID aliases/new code')
    for source,destination,value,operands in TABLES:
        need(guest[destination:destination+68]==base[offset(source):offset(source)+68], 'Every existing effective0..16 result conserved byte-for-byte')
        need(tuple(struct.unpack_from('<2I',guest,destination+68))==(value,value),'Independent real17/18 rows, never following instructions')
    need(guest[0xf4900:0xf49e0]==base[0xf4900:0xf49e0], 'All41 stock photographs, four endings and two owned biographies conserved')

def main():
    need(not OUT.exists(),'Fresh immutable actual diagnosis/source proof')
    transport=json.loads((RUN/'report.json').read_text())
    stopped=json.loads((RUN/'explicit_diagnostic_stop.json').read_text())
    need(not transport['passed'] and stopped['nativeExit']==transport['nativeTerminal']['nativeExit']==4294967295 and
         stopped['explicitlyStoppedAfterConfirmedError'] and not stopped['fullPortAcceptance'],
         'Explicitly stopped observed native failure preserved; no fabricated full-route/transport/gameplay success')
    need(len(stopped['actualErrorRegisterSnapshots'])==len(stopped['actualErrorEntryRecords'])==1,'Single genuine instruction-fetch guarded failure entry')
    base=prior.expected()
    snap,entry=stopped['actualErrorRegisterSnapshots'][0],stopped['actualErrorEntryRecords'][0]
    cause=failure_gate(snap,entry,base)
    faults=[]
    for label,key,value in (('ROM self-read instead of executing failure','pc','FFA59F10'),
                            ('wrong AI table base','A1','FF9B2210'),
                            ('proxy actor ID','counter','1'),
                            ('wrong illegal instruction PC','stack','003080200D40FF9C')):
        bad=copy.deepcopy(snap)
        badentry=copy.deepcopy(entry)
        if key=='stack':badentry[key]=value
        else:bad[key]=value
        try:failure_gate(bad,badentry,base)
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Corrupted real native fault unexpectedly accepted')
    sources=source_check();guest=expected_guest(base);guest_gate(guest,base)
    for label,at in (('old Sonya instruction callback',0xf3910+72),('new response wrong stock row',0xf3910),
                     ('unrelated sound marker',0xffbce),('new kick spacing corrupt',0xf395c+68)):
        bad=bytearray(guest);bad[at]^=1
        try:guest_gate(bytes(bad),base)
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Bad expected guest admitted')
    with gzip.open(RUN/'executed_sources.json.gz','rt',encoding='utf-8') as f:archive=json.load(f)
    for path,row in archive.items():
        # The original archive used read_text(), normalizing mixed CRLF/LF in
        # one inherited helper. Bind both its entire normalized text and the
        # still-present exact original bytes, not a guessed newline encoding.
        need(Path(path).read_text()==row['text'] and sha(path)==row['sha256']==transport['inputHashes'][path],
             'Every actually executed whole source: archived text plus exact original byte hash')
    paths=[Path(__file__).resolve(),Path(prior.__file__),RUN/'report.json',RUN/'run.log.gz',RUN/'explicit_diagnostic_stop.json',RUN/'executed_sources.json.gz',ROOT/'mk2/mk2-maincpu.bin']
    pins={str(p):sha(p) for p in paths}
    pins.update({path:sha(path) for path in archive})
    for name in sources:pins[str(STAGE/name)]=sha(STAGE/name)
    result=dict(passed=True,sourceOnlyAccepted=True,nativeFixAccepted=False,fullPortAcceptance=False,
      actualDiagnosis=cause,actualErrorSnapshot=snap,actualErrorEntry=entry,explicitNativeStop=stopped,
      stagedSourceHashes=sources,proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
      expectedGuestChangedBytes=sum(a!=b for a,b in zip(base,guest)),
      knownAdditionalLiveIDTables=7,pointerConsumers=8,oldEffectiveResultsPreserved=119,
      ownCharacterSignatureSlotsPreserved=[22,23],actualRecordFaultsRejected=faults,inputHashes=pins,
      scope='Seven known truncated live-ID AI tables: native response/defense continuations, packed common-attack kick spacing, optional general defensive sequence. Actor identities and character-specific specials preserved. Full native runtime regression required.',
      publicBuildPromoted=False,goalStatus='active')
    OUT.mkdir()
    with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as f:json.dump({str(p):dict(sha256=sha(p),text=p.read_text()) for p in [Path(__file__).resolve(),*(STAGE/name for name in sources)]},f)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','sourceOnlyAccepted','proposedGuestSHA256','expectedGuestChangedBytes','knownAdditionalLiveIDTables','nativeFixAccepted')}))

if __name__=='__main__':main()
