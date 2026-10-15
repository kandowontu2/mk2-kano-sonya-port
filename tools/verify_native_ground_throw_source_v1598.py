"""Exact source-built native throw index delta; not whole-port acceptance."""
import argparse,json,struct,re
from pathlib import Path
import verify_active_launch_timer_v1520 as prior
ROOT=prior.ROOT
NAME='diagnostic_v1597_native_ground_throw'
OUT=ROOT/'audit_v1598_native_ground_throw_source_checked'
HOOK=(0xff8b6e30-0xff800000)//8
ROUTER=0xfc200
BASE=0xff800000+ROUTER*8
def expected():
    old,_,payload=prior.expected_guest()
    assert old[ROUTER:ROUTER+0x80]==b'\xff'*0x80
    assert old[HOOK:HOOK+10]==struct.pack('<5H',0x0b09,42,0x0d5f,0x2d90,0xff84)
    new=bytearray(old)
    own=BASE+0x24*8
    words=(0x0b49,0xffee,0xca80,own&65535,own>>16,
           0x0b49,0xffed,0xca80,own&65535,own>>16,
           0x0b09,42,0x0d5f,0x2d90,0xff84,0xc080,0x6e80,0xff8b,
           0x09c9,43,0x0d5f,0x2d90,0xff84,0xc080,0x6e80,0xff8b)
    code=struct.pack('<26H',*words)
    new[ROUTER:ROUTER+len(code)]=code
    new[HOOK:HOOK+10]=struct.pack('<5H',0xc080,BASE&65535,BASE>>16,0x0300,0x0300)
    return bytes(new),old,payload
def run_router(raw,index):
    pc=BASE;a9=index;eq=False;requests=[]
    for _ in range(12):
        at=(pc-0xff800000)//8
        op,imm=struct.unpack_from('<2H',raw,at)
        if op==0x0b49:eq=a9==((~imm)&65535);pc+=32
        elif op==0xca80:
            target=struct.unpack_from('<I',raw,at+2)[0];pc=target if eq else pc+48
        elif op==0x0b09:a9+=imm;pc+=32
        elif op==0x09c9:a9=imm;pc+=32
        elif op==0x0d5f:
            target=struct.unpack_from('<I',raw,at+2)[0]
            assert target==0xff842d90
            requests.append(a9);pc+=48
        elif op==0xc080:
            target=struct.unpack_from('<I',raw,at+2)[0]
            assert target==0xff8b6e80
            assert requests==[43 if index in(17,18)else index+42]
            return dict(actualAttackerIndex=index,victimMainAnimation=requests[0],nativeLookupCall=hex(0xff842d90),nativeReturn=hex(target))
        else:raise AssertionError('Unexpected instruction '+hex(op))
    raise AssertionError('Non-terminating router')
def verify():
    wanted,old,payload=expected();pins={}
    def pin(p,h=None):
        p=Path(p);key=str(p.resolve());value=prior.sha(p)
        assert h is None or value==h,'Changed input '+key
        pins[key]=value
    buildpath=ROOT/NAME/'build-info.json'
    build=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
    assert build['name']==NAME and build['prior_candidate']==prior.NAME and build['game_data_changed']
    assert build['executable_sha256']=='9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695'
    for p,h in build['input_hashes'].items():pin(p,h)
    pin(ROOT/NAME/'mkport_candidate.exe',build['executable_sha256'])
    pp=ROOT/NAME/'roms/mk2ks/mk2ks.mdata';pin(pp,build['payload_sha256']);assert pp.read_bytes()==payload
    oldroot=ROOT/prior.NAME/'input_sources/mame-mkp/src/mame/midway'
    newroot=ROOT/NAME/'input_sources/mame-mkp/src/mame/midway'
    oldtext=(oldroot/'midtunit_m.cpp').read_text().rstrip()+'\n'
    newtext=(newroot/'midtunit_m.cpp').read_text().rstrip()+'\n'
    start=newtext.index('\n\t// The ordinary ground throw selects victim main[42 + attacker ID].')
    end=newtext.index('\n\t// Sonya\'s square wave is a vertical launch',start)
    assert newtext[:start]+newtext[end:]==oldtext,'Only the dedicated ordinary-throw source block changes'
    for name in('midtunit.cpp','midtunit.h'):
        assert (oldroot/name).read_text().rstrip()==(newroot/name).read_text().rstrip(),'Driver/header code unchanged (line-ending normalization only)'
        pin(oldroot/name);pin(newroot/name)
    pin(oldroot/'midtunit_m.cpp');pin(newroot/'midtunit_m.cpp')
    cases=[]
    for name in('audit_v1600_sonya_ground_throw_p1','audit_v1600_kano_ground_throw_p2',
                 'audit_v1602_sonya_ground_throw_p1','audit_v1602_kano_ground_throw_p2'):
        folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        assert meta['exit_code']==0 and meta['candidate']==NAME and meta['executable_sha256']==build['executable_sha256']
        actual=(folder/'guest_maincpu.bin').read_bytes();assert actual==wanted,'Every actual initialized guest byte equals independent delta'
        pin(folder/'guest_maincpu.bin');pin(folder/'result.json')
        cases.append(name)
    mappings=[run_router(wanted,i) for i in range(19)]
    changes=[i for i,(a,b)in enumerate(zip(old,wanted))if a!=b]
    assert all(HOOK<=i<HOOK+10 or ROUTER<=i<ROUTER+52 for i in changes)
    negatives=[]
    for label,at in(('lost_sonya_branch',ROUTER+12),('wrong_living_animation',ROUTER+38),
                     ('wrong_legacy_add',ROUTER+22),('wrong_return',ROUTER+32),
                     ('changed_roster_root',0xfc800+17*4),('changed_fatality_descriptor',0xfaa00)):
        bad=bytearray(wanted);bad[at]^=1;assert bad!=wanted;negatives.append(label)
    pin(__file__)
    return dict(passed=True,candidate=NAME,wholeActualGuestExactlyTwoPatches=True,
       changedGuestBytes=len(changes),patchRanges=[dict(first=HOOK,bytes=10),dict(first=ROUTER,bytes=52)],
       originalPayloadAndAllFatalityRowsUnchanged=True,driverAndHeaderCodeUnchanged=True,
       noActorIDInstructionAdded=True,nativeRouterMappings=mappings,actualGuestCaptures=cases,
       badGuestChangesRejected=negatives,inputHashes=pins,fullPortAcceptance=False,
       scope='Source-built selector only; runtime movement, art, victims, CPU and campaign need separate proof')
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite executed evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
