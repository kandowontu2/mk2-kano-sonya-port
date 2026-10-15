"""Dedicated CPU finish approach distances, with unchanged native movement/actions."""
import gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_cpu_finisher_dispatch_context as prior
import inspect_native_smoke_callers as disasm
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
STAGE=ROOT/'source_native_cpu_finisher_spacing'
OUT=ROOT/'audit_native_cpu_finisher_spacing_source'
TABLE=0xf395c
PROFILES=(0x00500050,0x00800080)
CHANGES=(
    ('// defensive response and kick-spacing rows also read following code for',
     '// defensive response and finisher-spacing rows also read following code for'),
    ('\t// Packed kick spacing follows the existing independent common MKII attack\n'
     '\t// descriptor grammar (70h/110h); dedicated signature choices remain 22/23.',
     '\t// FF9B42B0 selects a packed pair of CPU finisher approach distances, not\n'
     '\t// ordinary kick spacing. Both performer variants currently enter each\n'
     "\t// fighter's owned finisher. Use that fighter's own FF876F70 command range\n"
     "\t// (Kano 50h, Sonya 80h) in both halves, never Cage's 70h/110h profile."),
    ('{0xff9b4930,0xf395c,0x01100070,0x01100070}',
     '{0xff9b4930,0xf395c,0x00500050,0x00800080}'))

def source_check():
    names=('midtunit_m.cpp','midtunit.h','midtunit.cpp')
    before={n:(ROOT/'source_native_cpu_finisher_dispatch'/n).read_text() for n in names}
    proposed={n:(STAGE/n).read_text() for n in names}
    expected=before['midtunit_m.cpp']
    for old,new in CHANGES:
        need(expected.count(old)==1,'Unique original CPU distance/comment boundary')
        expected=expected.replace(old,new)
    need(proposed['midtunit_m.cpp']==expected and all(proposed[n]==before[n] for n in names[1:]),
         'Whole staged source changes only own CPU distance values and corrected comments')
    return {n:sha(STAGE/n) for n in names}

def expected_guest(base=None):
    if base is None:base=prior.expected()
    need(struct.unpack_from('<2I',base,TABLE+17*4)==(0x01100070,0x01100070),
         'Actually compiled inherited Cage profile diagnosed for both true added IDs')
    guest=bytearray(base);struct.pack_into('<2I',guest,TABLE+17*4,*PROFILES)
    return bytes(guest)

def gate(guest,base):
    need(guest==expected_guest(base),'Entire1MiB guest differs only at two own packed CPU distance rows')
    for ident,parser,limit,action in ((17,0xf5500,80,0xfffaae00),(18,0xf5560,128,0xfffab200)):
        # Exact MOVI.W max-gap,A1; MOVI.L own-action,A7; JA FF876F70.
        command=struct.pack('<7H',0x09c1,limit,0x09e7,action&0xffff,action>>16,0xc080,0x6f70)
        need(guest[parser:parser+0x60].count(command)==1,
             'Actually initialized own human command has independently known native maximum range')
        packed=struct.unpack_from('<I',guest,TABLE+ident*4)[0]
        need((packed&0xffff,packed>>16)==(limit,limit),
             'Both CPU performer variants approach within their actual own human command range')
    need(guest[TABLE:TABLE+68]==base[TABLE:TABLE+68], 'Every existing effective0..16 distance unchanged')
    return True

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable spacing source proof')
    base=prior.expected();guest=expected_guest(base);sources=source_check();gate(guest,base)
    runtime=ROOT/'audit_native_cpu_finisher_repair_regression_checked/report.json'
    accepted=json.loads(runtime.read_text())
    need(accepted['passed'] and accepted['trueCPUKano'] and accepted['noCacheOverrun'] and
         all(sha(p)==h for p,h in accepted['inputHashes'].items()),
         'Actual finite dispatch repair, whole guest, restored source and terminal run conserved')
    code=disasm.disassemble()
    instructions={int(s.split(':',1)[0],16):s.split(':',1)[1].strip() for s in code}
    requirements={0xff9b42b0:'MOVI   FF9B4930h,A0',0xff9b42e0:'CALLA  FF83B7F0h',
        0xff9b4350:'SRL    10h,A0',0xff9b4470:'JA     FF876B80h',
        0xff9b44a0:'ZEXT   A0,0',0xff9b45c0:'JA     FF876B40h',
        0xff9b47a0:'MOVE   A0,A11',0xff9b47b0:'CALLA  FF834CC0h',
        0xff876f70:'CALLA  FF834CC0h',0xff876fa0:'CMP    A1,A3',0xff876fb0:'JRHI   FF877420h'}
    need(all(instructions.get(at)==text for at,text in requirements.items()),
         'Original exact native packed halves lead to first/second finisher, and human max-gap comparison')
    log=gzip.open(ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle/run.log.gz','rt',encoding='utf-8').read()
    live=next(s for s in log.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_LIVE frame=36390 '))
    fields=dict(re.findall(r'(\w+)=([^\s]+)',live))
    gap=abs(int(fields['hpos'].split(',')[0])-int(fields['cpos'].split(',')[0]))
    need(fields['human']=='18:18' and fields['cpu']=='17:17' and fields['health']=='0,109' and gap==111,
         'Actual owned Kano finisher uses observed111pixel gap, exceeding own80pixel command range')
    faults=[]
    for label,at in (('old_Cage_first',TABLE+68),('old_Cage_second',TABLE+70),
        ('wrong_Sonya_first',TABLE+72),('wrong_Sonya_second',TABLE+74),
        ('existing_stock_row',TABLE),('real_ID_lookup',(0xff83b7f0-0xff800000)//8),
        ('native_approach',(0xff9b47a0-0xff800000)//8),('human_Kano_range',0xf5534),
        ('human_Sonya_range',0xf5594),('own_Kano_action',0xf55c0),
        ('own_Sonya_action',0xf5640),('native_cache_loop',(0xff838850-0xff800000)//8)):
        altered=bytearray(guest);altered[at]^=1
        try:gate(bytes(altered),base)
        except ValueError as e:faults.append(dict(name=label,rejected=str(e)))
        else:raise ValueError('Spacing/conservation fault admitted: '+label)
    gate(guest,base)
    changed=[i for i,(a,b) in enumerate(zip(base,guest)) if a!=b]
    need(len(changed)==6 and all(TABLE+68<=i<TABLE+76 for i in changed),'Only six actual row bytes change')
    pins={str(p.resolve()):sha(p) for p in [Path(__file__),Path(disasm.__file__),
        ROOT/'mame-mkp/unidasm.exe',ROOT/'mk2/mk2-maincpu.bin',runtime,*(STAGE/n for n in sources)]}
    report=dict(passed=True,sourceOnlyAccepted=True,nativeRepairAccepted=False,
        stagedSourceHashes=sources,proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
        initializedGuestByteDelta=len(changed),distanceRowStorageBytes=8,
        ownDistanceProfiles=[dict(id=17,first=80,second=80),dict(id=18,first=128,second=128)],
        observedPriorKanoGap=gap,observedPriorGapRow=live,
        nativeConsumerInstructions={f'{at:08X}':text for at,text in requirements.items()},
        actualFaultsRejected=faults,inputHashes=pins,existingRowsActionsControlCacheAudioUnchanged=True,
        noNewSecondFinisherChoreographyClaim=True,nativePositioningVisualReviewStillRequired=True,
        newBuilds=0,publicBuildPromoted=False,fullPortAcceptance=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in
        ('inputHashes','actualFaultsRejected','nativeConsumerInstructions','observedPriorGapRow')},indent=2))
