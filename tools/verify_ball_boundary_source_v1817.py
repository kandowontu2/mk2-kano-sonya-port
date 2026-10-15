"""Exact isolated native ball callback delta; no full-port acceptance."""
import json,struct
from pathlib import Path
import verify_native_ground_throw_source_v1598 as prior
from verify_human_special_phases_v1767 import sha
ROOT=prior.ROOT;NAME='diagnostic_v1816_ball_native_boundary'
OUT=ROOT/'audit_v1817_ball_boundary_source_checked'
HOOK=0xffba0;ROUTER=0xfc400;BASE=0xff800000+ROUTER*8
WORDS=(0x098f,0x00c0,0x0d5f,0x87c0,0xff82,0x09af,0x0300,0x0b45,0xfecf,0xc801,0x0960,0x09c0,3,0x0580,0x19d0,0x0106,0x0960)

def expected():
    old,_,payload=prior.expected()
    assert old[ROUTER:ROUTER+128]==b'\xff'*128
    assert old[HOOK:HOOK+12]==struct.pack('<6H',0x09c0,3,0x0580,0x19d0,0x0106,0x0960)
    guest=bytearray(old);guest[ROUTER:ROUTER+34]=struct.pack('<17H',*WORDS)
    guest[HOOK:HOOK+12]=struct.pack('<6H',0xc080,BASE&65535,BASE>>16,0x0300,0x0300,0x0300)
    return bytes(guest),old,payload

def model_callback(raw,x1,x2,own,iterator,timer):
    pc=BASE;regs={8:own,9:iterator};stack=[];carry=False;distance=0;stores=[]
    for _ in range(8):
        at=(pc-0xff800000)//8;op=struct.unpack_from('<H',raw,at)[0]
        if op==0x098f:
            assert struct.unpack_from('<H',raw,at+2)[0]==0x00c0;stack.append((regs[8],regs[9]));pc+=32
        elif op==0x0d5f:
            assert struct.unpack_from('<I',raw,at+2)[0]==0xff8287c0
            # Exact original helper loads global physical pointers and abs X gap.
            regs[8]=0x01034a00;regs[9]=0x01034c10;distance=abs(x1-x2);pc+=48
        elif op==0x09af:
            assert struct.unpack_from('<H',raw,at+2)[0]==0x0300;regs[8],regs[9]=stack.pop();pc+=32
        elif op==0x0b45:
            threshold=(~struct.unpack_from('<H',raw,at+2)[0])&65535;assert threshold==304
            carry=distance<threshold;pc+=32
        elif op==0xc801:pc+=32 if carry else 16
        elif op==0x09c0:assert struct.unpack_from('<H',raw,at+2)[0]==3;regs[0]=3;pc+=32
        elif op==0x0580:
            assert struct.unpack_from('<I',raw,at+2)[0]==0x010619d0;timer=regs[0];stores.append(timer);pc+=48
        elif op==0x0960:
            assert not stack and(regs[8],regs[9])==(own,iterator)
            assert stores==([3]if distance<304 else[])
            return dict(gap=distance,refreshed=bool(stores),timer=timer,actorAndIteratorPreserved=True)
        else:raise ValueError('Unexpected callback instruction '+hex(op))
    raise ValueError('Callback did not return')

def verify():
    guest,old,payload=expected();pins={}
    def pin(p,h=None):
        p=Path(p);value=sha(p);assert h is None or value==h,'Changed source '+str(p);pins[str(p.resolve())]=value
    bp=ROOT/NAME/'build-info.json';build=json.loads(bp.read_text(encoding='utf-8-sig'));pin(bp)
    assert build['name']==NAME and build['prior_candidate']==prior.NAME and build['game_data_changed']
    assert build['executable_sha256']=='31964536E5DC7C48763E593926688594B63ED64EDE25AE5CFCBD59279C337104'
    for p,h in build['input_hashes'].items():pin(p,h)
    pin(ROOT/NAME/'mkport_candidate.exe',build['executable_sha256'])
    pp=ROOT/NAME/'roms/mk2ks/mk2ks.mdata';assert pp.read_bytes()==payload;pin(pp,build['payload_sha256'])
    before=ROOT/prior.NAME/'input_sources/mame-mkp/src/mame/midway'
    after=ROOT/NAME/'input_sources/mame-mkp/src/mame/midway'
    oldtext=(before/'midtunit_m.cpp').read_text();newtext=(after/'midtunit_m.cpp').read_text()
    first=newtext.index('\t// Keep native body-push suppression only inside');last=newtext.index('\tunsigned ball_cursor = ball_action;',first)
    original='\temit(ball_repel, {0x09c0, 3, 0x0580, 0x19d0, 0x0106, 0x0960});\n'
    assert newtext[:first]+original+newtext[last:]==oldtext,'Only the ball callback source block changes'
    for name in('midtunit.cpp','midtunit.h'):assert(after/name).read_bytes()==(before/name).read_bytes();pin(after/name);pin(before/name)
    pin(before/'midtunit_m.cpp');pin(after/'midtunit_m.cpp')
    original_rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();pin(ROOT/'mk2/mk2-maincpu.bin')
    for a,b in((0xff8287c0,0xff828910),(0xff827c40,0xff8287c0),(0xff876650,0xff876b40)):
        lo,hi=(a-0xff800000)//8,(b-0xff800000)//8
        assert guest[lo:hi]==old[lo:hi]==original_rom[lo:hi],'Original native distance/body/fling implementation unchanged'
    cases=[]
    for side in(1,2):
        folder=ROOT/f'audit_v1824_human_ball_p{side}_boundary';meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        assert meta['exit_code']==0 and meta['candidate']==NAME and meta['executable_sha256']==build['executable_sha256']
        assert(folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual initialized guest equals independent two-range delta'
        pin(folder/'guest_maincpu.bin');pin(folder/'result.json');cases.append(str(folder))
    mappings=[model_callback(guest,220,220+gap,0x010350a0,0xff00dc20,2)for gap in(0,1,61,64,300,303,304,305,307,320,412)]
    changed=[i for i,(a,b)in enumerate(zip(old,guest))if a!=b]
    assert all(HOOK<=i<HOOK+12 or ROUTER<=i<ROUTER+34 for i in changed)
    pin(__file__)
    return dict(passed=True,candidate=NAME,wholeActualGuestExactlyCallbackDelta=True,changedGuestBytes=len(changed),
      patchRanges=[dict(first=HOOK,bytes=12),dict(first=ROUTER,bytes=34)],nativeSeparationThreshold=304,
      actorAndAnimationIteratorPreserved=True,originalDistanceBodyPushAndFlingBytesUnchanged=True,
      payloadAudioAttackDamageAndAllOtherGuestBytesUnchanged=True,noActorIDInstructionAdded=True,
      callbackModels=mappings,actualGuestCaptures=cases,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','callbackModels')},indent=2),flush=True)
